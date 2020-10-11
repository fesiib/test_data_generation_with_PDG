update-deps:
	pip-compile --upgrade
	pip-compile --upgrade --output-file dev-requirements.txt dev-requirements.in
	pip install --upgrade -r requirements.txt  -r dev-requirements.txt

install:
	pip install --editable .

init:
	pip install pip-tools
	rm -rf .tox

update: init update-deps install

.PHONY: update-deps init update install