# Virtual Environment
Here's how to run your virtual environment:

```
$ python3 -m venv myvenv
$ source myvenv/bin/activate
```

# Test Coverage
Procedure for raising the coverage is as follows.

```
$ pip install coverage
$ coverage run --source='.' manage.py test blog
$ coverage html
```
