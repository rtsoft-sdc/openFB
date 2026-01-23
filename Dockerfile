FROM debian:bullseye-slim

EXPOSE 61499
EXPOSE 4840

ENV APP_NAME=openfb
ENV APP_DIR=/opt/$APP_NAME
ENV VENV_DIR=$APP_DIR/venv


RUN apt update
# Install openfb
COPY openfb.deb .
RUN apt install -y ./openfb.deb



# Enable installed venv
ENV VIRTUAL_ENV=$VENV_DIR
ENV PATH=$VENV_DIR/bin:$PATH

ENTRYPOINT ["openfb"]