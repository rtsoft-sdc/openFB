#!/usr/bin/env bash

set -e

echo "Cleaning project directories..."

find . -name '__pycache__' -exec rm -rf {} +
find . -type f -name '*.pyc' -delete
find . -type f -name '*.pyo' -delete

rm -rf dist
rm -rf openfb.egg-info

rm -f openfb.deb
rm -f deb-packaging/openfb.deb
rm -f deb-packaging/openfb/opt/openfb/openfb-*-py3-none-any.whl
rm -f openfb/resources/data_model.fboot
rm -f openfb/resources/error_list.log

echo "Clean inside Linux completed successfully."