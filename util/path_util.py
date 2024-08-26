# standard library
from pathlib import Path
import os


def try_makedir(dir_path: str | Path) -> None:
    """
    嘗試創建目錄。

    Parameters
    ----------
    + `dir_path` : str | Path
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


def add_serial(path: Path, serial: int, *, zfill: bool = False) -> Path:
    """
    附加流水號

    Parameters
    ----------
    + `path` : Path
        路徑
    + `serial` : int
        流水號
    + `zfill` : bool, optional
        是否填滿 0

    Returns
    -------
    + Path
    """
    serial_str = str(serial)
    if zfill:
        serial_str = serial_str.zfill(16)
    return path.with_stem(f"{path.stem}-{serial_str}")
