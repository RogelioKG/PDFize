# standard library
from multiprocessing import RLock

# third party library
from tqdm import tqdm

# local library
from .progress_bar import CLIPbar


PBAR_OUTPUT_LOCK = RLock()


def initializer(pbar_output_lock, pbar_style: str) -> None:
    """
    新 process 的初始化設定

    Parameters
    ----------
    + `pbar_output_lock` : RLock
        進度條輸出鎖
    + `pbar_style` : str
        進度條樣式 (See also `progress_bar.PbarStyle`)
    """
    tqdm.set_lock(pbar_output_lock)
    CLIPbar.style = pbar_style