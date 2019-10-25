.PHONY: clean install
NAME=sirius-hla-con
DESKTOP=/home/$(shell whoami)/Desktop

clean :
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~'    -exec rm --force {} +
	find . -name '__pycache__'  -exec rm -rd --force {} +
install:
	cp siriushlacon/utils/images/LNLS.png ~/.local/share/icons
	cp miscellaneous/$(NAME).desktop $(DESKTOP)/$(NAME).desktop
