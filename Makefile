.PHONY: clean install
NAME=sirius-hla-con
PACKAGE_NAME=siriushlacon
DESKTOP=/home/$(shell whoami)/Desktop

clean-git:
	git clean -fdX

clean: clean-git
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~'    -exec rm --force {} +
	find . -name '__pycache__'  -exec rm -rd --force {} +
	rm -rf siriushlacon.egg-info/
	rm -rf dist/

install-files:
ifneq (,$(wildcard /usr/share/icons/sirius-hla-as-cons-lnls.png))
	sudo rm /usr/share/icons/sirius-hla-as-cons-lnls.png
endif
ifneq (,$(wildcard /home/sirius/Desktop/$(NAME).desktop))
	sudo rm /home/sirius/Desktop/$(NAME).desktop
endif
	sudo cp src/siriushlacon/utils/images/sirius-hla-as-cons-lnls.png /usr/share/icons/sirius-hla-as-cons-lnls.png
	sudo cp miscellaneous/$(NAME).desktop /home/sirius/Desktop/$(NAME).desktop

uninstall:
	make -C ./cons-common uninstall
	sudo /usr/bin/env python3 -m pip uninstall $(PACKAGE_NAME) -y
ifneq (,$(wildcard /usr/share/icons/sirius-hla-as-cons-lnls.png))
	sudo rm /usr/share/icons/sirius-hla-as-cons-lnls.png
endif
ifneq (,$(wildcard /home/sirius/Desktop/$(NAME).desktop))
	sudo rm /home/sirius/Desktop/$(NAME).desktop
endif

install: clean clean-git install-files
	make -C ./cons-common install
	sudo /usr/bin/env python3 -m pip install -r requirements_sirius.txt .

deploy: clean
	sed -i -e "s/__version__ =.*/__version__ = \"$(shell git describe --tags)\"/" siriushlacon/__init__.py
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload dist/*

