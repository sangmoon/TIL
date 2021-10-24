# WebFlux

앞 부분은 이전 스터디와 겹치기 때문에 생략

## 레시피 5-9 리액티브 핸들러 함수 작성하기

* ``@RequestMapping `` 대신  핸들러 함수로 작성할 수 있음

```java
@FunctionalInterface
public interface HandlerFunction<T extends ServerResponse> {
    Mono<T> handle(ServerRequest request);
}
```

* ServerRequest, ServerResponse 를 통해 요청/응답의 다양한 파트들에 비동기적으로 접근 가능

### 핸들러 함수 작성

```java

@Component  //1 다른 어노테이션 없이 Component 만 선언해주면 됨
public class ReservationRestController {

    private final ReservationService reservationService;

    public ReservationRestController(ReservationService reservationService) {
        this.reservationService = reservationService;
    }

    public Mono<ServerResponse> listAll(ServerRequest request) {
        return ServerResponse.ok().body(reservationService.findAll(), Reservation.class); 
        //이 녀석이 HandlerFunction
    }

    public Mono<ServerResponse> find(ServerRequest request) {
        return ServerResponse
                .ok()
                .body(
                    request.bodyToMono(ReservationQuery.class)
                    .flatMapMany(q -> reservationService.query(q.getCourtName())), Reservation.class); 
                    // 이 녀석이 HandlerFunction
    }
}
```

#### ServerRequest 에서 value 빼오기

```java
// 이와 같은 method로 request parts에 접근 가능
Mono<String> string = request.bodyToMono(String.class);
Mono<String> string = request.body(BodyExtractors.toMono(String.class));

Flux<Person> people = request.bodyToFlux(Person.class);
Flux<Person> people = request.body(BodyExtractors.toFlux(Person.class));

Mono<MultiValueMap<String, String> map = request.body(BodyExtractors.toFormData());

Mono<MultiValueMap<String, Part> map = request.body(BodyExtractors.toMultipartData());

Flux<Part> parts = request.body(BodyExtractors.toParts());
```

### ServerResponse 채우기

```java
ServerResponse.ok().contentType(MediaType.APPLICATION_JSON).body(person, Person.class); // 200 code로 json response 보냄

ServerResponse.created(location).build(); // 201 code로 body 없이 location header만 보냄
```

### 요청을 핸들러 함수로 보내기

* 라우팅을 담당

```java
@Bean
public RouterFunction<ServerResponse> reservationsRouter(ReservationRestController handler) {
    return RouterFunctions
            .route(GET("/persons/{id}"), handler::getPersion)           //1
            .andRoute(GET("/*/reservations"), handler::listAll)         //2
            .andRoute(POST("/*/reservations"), handler::find)
            .andRoute(GET(""), request -> ServerResponse.ok().body(fromObject("Hello World"))); //3
}
```
1. path variable 사용 가능
2. wildcard 가능
3. 그냥 lambda function 으로도 가능


## 리엑티브 프로그래밍

> 비동기 프로세스로 동작하는 이벤트 기반의 non-blocking 어플리케이션을 구현하는 프로그래밍
>> "Reactive" 라는 용어는 변화에 반응하여 구축되는 프로그래밍 모델을 말합니다. 네트워크 구성 요소가 I / O 이벤트에 반응하고 UI 컨트롤러가 마우스 이벤트 등에 반응합니다. 이러한 의미에서 non-blocking은 reactive 입니다. 왜냐하면 차단되는 대신 알림에 반응하는 방식이기 때문입니다. **<스프링 docs>**

## 스프링 웹플럭스

* Servlet 3.1부터 non-blocking I/O 지원.
* 하지만 여러 API(``Filter``, ``Servlet``은 Synchronous, ``getParameter``, ``getPart`` 는 blocking) non-blocking 하지 않음.
* 기존 Spring MVC에서 non-blocking 한계가 있기에, 새롭게 web-flux 프로젝트 만듬
* vert.x 와 유사...

## Reactive Stream

* Stream은 data의 흐름(Publisher가 data를 만들고, Subscriber가 data 처리하는 구조)
* Reactive Stream은 Subscriber가 stream의 속도를 제어할 수 있음(back pressure)

## 프로그래밍 모델

