# Changelog
All notable changes to this project will be documented in this file.


## [Unreleased]

## [0.3.2] - 2024-08-23
### Modified
+ **Refactor**
  + changed param type to `Path` and encapsulated `image_main_path` function
### Fixed
+ **Bug**
  + the first argument of `super().__init__` should not be `self`


## [0.3.1] - 2024-08-07
### Added
+ **Feature** : Optional CLI progress bar
### Modified
+ **Option** : `--range` option in the merge command
  + removed the default value
  + changed the type to `tuple[int, int]`


## [0.3.0] - 2024-08-04
### Modified
+ **Refactor** : extracted all reusable components from the CLI interface


## [0.2.1] - 2024-05-10
### Added
+ **Feature** : progress bar color - yellow & green & red


## [0.2.0] - 2024-05-05
### Added
+ **Feature** : `-S` option
+ **Feature** : command group
+ **Feature** : split PDF
+ **Feature** : merge PDF


## [0.1.0] - 2024-05-04
### Added
+ **Demo**


[Unreleased]:#Unreleased
[0.1.0]:#0.1.0
[0.2.0]:#0.2.0
[0.2.1]:#0.2.1
[0.3.0]:#0.3.0
[0.3.1]:#0.3.1
[0.3.2]:#0.3.2