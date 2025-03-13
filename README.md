# PDFize

[![python-version](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/downloads/release/python-3114/)
[![License](https://img.shields.io/github/license/RogelioKG/PDFize?style=flat)](./LICENSE)

## Brief
Just a simple command-line tool for converting PDF files into images, with support for multiprocessing to enhance performance.
<!-- GIF -->
![pdfize](./demo/pdfize.gif?raw=true)

## Installation
```bash
pip install pdfize
```

## Third Party Library

  1. `PyMuPDF` : AGPL 3.0
  2. `Pillow` : HPND
  3. `click` : BSD
  4. `tqdm` : MIT, MPL 2.0
  5. `click-help-colors` : MIT

## Help

+ general options

  + `--pbar/--no-pbar` : 開啟命令行進度條 (flag)

  + `-s` | `--style` : 進度條樣式
    ```bash
    ASCII_GRADIENT :  ░▒▓█
    ASCII_PIXEL    :  ▖▘▝▗▚▞█
    ASCII_SQUARE   :  ▨■
    ASCII_CIRCLE   :  ○◐⬤
    ASCII_SPEED    :  ▱▰
    ASCII_DOT      :  ⣀⣦⣿
    ASCII_BOX      :  ▯▮
    ```

+ command

  + `img-to-pdf` : image 轉 PDF

    + `-o` | `--output` : 指定 pdf 檔案名稱
      ```bash
      pdfize img-to-pdf "input.jpeg" -o "output.pdf"
      pdfize img-to-pdf "images_dir/" -o "output.pdf"
      ```

  + `pdf-to-img` : PDF 轉 image

    + `-d` | `--dpi` : 指定 image 解析度 (預設: 100)
      ```bash
      pdfize pdf-to-img "input.pdf" -o "output/" -d 400
      ```

    + `-f` | `--format` : 指定 image 格式 (預設: png)
      ```bash
      pdfize pdf-to-img "input.pdf" -o "imgdir/" -f "webp"
      ```

    + `-n` | `--name` : 指定 image 主名稱 (預設: 同輸入 pdf 名稱)
      ```bash
      pdfize pdf-to-img "input.pdf" -o "imgdir/" -n "output"
      ```

    + `-o` | `--output` : 指定 image 目錄名稱
      ```bash
      pdfize pdf-to-img "input.pdf" -o "imgdir/"
      ```

    + `--parallel` : 開啟多進程平行執行 (flag)
      ```bash
      pdfize pdf-to-img "input.pdf" -o "imgdir/" --parallel
      ```

    + `--subdir` : 有多個 pdf 時，以原 pdf 名稱作為子目錄 (flag)
      ```bash
      pdfize pdf-to-img "pdfs_dir/" -o "result/" --subdir
      ```

    + `-w` | `--worker` : 若有開啟多進程平行執行，選擇使用幾顆 cores 加速
      > 開很多 process 速度加倍，但會吃非常多記憶體
      ```bash
      pdfize pdf-to-img "pdfs_dir/" -o "result/" --parallel -w 4 
      ```

  + `split` : PDF 拆分

    + `-o` | `--output` : 輸出 pdf 檔案
      ```bash
      pdfize split "input.pdf" -r 2 5 -o "output.pdf"
      ```

    + `-r` | `--range` : 頁數範圍
      > 支援負數索引 (如 -1 代表最後一頁)。若 from 頁數比 to 頁數後面，表示倒序。
      ```bash
      pdfize split "input.pdf" -r 2 5 -o "output.pdf"
      pdfize split "input.pdf" -r 2 -1 -o "output.pdf"
      pdfize split "input.pdf" -r 5 2 -o "output.pdf"
      pdfize split "input.pdf" -r -2 2 -o "output.pdf"
      ```

  + `merge` : PDF 合併

    + `-o` | `--output` : 輸出檔案
      ```bash
      pdfize merge "pdfs_dir/" -o "output.pdf"
      ```