* ``Annotated Controllers``: 기존 MVC 개발 방식처럼 @Controller, @GetMapping 쓰는 방식
* ``Functional EndPoints``:  람다 기반으로 콜백을 통해 리퀘스트 처리

## Thread Model

* 스프링 MVC와 Webflux 모두 어노테이션 controller를 지원하지만, 동시성 모델에서 큰 차이를 보임
* Spring MVC: 어플리케이션은 현재 쓰레드를 블럭할 수 있다고 가정. 따라서 서블렛 컨테이너는 이를 수용하기 위한 큰 쓰레드 풀이 필요
* Spring WebFlux: 어플리케이션은 쓰레드 블럭을 하지 않는다고 가정. 따라서 적은 쓰레드만을 이용. ``vanilla WebFlux Server`` 라면 1개의 기본 쓰레드와 CPU core 수만큼의 request processing 쓰레드 있음
* 물론 WebFlux에서도 ``publishOn`` 메소드를 통해 다른 쓰레드에서 작업할 수 있게 API 있음(그런데 쓰지 말라고 공식 가이드에서 ... DB작업은 어쩌지..?)

## Mono Flux

* Mono : 0 또는 1개의 data를 담음
* Flux : 0 에서 n개의 data를 담음

* Mono && Flux는 Future와 비슷하지만, lazy 하다는 점에서 다르다

### CompletableFuture

```java
public CompletableFuture myNonBlockingHttpCall(Object someData) {
    var uncompletedFuture = new CompletableFuture(); // 

    myAsyncHttpClient.execute(someData, (result, exception -> {
        if(exception != null) {
            uncompletedFuture.completeExceptionally(exception);
            return;
        }
        uncompletedFuture.complete(result);
    }));

    return uncompletedFuture;
}

public CompletableFuture myUpperLevelBusinessLogic() {
    var future = myNonBlockingHttpCall(); // 호출하는 시점에서 실행됨

    // ... 

    if (something) {
       // 그냥 에러를 던지자
       var errorFuture = new CompletableFuture();
       errorFuture.completeExceptionally(new RuntimeException());

       return errorFuture;
    }

   return future;
}
```
``myUpperLevelBusinessLogic`` 를 호출하면 ``myAsyncHttpClient.execute`` 는 바로 실행됨.
어떠한 전/후 컨디션에 따라 실행될 필요가 없다고 해도 제어할 수 없음

### Mono

```java
public Mono myNonBlockingHttpCallWithMono(Object someData) {
    return Mono.create(sink -> {
            myAsyncHttpClient.execute(someData, (result, exception -> {
                if(exception != null) {
                    sink.error(exception);
                    return;
                }
                sink.success(result);
            }))
    });
} 

public Mono myUpperLevelBusinessLogic() {
    var mono = myNonBlockingHttpCallWithMono(); // 호출 시점에서는 그냥 mono.. 내부 핸들러는 실행되지 않음

    // ... some code

    if (something) {
       // 에러를 던지자

       return Mono.error(new RuntimeException());
    }

   return mono;
}
```

모노의 경우는 ``myUpperLevelBusinessLogic`` 을 실행시켰을 때 http 요청을 날리지 않음. 최종 return Mono를 subscribe() 할 때 비로소 실행됨..

* 이러한 특징으로 back pressure 이용 가능. subscriber 가 publisher 속도 제어 가능


## view 를 추가하고 싶다면?

```java
Rendering index() {
    return Rendering.view("index")
                    .modelAttribute("message", Message.of("hello world!"))
                    .build();
}
```

### validation 하고 싶다면?

```java
public class PersonHandler {

	private final Validator validator = new PersonValidator(); // (1) validator 추가

	public Mono<ServerResponse> createPerson(ServerRequest request) {
		Mono<Person> person = request.bodyToMono(Person.class).doOnNext(this::validate); // (2) chaining 으로 vaildation 가능
		return ok().build(repository.savePerson(person));
	}

	private void validate(Person person) {
		Errors errors = new BeanPropertyBindingResult(person, "person");
		validator.validate(person, errors);
		if (errors.hasErrors) {
			throw new ServerWebInputException(errors.toString()); // (3) 404 Not Found 발생
		}
	}
```