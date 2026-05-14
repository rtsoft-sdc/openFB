#!/usr/bin/env bash
set -e
_CLEANUP_DONE=0
cleanup() {
  [ "$_CLEANUP_DONE" -eq 1 ] && return
  _CLEANUP_DONE=1
  echo '=== 6. Смена владельца артефактов на пользователя хоста ==='
  if [ -n "${HOST_UID:-}" ] && [ "${HOST_UID}" != "$(id -u)" ]; then
    chown -R "${HOST_UID}:${HOST_GID}" .
  fi
}

trap cleanup EXIT INT TERM
PACKAGE_VERSION="${PACKAGE_VERSION:?PACKAGE_VERSION is not set}"

echo '=== 0. Обновление deb-packaging/openfb/DEBIAN/control and openfb/__init__.py ==='
sed "s/Version: .*/${PACKAGE_VERSION}/g" deb-packaging/openfb/DEBIAN/control
sed "s/__version__ = .*/__version__ = '${PACKAGE_VERSION}'/" openfb/__init__.py

echo '=== 1. Сборка Python wheel ==='
make install
make whl

echo '=== 2. Определение имени wheel-файла ==='
WHEEL_NAME=$(ls dist/openfb-*.whl 2>/dev/null | head -1 | xargs basename)
echo "Wheel: $WHEEL_NAME"

echo '=== 3. Копирование wheel в директорию пакета ==='
cp "dist/$WHEEL_NAME" deb-packaging/openfb/opt/openfb/

echo '=== 4. Сборка .deb пакета (dpkg-deb) ==='
make deb

echo '=== 5. Копирование артефактов в корень сборки ==='
mv openfb.deb "openfb_${PACKAGE_VERSION}.deb"
cp "dist/$WHEEL_NAME" .
