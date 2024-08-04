# third party library
import fitz
from pathlib import Path

# local library
from .path_util import *
from .pdf_util import PdfFile
from .progress_bar import Pbar


class ImageFile:

    def __init__(self, path: str):
        """
        Parameters
        ----------
        + `path` : str
            image 路徑 (可為目錄或檔案)
        """
        self.path = Path(path)

    def to_pdf(self, pdf: PdfFile):
        """
        將 image 轉為 pdf
        """
        assert pdf.path.suffix == ".pdf"

        with fitz.open() as pdf_file:  # 空檔案
            image_paths = tuple(get_filepaths(self.path))
            with Pbar(total=len(image_paths), unit="image") as pbar:
                for image_path in image_paths:  # 遍歷每一張 image
                    with fitz.open(image_path) as image_file:  # 開啟 image
                        pdfbytes = image_file.convert_to_pdf()  # image 轉成一頁 PDF
                    with fitz.open("pdf", pdfbytes) as one_pdf:  # 以 PDF 開啟
                        pdf_file.insert_pdf(one_pdf)  # 空檔案附加一頁 PDF
                    pbar.update(1)
            pdf_file.save(pdf.path)
