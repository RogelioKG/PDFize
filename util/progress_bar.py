# standard library
from __future__ import annotations
from types import TracebackType
from typing import Protocol
from enum import Enum

# third party library
from tqdm import tqdm


# 樣式
class PbarStyle(Enum):
    ASCII_GRADIENT = "░▒▓█"
    ASCII_PIXEL = " ▖▘▝▗▚▞█"
    ASCII_SQUARE = " ▨■"
    ASCII_CIRCLE = " ○◐⬤"
    ASCII_SPEED = " ▱▰"
    ASCII_DOT = " ⣀⣦⣿"
    ASCII_BOX = " ▯▮"


# 顏色
class PbarColor(Enum):
    ORANGE = "#CF5B22"  # 主進度條顏色：執行中
    YELLOW = "#F0C239"  # 進度條顏色：執行中
    GREEN = "#44B159"  # 進度條顏色：正常結束
    PINK = "#E75480"  # 進度條顏色：異常結束


class Pbar(Protocol):
    style: str

    def __init__(self, *args, **kwargs) -> None: ...

    def __enter__(self) -> Pbar: ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...

    def update(self, n: float | None) -> bool | None: ...


class NoPbar:
    style = ""

    def __init__(self, *args, **kwargs):
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

    def update(self, n: float | None) -> bool | None:
        pass


class CLIPbar(tqdm):
    style = PbarStyle.ASCII_BOX.name

    def __init__(self, *args, main: bool = False, **kwargs) -> None:
        """NOTE: if `main=True`, color would be orange"""
        if kwargs.get("ascii") is None:
            kwargs["ascii"] = PbarStyle[CLIPbar.style].value
        if kwargs.get("colour") is None:
            kwargs["colour"] = (
                PbarColor.ORANGE.value if main else PbarColor.YELLOW.value
            )
        super().__init__(*args, **kwargs)

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """NOTE: context manager - change color upon completion"""
        self.colour = PbarColor.PINK.value if exc_type else PbarColor.GREEN.value
        self.refresh()
        super().__exit__(exc_type, exc_value, traceback)


class GUIPbar:  # TODO: This feature will be implemented someday.
    style = ""

    def __init__(self, *args, **kwargs) -> None:
        pass

    def update(self, n: float | None) -> bool | None:
        pass
