# Reactive Programming

- Reactive Programming이 어떤 것인지 rxJava(reactive java) 를 통해 설명
- webflux 는 이것과 용어는 다르겠지만.. 핵심 개념이나 프로그래밍 방식은 유사할 것이라 생각
- Reactive programmming with rxJava ch.4 까지 참조

```java
public class Main {
    public static void main(String[] args) {
        Observable.just("Hello world").subscribe(System.out::println);
    }
}
```

## 미리 알아야 할 것
> Generic, lambda, method reference

## what is Monad?
rx 들어가기 전에 모나드가 무엇인지 알아보자.
CompletableFuture니 Observable이니 Flux 니 다 모나드이기 때문에 알면 확실히 편하다!


모나드 정의 대한 가장 쉬운 설명

![flip](https://github.com/sangmoon/TIL/raw/master/springStudy/resource/monad.png)

...? 갑자기 수학이..?

- flatMap은 ``monad`` 가 구현해야 하는 bind method, m 은 모나드, x는 모나드의 내부 값..
- 결합법칙이 적용되어야 한다
- 2,3 번은 중립적이어야 한다는 말인데..설명할 수 없다. 아는게 설명할 수가 없어..

또 프로그래밍 언어에서는 다음 3개의 특징을 만족해야 한다
- 모나드는 다른 타입을 받는 타입이다 (Generic)
- 모나드 의 값을 생성하는 함수가 있어야 한다(생성자)
- 다른 모나드타입으로 진행하는 함수가 있어야 한다(flatMap)

... 일단 이렇다고 알아두고 구체적인 설명으로 들어가 봅시다.

### functor

functor는 다음 조건을 만족하는 녀석을 말한다.  
함수를 인자로 받아 결과를 반환하는 method(여기선 map) 만 있으면 됨

```java
import java.util.function.Function;

interface Functor<T> {
    <R> Functor<R> map(Function<T,R> f);
}
```

예를 들어보자면 ...

```java
class Identity<T> implements Functor<T, Identity<?>> {
    private final T value;

    Identity(T value) { this.value = value; }

    public <R> Identity<R> map(Function<T,R> f) {
        final R result = f.apply(value);
        return new Identity<>(result);
    }
}
```

```java
// 다음과 같이 쓸 수 있다.
Identity<String> idString = new Identity<>("abc");
Identity<Integer> idInt = idString.map(String::length);

// chaining 도 물론 가능!
Identity<byte[]> idBytes = new Identity<>(customer)
    .map(Customer::getAddress)
    .map(Address::street)
    .map((String s) -> s.substring(0,3))
    .map(String::toLowerCase)
    .map(String::getBytes);
```
그런데 이렇게만 보면 method chaining과 다를 바가 없음

```java
// 그냥 method chaining
byte[] bytes = customer
    .getAddress()
    .street()
    .substring(0,3)
    .toLowerCase()
    .getBytes();
```

펑터의 장점은 무엇일까??
1. 내부에서 함수의 동작을 제어할 수 있다.

java8 에 추가된 Optional을 직접 구현한 FOptional 클래스를 보자
Optional은 NPE 를 피하며 프로그래밍하기 위한 API!

```java
class FOptional<T> implements Functor<T,FOptional<?>> {
    private final T valueOrNull;

    private FOptional(T valueOrNull) {
        this.valueOrNull = valueOrNull;
    }
    public <R> FOptional<R> map(Function<T,R> f) {
        if (valueOrNull == null) // 비어있으면 f 를 사용하지 않음
            return empty();
        else
            return of(f.apply(valueOrNull));
    }
    public static <T> FOptional<T> of(T a) {
        return new FOptional<T>(a);
    }
    public static <T> FOptional<T> empty() {
        return new FOptional<T>(null);
    }
}
```

팩토리 메소드를 통해 값을 갖는 optional과 null인 optional 생성 가능.  
값이 null 이면 원래는 NPE지만 함수를 실행시키지 않고 빈 optional 반환. 신기하죠?

또 다른 예제는 List 를 펑터 형태로 바꾼 Flist

```java
public class FList<T> implements Functor<T, FList<?>> {
    private final List<T> list; // immutable 해야함

    FList(Iterable<T> iterable) {
        list = new ArrayList<>();
        iterable.forEach(list::add); // 대략 이런 느낌
    }

    @Override
    public <R> FList<R> map(Function<T, R> f) {
        ArrayList<R> result = new ArrayList<R>(list.size());
        for(T t: list) {
            result.add(f.apply(t));
        }
        return new FList<>(result);
    }
}
```

Flist의 장점은 무엇일까?? 내부 값이 1개든 10개든 같은 메소드 적용 가능하다는 것!

```java
import static java.util.Arrays.asList;

FList<Customer> customers = new FList<>(asList(cust1, cust2));
FList<String> streets = customers
        .map(Customer::getAddress)
        .map(Address::street);
```
단순 메소드 체이닝으로는 불가능한 영역. flist 대신에 java8의 Stream 사용해도 되지 않을까?  
사실 Stream 도 functor 이자 모나드 이다!!

### functor 에서 모나드로

```java
FOptional<Integer> tryParse(String s) {
    try {
        final int i = Integer.parseInt(s);
        return FOptional.of(i);
    } catch (NumberFormatException e) {
        return FOptional.empty();
    }
}
```
위와 같이 Optinal을 반환하는 메소드를 생각해보자. 스트링을 받아 Integer로 변환되면 해당 값을 Optional로 반환하고,
실패하면 빈 Optional을 반환한다. ( Exception을 throw 하지 않는 이유는 함수형 언어 스타일과 맞지 않기 때문..
순수 함수형 언어에는 예외가 없다, 오류나 부적절한 조건도 값으로 명시)

그러면 client code는 ?

```java
FOptional<String> str = FOptional.of("42");
FOptional<FOptional<Integer>> num = str.map(this::tryParse); // Optional 안에 Optional이 !?
```
functor 예제에서는 단순 Type을 메소드 반환값으로 해서 괜찮았으나 Optional을 반환형으로 하게 되면 문제가 생긴다.
보기에도 가독성이 떨어지고, 메소드 체이닝에도 문제가 생긴다.

```java
FOptional<Integer> num1 = // ...
FOptional<FOptional<Integer>> num2 = // ...

FOptional<Date> date1 = num1.map(t -> new Date(t));
// 컴파일 안됨
FOptional<Date> date2 = num2.map(t -> new Date(t));
```
펑터를 2번 감싸는 것으로 문제가 발생함.. 이를 해결하기 위해 모나드 탄생

```java
public interface Monad<T, M extends Monad<?,M>> extends Functor<T, M>{
    M flatMap(Function<T,M> f);
// <R> Functor<R> map(Function<T,R> f);
// Functor<R> 을 반환하지 않고 새로운 M을 반환함 
}
```

```java
// optional 에 구현한 코드
    public FOptional<?> flatMap(Function<T, FOptional<?>> f) {
        if(valueOrNull == null) {
            return FOptional.empty();
        } else {
            return f.apply(valueOrNull);
            // return of(f.apply(valueOrNull));
        }
    }
```

```java
FOptional<String> num = FOptional.of("42");
// 이젠 정상 동작
FOptional<Integer> answer = num.flatMap(this::tryParse);
```

여기까지가 모나드 정리..!
사실 오늘 강의 끝내도 됨...
이제 rxJava 로 들어가 봅시다.

## Reactive Programming with rxJava

rxJava 의 특징

### Observable and Observer (Push versus Pull)

``Observable``(Supplier) 과 ``Observer``(Consumer) 를 우선 구분해야 합니다.

```java
interface Observable<T> {
    Subscription subscribe(Observer s)
}
```

```java
interface Observer<T> {
    void onNext(T t)            // 이벤트 발생시
    void onError(Throwable t)   // 에러 발생시
    void onCompleted()          // 스트림 완료시
}
```

### Async versus Sync

Observable은 async 하지만 꼭 그럴 필요는 없습니다.  
synchronous 하게 할 수 있고 default 는 sync 입니다.  
synchronous ``Observable`` 은 subscribe 되면  모든 데이터를 subscriber 쓰레드로 보내고 완료됩니다.

```java
Obervable.create(s -> {
    s.onNext("Hello World");    // (1) 여기가 blocking long time IO 라면?? 그만큼 기다려야 함.
    s.onCompleted();
}).subscribe(hello -> System.out.println(hello));
```

이 예제는 완벽히 sync 함..(하나의 thread 가 전부 수행)
1. Obervable.create로 Observable 생성
2. subscribe() 통해 구독
3. Obervable 시작되면서 onNext("hello World) 실행
4. onCompleted() 실행

(1) 이 오래걸리는 blocking job 이라면 그 만큼 block 됨
(2) 여러 쓰래드에 작업을 할당하는 것은 뒤 챕터에서 ...



### Concurrency and Parallelism
- Concurrency: 하나의 CPU에서 여러 task를 ``time slicing`` 으로 진행
- Parallelism: 멀티코어에서 동시에 작업 진행

> ``하나의 Observable에 대해 이벤트(onNext(), onCompleted(), onError()) 는 concurrently 하게 발생할 수 없다``  고 rxJava 규약에 나와 있음

Observable은  여러 쓰레드가 이벤트를 발생시킬 수 있지만, 하나의 쓰레드가 이벤트 발생 중이면, 다른 쓰레드가 inter-leaving 해서는 안 된다.  

```java
// 이렇게 쓰지 말자
Observable.create(s -> {
    // Thread A
    new Thread(() -> {
        s.onNext("one");
        s.onNext("two");

    }).start();

    // Thread B
    new Thread(() -> {
        s.onNext("three");
        s.onNext("four");
    }).start();
})
```

그럼 멀티쓰레딩 이용 못하는 것 아닌가?? rxJava 에서는 Composition을 이용해 해결

> 하나의 Observable 스트림은 항상 serialize 해야 한다. 하지만 각각의 스트림은 독립적으로 동작할 수 있으니 그걸 합치자!

```java
// 규약에 맞는 버전
Observable<String> a = Observable.create(s -> {
    new Thread(() -> {
        s.onNext("one");
        s.onNext("two");

    }).start();
});
Observable<String> b = Observable.create(s -> {
    new Thread(() -> {
        s.onNext("three");
        s.onNext("four");
    }).start();
});

// c 는 a와 b를 subscribe 하면서 새로운 serialized stream을 만듬
// 내부적으로 atomic 연산 사용
Observable<String> c = Observable.merge(a, b);
```

### Duality

``Observable`` 은 ``Iterable`` 과 쌍둥이 같은 존재

| Pull(``Iterable``)| Push(``Observable``)|          
| -------------     | -------------     |
| T next()          | onNext(T)         | 
| throws Exception  | onError(Throwable)|   
| returns           | onCompleted()     |

- Iterable 은 Consumer가 next()를 호출해서 데이터를 가져옴
- Observable 은 producer가 onNext()를 실행해 데이터를 밀어 넣어줌

rxJava는 Pull 이 아닌 Push 를 기반으로 동작(pull 도 되긴 합니다..)

### Cardinality

Observable 은  여러 값을 push 하는 것을 지원(마치 async Iterable 처럼)

|    | One| Many|          
----- | -------------     | -------------  |
|Synchronous | T getData()         | Iterable<T> getData() | 
|Asynchronous| ``Future``\<T\> getData()  | ``Observable``\<T\> getData()| 

## Reactive Extension

reactive extension 의 용어들과 core concept 설명

### Subscribing to Notifications from Observable

Subscribe 할 때는 3개의 콜백을 등록할 수 있음(onNext, onError, onCompleted)  
``onNext``* ( ``onCompleted`` | ``onError`` )? 로 요약 가능  
onNext 0개 이상 발행 후 onCompleted 나 onError 가 불릴 수 있음

```java
Observable<Tweet> tweets = //..

// Type A: lambda
tweets.subscribe(
    (Tweet tweet) -> {System.out.println(tweet);},
    (Throwable t) -> {t.printStackTrace();},
    () -> {this.noMore();}
);

// Type B: method reference
tweets.subscribe(
    System.out::println,
    Throwable::printStackTrace,
    this::noMore);
```

아예 observer 객체를 따로 만들 수 있음
```java
Observer<Tweet> observer = new Observer<Tweet> {
    // 가장 고전적인 방법
    @Override
    public void onNext(Tweet tweet) {
        System.out.println(tweet);
    }

    @Override
    public void onError(Throwable e) {
        e.printStackTrace();
    }

    @Override
    public void onCompleted() {
        noMore();
    }
}
```

### Controlling Listeners by Using Subscription and Subscriber<T>

observable - observer 관계를 Subscription 객체를 통해 알 수 있다.
```java
Subscription subscription = tweets.subscribe(System.out::println);
subscription.unsubscribe(); // 구독 취소할 수 있음
```
### Creating Observable

앞에선 Observable::create 를 통해 observable 객체를 만듬  
미리 만들어 놓은 helper method 들이 있음  
```java
Observable.just(value)
/*
    value 하나만 emit 하고 completed 되는 Observable
*/

Observable.from(value)
/*
    Just랑 비슷하지만, Iterable<T> 나 T[] 를 인풋으로 받아 순차적으로 emit 하고 complete 돠는 Observable
*/

Observable.range(from, n)
/*
    from 부터 시작해 n개의 integer를 emit 하고 complete 되는 observable
*/

Observable.empty()
/*
    바로 완료되는 observable
*/

Observable.never()
/*
    아무런 이벤트도 emit 하지 않는 observable
*/
Observable.error()
/*
    error를 바로 emit 하는 observable
*/
```

just 의 내부 구현을 생각해본다면..

```java
static <T> Observable<T> just<T x> {
    return Observable.create(subscriber -> {
        subscriber.onNext(x);
        subscriber.onCompleted();
    });
}
```

나머지 5개는 숙제~

#### Mastering Observable.create()

create 는 default sync. 이를 이용해 내부 동작을 더 잘 알아보자

```java
// 로그용 함수
private static void log(Object msg) {
    Ststem.out.println(Thread.getCurrentThread().getName() + ": " + msg);
}

log("before");
Observable.range(5,3).subscribe(i -> {
    log(i);
});
log("after")


/*
결과
main: before
main: 5
main: 6
main: 7
main: after
*/
```

만약 여러 subscriber 가 있다면?

```java
Observable<Integer> ints = 
    Observable.create(subscriber -> {
        log("create");
        subscriber.onNext(42);
        subscriber.onCompleted();
    });

log("start");
ints.subscribe(i -> log("Element A: " + i));
ints.subscribe(i -> log("Element B: " + i));
log("exit");

/*
결과
main: start
main: create
main: Element A: 42
main: create
main: Element B: 42
main: exit
*/
```

subscribe를 순차적으로 실행함을 알 수 있음

## Operators and Transformations

하이레벨 데이터 파이프 라이닝 방식을 알아 보자  
marble diagram 이란 것으로 스트림 파이프라이닝을 표현
![flip](https://github.com/sangmoon/TIL/raw/master/springStudy/resource/flip.png)

### Core Operators: Mapping and Filtering(FlatMap)

Stream API 와 아주 유사. 거의 같다고 볼 수 있다.

- 관심 없는 이벤트가 있다면? filter를 사용하자

```java
Observable<String> strings = someFileSource.lines();
Observable<String> comments = strings.filter(s -> s.startWith("#"));
Observable<String> instructions = strings.filter(s -> s.startWith(">"));
Observable<Empty> empty = strings.filter(String::isBlank);
```
![filter](https://github.com/sangmoon/TIL/raw/master/springStudy/resource/filter.png)

- 변환을 시키려면 ? map 을 쓰자

```java
Observable<Tweets> tweets = //
Observable<Date> dates = tweets.map(status -> status.getCreatedAt()); // 변환 가능
Observable<Instant> instants = tweeets.map(Status::getCreatedAt).map(Date::toInstant); // chaining 도 물론 가능
```

![map](https://github.com/sangmoon/TIL/raw/master/springStudy/resource/map.png)

```java
// 실행 결과는??
Observable.just(8, 9, 10)
    .doOnNext(i -> System.out.println("A: " + i))
    .filter(i -> i % 3 > 0)
    .doOnNext(i -> System.out.println("B: " + i))
    .map(i -> "#" + i * 10)
    .doOnNext(i -> System.out.println("C: " + i))
    .filter(s -> s.length() < 4);

```

```java
// 실행 결과는??
Observable.just(8, 9, 10)
    .doOnNext(i -> System.out.println("A: " + i))
    .filter(i -> i % 3 > 0)
    .doOnNext(i -> System.out.println("B: " + i))
    .map(i -> "#" + i * 10)
    .doOnNext(i -> System.out.println("C: " + i))
    .filter(s -> s.length() < 4)
    .subscribe(i -> System.out.println("D: " + i));

/*
A: 8
B: 8
C: #80
D: #80
A: 9
A: 10
B: 10
C: #100
*/
```

- ``flatMap`` 아마.. 가장 중요한 메소드

1. map과 유사하지만, 새로운 Observable을 반환한다.
2. 1의 특징 때문에 asynchronus fork-join 처럼 사용될 수 있다.(Observable은 asynchronous 작업을 뜻하기 때문)
3. 내부 로직을 뜯어보면 각각 새로운 inner Observable을 생성하고(fork execution), inner Observable을 모두 구독하여 하나의 Stream 처럼 행동(join) 한다.

![flatmap](https://github.com/sangmoon/TIL/raw/master/springStudy/resource/flatmap.png)

flatmap 예시.. 차량 번호판 판독기를 만들고자 함
- 고속도로 통과하는 차량 사진을 스트림으로 받음
- 비전 알고리즘을 돌려서 번호판만 따로 뽑아냄
- 판독에 실패 할 수도 있고, 어떤 경우에는 차 1대에서 2개의 번호판을 뽑아낼 수도 있음

```java
Observable<CarPhoto> cars() {
// ...
}
Observable<LicensePlate> recognize(CarPhoto car) {
// ...
}
```
Observable<LicensePlate> 를 기본 data stream 으로 하면 다음과 같이 설계 가능
- 사진에서 번호판 못 찾음(empty())
- 모듈에서 심각한 에러가 발생해 실패함(onError())
- 하나 이상의 번호판을 발견(onNext()* onComplete())

```java
Observable<CarPhoto> cars = cars();

// generic을 2번 해야함...
Observable<Observable<LicensePlate>> plates = cars.map(this::recognize);

// generic을 1번만 써도 됨!
Observable<LicensePlate> plates2 = cars.flatMap(this::recognize);
```
- map 은 내부 Observable로 값을 감싼다.(이전 예제 에선 그냥 값을 반환하는 function 을 map에 사용해서 문제 없었음)
- nested Observable은 가독성도 떨어지고, 문제가 많음
- flatMap은 이를 해결할 수 있음

이것 말고도 merge, zip collect, reduce, custom operator 등 많은데 시간 관계상 스킵
<!-- ### More Than One Observable -->

## Applying Reactive Programming to Existing Applications

지금까지 single thread 로만 했으니 멀티 쓰레딩을 적용해보자

### Imperative Concurrency

보통의 enterprise 어플리케이션은 하나의 쓰레드가 하나의 요청을 수행함
- TCP 요청 받기
- HTTP 요청 파싱
- controller나 serlvet 호출
- db call blocking
- 결과 계산
- response 인코딩
- raw bytes 클라이언트에 전송

이게 thread 엄청 잡아먹으니... event-driven 나오게 되었음

예제 상황  
비행기 예매 시스템  
1. 클라이언트가 clientID, 비행기ID 입력
2. 승객, 비행기 각각 조회 후
3. 비행기 예약하고
4. 이메일로 티켓정보 보내줘야함

```java
// 고전적인 스타일
// 모두 blocking job 이라 가정
Flight lookupFlight(String flightNo);   // 비행기 조회
Passenger findPassenger(long id);       // 승객 조회
Ticket bookTicket(Flight flight, Passenger passenger); // 티켓예매
SmtpResponse sendEmail(Ticket ticket);  // 이메일 전송

// client code
Flight flight = lookupFlight("KA 783");
Passenger passenger = findPassenger(42);
Ticket ticket = bookTicket(flight, passenger);
sendEmail(ticket);
```

다 블럭킹 메소드이기 때문에 순차적으로 진행. 몇몇 포인트 들이 보임
- 비행기 조회와 승객 검색은 동시에 할 수 있음 
- 예매는 앞의 2개 작업이 끝나야 함
- 예매의 결과 내보내는 작업과 email 전송은 동시에 진행할 수 있음

이를 rx 스타일로 바꾸면?

```java
// Observable wrapper
Observable<Flight> rxLookupFlight(String FlightNo) {
    return Observable.defer(() -> {
        Observable.just(lookupFlight(flightNo));
    });
}

Observable<Passenger> rxFindPassenger(long id) {
    return Observable.defer(()-> {
        Observable.just(findPassenger(id));
    });
}

//client code
Observable<Flight> flight = rxLookupFlight("KA 783"); // 1
Observable<Passenger> passenger = rxFindPassenger(42); 
Observable<Ticket> ticket = flight.zipWith(passenger, (f, p) -> bookTicket(f, p)); //2
ticket.subscribe(this::sendEmail); //3
```

위 코드는 고전 스타일 코드와 결과적으로 동일하게 동작함.
1. flight, passenger 의 Observable을 만듬.(defer를 썼기 때문에 blocking 작업도 lazy 하게 처리)
2. 두 Observable을 zip 해서 예매하는 ticket Observable 생성
아직 까지 어떠한 콜백도 실행되지 않음
3. ``ticket.subscribe`` 를 실행하는 순간 flight와 passenger도 자동적으로 구독하게 됨
4.  우선 flight의 lookupFlight 메소드 실행됨
5. 그리고 passenger 의 findPassenger 실행
6. 이제 downstream으로 데이터가 내려와 bookTicket 실행
7. 마지막으로 this::sendEmail 실행

이제 conccurency 적용해보자

```java
//client code
Observable<Flight> flight = rxLookupFlight("KA 783").subscribeOn(Scheduler.io()); //1
Observable<Passenger> passenger = rxFindPassenger(42).subscribeOn(Scheduler.io()); 
Observable<Ticket> ticket = flight.zipWith(passenger, (f, p) -> bookTicket(f, p)); 
ticket.subscribe(this::sendEmail); //3
```

1. subscribeOn 사용하면 Observable.create 가 실행되는 쓰레드를 설정할 수 있음..
결과는 같지만 concurrency 적용할 수 있다.

<!-- ### flatMap() as Asynchronous chaining Operator -->

<!-- ### Repacing Callbacks with Streams -->

<!-- ### Multithreading in rxJava -->

# 끝
## 과제 어떻게 하지...
1. rxJava로만 가능하게
2. 배우진 않았지만 webflux 로..
3. rxNetty 활용한 서버로..?