# standard library
from types import TracebackType

# third party library
from tqdm import tqdm

# local library
from config import DEBUG


class Pbar(tqdm):
    __yellow = "#F0C239"  # 執行中
    __green = "#44B159"  # 沒有發生錯誤，正常結束
    __pink = "#E75480"  # 發生錯誤，異常結束
    style = {"ascii": "░▒█", "colour": __yellow, "disable": DEBUG, "leave": True}

    def __init__(self, **kwarg):
        super().__init__(self, **Pbar.style, **kwarg)

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """上下文管理器：增寫功能 - 結束時改變顏色"""
        if exc_type:
            self.colour = Pbar.__pink
        else:
            self.colour = Pbar.__green
        self.refresh()
        super().__exit__(exc_type, exc_value, traceback)
