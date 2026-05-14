help:
	@echo "Usage: "
	@echo "    make install  Install uv and sync virtual environment "
	@echo "    make deb  Create .deb packet with openFB wheel"
	@echo "    make whl  Create package of openfb as python wheel"
	@echo "    make clean Clean directories"

install:
	python3 -m pip install uv 
	uv sync

deb:
	cp dist/openfb-*-py3-none-any.whl deb-packaging/openfb/opt/openfb/
	cd deb-packaging && dpkg-deb -Zxz --build openfb && cp openfb.deb ..

whl:
	@echo "Create python wheel"
	uv build 

clean:
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


