# standard library
from types import TracebackType

# third party library
from tqdm import tqdm

# local library
from config import DEBUG


class Pbar(tqdm):
    __green = "#44B159"
    __pink = "#E75480"
    style = {"ascii": "░▒█", "leave": True, "colour": __pink, "disable": DEBUG}

    def __init__(self, **kwarg):
        super().__init__(self, **Pbar.style, **kwarg)

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """上下文管理器增寫功能，結束後將顏色改成綠色"""
        self.colour = Pbar.__green
        self.refresh()
        super().__exit__(exc_type, exc_value, traceback)
