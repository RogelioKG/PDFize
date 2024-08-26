# standard library
from concurrent.futures import ProcessPoolExecutor, Future, as_completed
import itertools
from multiprocessing import current_process
from pathlib import Path
from typing import Type
import io
import shutil
import uuid

# third party library
from PIL import Image
import fitz

# local library
from . import initializer, PBAR_OUTPUT_LOCK
from .path_util import *
from .processor import PdfProcessor
from .progress_bar import Pbar, NoPbar


def zero_base_indexing(page_num: int, page_count: int) -> int:
    """
    convert 1-base indexing (support negative `page_num`)
    to 0-base indexing (positive `page_num` only)

    Parameters
    ----------
    + `page_num` : int
    + `page_count` : int

    Returns
    -------
    + int
    """
    if page_num < 0:
        page_num += page_count
    elif page_num > 0:
        page_num -= 1
    else:
        raise ValueError("Invalid page number: 1-based indexing does not include 0.")

    assert 0 <= page_num < page_count

    return page_num


def divide(page_count: int, workers: int) -> list[tuple[int, int]]:
    """
    Divides the total number of pages into chunks assigned to each worker.

    Parameters
    ----------
    + `page_count` : int
        The total number of pages to be divided.
    + `workers` : int
        The number of workers to divide the pages among.

    Returns
    -------
    + list[tuple[int, int]]
        A list of tuples, where each tuple represents the start and end pages for each worker, using 1-based indexing.

    Example
    -------
    >>> divide(250, 5)
    [(1, 50), (51, 100), (101, 150), (151, 200), (201, 250)]
    >>> divide(254, 5)
    [(1, 51), (52, 102), (103, 153), (154, 204), (205, 254)]
    >>> divide(3, 5)
    AssertionError
    """
    assert page_count >= workers

    pages_per_worker = page_count // workers
    remainder = page_count % workers

    page_ranges = []
    start_page = 1

    for i in range(workers):
        end_page = start_page + pages_per_worker - 1
        if i < remainder:
            end_page += 1
        page_ranges.append((start_page, end_page))
        start_page = end_page + 1

    return page_ranges


def get_pdf_page_count(filepath: str | Path) -> int:
    # 開啟多進程加速多 pdf 且又有 --name 選項時，
    # 為了確保流水號的順序性，逼不得以需開啟 pdf 得知 page_count。
    # NOTE: 我想或許有更好的做法
    doc = fitz.open(filepath)
    page_count = doc.page_count
    doc.close()
    return page_count


