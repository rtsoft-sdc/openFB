DINASORE_DIR=/home/orangepi/dinasore/
MODEL_FOLDER=/home/orangepi/demo


docker run --rm  --privileged -v $DINASORE_DIR:/dinasore \
    -v $MODEL_FOLDER:/demo \
    -v /proc/device-tree/compatible:/proc/device-tree/compatible \
    -v /dev/bus/usb:/dev/bus/usb \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -p 62499:62499 -p 4840:4840 \
    -e DISPLAY=:0.0 -e QT_X11_NO_MITSHM=1 \
    -it dinasore:v0 
