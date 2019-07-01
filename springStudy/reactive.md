# Reactive Programming

```java
public class Main {
    public static void main(String[] args) {
        Observable.just("Hello world").subscribe(System.out::println);
    }
}
```

## what is Monad?
## rx 와 callback 차이



## Reactive Programming with rxJava

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

### Reactive Abstraction

## Reactive Extension

### Anatomy of rx.Observable

### Subscribing to Notifications from Observable

### Controlling Listeners by Using Subscription and Subscriber<T>

### Creating Oservable

## Operators and Transformations

### Core Operators: Mapping and Filtering(FlatMap)

### More Than One Observable

## Applying Reactive Programming to Existing Applications

### From Collections to Observables

### Composing Observables

### Imperative Concurrency

### FlatMap() as Asynchronous Chaining Operator

### Repacing Callbacks with Streams

### Multithreading in rxJava