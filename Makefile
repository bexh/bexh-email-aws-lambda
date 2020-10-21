#!make

export PYTHON_VERSION := 3.8

#SHELL := /bin/bash

install-dev:
	@+pipenv install --python ${PYTHON_VERSION} --dev

install:
	@+pipenv install --python ${PYTHON_VERSION}

clean:
	rm -rf venv
	rm -rf ./dist/bexh-email-aws-lambda.zip

build:
	{ \
  	set -e ;\
	python3 -m venv venv ;\
	. venv/bin/activate ;\
	python -m pip install --upgrade pip ;\
	pip install -r requirements.txt ;\
	mkdir -p dist ;\
	cd venv/lib/python3.8/site-packages ;\
	zip -r9 $${OLDPWD}/dist/bexh-email-aws-lambda.zip . ;\
	cd $${OLDPWD} ;\
	zip -g -r ./dist/bexh-email-aws-lambda.zip ./main/ ;\
	}

test:
	pipenv run pytest -q main/test/sample_tests.py

help:
	{ \
	echo 'Commands:' ;\
    echo '    clean          Cleans venv and package from old builds' ;\
    echo '    build          Bundle package for deployment' ;\
    echo '    test           Runs all test cases' ;\
    echo '    install        Installs pipfile libraries' ;\
    echo '    install-dev    Installs pipfile libraries for development purposes' ;\
	}
