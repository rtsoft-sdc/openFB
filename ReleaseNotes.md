# Release Notes — Версия [2.1]

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

## Исправления ошибок

---
*Дата релиза: 03.07.2026*