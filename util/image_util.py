# standard library
from __future__ import annotations
from typing import Type

# third party library
import fitz
from pathlib import Path

# local library
from .path_util import *
from .progress_bar import Pbar, NoPbar


class ImageProcessor:

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

    def to_pdf(self, pdf: Path):
        """
        將 image 轉為 pdf
        """
        assert pdf.suffix == ".pdf"

        with fitz.open() as pdf_file:  # 空檔案
            image_paths = tuple()

            if self.pbar_class == NoPbar:  # 無進度條
                image_paths = get_filepaths(self.path)
                total_images = 0
            else:
                image_paths = tuple(get_filepaths(self.path))
                total_images = len(image_paths)

            with self.pbar_class(total=total_images, unit="image") as pbar:
                for image_path in image_paths:  # 遍歷每一張 image
                    with fitz.open(image_path) as image_file:  # 開啟 image
                        pdfbytes = image_file.convert_to_pdf()  # image 轉成一頁 PDF
                    with fitz.open("pdf", pdfbytes) as one_pdf:  # 以 PDF 開啟
                        pdf_file.insert_pdf(one_pdf)  # 空檔案附加一頁 PDF
                    pbar.update(1)

            pdf_file.save(pdf)
