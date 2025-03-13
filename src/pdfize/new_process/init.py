# standard library
from multiprocessing.synchronize import RLock

# third party library
from tqdm import tqdm

# local module
from ..progress_bar.cli import CLIPbar


def initializer(pbar_output_lock: RLock, pbar_style: str) -> None:
    """
    新 process 的初始化設定

    Parameters
    ----------
    + `pbar_output_lock` : RLock
        進度條輸出鎖
    + `pbar_style` : str
        進度條樣式 (詳見 `src.progress_bar.enums.PbarStyle`)
    """
    tqdm.set_lock(pbar_output_lock)
    CLIPbar.style = pbar_style
