# Changelog
All notable changes to this project will be documented in this file.


## [Unreleased]

## [0.3.5] - 2025-03-13
### Update
+ **Pypi**
  + you can use `pip install pdfize` to download this tool now
+ **Package Manager**
  + switch to `uv`

## [0.3.4] - 2025-02-28
### Modify
+ **Refactor**
  + directory structure
### Update
+ **Types**
  + mypy check
### Add
+ **CLI**
  + colorized help info


## [0.3.3] - 2024-08-27
### Add
+ **Progress Bar**
  + new color & ascii style
+ **Feature**
  + multiprocessing (`pdf-to-image` command)
+ **CLI**
  + add `--parallel` flag
  + add `-w` option


## [0.3.2] - 2024-08-23
### Modify
+ **Refactor**
  + changed param type to `Path` and encapsulated `image_main_path` function
### Fix
+ **Mistake**
  + the first argument of `super().__init__` should not be `self`


## [0.3.1] - 2024-08-07
### Add
+ **Progress Bar**
  + optional CLI progress bar
### Modify
+ **CLI**
  + `--range` option (`merge` command)
    + removed the default value
    + changed the type to `tuple[int, int]`


## [0.3.0] - 2024-08-04
### Modify
+ **Refactor**
  + extracted all reusable components from the CLI interface


## [0.2.1] - 2024-05-10
### Add
+ **Progress Bar**
  + color - yellow & green & red


## [0.2.0] - 2024-05-05
### Add
+ **CLI**
  + add `--subdir` option (`pdf-to-image` command)
  + add command group
  + add `split` command
  + add `merge` command


## [0.1.0] - 2024-05-04
### Add
+ **Demo**
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


[Unreleased]:#Unreleased
[0.1.0]:#0.1.0
[0.2.0]:#0.2.0
[0.2.1]:#0.2.1
[0.3.0]:#0.3.0
[0.3.1]:#0.3.1
[0.3.2]:#0.3.2
[0.3.3]:#0.3.3
[0.3.4]:#0.3.4
[0.3.5]:#0.3.5**