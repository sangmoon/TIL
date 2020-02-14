## Item 1: Know Which Version of Python You're Using

``python`` 은 보통 python2.7 의 alias 이다. 가끔은 더 낮은 버전을 쓰는 곳도 있다.
이를 확실히 하기 위해선 --version flag를 사용한다.
```shell
$ python --version
Python 2.7.10
```

``python3`` 는 보통 Python3를 사용하기위해 쓰인다.
```shell
$ python3 --version
Python 3.8.0
```

runtime 에서도 sys module을 통해 호출 가능하다.

```python
import sys
print(sys.version_info)
print(sys.version)

# sys.version_info(major=3, minor=6, micro=9, releaselevel='final', serial=0)
# 3.6.9 (default, Jan 15 2020, 10:45:58) [GCC 5.4.0 20160609]
```

### 기억해야 할 것
- Python3가 최신이고 지원되는 버전이며 앞으로 프로젝트는 이걸로 해야 한다.
- 당신 시스템 버전이 기대하는 버전과 맞는지 항상 확인해라
- Python2는 2020 1월 부로 지원 중단된다.

