call python -m pip install offline_package/pip-18.1-py2.py3-none-any.whl
call pip install offline_package/virtualenv-16.1.0-py2.py3-none-any.whl
call virtualenv --no-site-packages venv
call venv\Scripts\activate.bat
call pip install  --no-index --find-links=offline_package -r requirements.txt
pause