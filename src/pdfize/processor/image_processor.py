# standard library
from pathlib import Path

# third party library
import fitz

# local module
from ..progress_bar.base import NoPbar, Pbar
from .base import Processor


class ImageProcessor(Processor):
    def __init__(self, path: str | Path, *, pbar_class: type[Pbar]) -> None:
        super().__init__(path, pbar_class=pbar_class)

    def to_pdf(self, pdf: Path):
        """
        將 image 轉為 pdf
        """
        raise NotImplementedError


class ImageSingleProcessor(ImageProcessor):
    def __init__(self, path: str | Path, *, pbar_class: type[Pbar] = NoPbar) -> None:
        super().__init__(path, pbar_class=pbar_class)

    def to_pdf(self, pdf: Path) -> None:
        """
        將 image 轉為 pdf
        """
        assert pdf.suffix == ".pdf"

        with fitz.open() as pdf_file:  # 空檔案
            image_paths = self.get_filepaths()  # lazy evaluation
            total_images = 0
            if self.pbar_class != NoPbar:  # 有進度條
                image_paths = tuple(image_paths)
                total_images = len(image_paths)

            with self.pbar_class(total=total_images, unit="image") as pbar:
                for image_path in image_paths:  # 遍歷每一張 image
                    with fitz.open(image_path) as image_file:  # 開啟 image
                        pdfbytes = image_file.convert_to_pdf()  # image 轉成一頁 PDF
                    with fitz.open("pdf", pdfbytes) as one_pdf:  # 以 PDF 開啟
                        pdf_file.insert_pdf(one_pdf)  # 空檔案附加一頁 PDF
                    pbar.update(1)

            pdf_file.save(pdf)
