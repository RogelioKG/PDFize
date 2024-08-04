# standard library
from __future__ import annotations
import fitz
import io
from pathlib import Path
from PIL import Image

# local library
from .progress_bar import Pbar
from .path_util import *
from .image_util import *


class PdfFile:
    def __init__(self, path: str):
        """
        Parameters
        ----------
        + `path` : str
            pdf 路徑 (可為目錄或檔案)
        """
        self.path = Path(path)

    def to_images(
        self,
        image: ImageFile,
        dpi: int,
        format: str,
        name: str | None,
        *,
        subdir: bool = False,
    ) -> None:
        """
        將 pdf 轉為 image
        """
        # 如果有 name
        #   如果輸入是目錄 : (image.path / name)
        #       如果有 subdir 選項 : (image.path / name / name)
        #   如果輸入是檔案 : (image.path / name)
        # 如果沒有 name
        #   如果輸入是目錄 : (image.path / pdf_path.stem)
        #       如果有 subdir 選項 : (image.path / pdf_path.stem / pdf_path.stem)
        #   如果輸入是檔案 : (image.path / self.path.stem)

        try_makedir(image.path)  # 嘗試創建目錄

        if name is not None:
            image_main_path = image.path / name
            if self.path.is_dir() and subdir:
                try_makedir(image_main_path)  # 嘗試創建目錄
                image_main_path = image_main_path / name
        elif self.path.is_file():
            image_main_path = image.path / self.path.stem

        for pdf_path in get_filepaths(self.path):  # 遍歷每一份 PDF
            if name is None and self.path.is_dir():
                image_main_path = image.path / pdf_path.stem
                if subdir:
                    try_makedir(image_main_path)  # 嘗試創建目錄
                    image_main_path = image_main_path / pdf_path.stem
            PdfFile._one_pdf_to_images(pdf_path, image_main_path, dpi, format)

    def split(self, output_pdf: PdfFile, from_page: int, to_page: int) -> None:
        """
        將 pdf 拆分
        """
        assert self.path.suffix == ".pdf" and output_pdf.path.suffix == ".pdf"

        with fitz.open(self.path) as old_pdf, fitz.open() as new_pdf:
            from_page = PdfFile.zero_base_indexing(from_page, old_pdf.page_count)
            to_page = PdfFile.zero_base_indexing(to_page, old_pdf.page_count)
            total_pages = abs(to_page - from_page) + 1  # 計算總頁數
            with Pbar(total=total_pages, unit="page") as pbar:
                new_pdf.insert_pdf(old_pdf, from_page, to_page)
                new_pdf.save(output_pdf.path)
                pbar.update(total_pages)

    def merge(self, output_pdf: PdfFile) -> None:
        """
        將 pdf 合併
        """
        with fitz.open() as new_pdf:  # 空檔案
            input_files = tuple(get_filepaths(self.path))
            with Pbar(total=len(input_files), unit="pdf") as pbar:
                for input_file in input_files:  # 遍歷每一份 PDF
                    with fitz.open(input_file) as old_pdf:
                        new_pdf.insert_pdf(old_pdf)  # 檔案附加 PDF
                    pbar.update(1)
            new_pdf.save(output_pdf.path)

    @staticmethod
    def _one_pdf_to_images(
        pdf_path: Path, image_main_path: Path, dpi: int, format: str
    ) -> None:
        with fitz.open(pdf_path) as pdf_file:
            with Pbar(total=pdf_file.page_count, unit="page") as pbar:  # 進度條
                for count, page in enumerate(
                    pdf_file.pages(), start=1
                ):  # count 為頁數後綴
                    pixmap = page.get_pixmap(dpi=dpi)
                    image_file = Image.open(io.BytesIO(pixmap.tobytes()))
                    image_file.save(f"{image_main_path}-{count}.{format}")  # 儲存圖片
                    pbar.update(1)

    @staticmethod
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
            raise ValueError(
                "Invalid page number: 1-based indexing does not include 0."
            )
        assert 0 <= page_num < page_count

        return page_num
