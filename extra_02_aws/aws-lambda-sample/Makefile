#!make
SHELL = /usr/bin/env bash

.PHONY: help clean clean-pyc clean-build dist
.DEFAULT_GOAL := help

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
mkfile_dir := $(dir $(mkfile_path))
current_dir := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))

cwd:  ## show Makefile directory path 
	echo $(mkfile_dir)

help:  ## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/:.*##/:\t/'

setuptools: ## Upgrade setup tools
	pip install --upgrade wheel setuptools pip
	sleep 1

clean: clean-build clean-pyc ## remove all artifacts

clean-build:  ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:  ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

dist: clean setuptools  ## Make distribution of Lambda layer and code
	$(mkfile_dir)/build.sh $(mkfile_dir)
