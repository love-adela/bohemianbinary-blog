## pytest 구동 방법
```PYTHONPATH=. pytest```

## Coverage 수행 방법 

실행하며 다른 모듈(pytest...)을 동시에 수행
```PYTHONPATH=. coverage run -m pytest```

### Coverage 도움말
```coverage help```

### Coverage 현황 보고
* 터미널에서 확인하기 : ```coverage report```
* html로 확인하기 : ```coverage html```
    * html 문서 열기 : ```open htmlcov/index.html```
    
    
TODO: test_ddd로 파일명을 지정해야 함 (역할별로 나눠서 바꿀 것.)
* 최소 routes.py coverage는 100% 였으면 좋겠다.



