# Makefile for the 'i3menu' package.
#
# Author: Giacomo Spettoli <giscomo.spettoli@gmail.com>
# Last Change: Feb 27, 2016

.DEFAULT_GOAL = help

.PHONY: help install uninstall python sdist sdist_upload codecheck clean publish tests

PYTHON:=$(shell which python 2>/dev/null)
PIP:=$(shell which pip 2>/dev/null)
FLAKE8=$(shell which flake8 2>/dev/null)
WHEEL=$(shell $(PYTHON) -c "import wheel")
VIRTUALENV_DIR := $(CURDIR)/venv
ifndef PYTHON
    $(error "python is not available. For debian like systems you can run: sudo apt-get install python")
endif
ifndef PIP
    $(error "pip is not available. For debian like systems you can run: sudo apt-get install python-pip")
endif

CHECK_MENU_PROVIDERS = $(if $(shell which 'rofi'),'rofi found',\
	$(if $(shell which 'dmenu'),'dmenu found',\
	$(error "No menu provider found. At least one between 'rofi' and 'dmenu' is required")))

help:
	@echo "Makefile for the 'i3menu' package"
	@echo
	@echo 'Commands:'
	@echo
	@echo '    make install         install the package using pip'
	@echo '    make uninstall       uninstall the package using pip'
	@echo '    make clean           cleanup all temporary files'
	@echo '    make codecheck       check the coding style'
	@echo '    make push            push changes to GitHub'
	@echo '    make sdist           build the tarball of package to be published'
	@echo '    make sdist_upload    upload the tarball of package to pypi'
	@echo
	@echo 'Variables:'
	@echo
	@echo "    PYTHON = $(PYTHON)"
	@echo "    PIP = $(PIP)"

venv: ${VIRTUALENV_DIR}/bin/activate
${VIRTUALENV_DIR}/bin/activate:
	test -d ${VIRTUALENV_DIR} || virtualenv ${VIRTUALENV_DIR}
	${VIRTUALENV_DIR}/bin/pip install pdbpp
	touch ${VIRTUALENV_DIR}/bin/activate

tests: venv
	${VIRTUALENV_DIR}/bin/pip install tox
	${VIRTUALENV_DIR}/bin/tox -v

develop: venv
	${VIRTUALENV_DIR}/bin/pip install -e .

python:
	$(PYTHON) setup.py build

install:
	$(PIP) install .

uninstall:
	$(PIP) uninstall i3menu

sdist: clean
	$(PYTHON) setup.py sdist

sdist_upload: clean
	$(PYTHON) setup.py sdist upload 2>&1 |tee upload.log

bdist_wheel: clean
	test -x "$(WHEEL)" || $(PIP) install wheel
	$(PYTHON) setup.py bdist_wheel --universal

bdist_wheel_upload: clean
	test -x "$(WHEEL)" || $(PIP) install wheel
	$(PYTHON) setup.py bdist_wheel --universal upload 2>&1 | tee upload.log

codecheck:
	test -x "$(FLAKE8)" || $(PIP) install flake8
	flake8

clean:
	@echo "Cleaning up distutils stuff"
	rm -rf build
	rm -rf dist
#	rm -rf ${VIRTUALENV_DIR}
	rm -rf lib/i3menu.egg-info/
	rm -rf .tox
	rm -rf .coverage
	rm -rf .cache
	rm -rf .eggs
	@echo "Cleaning up byte compiled python stuff"
	find . -type f -regex ".*\.py[co]$$" -delete
	find . -type f -name '*.pyc' -delete
	find . -name "__pycache__" -delete

push: clean
	git push origin && git push --tags origin

extract_messages: venv
	$(VIRTUALENV_DIR)/bin/pip install babel
	$(VIRTUALENV_DIR)/bin/python setup.py extract_messages -o lib/i3menu/locale/i3menu.pot --input-dirs=lib/i3menu
