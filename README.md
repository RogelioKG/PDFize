# PDFize

## Spec

+ `-I/ ` | `--img-to-pdf/--pdf-to-img` : image 轉 PDF (flag)
  ```bash
  pdfize -I "imgdir/" -o "output.pdf"
  ```

+ `-d` | `--dpi` : 指定 image 解析度 (type = int)
  ```bash
  pdfize "input.pdf" -o "output.jpeg" -d 400
  ```

+ `-e` | `--extension` : 指定 image 檔名
  ```bash
  pdfize "input.pdf" -o "imgdir/" -e webp
  ```

+ `-o` | `--output-file` : 輸出檔案 (type = str)
  ```bash
  pdfize "input.pdf" -o "output.jpeg"
  ```

## Behaviors

+ PDF : image
  + 1 PDF : 1 image
    + 表現行為同 1 PDF : m image
  + 1 PDF : m images
    + 路徑：檔案:檔案 (image 主名稱與副檔名都已指定好)
    + 路徑：檔案:目錄 (image 主名稱為原 pdf 檔名。-e 指定副檔名，預設 png)
  + m PDFs : 1 image
    + X
  + m PDFs : m images
    + 路徑：目錄:目錄 (image 主名稱為原 pdf 檔名。-e 指定副檔名，預設 png) (-S 子目錄 flag 選項)
+ image : PDF
  + 1 image : 1 PDF
    + 路徑：檔案:檔案
  + 1 image : m PDFs
    + X
  + m images : 1 PDF
    + 路徑：目錄:檔案
  + m images : m PDFs
    + X

## Third Party Library
  1. `PyMuPDF`
  2. `Pillow`
  3. `click`
  4. `tqdm`

## To-do Notes
  + [ ] -S 選項 (pdf:image 根據 pdf 放子目錄)
  + [ ] pdf 拆分
  + [ ] pdf:image 分別數字後綴 or 共用數字後綴
  + [ ] 多線程

## Developer Notes
<!-- https://www.cnblogs.com/eliwang/p/16230381.html -->
