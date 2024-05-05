# standard library
import io
from pathlib import Path

# third party library
from PIL import Image
import click
import fitz

# local library
from toolkits.progress_bar import Pbar
from toolkits.path_tool import *


def pdf_to_img(input_path: Path, output_path: Path, ext: str, dpi: int) -> None:
    """

    Parameters
    ----------
    + `input_path` : Path
        輸入路徑 (PDF)
    + `output_path` : Path
        輸出路徑 (image)
    + `ext` : str
        副檔名 (image)
    + `dpi` : int
        dots per inch
    """
    try_create_dir(output_path)
    if output_path.suffix:  # 如果輸出路徑為檔案
        output_base = output_path.parent / output_path.stem
        output_ext = output_path.suffix
    else:  # 如果輸出路徑為目錄
        output_ext = "." + ext  # -e 指定副檔名

    for input_file in get_files(input_path):  # 遍歷每一份 PDF
        if not output_path.suffix:  # 如果輸出路徑為目錄
            output_base = output_path / input_file.stem  # image 主名稱為其所屬 pdf 名稱
        with fitz.open(input_file) as pdf:
            # 進度條 (顏色：green) (單位：處理頁數)
            with Pbar(total=pdf.page_count, unit="page") as pbar:
                for count, page in enumerate(pdf.pages(), start=1):  # count 為頁數後綴
                    pixmap = page.get_pixmap(dpi=dpi)
                    image = Image.open(io.BytesIO(pixmap.tobytes()))
                    image.save(f"{output_base}-{count}{output_ext}")  # 儲存圖片
                    pbar.update(1)


def img_to_pdf(input_path: Path, output_path: Path) -> None:
    """image 轉 PDF

    Parameters
    ----------
    + `input_path` : Path
        輸入路徑 (image)
    + `output_path` : Path
        輸出路徑 (PDF)
    """
    with fitz.open() as pdf:  # 空檔案
        input_files = list(get_files(input_path))
        # 進度條 (顏色：pink) (單位：處理圖片數)
        with Pbar(total=len(input_files), unit="image") as pbar:
            for input_file in input_files:  # 遍歷每一張 image
                with fitz.open(input_file) as img:  # 開啟 image
                    pdfbytes = img.convert_to_pdf()  # image 轉 PDF
                with fitz.open("pdf", pdfbytes) as imgpdf: # 開啟 PDF
                    pdf.insert_pdf(imgpdf)  # 空檔案附加一份 PDF
                pbar.update(1)
        pdf.save(output_path)


@click.command()
@click.option(
    "-I/ ",
    "--img-to-pdf/--pdf-to-img",
    "input_is_img",
    help="If this flag is set, convert image to PDF; otherwise, convert PDF to image.",
)
@click.option(
    "-d", "--dpi", "dpi", type=int, default=100, show_default=True, help="DPI of image"
)
@click.option(
    "-e",
    "--extension",
    "ext",
    default="png",
    show_default=True,
    help="File extension of image",
)
@click.option(
    "-o",
    "--output-path",
    "output_path",
    required=True,
    help="Output directory or filename",
)
@click.argument("input_path", nargs=1, required=True)
def pdf_tool(input_path: str, output_path: str, input_is_img: bool, ext: str, dpi: int):
    input_path = Path(input_path)
    output_path = Path(output_path)
    if input_is_img:  # 如果輸入路徑給定 image
        img_to_pdf(input_path, output_path)
    else:  # 如果輸入路徑給定 PDF
        pdf_to_img(input_path, output_path, ext, dpi)


if __name__ == "__main__":
    pdf_tool()
