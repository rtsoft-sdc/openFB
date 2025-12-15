FROM ubuntu:22.04 AS source
RUN apt update && apt install -y git && git clone --depth 1 https://github.com/airockchip/rknn-toolkit2.git /rknn-toolkit2
RUN cd /rknn-toolkit2 && git checkout  tags/v2.3.0

RUN cp /rknn-toolkit2/rknpu2/runtime/Linux/librknn_api/include/* /usr/include/
RUN cp /rknn-toolkit2/rknpu2/runtime/Linux/librknn_api/aarch64/librknnrt.so /usr/lib/
RUN ldconfig


RUN apt update && apt upgrade -y && apt install software-properties-common -y 
RUN add-apt-repository ppa:deadsnakes/ppa
RUN  apt install python3.10 python3-pip libgl1 libxrender1 libxext6 libgl1-mesa-glx libqt5widgets5 libqt5gui5 libqt5core5a -y 

RUN python3 -m pip install /rknn-toolkit2/rknn-toolkit-lite2/packages/rknn_toolkit_lite2-2.3.0-cp310-cp310-manylinux_2_17_aarch64.manylinux2014_aarch64.whl 
RUN rm -rf /rknn-toolkit2
RUN apt clean
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
EXPOSE 62499
EXPOSE 4840