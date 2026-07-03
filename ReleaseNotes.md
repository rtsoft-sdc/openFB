# Release Notes — OpenFB Version 1.2

## New features

* **Partial implementation of the OpenCV library (up to version `4.13`)**
  * **Drawing:** CIRCLE, FILLPOLY, LINE, PUT_TEXT, RECTANGLE, DRAW_ARUCO_MARKERS
  * **Filtering:** BLUR, BUILD_PYRAMID, DILATE, ERODE, GAUSSIAN_BLUR, LAPLACIAN, MEDII_BLUR, MORPHOLOGY_EX, SCHARR, SOBEL
  * **Trackers:** ARUCO_DETECTOR, CORNER_HARRIS, GOOD_FEATURES_TO_TRACK
  * **Tranforms:** ADAPTIVE_THRESHOLD, CVT_COLOR, RESIZE, THRESHOLD, WARP_AFFINE, WARP_PERSPECTIVE, WARP_POLAR
  * **Videoprocessing:** CAMERA, IMREAD, IMWRITE, IMSHOW, VIDEOWRITER
* **Added OpenCV usage example**
* **Added OPC UA client block**
* **Added MQTT client block** 
* **Added the project converter utility** — migration from **Version 2.0** to **Version 3.0**.

## Changes and improvements

* **Updated OPC UA variables publication format** — the structure of the transmitted data corresponds to 4diac forte.
* **Error correction**



## Новые функции

* **Частичная реализация библиотеки OpenCV (до версии `4.13`)**
  * **Раздел drawing:** CIRCLE, FILLPOLY, LINE, PUT_TEXT, RECTANGLE, DRAW_ARUCO_MARKERS
  * **Раздел filtering:** BLUR, BUILD_PYRAMID, DILATE, ERODE, GAUSSIAN_BLUR, LAPLACIAN, MEDIAN_BLUR, MORPHOLOGY_EX, SCHARR, SOBEL
  * **Раздел trackers:** ARUCO_DETECTOR, CORNER_HARRIS, GOOD_FEATURES_TO_TRACK
  * **Раздел tranforms:** ADAPTIVE_THRESHOLD, CVT_COLOR, RESIZE, THRESHOLD, WARP_AFFINE, WARP_PERSPECTIVE, WARP_POLAR
  * **Раздел videoprocessing:** CAMERA, IMREAD, IMWRITE, IMSHOW, VIDEOWRITER
* **Добавлен пример использования OpenCV**
* **Добавлен блок OPC UA клиента**
* **Добавлен блок MQTT клиента** 
* **Добавлена утилита-конвертер проектов** — перенос с **Версии 2.0** на **Версию 3.0**.

## Изменения и улучшения

* **Обновлен формат публикации OPC UA переменных** — структура передавамых данных соответсвует 4diac forte.
* **Исправление ошибок**

---
*Дата релиза: 03.07.2026*