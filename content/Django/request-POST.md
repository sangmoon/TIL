view에서 user의 request를 보통 ``GET`` 과 ``POST``로 받는다.
browser에서 ajax POST request를 보낼 때 ``request.POST``로 받으면 
될 거라고 생각했는데, ``request.body``로 바로 접근해야 한다. django에서 ``request.POST``는
form data 같은 걸 받을 때 사용하는 것이다.
