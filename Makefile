SHELL:=/bin/bash
UNAME:=$(shell uname)
TIMESTAMP=$(shell date '+%Y-%m-%d-%H-%M-%S')
# ~~~~~ Setup Conda ~~~~~ #
PATH:=$(CURDIR)/conda/bin:$(PATH)
unexport PYTHONPATH
unexport PYTHONHOME

# install versions of conda for Mac or Linux, Python 2 or 3
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
	conda install -y \
	django=2.2.5

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
# export SECRET_KEY:=$(shell cat ../secret-key.txt)
export DB_DIR:=$(CURDIR)/db
export DB_BACKUP_BASEDIR:=$(CURDIR)/backup
export DB_BACKUP_DIR:=$(DB_BACKUP_BASEDIR)/$(TIMESTAMP)
export SECRET_KEY:=foo
export LIMS_DB:=$(DB_DIR)/lims.sqlite3
export DJANGO_DB:=$(DB_DIR)/db.sqlite3
export MEDIA_ROOT:=uploads
export DJANGO_ENABLE_DEBUG:=1

# dirs containing sequencing samplesheets and runs
export SAMPLESHEETS_EXTERNAL_DIR:=$(CURDIR)/examples/samplesheets
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

backup: $(DB_BACKUP_DIR)
	gzip "$(LIMS_DB)" -c > "$(DB_BACKUP_DIR)/$$(basename $(LIMS_DB)).gz"
	gzip "$(DJANGO_DB)" -c > "$(DB_BACKUP_DIR)/$$(basename $(DJANGO_DB)).gz"
$(DB_BACKUP_DIR):
	mkdir -p "$(DB_BACKUP_DIR)"

# ~~~~~ IMPORT/EXPORT DATA ~~~~~ #
# add, remove, delete entries from the database

# batch import into the database
import:
	python importer/importer.py example-data/runs exps
	python importer/importer.py example-data/samplesheets NGS580samplesheets

# dump the database for viewing
dump:
	sqlite3 -column -header lims.sqlite3 "select * from lims_experiment"
	sqlite3 -column -header lims.sqlite3 "select * from lims_ngs580experiment"
	sqlite3 -column -header lims.sqlite3 "select * from lims_ngs580samplesheet"
	sqlite3 -column -header lims.sqlite3 "select * from lims_ngs580sample"
# sqlite3 lims.sqlite3 .dump

# quick search for terms among the project files for refactoring, etc
VAR:=
search:
	find . -type f  ! -name "*.pyc" ! -name '*.sqlite3*' ! -path '*.git/*' ! -path '*/conda/*' ! -path '*/migrations/*' -exec grep -wl "$(VAR)" {} \;


# ~~~~~ DEBUGGING ~~~~~ #
# destroy lims database
nuke:
	rm -rf lims/migrations/__pycache__
	rm -f lims/migrations/0*.py
	rm -f "$(LIMS_DB)"

# run unit tests
test:
	python manage.py test lims

# run a command in the environment set up with conda
run:
	$(CMD)

# for debugging; start interactive shells with environment setup
python:
	python

bash:
	bash

# ~~~~~ DONT USE THESE:

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
