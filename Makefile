install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	black library/*.py *.py

lint:
	pylint --disable=R,C library/*.py *.py

all: install lint