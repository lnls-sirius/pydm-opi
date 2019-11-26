.PHONY: clean install
NAME=sirius-hla-con
DESKTOP=/home/$(shell whoami)/Desktop

clean :
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~'    -exec rm --force {} +
	find . -name '__pycache__'  -exec rm -rd --force {} +

install-files:
	cp siriushlacon/utils/images/sirius-hla-as-cons-lnls.png /usr/share/icons
	cp miscellaneous/$(NAME).desktop /home/sirius/Desktop/$(NAME).desktop

install: install-files clean-git
	sudo ./setup.py install --single-version-externally-managed --compile --force --record /dev/null

develop: clean
	sudo ./setup.py develop

clean-git:
	git clean -fdX
