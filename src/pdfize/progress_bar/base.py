# standard library
from types import TracebackType
from typing import Protocol


class Pbar(Protocol):
    style: str

    def __init__(self, *args, **kwargs) -> None: ...

    def __enter__(self) -> "Pbar": ...

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
        """Dummy 進度條"""
        pass

    def __enter__(self) -> "NoPbar":
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
