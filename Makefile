SHELL:=/bin/bash
UNAME:=$(shell uname)

# ~~~~~ Setup Conda ~~~~~ #
PATH:=$(CURDIR)/conda/bin:$(PATH)
unexport PYTHONPATH
unexport PYTHONHOME

# install versions of conda for Mac or Linux, Python 2 or 3
# Python 3.6.5 |Anaconda, Inc.| (default, Apr 29 2018, 16:14:56)
# [GCC 7.2.0]
# 2.7.15 |Anaconda, Inc.| (default, May  1 2018, 18:37:05)
# [GCC 4.2.1 Compatible Clang 4.0.1 (tags/RELEASE_401/final)]
ifeq ($(UNAME), Darwin)
CONDASH:=Miniconda3-4.5.4-MacOSX-x86_64.sh
endif

ifeq ($(UNAME), Linux)
CONDASH:=Miniconda3-4.5.4-Linux-x86_64.sh
endif

CONDAURL:=https://repo.continuum.io/miniconda/$(CONDASH)
conda:
	@echo ">>> Setting up conda..."
	@wget "$(CONDAURL)" && \
	bash "$(CONDASH)" -b -p conda && \
	rm -f "$(CONDASH)"

conda-install: conda
	conda install -y django=2.1.2

# ~~~~~ SETUP DJANGO APP ~~~~~ #
# setting up & re-setting up the app
# setup:
# 	django-admin startproject tuco .
# 	python manage.py startapp lims
init:
	python manage.py makemigrations
	python manage.py migrate
	python manage.py migrate lims --database=lims_db
	python manage.py createsuperuser

# re-initialize just the databases
reinit:
	python manage.py makemigrations
	python manage.py migrate
	python manage.py migrate lims --database=lims_db

# ~~~~~ RUN ~~~~~ #
# shortcut commands for running and managing the app
export SECRET_KEY:=$(shell cat ../secret-key.txt)
export LIMS_DB:=lims.sqlite3
export DJANGO_DB:=db.sqlite3
export DJANGO_ENABLE_DEBUG:=1

# dirs containing sequencing samplesheets and runs
export SAMPLESHEETS:=example-data/samplesheets
# _SAMPLESHEETS:=$(shell python -c 'import os; print(os.path.realpath("$(SAMPLESHEETS)"));')
export RUNS:=example-data/runs
# _RUNS:=$(shell python -c 'import os; print(os.path.realpath("$(RUNS)"));')

CMD:=

# run Django 'manage'
manage:
	python manage.py $(CMD)

# create admin user
createsuperuser:
	python manage.py createsuperuser

# runs the web server
runserver:
	python manage.py runserver

# start interactive shell
shell:
	python manage.py shell

# prepare database migrations
makemigrations:
	python manage.py makemigrations $(CMD)

# migrate databses
migrate:
	python manage.py migrate $(CMD)

# run a command in the environment set up with conda
run:
	$(CMD)

# same as above but with Python
py:
	python $(CMD)


# ~~~~~ IMPORT/EXPORT DATA ~~~~~ #
# add, remove, delete entries from the database

# import all LIMS data from samplesheets into db's
import-lims-db:
	$(MAKE) py CMD='import-runs.py $(RUNS)'
	$(MAKE) py CMD='import-samplesheets.py $(SAMPLESHEETS)'
	$(MAKE) py CMD='import-samplesheet-samples.py $(SAMPLESHEETS)'
	$(MAKE) py CMD='import-samplesheet-pairs.py $(SAMPLESHEETS)'
	$(MAKE) py CMD='import-seqtypes.py $(SAMPLESHEETS)'




# remove all entries from data db's
clear-db-runs:
	echo 'from lims.models import SequencingRun; SequencingRun.objects.all().delete();' | python manage.py shell
clear-db-samples:
	echo 'from lims.models import SequencingSample; SequencingSample.objects.all().delete();' | python manage.py shell
clear-db-samplesheets:
	echo 'from lims.models import SequencingSampleSheet; SequencingSampleSheet.objects.all().delete();' | python manage.py shell

clear-db: clear-db-runs clear-db-samplesheets clear-db-samples

# delete all db contents then re-import
reset-lims-db: clear-db
	$(MAKE) import-lims-db

# print db contents
all-runs:
	echo 'from lims.models import SequencingRun; print(SequencingRun.objects.all());' | python manage.py shell

all-samples:
	echo 'from lims.models import DemuxSample; print(DemuxSample.objects.all());' | python manage.py shell

all-samplesheets:
	echo 'from lims.models import SequencingSampleSheet; print(SequencingSampleSheet.objects.all());' | python manage.py shell
