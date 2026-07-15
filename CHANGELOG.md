# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.2.0] - 2026-07-XX

### Added

- Partial implementation of the OpenCV library:
  * **Drawing:** CIRCLE, FILLPOLY, LINE, PUT_TEXT, RECTANGLE, DRAW_ARUCO_MARKERS
  * **Filtering:** BLUR, BUILD_PYRAMID, DILATE, ERODE, GAUSSIAN_BLUR, LAPLACIAN, MEDIAN_BLUR, MORPHOLOGY_EX, SCHARR, SOBEL
  * **Detectors:** ARUCO_DETECTOR, CORNER_HARRIS, GOOD_FEATURES_TO_TRACK
  * **Tranforms:** ADAPTIVE_THRESHOLD, CVT_COLOR, RESIZE, THRESHOLD, WARP_AFFINE, WARP_PERSPECTIVE, WARP_POLAR
  * **Videoprocessing:** CAMERA, IMREAD, IMWRITE, IMSHOW, VIDEOWRITER
- OpenCV usage examples
- OPC UA client block
- MQTT client block
- Build-in IDE project converter utility — migration from `Version 2.0` to `Version 3.0`.

### Changed

- Updated OPC UA variables publication format — the structure of the transmitted data corresponds to 4diac forte.
- Stability improvements

## [1.1.0] - 2026-05-08

### Added
- New method for registraion inputs and outputs of functional block in OPC UA server.
- CLI support: the project can now be installed as a Python module in a virtual environment and used as a command-line utility.
- Logging handler to forward logs to an arbitrary UNIX socket for integration with logging collector tools.
- Expanded functional block library with new modules: `convert`, `events`, `iec61131`, `utils`.

### Changed
- Refactored project structure.
- Fixed OPC UA node value updates in the embedded server.
- Standardized log output using Python's built-in `logging` module.
- Updated CLI startup arguments.
- Updated project dependencies.

### Removed
- Functional block execution analytics.

## [1.0.0] - 2025-12-10

- Initial release.