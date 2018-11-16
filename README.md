This repo shows how we start working with mocking in python 3.6.6

#get started

```bash
echo 'install pyenv            ref. https://github.com/pyenv/pyenv#installation'
echo 'install pyenv virtualenv ref. https://github.com/pyenv/pyenv-virtualenv#installing-as-a-pyenv-plugin'

# install python 3.6.6
pyenv install 3.6.6

# create venv for this app
CODE='the folder where you clone this repo - TODO set your path here'
THIS_APP=python-mock-start
pyenv virtualenv 3.6.6 $THIS_APP
cd "$CODE"
pyenv local $THIS_APP
ln -s $(pyenv root)/versions/python-mock-start venv

# install pip packages
cd "$CODE"
pip install --upgrade pip
pip install -r requirements.txt && pip freeze > requirements.lock

# run test
pytest                                           # run all
pytest -x                                        # stop after 1st failed test
pytest -s tests/path/to/your_test.py             # run tests in a file
pytest -k tests/path/to/your_test.py:test_method # run a specific test method

```
