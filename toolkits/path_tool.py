# standard library
import os
from pathlib import Path
from typing import Generator, Any


def get_files(path: Path) -> Generator[Path, Any, None]:
    """若路徑存在且為檔案，生成檔案名稱。若路徑存在且為目錄，生成目錄中檔案名稱。

    Parameters
    ----------
    + `path` : Path
        路徑

    Returns
    -------
    + Generator[Path, Any, None]
        檔案名稱生成器
    """
    if path.is_file():  # 如果路徑存在且為檔案
        yield path
    elif path.is_dir():  # 如果路徑存在且為目錄
        yield from path.iterdir()  # 生成器委託


def try_create_dir(path: Path) -> None:
    """
    若路徑為檔案，確認其父目錄是否存在，若存在但內有東西，丟出例外；若不存在則創建。
    若路徑為目錄，確認其是否存在。若存在但內有東西，丟出例外；若不存在則創建。

    Parameters
    ----------
    + `path` : Path
        路徑

    Raises
    ------
    + FileExistsError
        丟出例外。
    """

    d = path.parent if path.suffix else path

    if d.exists():  # 目錄存在
        try:
            if next(d.iterdir()):  # 若內有東西
                raise FileExistsError(f"Directory {d} not empty!")
        except StopIteration: # 空目錄
            pass
    else:
        os.makedirs(d)  # 創建目錄
