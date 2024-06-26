# PDFize

## Breif
純粹練習 git workflow 與嘗試寫寫看 CLI tool

## Third Party Library
  1. `PyMuPDF`
  2. `Pillow`
  3. `click`
  4. `tqdm`
  5. `pyinstaller`

## Spec

+ `img-to-pdf` : image 轉 PDF

  + `-o` | `--output-file` : 輸出檔案
    ```bash
    pdfize "input.jpeg" -o "output.pdf"
    ```

+ `pdf-to-img` : PDF 轉 image

  + `-S/ ` | `--subdir` : 以原 PDF 名稱作為子目錄，輸出路徑限定目錄 (flag)
    ```bash
    pdfize -S "pdfdir/" -o "result/"
    ```

  + `-d` | `--dpi` : 指定 image 解析度
    ```bash
    pdfize "input.pdf" -o "output.jpeg" -d 400
    ```

  + `-e` | `--extension` : 指定 image 檔名 (預設 png)
    ```bash
    pdfize "input.pdf" -o "imgdir/" -e webp
    ```

  + `-o` | `--output-file` : 輸出檔案
    ```bash
    pdfize "input.pdf" -o "output.jpeg"
    ```

+ `split` : PDF 拆分

  + `-o` | `--output-file` : 輸出檔案
    ```bash
    pdfize "input.pdf" -o "output.pdf"
    ```

  + `-r` | `--range` : 頁數範圍 (預設 from 1 to -1)
    > -1 代表最後一頁。若 from 頁數比 to 頁數後面，表示倒序。
    ```bash
    pdfize "input.pdf" -r 2,5 -o "output.pdf"
    pdfize "input.pdf" -r 2,-1 -o "output.pdf"
    pdfize "input.pdf" -r 5,2 -o "output.pdf"
    pdfize "input.pdf" -r -1,2 -o "output.pdf"
    ```
+ `merge` : PDF 合併

  + `-o` | `--output-file` : 輸出檔案
    ```bash
    pdfize "pdfdir/" -o "output.pdf"
    ```

## Behaviors

+ PDF : image
  + 1 PDF : 1 image
    + 表現行為同 1 PDF : m image
  + 1 PDF : m images
    + 路徑：檔案:檔案 (image 主名稱與副檔名都已指定好)
    + 路徑：檔案:目錄 (image 主名稱為原 pdf 檔名。) (-e 指定副檔名)
  + m PDFs : 1 image
    + X
  + m PDFs : m images
    + 路徑：目錄:目錄 (image 主名稱為原 pdf 檔名。)(-e 指定副檔名) (-S 子目錄 flag 選項)
+ image : PDF
  + 1 image : 1 PDF
    + 路徑：檔案:檔案
  + 1 image : m PDFs
    + X
  + m images : 1 PDF
    + 路徑：目錄:檔案
  + m images : m PDFs
    + X

## To-do Notes
  + [ ] 多線程

## Developer Notes
