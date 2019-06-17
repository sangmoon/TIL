# WebFlux

## 리엑티브 프로그래밍

> 비동기 프로세스로 동작하는 이벤트 기반의 non-blocking 어플리케이션을 구현하는 프로그래밍
>> "Reactive" 라는 용어는 변화에 반응하여 구축되는 프로그래밍 모델을 말합니다. 네트워크 구성 요소가 I / O 이벤트에 반응하고 UI 컨트롤러가 마우스 이벤트 등에 반응합니다. 이러한 의미에서 non-blocking은 reactive 입니다. 왜냐하면 차단되는 대신 알림에 반응하는 방식이기 때문입니다. <스프링 docs>

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
* 물론 WebFlux에서도 ``publishOn`` 메소드를 통해 다른 쓰레드에서 작업할 수 있게 API 있음

## 레시피 5-5 스프링 웹플럭스로 reactive 앱 개발하기

```java
public interface HttpHandler {
    // Spring WebFlux 최하위 컴포넌트
    Mono<Void> handle(ServerHttpRequest request, ServerHttpResonse response);
}
```

### Mono Flux