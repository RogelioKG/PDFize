# standard library
from __future__ import annotations
import io
from pathlib import Path
from typing import Type

# third party library
from PIL import Image
import fitz

# local library
from .progress_bar import *
from .path_util import *
from .image_util import *


def zero_base_indexing(page_num: int, page_count: int) -> int:
    """convert 1-base indexing (support negative `page_num`)
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


class PdfProcessor:
    def __init__(self, path: str, *, pbar_class: Type[Pbar] = NoPbar):
        """
        Parameters
        ----------
        + `path` : str
            pdf 路徑 (可為目錄或檔案)
        + `pbar_class`: Type[Pbar]
            進度條類型
        """
        self.path = Path(path)
        self.pbar_class = pbar_class

    def to_images(
        self,
        image: Path,
        dpi: int,
        format: str,
        name: str | None,
        *,
        subdir: bool,
    ) -> None:
        """
        將 pdf 轉為 image
        """
        image_main_path = self._try_build_image_main_path(image, name, subdir)
        for pdf_path in get_filepaths(self.path, suffix=".pdf"):  # 遍歷每一份 PDF
            if image_main_path is None:
                image_main_path = self._build_image_main_path(
                    image, pdf_path, name, subdir
                )
            self._one_pdf_to_images(pdf_path, image_main_path, dpi, format)

    def _try_build_image_main_path(
        self, image: Path, name: str | None, subdir: bool
    ) -> Path | None:
        """
        Explaination
        ---
        如果有 name
          如果輸入是目錄 : (image / name)
              如果有 subdir 選項 : (image / name / name)
          如果輸入是檔案 : (image / name)
        如果沒有 name
          如果輸入是目錄 : (image / pdf_path.stem)
              如果有 subdir 選項 : (image / pdf_path.stem / pdf_path.stem)
          如果輸入是檔案 : (image / self.path.stem)

        See Also
        ---
        + `PdfProcessor._build_image_main_path`
        """
        try_makedir(image)  # 嘗試創建目錄

        image_main_path = None
        if name is not None:
            image_main_path = image / name
            if self.path.is_dir() and subdir:
                try_makedir(image_main_path)  # 嘗試創建目錄
                image_main_path = image_main_path / name
        elif self.path.is_file():
            image_main_path = image / self.path.stem

        return image_main_path

    def _build_image_main_path(
        self, image: Path, pdf_path: Path, name: str | None, subdir: bool
    ) -> Path:
        if name is None and self.path.is_dir():
            image_main_path = image / pdf_path.stem
            if subdir:
                try_makedir(image_main_path)  # 嘗試創建目錄
                image_main_path = image_main_path / pdf_path.stem
        return image_main_path

    def _one_pdf_to_images(
        self, pdf_path: Path, image_main_path: Path, dpi: int, format: str
    ) -> None:
        """
        一份 pdf 轉 image
        """
        with fitz.open(pdf_path) as pdf_file:

            if self.pbar_class == NoPbar:  # 無進度條
                page_count = 0
            else:
                page_count = pdf_file.page_count

            with self.pbar_class(total=page_count, unit="page") as pbar:
                for count, page in enumerate(pdf_file.pages(), start=1):
                    pixmap = page.get_pixmap(dpi=dpi)
                    image_file = Image.open(io.BytesIO(pixmap.tobytes()))
                    image_file.save(f"{image_main_path}-{count}.{format}")  # 儲存圖片
                    pbar.update(1)

    def split(self, output_pdf: Path, from_page: int, to_page: int) -> None:
        """
        將 pdf 拆分
        """
        assert self.path.suffix == ".pdf" and output_pdf.suffix == ".pdf"

        with fitz.open(self.path) as old_pdf, fitz.open() as new_pdf:
            from_page = zero_base_indexing(from_page, old_pdf.page_count)
            to_page = zero_base_indexing(to_page, old_pdf.page_count)

            if self.pbar_class == NoPbar:  # 無進度條
                total_pages = 0
            else:
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

            if self.pbar_class == NoPbar:  # 無進度條
                pdf_paths = get_filepaths(self.path, suffix=".pdf")  # lazy evaluation
                total_pdfs = 0
            else:
                pdf_paths = tuple(get_filepaths(self.path, suffix=".pdf"))
                total_pdfs = len(pdf_paths)

            with self.pbar_class(total=total_pdfs, unit="pdf") as pbar:
                for pdf_path in pdf_paths:  # 遍歷每一份 PDF
                    with fitz.open(pdf_path) as old_pdf:
                        new_pdf.insert_pdf(old_pdf)  # 檔案附加 PDF
                    pbar.update(1)

            new_pdf.save(output_pdf)