class PdfSingleProcessor(PdfProcessor):
    def __init__(self, path: str, *, pbar_class: Type[Pbar] = NoPbar):
        super().__init__(path, pbar_class=pbar_class)

    def _build_image_main_path(
        self, image: Path, pdf_path: Path, name: str | None, subdir: bool
    ) -> Path:
        """
        Explanation
        ---
        如果沒有 name
          如果輸入是目錄 : (image / pdf_path.stem)
              如果有 subdir 選項 : (image / pdf_path.stem / pdf_path.stem)
          如果輸入是檔案 : (image / self.path.stem)
        如果有 name : (image / name)
        """

        image_main_path = image

        if name is None:
            if self.path.is_dir():
                image_main_path = image_main_path / pdf_path.stem
                if subdir:
                    try_makedir(image_main_path)
                    image_main_path = image_main_path / pdf_path.stem
            elif self.path.is_file():
                image_main_path = image_main_path / self.path.stem
        else:
            image_main_path = image / name

        return image_main_path

    def to_images(
        self,
        image: Path,
        dpi: int,
        format: str,
        *,
        name: str | None = None,
        subdir: bool,
    ) -> None:
        """
        將 pdf 轉為 image
        """
        assert not (name and subdir)  # mutual exclusion check
        try_makedir(image)  # 嘗試創建 image 目錄

        start = 1
        for pdf_path in self.get_filepaths(suffix=".pdf"):  # 遍歷每一份 PDF
            image_main_path = self._build_image_main_path(image, pdf_path, name, subdir)
            next_start = self._one_pdf_to_images(
                pdf_path, image_main_path, dpi, format, start=start
            )
            if name is not None:
                start = next_start

    def _one_pdf_to_images(
        self,
        pdf_path: Path,
        image_main_path: Path,
        dpi: int,
        format: str,
        *,
        start: int = 1,
        worker_id: int = 0,
        leave: bool = True,
    ) -> int:
        """
        一份 pdf 轉 image
        """
        with fitz.open(pdf_path) as pdf_file:
            page_count = pdf_file.page_count

            with self.pbar_class(
                total=page_count,
                desc=f"#worker {worker_id:0>2}",
                position=worker_id,
                unit="page",
                leave=leave,
            ) as pbar:
                for count, page in enumerate(pdf_file.pages(), start=start):
                    pixmap = page.get_pixmap(dpi=dpi)
                    image_file = Image.open(io.BytesIO(pixmap.tobytes()))
                    image_path = add_serial(image_main_path, count).with_suffix(
                        f".{format}"
                    )
                    image_file.save(image_path)  # 儲存圖片
                    pbar.update(1)

        return start + page_count

    def split(self, output_pdf: Path, from_page: int, to_page: int) -> None:
        """
        將 pdf 拆分
        """
        assert self.path.suffix == ".pdf" and output_pdf.suffix == ".pdf"

        with fitz.open(self.path) as old_pdf, fitz.open() as new_pdf:
            page_count = old_pdf.page_count
            from_page = zero_base_indexing(from_page, page_count)
            to_page = zero_base_indexing(to_page, page_count)
            total_pages = abs(to_page - from_page) + 1  # 計算總頁數

            with self.pbar_class(total=total_pages, unit="page") as pbar:
                new_pdf.insert_pdf(old_pdf, from_page, to_page)
                new_pdf.save(output_pdf)
                pbar.update(total_pages)

    def merge(self, output_pdf: Path) -> None:
        """
        將 pdf 合併
        """
        with fitz.open() as new_pdf:  # 空檔案
            pdf_paths = self.get_filepaths(suffix=".pdf")  # lazy evaluation
            total_pdfs = 0
            if self.pbar_class != NoPbar:  # 有進度條
                pdf_paths = tuple(pdf_paths)
                total_pdfs = len(pdf_paths)

            with self.pbar_class(total=total_pdfs, unit="pdf") as pbar:
                for pdf_path in pdf_paths:  # 遍歷每一份 PDF
                    with fitz.open(pdf_path) as old_pdf:
                        new_pdf.insert_pdf(old_pdf)  # 檔案附加 PDF
                    pbar.update(1)

            new_pdf.save(output_pdf)


