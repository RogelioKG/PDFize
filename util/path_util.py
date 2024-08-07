# standard library
import os
from pathlib import Path
from typing import Iterable

PathLike = str | Path


def get_filepaths(
    path: PathLike, *, suffix: set[str] | str | None = None
) -> Iterable[Path]:
    """
    路徑需存在。
    若為檔案，回傳檔案路徑。
    若為目錄，回傳目錄中所有檔案與子目錄路徑 (lazy evaluation)。

    Parameters
    ----------
    + `path` : PathLike
        路徑
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
    if os.path.isfile(path):
        filepaths = (Path(path),)
    elif os.path.isdir(path):
        filepaths = map(Path, os.scandir(path))
    else:
        raise FileNotFoundError(f"'{path}' does not exist.")

    if isinstance(suffix, str):
        filepaths = filter(
            lambda filepath: getattr(filepath, "suffix") == suffix, filepaths
        )
    elif isinstance(suffix, set):
        filepaths = filter(
            lambda filepath: getattr(filepath, "suffix") in suffix, filepaths
        )

    return filepaths


def try_makedir(dir_path: PathLike) -> None:
    """
    嘗試創建目錄。

    Parameters
    ----------
    + `dir_path` : PathLike
        路徑

    Raises
    ------
    + FileExistsError
        不為空目錄所引起的錯誤
    """
    if not os.path.exists(dir_path):  # 不存在
        os.makedirs(dir_path)
    elif os.listdir(dir_path):  # 存在且但不為空目錄
        raise FileExistsError(f"Directory '{os.path.abspath(dir_path)}' not empty.")
