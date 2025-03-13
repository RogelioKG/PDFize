# standard library
from enum import Enum


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
