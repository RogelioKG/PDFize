# PDFize

a command-line tool that converts PDF files into images

## Third Party Library
  1. `PyMuPDF`
  2. `Pillow`
  3. `click`
  4. `tqdm`
  5. `pyinstaller`
  6. `multiprocessing`

## Help

+ general options

  + `--pbar/--no-pbar` : 開啟命令行進度條 (flag)

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
      pdfize pdf-to-img "input.pdf" -o "imgdir/" -e "webp"
      ```

    + `-n` | `--name` : 指定 image 主名稱 (預設: 同輸入 pdf 名稱)
      ```bash
      pdfize pdf-to-img "input.pdf" -o "imgdir/" -n "output"
      ```

    + `-o` | `--output` : 指定 image 目錄名稱
      ```bash
      pdfize pdf-to-img "input.pdf" -o "imgdir/"
      ```

    + `--subdir` : 有多個 pdf 時，以原 pdf 名稱作為子目錄 (flag)
      ```bash
      pdfize pdf-to-img "pdfs_dir/" -o "result/" --subdir
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

## Behaviors

+ PDF -> image
  + 1 PDF -> 1 image
    + 路徑：檔案 -> 目錄
  + 1 PDF -> m images
    + 路徑：檔案 -> 目錄
  + m PDFs -> 1 image
    + x
  + m PDFs -> m images
    + 路徑：目錄 -> 目錄
+ image -> PDF
  + 1 image -> 1 PDF
    + 路徑：檔案 -> 檔案
  + 1 image -> m PDFs
    + x
  + m images -> 1 PDF
    + 路徑：目錄 -> 檔案
  + m images -> m PDFs
    + x

## To-do Notes
  + [ ] GUI