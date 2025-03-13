# standard library
import multiprocessing as mp
from pathlib import Path

# third party library
import click
from click_help_colors import HelpColorsGroup, version_option

# local module
from .info import __project__, __version__
from .new_process import init, lock
from .processor.image_processor import ImageSingleProcessor
from .processor.pdf_processor import (
    PdfParallelProcessor,
    PdfProcessor,
    PdfSingleProcessor,
)
from .progress_bar.base import NoPbar
from .progress_bar.cli import CLIPbar
from .progress_bar.enums import PbarStyle


class ColorChoice(click.Choice):
    def get_metavar(self, param):
        return "[PbarStyle]"

    def get_help_record(self):
        return f"Progress bar style ({', '.join(self.choices)})."


color_choice_type = ColorChoice([item.name for item in PbarStyle])


@click.group(
    cls=HelpColorsGroup,
    help_headers_color="bright_cyan",
    help_options_color="bright_blue",
    no_args_is_help=True,
)
@version_option(
    prog_name=__project__,
    prog_name_color="bright_cyan",
    version=__version__,
    version_color="bright_blue",
    message="%(prog)s %(version)s",
)
@click.option(
    "--pbar/--no-pbar",
    "has_pbar",
    is_flag=True,
    default=True,
    show_default=True,
    help="""
    Enable or disable the CLI progress bar. Use --pbar to enable and --no-pbar to disable.
    """,
)
@click.option(
    "-s",
    "--style",
    "pbar_style",
    default=PbarStyle.ASCII_BOX.name,
    show_default=True,
    help=color_choice_type.get_help_record(),
    type=color_choice_type,
)
@click.pass_context
def pdfize(ctx: click.Context, has_pbar: bool, pbar_style: str) -> None:
    ctx.ensure_object(dict)
    ctx.obj["HAS_PBAR"] = has_pbar
    init.initializer(lock.PBAR_OUTPUT_LOCK, pbar_style)


@pdfize.command("pdf-to-img", short_help="Convert PDF to image.")
@click.option(
    "-w",
    "--workers",
    "workers",
    type=int,
    help="""
    Specifies the number of worker processes to use for multiprocessing.
    [default: the number of CPU cores]
    """,
)
@click.option(
    "--parallel",
    "parallel",
    is_flag=True,
    default=False,
    show_default=True,
    help="""
    Enable parallel processing to speed up PDF processing tasks.
    """,
)
@click.option(
    "--subdir",
    "subdir",
    is_flag=True,
    default=False,
    show_default=True,
    help="""
    Use the original PDF filename as the name of subdirectory.
    """,
)
@click.option("-d", "--dpi", "dpi", type=int, default=100, show_default=True, help="Image DPI.")
@click.option(
    "-f",
    "--format",
    "format",
    default="png",
    show_default=True,
    help="""
    Image file format.
    """,
)
@click.option(
    "-n",
    "--name",
    "name",
    help="""
    Image main filename.
    [default: PDF filename]
    """,
)
@click.option(
    "-o",
    "--output",
    "output_path",
    required=True,
    prompt="Output path",
    type=click.Path(exists=False, file_okay=False, dir_okay=True, resolve_path=True),
    help="""
    Output directory.
    """,
)
@click.argument(
    "input_path",
    nargs=1,
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True, resolve_path=True),
)
@click.pass_context
def pdf_to_img(
    ctx: click.Context,
    input_path: str,
    output_path: str,
    subdir: bool,
    parallel: bool,
    workers: int | None,
    dpi: int,
    format: str,
    name: str | None = None,
) -> None:
    has_pbar: bool = ctx.obj["HAS_PBAR"]
    pbar_class = CLIPbar if has_pbar else NoPbar

    # multiprorocessing
    pdf: PdfProcessor
    if parallel:
        pdf = PdfParallelProcessor(input_path, pbar_class=pbar_class, workers=workers)
    elif workers is not None:
        raise click.UsageError("The '--workers' option requires '--parallel' to be enabled.")
    else:
        pdf = PdfSingleProcessor(input_path, pbar_class=pbar_class)

    # mutual exclusion check
    if name and subdir:
        raise click.UsageError("The '--name' and '--subdir' options cannot be used together.")

    image = Path(output_path)
    pdf.to_images(image, dpi, format, name=name, subdir=subdir)


@pdfize.command("img-to-pdf", short_help="Convert image to PDF.")
@click.option(
    "-o",
    "--output",
    "output_path",
    required=True,
    prompt="Output path",
    type=click.Path(exists=False, file_okay=True, dir_okay=False, resolve_path=True),
    help="""
    Output file.
    """,
)
@click.argument(
    "input_path",
    nargs=1,
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True, resolve_path=True),
)
@click.pass_context
def img_to_pdf(ctx: click.Context, input_path: str, output_path: str):
    has_pbar: bool = ctx.obj["HAS_PBAR"]
    image = ImageSingleProcessor(input_path, pbar_class=CLIPbar if has_pbar else NoPbar)
    pdf = Path(output_path)
    image.to_pdf(pdf)


@pdfize.command("split", short_help="Split PDF.")
@click.option(
    "-o",
    "--output",
    "output_path",
    required=True,
    prompt="Output path",
    type=click.Path(exists=False, file_okay=True, dir_okay=False, resolve_path=True),
    help="""
    Output file.
    """,
)
@click.option(
    "-r",
    "--range",
    "page_range",
    type=(int, int),
    prompt="Page range",
    help="""
    Specifies the range of pages to copy using 1-based indexing, with support for negative indices.
    If the start page is greater than the end page, the pages will be copied in reverse order.
    Note: '-1' represents the last page.
    """,
)
@click.argument(
    "input_path",
    nargs=1,
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True),
)
@click.pass_context
def pdf_split(
    ctx: click.Context, input_path: str, output_path: str, page_range: tuple[int, int]
) -> None:
    has_pbar: bool = ctx.obj["HAS_PBAR"]
    input_pdf = PdfSingleProcessor(input_path, pbar_class=CLIPbar if has_pbar else NoPbar)
    output_pdf = Path(output_path)
    from_page, to_page = page_range
    input_pdf.split(output_pdf, from_page, to_page)


@pdfize.command("merge", short_help="Merge PDF.")
@click.option(
    "-o",
    "--output",
    "output_path",
    required=True,
    prompt="Output path",
    type=click.Path(exists=False, file_okay=True, dir_okay=False, resolve_path=True),
    help="""
    Output file.
    """,
)
@click.argument(
    "input_path",
    nargs=1,
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True, resolve_path=True),
)
@click.pass_context
def pdf_merge(ctx: click.Context, input_path: str, output_path: str) -> None:
    has_pbar: bool = ctx.obj["HAS_PBAR"]
    input_pdfs = PdfSingleProcessor(input_path, pbar_class=CLIPbar if has_pbar else NoPbar)
    output_pdf = Path(output_path)
    input_pdfs.merge(output_pdf)


if __name__ == "__main__":
    mp.freeze_support()  # support freeze executable on Windows (if using multiprocessing)
    pdfize()
