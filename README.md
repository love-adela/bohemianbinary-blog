# Bohemian Binary Blog

## 가상환경

다음과 같이 가상 환경을 설정합니다.

```sh
$ python3 -m venv myvenv
$ source myvenv/bin/activate
```

## 테스트

`--settings=mysite.settings.unittest` 세팅에서 테스트를 진행합니다.

```sh
python manage.py test --settings=c
```

## 테스트 커버리지

테스트 커버리지를 얻기 위해서는 아래의 절차를 진행합니다.

```sh
$ pip install coverage
$ coverage run --source='.' manage.py test --settings=mysite.settings.unittest
$ coverage html
```