class PdfParallelProcessor(PdfSingleProcessor):
    def __init__(
        self,
        path: str,
        *,
        pbar_class: Type[Pbar] = NoPbar,
        workers: int | None = None,
    ):
        super().__init__(path, pbar_class=pbar_class)
        if workers is None:
            cpu_count = os.cpu_count()
            assert cpu_count is not None
            self.workers = cpu_count
        else:
            self.workers = workers

    def to_images(
        self,
        image: Path,
        dpi: int,
        format: str,
        *,
        name: str | None = None,
        subdir: bool,
    ) -> None:
        """`@Override`
        將 pdf 轉為 image (multiprocessing)
        """
        assert not (name and subdir)  # mutual exclusion check
        try_makedir(image)  # 嘗試創建 image 目錄
        pdf_paths = tuple(self.get_filepaths(suffix=".pdf"))

        if len(pdf_paths) == 1:  # 只有一份 PDF
            original_pdf_path = self.path  # 原先 PDF 路徑
            temp_pdf_dir = self._one_pdf_parallel(
                image, pdf_paths, dpi, format, name=name or pdf_paths[0].stem, subdir=subdir
            )
            shutil.rmtree(temp_pdf_dir, ignore_errors=True)  # 刪除暫時目錄
            self.path = original_pdf_path  # 回復原先 PDF 路徑
        else:
            self._many_pdfs_parallel(
                image, pdf_paths, dpi, format, name=name, subdir=subdir
            )

    def _split(self, pdf_path: Path, temp_pdf_dir: Path) -> list[int]:
        """
        單一 PDF 切割成多份暫時的小 PDF

        Parameters
        ----------
        + `pdf_path` : Path
            PDF 路徑 (非目錄)
        + `temp_pdf_dir` : Path
            暫時目錄

        Returns
        -------
        + list[int]
            start_pages
        """
        with fitz.open(pdf_path) as old_pdf:
            page_count = old_pdf.page_count
            page_ranges = divide(page_count, self.workers)

            for from_page, to_page in page_ranges:
                with fitz.open() as temp_pdf:
                    from_page = zero_base_indexing(from_page, page_count)
                    to_page = zero_base_indexing(to_page, page_count)
                    temp_pdf.insert_pdf(old_pdf, from_page, to_page)
                    temp_pdf_name = add_serial(
                        temp_pdf_dir / pdf_path.stem, from_page, zfill=True
                    ).with_suffix(".pdf")
                    temp_pdf.save(temp_pdf_name)

            start_pages = [page_range[0] for page_range in page_ranges]
            return start_pages

    def _one_pdf_to_images(
        self,
        pdf_path: Path,
        image_main_path: Path,
        dpi: int,
        format: str,
        *,
        start: int = 1,
    ) -> None:
        """`@Override`
        一份 pdf 轉 image (multiprocessing)
        """
        # 帶著 ID 進場
        super()._one_pdf_to_images(
            pdf_path,
            image_main_path,
            dpi,
            format,
            start=start,
            worker_id=current_process()._identity[0],
            leave=False,
        )

    def _many_pdfs_parallel(
        self,
        image: Path,
        pdf_paths: tuple[Path, ...],
        dpi: int,
        format: str,
        *,
        name: str | None,
        subdir: bool,
        start_pages: list[int] | None = None,
    ) -> None:
        """
        多份 pdf 平行處理
        """

        if name is None:  # 沒有 name 選項的 many pdfs (流水號都從 1 開始)
            start_pages = [1] * len(pdf_paths)
        elif start_pages is None:  # 有 name 選項的 many pdfs (流水號累加)
            start_pages = list(
                itertools.accumulate(
                    [1] + [get_pdf_page_count(pdf_path) for pdf_path in pdf_paths]
                )
            )
        else:  # 否則就是被拆分的 one pdf
            pass

        with ProcessPoolExecutor(
            max_workers=self.workers,
            initializer=initializer,
            initargs=(PBAR_OUTPUT_LOCK, self.pbar_class.style),
        ) as pool:

            futures: list[Future] = []
            for start, pdf_path in zip(start_pages, pdf_paths):  # 遍歷每一份 PDF
                image_main_path = self._build_image_main_path(
                    image, pdf_path, name, subdir
                )  # 對被拆分的 one pdf 而言，name 是無流水號的名稱 (或者自訂名稱)
                futures.append(
                    pool.submit(
                        self._one_pdf_to_images,
                        pdf_path,
                        image_main_path,
                        dpi,
                        format,
                        start=start,
                    )
                )

            with self.pbar_class(
                total=len(futures), unit="workers", position=0, main=True
            ) as pbar:
                for _ in as_completed(futures):
                    pbar.update(1)

    def _one_pdf_parallel(
        self,
        image: Path,
        pdf_paths: tuple[Path, ...],
        dpi: int,
        format: str,
        *,
        name: str,
        subdir: bool,
    ) -> Path:
        """
        單份 pdf 平行處理

        Returns
        -------
        + Path
            返回暫時目錄
        """
        temp_pdf_dir = Path(image / f".tempdir_{uuid.uuid4().hex}")
        try_makedir(temp_pdf_dir)  # 嘗試創建暫時 PDF 目錄
        start_pages = self._split(pdf_paths[0], temp_pdf_dir)  # 拆分 PDF 放到暫時目錄
        self.path = temp_pdf_dir  # PDF 路徑切換至暫時目錄
        temp_pdf_paths = tuple(self.get_filepaths(suffix=".pdf"))  # 從暫時目錄拿 PDF

        # 轉為多份 pdf 平行處理任務
        self._many_pdfs_parallel(
            image,
            temp_pdf_paths,
            dpi,
            format,
            name=name,  # 原 PDF 名稱
            subdir=subdir,
            start_pages=start_pages,
        )

        return temp_pdf_dir
