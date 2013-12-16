# codify

[![Build Status](https://travis-ci.org/erbridge/codify.png?branch=master)](https://travis-ci.org/erbridge/codify)

Generate a barcode-like vector graphic from a string.


## Setup

[Install](http://cairographics.org/download/) `cairo`.

Setup the `virtualenv`:
```sh
virtualenv --python=/usr/bin/python3 venv
source venv/bin/activate
```

Install `pycairo`:
```sh
cd pycairo
python setup.py install
cd ..
```

Install the requirements:
```sh
pip install --no-deps -r requirements.txt
```
