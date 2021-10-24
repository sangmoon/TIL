``django2.0`` 부터 ``path``, ``re_path`` 함수로 라우팅을 한다.

(django_docs_link)[https://docs.djangoproject.com/en/2.0/topics/http/urls/#how-django-processes-a-request]

```python
from django.conf.urls import path, re_path
from . import views

urlpatterns = [
    path('index/<int:index_id>', views.index, name='index'),
    re_path(r'^index/(?P<index_id>\d+)/$'),
]
```

위의 path()와 re_path는 같은 url을 나타낸 것이다.
path에서는 정규식을 명시적으로 사용하지 않고 ``<>`` 로 단순한 패턴들을
매칭한다. ``int``, ``str``,``slug``, ``uuid``, ``path`` 가 default path converter 이다. custom conveter 도 등록 가능하다.
re_path의 경우 기존 urls.url 함수의 이름이 바뀐 것이다. 정규식으로 패턴을 표현한다. 
