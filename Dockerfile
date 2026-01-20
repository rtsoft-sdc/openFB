FROM debian:bullseye-slim

RUN apt update
RUN apt install -y python3 python3-pip

# Install uv for python and package managment
RUN pip3 install uv
RUN uv python install 3.9 

RUN mkdir ~/.OpenFB && cd ~/.OpenFB && uv venv

# Enable installed venv
ENV VIRTUAL_ENV=/root/.OpenFB/.venv
ENV PATH=/root/.OpenFB/.venv/bin:$PATH

RUN uv pip install pip

# Install openfb
COPY openfb-1.0.0-py3-none-any.whl .
RUN python3 -m pip install --no-cache openfb-1.0.0-py3-none-any.whl 
RUN rm openfb-1.0.0-py3-none-any.whl 

