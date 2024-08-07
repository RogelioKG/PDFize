# third party library
import click

# local library
from util.image_util import *
from util.path_util import *
from util.pdf_util import *


@click.group()
@click.option(
    "--pbar/--no-pbar",
    "has_pbar",
    default=True,
    show_default=True,
    help="Enable or disable the CLI progress bar. Use --pbar to enable and --no-pbar to disable",
)
@click.pass_context
def cli(ctx: click.Context, has_pbar: bool):
    ctx.ensure_object(dict)
    ctx.obj["HAS_PBAR"] = has_pbar


@cli.command("pdf-to-img", short_help="Convert PDF to image")
@click.option(
    "--subdir",
    "subdir",
    is_flag=True,
    default=False,
    show_default=True,
    help="If this flag is set, use the original PDF filename as the name of subdirectory",
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
    type=click.Path(exists=False, file_okay=False, dir_okay=True, resolve_path=True),
    help="Output directory",
)
@click.argument(
    "input_path",
    nargs=1,
    required=True,
    type=click.Path(
        exists=True, file_okay=True, dir_okay=True, readable=True, resolve_path=True
    ),
)
@click.pass_context
def pdf_to_img(
    ctx: click.Context,
    input_path: str,
    output_path: str,
    subdir: bool,
    dpi: int,
    format: str,
    name: str | None = None,
):
    has_pbar: bool = ctx.obj["HAS_PBAR"]
    pdf = PdfProcessor(input_path, pbar_class=CLIPbar if has_pbar else NoPbar)
    image = ImageProcessor(output_path)
    pdf.to_images(image, dpi, format, name, subdir=subdir)


@cli.command("img-to-pdf", short_help="Convert image to PDF")
@click.option(
    "-o",
    "--output",
    "output_path",
    type=click.Path(exists=False, file_okay=True, dir_okay=False, resolve_path=True),
    help="Output file",
)
@click.argument(
    "input_path",
    nargs=1,
    required=True,
    type=click.Path(
        exists=True, file_okay=True, dir_okay=True, readable=True, resolve_path=True
    ),
)
@click.pass_context
def img_to_pdf(ctx: click.Context, input_path: str, output_path: str):
    has_pbar: bool = ctx.obj["HAS_PBAR"]
    image = ImageProcessor(input_path, pbar_class=CLIPbar if has_pbar else NoPbar)
    pdf = PdfProcessor(output_path)
    image.to_pdf(pdf)


@cli.command("split", short_help="Split PDF")
@click.option(
    "-o",
    "--output",
    "output_path",
    required=True,
    type=click.Path(exists=False, file_okay=True, dir_okay=False, resolve_path=True),
    help="Output file",
)
@click.option(
    "-r",
    "--range",
    "page_range",
    type=(int, int),
    help="Specifies the range of pages to copy using 1-based indexing, with support for negative indices. If the start page is greater than the end page, the pages will be copied in reverse order. Note: '-1' represents the last page",
)
@click.argument(
    "input_path",
    nargs=1,
    required=True,
    type=click.Path(
        exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True
    ),
)
@click.pass_context
def pdf_split(
    ctx: click.Context, input_path: str, output_path: str, page_range: tuple[int, int]
):
    has_pbar: bool = ctx.obj["HAS_PBAR"]
    input_pdf = PdfProcessor(input_path, pbar_class=CLIPbar if has_pbar else NoPbar)
    output_pdf = PdfProcessor(output_path)
    from_page, to_page = page_range
    input_pdf.split(output_pdf, from_page, to_page)


@cli.command("merge", short_help="Merge PDF")
@click.option(
    "-o",
    "--output",
    "output_path",
    required=True,
    type=click.Path(exists=False, file_okay=True, dir_okay=False, resolve_path=True),
    help="Output file",
)
@click.argument(
    "input_path",
    nargs=1,
    required=True,
    type=click.Path(
        exists=True, file_okay=True, dir_okay=True, readable=True, resolve_path=True
    ),
)
@click.pass_context
def pdf_merge(ctx: click.Context, input_path: str, output_path: str):
    has_pbar: bool = ctx.obj["HAS_PBAR"]
    input_pdfs = PdfProcessor(input_path, pbar_class=CLIPbar if has_pbar else NoPbar)
    output_pdf = PdfProcessor(output_path)
    input_pdfs.merge(output_pdf)


if __name__ == "__main__":
    cli()
