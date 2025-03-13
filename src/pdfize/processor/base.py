# standard library
import os
from collections.abc import Iterable
from pathlib import Path

# local module
from ..progress_bar.base import Pbar


class Processor:
    def __init__(self, path: str | Path, *, pbar_class: type[Pbar]) -> None:
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
        filepaths: Iterable[Path]

        if os.path.isfile(self.path):
            filepaths = (self.path,)
        elif os.path.isdir(self.path):
            filepaths = (Path(entry.path) for entry in os.scandir(self.path))
        else:
            raise FileNotFoundError(f"'{self.path.resolve()}' does not exist.")

        if isinstance(suffix, str):
            filepaths = filter(lambda filepath: filepath.suffix == suffix, filepaths)
        elif isinstance(suffix, set):
            filepaths = filter(lambda filepath: filepath.suffix in suffix, filepaths)

        return filepaths
