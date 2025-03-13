# standard library
from types import TracebackType

# third party library
from tqdm import tqdm

# local module
from .enums import PbarColor, PbarStyle


class CLIPbar(tqdm):
    style = PbarStyle.ASCII_BOX.name

    def __init__(self, *args, main: bool = False, **kwargs) -> None:
        """CLI 進度條 (繼承自 `tqdm.tqdm`)

        Note
        ---
        if `main=True`, color would be orange
        """
        if kwargs.get("ascii") is None:
            kwargs["ascii"] = PbarStyle[CLIPbar.style].value
        if kwargs.get("colour") is None:
            if main:
                kwargs["colour"] = PbarColor.ORANGE.value
            else:
                kwargs["colour"] = PbarColor.YELLOW.value
        super().__init__(*args, **kwargs)

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """
        Note
        ---
        context manager - change color upon completion
        """
        self.colour = PbarColor.PINK.value if exc_type else PbarColor.GREEN.value
        self.refresh()
        super().__exit__(exc_type, exc_value, traceback)
