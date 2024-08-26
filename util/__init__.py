# standard library
from multiprocessing import RLock

# third party library
from tqdm import tqdm

# local library
from .progress_bar import CLIPbar


PBAR_OUTPUT_LOCK = RLock()


def initializer(pbar_output_lock, pbar_style: str) -> None:
    """Initialize progress bar settings.

    This function sets up the progress bar by configuring the lock for 
    thread-safe output and setting the style for the progress bar.

    Parameters
    ----------
    + `pbar_output_lock` : RLock
        A lock object used to ensure thread-safe access to the progress 
        bar output across multiple processes.
    + `pbar_style` : str
        A string representing the style to be applied to the progress bar.
        This style is shared across processes.
        See also `progress_bar.PbarStyle`.
    """
    tqdm.set_lock(pbar_output_lock)
    CLIPbar.style = pbar_style