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
make import-lims-db SAMPLESHEETS=/path/to/samplesheets-dir/
```
- see description in `import-samplesheets.py` file for details on directory and file formats

# Software

- Linux or macOS
