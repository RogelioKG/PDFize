# standard library
from __future__ import annotations
from types import TracebackType
from typing import Protocol

# third party library
from tqdm import tqdm


YELLOW = "#F0C239"  # 進度條顏色：執行中
GREEN = "#44B159"  # 進度條顏色：正常結束
PINK = "#E75480"  # 進度條顏色：異常結束


class Pbar(Protocol):
    def __init__(self, total: int, unit: str) -> None: ...
    def __enter__(self) -> Pbar: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...
    def update(self, n: float) -> None: ...


class NoPbar:
    def __init__(self, total: int, unit: str):
        pass

    def __enter__(self) -> NoPbar:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        pass

    def update(self, n: float):
        pass


class CLIPbar(tqdm):

    style = {"ascii": "░▒█", "colour": YELLOW, "leave": True}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **CLIPbar.style, **kwargs)

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """上下文管理器：增寫功能 - 結束時改變顏色"""
        if exc_type:
            self.colour = PINK
        else:
            self.colour = GREEN
        self.refresh()
        super().__exit__(exc_type, exc_value, traceback)


class GUIPbar:  # TODO: This feature will be implemented someday.
    def __init__(self, total: int, unit: str):
        pass

    def update(self, n: float):
        pass
