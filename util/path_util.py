# standard library
import os
from pathlib import Path
from typing import Iterable

PathLike = str | Path

def get_filepaths(path: PathLike, *, use_pathlib=True) -> Iterable[PathLike]:
    """
    路徑需存在。
    若為檔案，回傳檔案路徑。
    若為目錄，回傳目錄中所有檔案與子目錄路徑 (lazy evaluation)。

    Parameters
    ----------
    + `path` : PathLike
        路徑
    + `pathlib` : bool
        選擇路徑是否要轉成 `pathlib.Path`

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
        return (Path(path),) if use_pathlib else (path,)
    elif os.path.isdir(path):
        return map(Path, os.scandir(path)) if use_pathlib else os.scandir(path)
    else:
        raise FileNotFoundError(f"'{path}' does not exist.")
    


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
    if not os.path.exists(dir_path): # 不存在
        os.makedirs(dir_path)
    elif os.listdir(dir_path): # 存在且但不為空目錄
        raise FileExistsError(f"Directory '{os.path.abspath(dir_path)}' not empty.")
