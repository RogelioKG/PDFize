# standard library
from pathlib import Path
from typing import Type, Iterable
import os

# local library
from .progress_bar import Pbar


class Processor:
    def __init__(self, path: str | Path, *, pbar_class: Type[Pbar]) -> None:
        """
        Parameters
        ----------
        + `path` : str
            路徑 (可為目錄或檔案)
        + `pbar_class`: Type[Pbar]
            進度條類型
        """
        self.path = Path(path)
        self.pbar_class = pbar_class

    def get_filepaths(self, *, suffix: set[str] | str | None = None) -> Iterable[Path]:
        """
        路徑需存在。
        若為檔案，回傳檔案路徑。
        若為目錄，回傳目錄中所有檔案與子目錄路徑 (lazy evaluation)。

        Parameters
        ----------
        + `suffix` : set[str] | str | None
            限定副檔名 (for example: ".pdf" or {".jpg", ".png"})

        Returns
        -------
        + Iterable[PathLike]
            所有檔案名稱

        Raises
        ------
        + FileNotFoundError
            路徑不存在所引起的錯誤
        """
        if os.path.isfile(self.path):
            filepaths = (self.path,)
        elif os.path.isdir(self.path):
            filepaths = map(Path, os.scandir(self.path))
        else:
            raise FileNotFoundError(f"'{self.path.resolve()}' does not exist.")

        if isinstance(suffix, str):
            filepaths = filter(lambda filepath: filepath.suffix == suffix, filepaths)
        elif isinstance(suffix, set):
            filepaths = filter(lambda filepath: filepath.suffix in suffix, filepaths)

        return filepaths


class PdfProcessor(Processor):
    def __init__(self, path: str, *, pbar_class: Type[Pbar]):
        super().__init__(path, pbar_class=pbar_class)

    def to_images(
        self,
        image: Path,
        dpi: int,
        format: str,
        *,
        name: str | None,
        subdir: bool,
    ) -> None:
        """
        將 pdf 轉為 image
        """
        raise NotImplementedError

    def split(self, output_pdf: Path, from_page: int, to_page: int) -> None:
        """
        將 pdf 拆分
        """
        raise NotImplementedError

    def merge(self, output_pdf: Path) -> None:
        """
        將 pdf 合併
        """
        raise NotImplementedError


class ImageProcessor(Processor):
    def __init__(self, path: str | Path, *, pbar_class: Type[Pbar]):
        super().__init__(path, pbar_class=pbar_class)

    def to_pdf(self, pdf: Path):
        """
        將 image 轉為 pdf
        """
        raise NotImplementedError
