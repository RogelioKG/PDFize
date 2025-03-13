# standard library
import concurrent.futures as future
import io
import itertools
import multiprocessing as mp
import os
import shutil
import uuid
from pathlib import Path

# third party library
import fitz
from PIL import Image

# local module
from ..new_process import init, lock
from ..progress_bar.base import NoPbar, Pbar
from ..util import path_util, pdf_util
from .base import Processor


class PdfProcessor(Processor):
    def __init__(self, path: str, *, pbar_class: type[Pbar]) -> None:
        super().__init__(path, pbar_class=pbar_class)

    def to_images(
        self,
        image: Path,
        dpi: int,
        format: str,
        *,
        name: str | None,
        subdir: bool,
    ) -> None:
        """
        將 pdf 轉為 image
        """
        raise NotImplementedError

    def split(self, output_pdf: Path, from_page: int, to_page: int) -> None:
        """
        將 pdf 拆分
        """
        raise NotImplementedError

    def merge(self, output_pdf: Path) -> None:
        """
        將 pdf 合併
        """
        raise NotImplementedError


class PdfSingleProcessor(PdfProcessor):
    def __init__(self, path: str, *, pbar_class: type[Pbar] = NoPbar) -> None:
        super().__init__(path, pbar_class=pbar_class)

    def _build_image_main_path(
        self, image: Path, pdf_path: Path, name: str | None, subdir: bool
    ) -> Path:
        """
        Returns
        -------
        + Path
            image_main_path
        """

        # Explanation
        # 如果沒有 name
        #   如果輸入是目錄 : (image / pdf_path.stem)
        #     如果有 subdir 選項 : (image / pdf_path.stem / pdf_path.stem)
        #   如果輸入是檔案 : (image / self.path.stem)
        # 如果有 name : (image / name)

        image_main_path = image

        if name is None:
            if self.path.is_dir():
                image_main_path = image_main_path / pdf_path.stem
                if subdir:
                    path_util.try_makedir(image_main_path)
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
        path_util.try_makedir(image)  # 嘗試創建 image 目錄

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
        leave: bool = True,
    ) -> int:
        """
        一份 pdf 轉 image

        Returns
        -------
        int
            下一個起點頁碼
        """
        try:
            worker_id = mp.current_process()._identity[0]  # 多進程
        except IndexError:
            worker_id = 0  # 單進程

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
                    image_path = path_util.add_serial(image_main_path, count).with_suffix(
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
            from_page = pdf_util.zero_base_indexing(from_page, page_count)
            to_page = pdf_util.zero_base_indexing(to_page, page_count)
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
        pbar_class: type[Pbar] = NoPbar,
        workers: int | None = None,
    ) -> None:
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
        """
        將 pdf 轉為 image (multiprocessing)
        """
        assert not (name and subdir)  # mutual exclusion check
        path_util.try_makedir(image)  # 嘗試創建 image 目錄
        pdf_paths = tuple(self.get_filepaths(suffix=".pdf"))

        if len(pdf_paths) == 1:  # 只有一份 PDF
            original_pdf_path = self.path  # 原先 PDF 路徑
            temp_pdf_dir = self._one_pdf_parallel(
                image,
                pdf_paths,
                dpi,
                format,
                name=name or pdf_paths[0].stem,
                subdir=subdir,
            )
            shutil.rmtree(temp_pdf_dir, ignore_errors=True)  # 刪除暫時目錄
            self.path = original_pdf_path  # 回復原先 PDF 路徑
        else:
            self._many_pdfs_parallel(image, pdf_paths, dpi, format, name=name, subdir=subdir)

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
            page_ranges = pdf_util.divide(page_count, self.workers)

            for from_page, to_page in page_ranges:
                with fitz.open() as temp_pdf:
                    from_page = pdf_util.zero_base_indexing(from_page, page_count)
                    to_page = pdf_util.zero_base_indexing(to_page, page_count)
                    temp_pdf.insert_pdf(old_pdf, from_page, to_page)
                    # 讀取一個目錄中檔案時，名稱按字典序，因此流水號需補 0
                    page_digits = len(str(page_count))
                    temp_pdf_name = path_util.add_serial(
                        temp_pdf_dir / pdf_path.stem, from_page, width=page_digits
                    ).with_suffix(".pdf")
                    temp_pdf.save(temp_pdf_name)

            start_pages = [page_range[0] for page_range in page_ranges]
            return start_pages

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
                    [1] + [pdf_util.get_pdf_page_count(pdf_path) for pdf_path in pdf_paths]
                )
            )
        else:  # 否則就是被拆分的 one pdf
            pass

        with future.ProcessPoolExecutor(
            max_workers=self.workers,
            initializer=init.initializer,
            initargs=(lock.PBAR_OUTPUT_LOCK, self.pbar_class.style),
        ) as pool:
            futures: list[future.Future] = []
            for start, pdf_path in zip(start_pages, pdf_paths, strict=False):  # 遍歷每一份 PDF
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
                        leave=False,
                    )
                )

            with self.pbar_class(total=len(futures), unit="workers", position=0, main=True) as pbar:
                for _ in future.as_completed(futures):
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
            暫時目錄路徑
        """
        temp_pdf_dir = image / f".tempdir_{uuid.uuid4().hex}"
        path_util.try_makedir(temp_pdf_dir)  # 嘗試創建暫時 PDF 目錄
        start_pages = self._split(pdf_paths[0], temp_pdf_dir)  # 拆分 PDF 放到暫時目錄
        self.path = temp_pdf_dir  # PDF 路徑切換至暫時目錄
        temp_pdf_paths = tuple(self.get_filepaths(suffix=".pdf"))  # 從暫時目錄拿 PDF

        # 轉為多份 pdf 平行處理任務
        self._many_pdfs_parallel(
            image,
            temp_pdf_paths,
            dpi,
            format,
            name=name,  # 原 PDF 名稱 (或者自訂名稱)
            subdir=subdir,
            start_pages=start_pages,
        )

        return temp_pdf_dir
