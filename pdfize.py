# third party library
import click

# local library
from util.image_util import *
from util.path_util import *
from util.pdf_util import *


@click.group()
def cli():
    pass


@cli.command("pdf-to-img", short_help="Convert PDF to image")
@click.option(
    "-S",
    "--subdir/--no-subdir",
    "subdir",
    help="If this flag is set, use the original PDF filename as the name of subdirectory.",
)
@click.option(
    "-d", "--dpi", "dpi", type=int, default=100, show_default=True, help="Image DPI"
)
@click.option(
    "-f",
    "--format",
    "format",
    default="png",
    show_default=True,
    help="Image file format",
)
@click.option(
    "-n",
    "--name",
    "name",
    help="Image main filename [default: PDF filename]",
)
@click.option(
    "-o",
    "--output",
    "output_path",
    required=True,
    help="Output directory",
)
@click.argument("input_path", nargs=1, required=True)
def pdf_to_img(
    input_path: str,
    output_path: str,
    subdir: bool,
    dpi: int,
    format: str,
    name: str | None = None,
):
    pdf = PdfFile(input_path)
    image = ImageFile(output_path)
    pdf.to_images(image, dpi, format, name, subdir=subdir)


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
    image = ImageFile(input_path)
    pdf = PdfFile(output_path)
    image.to_pdf(pdf)


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
    "page_range",
    default="1,-1",
    show_default=True,
    help="Specifies the range of pages to copy using 1-based indexing, with support for negative indices. If the start page is greater than the end page, the pages will be copied in reverse order. Note: '-1' represents the last page.",
)
@click.argument("input_path", nargs=1, required=True)
def pdf_split(input_path: str, output_path: str, page_range: str):
    input_pdf = PdfFile(input_path)
    output_pdf = PdfFile(output_path)
    from_page, to_page = map(int, page_range.split(","))
    input_pdf.split(output_pdf, from_page, to_page)


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
    input_pdfs = PdfFile(input_path)
    output_pdf = PdfFile(output_path)
    input_pdfs.merge(output_pdf)

if __name__ == "__main__":
    cli()
