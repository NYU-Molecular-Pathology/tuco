[![Build Status](https://travis-ci.org/NYU-Molecular-Pathology/tuco.svg?branch=master)](https://travis-ci.org/NYU-Molecular-Pathology/tuco)
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

# Software

- Linux or macOS

- Python 3.6+
