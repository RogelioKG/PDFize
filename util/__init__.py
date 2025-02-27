# standard library
from multiprocessing.synchronize import RLock

# third party library
from tqdm import tqdm

# local library
from .progress_bar import CLIPbar


def initializer(pbar_output_lock: RLock, pbar_style: str) -> None:
    """
    新 process 的初始化設定

    Parameters
    ----------
    + `pbar_output_lock` : RLock
        進度條輸出鎖 (由 main process 提供)
    + `pbar_style` : str
        進度條樣式 (See also `progress_bar.PbarStyle`)
    """
    tqdm.set_lock(pbar_output_lock)
    CLIPbar.style = pbar_style