# tuco

Laboratory Information Management System (LIMS) for track lab sequencing experiments and samples.

# Setup

Clone this repository

```
git clone --recurse-submodules https://github.com/NYU-Molecular-Pathology/tuco.git
cd tuco
```

Install `conda` and Django

```
make conda-install
```

Initialize app databases and create an admin user

```
make init
```

Import data from a directory containing sequencing samplesheets:

```
make import-lims-db SAMPLESHEETS_DIR=/path/to/samplesheets-dir/ RUNS_DIR=/path/to/samplesheets-dir/
```
- see description in `import-samplesheets.py` file for details on directory and file formats

## Example

You can demo the app with the included example data:

```
make conda-install

LIMS_DB="$(echo "$(python -c 'import os; print(os.path.realpath("."))')/lims.sqlite")"
DJANGO_DB="$(echo "$(python -c 'import os; print(os.path.realpath("."))')/db.sqlite")"
make init SECRET_KEY=foo LIMS_DB="${LIMS_DB}" DJANGO_DB="${DJANGO_DB}"

make import-lims-db SECRET_KEY=foo LIMS_DB="${LIMS_DB}" DJANGO_DB="${DJANGO_DB}"  SAMPLESHEETS_DIR=example-samplesheets/ RUNS_DIR=example-samplesheets/

make runserver SECRET_KEY=foo LIMS_DB="${LIMS_DB}" DJANGO_DB="${DJANGO_DB}"

# navigate to http://127.0.0.1:8000/admin in web browser
```

# Software

- Linux or macOS

- Python 3.6+, Django 2.1.2 (included with `conda`)
