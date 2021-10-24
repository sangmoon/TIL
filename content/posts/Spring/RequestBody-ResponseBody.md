``@RequestBody`` anotation 은 controller로 들어온 요청에서
request body의 내용물을 converting 할때 사용한다.
우선 request의 ``Content-type``을 처리할 수 있는 HttpMessageConverter 구현체를 찾는다.
그리고 converting 처리를 통해 request body를 java object로 바꿔서 사용한다.

```json
POST / HTTP/1.1
Host: localhost:8000
Connection: keep-alive
Content-Type: application/json

{
	"name": "sangmoon",
	"age": "26"
}
```

```java
Class Person{
	String name;
	Integer age;
}
```

```java
@RequestMapping(value="/", method=RequestMethod.POST)
public String test(@requestBody Person person){
	....
}
```

``@ResponseBody``는 jsp를 return 해주지 않고 바로 http response를 return 해주기 위한 annotation 이다.
보통 ``@Controller`` + ``@ResponseBody``를 해서 Rest용 Controller를 만드는데 ``@RestController`` annotation은 
이둘을 합쳐놓은 것이다. request header에 있는 ``Accept`` keyword를 통해 보통 convert된다.

``@ResponseBody`` 를 사용하면 예외 처리 상황에서 어려움을 겪을 수 있다. 이 때 ``ResponseEntity``를 사용하면
404나 500같은 상태 코드를 사용자에게 전송할수 있다.