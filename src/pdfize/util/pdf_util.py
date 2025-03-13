# standard library
from pathlib import Path

# third party library
import fitz


def zero_base_indexing(page_num: int, page_count: int) -> int:
    """
    將 1-base indexing (which support negative `page_num`) 的頁碼
    轉為 0-base indexing (which support positive `page_num` only) 的頁碼

    Parameters
    ----------
    + `page_num` : int
    + `page_count` : int

    Returns
    -------
    + int
    """
    if page_num < 0:
        page_num += page_count
    elif page_num > 0:
        page_num -= 1
    else:
        raise ValueError("Invalid page number: 1-based indexing does not include 0.")

    assert 0 <= page_num < page_count

    return page_num


def divide(page_count: int, workers: int) -> list[tuple[int, int]]:
    """
    將給定頁數切成數份分給 workers，回傳每個 worker 負責的起終點頁碼

    Parameters
    ----------
    + `page_count` : int
        總頁數
    + `workers` : int
        有幾個 workers 要分擔工作

    Returns
    -------
    + list[tuple[int, int]]
        每個 worker 負責的起終點頁碼 (using 1-based indexing)

    Example
    -------
    >>> divide(250, 5)
    [(1, 50), (51, 100), (101, 150), (151, 200), (201, 250)]
    >>> divide(254, 5)
    [(1, 51), (52, 102), (103, 153), (154, 204), (205, 254)]
    >>> divide(3, 5)
    AssertionError
    """
    assert page_count >= workers

    pages_per_worker = page_count // workers
    remainder = page_count % workers

    page_ranges = []
    start_page = 1

    for i in range(workers):
        end_page = start_page + pages_per_worker - 1
        if i < remainder:
            end_page += 1
        page_ranges.append((start_page, end_page))
        start_page = end_page + 1

    return page_ranges


def get_pdf_page_count(filepath: str | Path) -> int:
    # 開啟多進程加速多 pdf 且又有 --name 選項時，
    # 為了確保流水號的順序性，逼不得以需開啟 pdf 得知 page_count。
    doc = fitz.open(filepath)
    page_count = doc.page_count
    doc.close()

    return page_count
