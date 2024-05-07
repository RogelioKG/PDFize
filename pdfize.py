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


@click.group()
def cli():
    pass


@cli.command("pdf-to-img", short_help="Convert PDF to image")
@click.option(
    "-S",
    "--subdir/--no-subdir",
    "subdir_option",
    help="If this flag is set, use the original PDF name as the name of subdirectory. The output path can only be directory.",
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
def pdf_to_img(
    input_path: str, output_path: str, subdir_option: bool, ext: str, dpi: int
):
    input_path: Path = Path(input_path)
    output_path: Path = Path(output_path)

    if subdir_option:  # -S 選項
        assert not output_path.suffix  # 輸出路徑限定為目錄

    try_create_dir(output_path)

    if output_path.suffix:  # 如果輸出路徑為檔案
        output_base = output_path.parent / output_path.stem
        output_ext = output_path.suffix
    else:  # 如果輸出路徑為目錄
        output_ext = "." + ext  # -e 指定副檔名

    for input_file in get_files(input_path):  # 遍歷每一份 PDF
        if not output_path.suffix:  # 如果輸出路徑為目錄
            output_base = output_path / input_file.stem
            if subdir_option:  # -S 選項
                try_create_dir(output_base)
                output_base = output_base / input_file.stem
        with fitz.open(input_file) as pdf:
            # 進度條
            with Pbar(total=pdf.page_count, unit="page") as pbar:
                for count, page in enumerate(pdf.pages(), start=1):  # count 為頁數後綴
                    pixmap = page.get_pixmap(dpi=dpi)
                    image = Image.open(io.BytesIO(pixmap.tobytes()))
                    image.save(f"{output_base}-{count}{output_ext}")  # 儲存圖片
                    pbar.update(1)


@cli.command("img-to-pdf", short_help="Convert image to PDF")
@click.option(
    "-o",
    "--output-path",
    "output_path",
    required=True,
    help="Output filename",
)
@click.argument("input_path", nargs=1, required=True)
def img_to_pdf(input_path: str, output_path: str):
    input_path: Path = Path(input_path)
    output_path: Path = Path(output_path)

    with fitz.open() as pdf:  # 空檔案
        input_files = list(get_files(input_path))
        # 進度條
        with Pbar(total=len(input_files), unit="image") as pbar:
            for input_file in input_files:  # 遍歷每一張 image
                with fitz.open(input_file) as img:  # 開啟 image
                    pdfbytes = img.convert_to_pdf()  # image 轉 PDF
                with fitz.open("pdf", pdfbytes) as imgpdf:  # 開啟 PDF
                    pdf.insert_pdf(imgpdf)  # 空檔案附加一份 PDF
                pbar.update(1)
        pdf.save(output_path)


@cli.command("split", short_help="Split PDF")
@click.option(
    "-o",
    "--output-path",
    "output_path",
    required=True,
    help="Output filename",
)
@click.option(
    "-r",
    "--range",
    "r",
    default="1,-1",
    show_default=True,
    help="The range of pages to copy, using 1-based indexing. The value '-1' denotes the last page. If the from-page value is greater than the to-page value, the result will be in reverse order.",
)
@click.argument("input_path", nargs=1, required=True)
def pdf_split(input_path: str, output_path: str, r: str):
    assert input_path.endswith(".pdf") and output_path.endswith(".pdf")  # 斷言皆為 PDF
    from_page, to_page = map(int, r.split(","))

    with fitz.open(input_path) as old_pdf, fitz.open() as new_pdf:
        # 1-base -> 0-base
        from_page = from_page - 1 if from_page != -1 else old_pdf.page_count - 1
        to_page = to_page - 1 if to_page != -1 else old_pdf.page_count - 1
        # 斷言合理頁數範圍
        assert 0 <= from_page < old_pdf.page_count
        assert 0 <= to_page < old_pdf.page_count
        # PDF 拆分
        total_pages = abs(to_page - from_page) + 1
        # 進度條
        with Pbar(total=total_pages, unit="page") as pbar:
            new_pdf.insert_pdf(old_pdf, from_page, to_page)
            new_pdf.save(output_path)
            pbar.update(total_pages)


@cli.command("merge", short_help="Merge PDF")
@click.option(
    "-o",
    "--output-path",
    "output_path",
    required=True,
    help="Output filename",
)
@click.argument("input_path", nargs=1, required=True)
def pdf_merge(input_path: str, output_path: str):
    input_path: Path = Path(input_path)
    output_path: Path = Path(output_path)

    with fitz.open() as new_pdf:  # 空檔案
        input_files = list(get_files(input_path))
        with Pbar(total=len(input_files), unit="pdf") as pbar:
            for input_file in input_files:  # 遍歷每一份 PDF
                with fitz.open(input_file) as old_pdf:
                    new_pdf.insert_pdf(old_pdf)  # 檔案附加 PDF
                pbar.update(1)
        new_pdf.save(output_path)


if __name__ == "__main__":
    cli()
