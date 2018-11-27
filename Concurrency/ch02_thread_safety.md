# 쓰레드 안전성

- 객체의 상태 = 인스턴스나 static 변수 같은상태 변수에 저장된 객체의 데이터
- 공유되었다 = 여러 쓰레드가 특정 변수에 접근할 수 있다
- 변경할 수 있다(mutable) = 해당 변수 값이 변경될 수 있다
- 쓰레드 안전성 = 데이터에 제어 없이 동시에 접근하는걸 막으려는 것

- 하나 이상의 쓰레드가 상태 변수에 접근하고, 하나라도 변수에 값을 쓰면 해당 변수에 접근할 때 관련 쓰레드는 동기화 사용해야 함

- 자바에서 동기화 수단: synchronized, volaitile, 명시적 락, atomic variable

> 여러 쓰레드가 동기화 없이 변경 가능한 하나의 상태 변수에 접근하면 잘못된 프로그램임. 이를 고치려면 </br>
상태 변수를 스레드 간 공유하지 않거나(thread-local, single-threaded) </br>
상태 변수를 변경 불가능하게 하거나(immutable)</br>
상태 변수를 접근할 땐 언제나 동기화 한다</br>

## 2.1 쓰레드 안전성(thread safety)이란

> 여러 쓰레드가 클래스에 접근할 때, 실행 환경이 해당 쓰레드들의 실행을 어떻게 스케줄하든 호출하는 쪽에서
> 추가적인 동기화나 다른 조율 없이도 정확하게 동작하면 해당 클래스는 쓰레드 안전하다고 말한다.

> 쓰레드 안전한 클래스는 클라이언트 쪽에서 별도로 동기화할 필요 없도록 동기화 기능이 캡슐화 되어 있다.

### 2.1.1 상태없는 서블릿 (stateless servlet)

인수분해할 숫자를 request에서 가져와 인수분해하고 response에 담는다.
```java
@ThreadSafe
public class StatelesFactorizer implments Servlet  {
    public void service(ServletRequest req, ServletResponse resp) {
        BigInteger i = extractFromRequest(req);
        BigInteger[] factors = factor(i);
        encodeIntoResponse(resp, factors);
    }
}
```

- 맴버 변수 없음
- 다른 클래스 맴버변수 참조 안함
- 일시적 상태는 local variable에 저장

따라서 stateless 하기 때문에 항상 thread-safe 하다.

## 2.2 단일 연산

위 클래스에 요청 횟수를 기록하는 접속 카운터를 추가.

```java
public class UnsafeCountingFactorizer implments Servlet  {

    private long count = 0;

    public getCount(){ return count;}

    public void service(ServletRequest req, ServletResponse resp) {
        BigInteger i = extractFromRequest(req);
        BigInteger[] factors = factor(i);
        ++count;  // critical section
        encodeIntoResponse(resp, factors);
    }
```

- ``++`` 연산은 내부적으로 3개의 단일 연산의 시퀀스로 구성( 현재 값 가져오기/1더하기/새 값 저장하기)
- 이 부분에서 여러 쓰레드가 접근하면 문제 발생 가능
- 경쟁 조건 생김. 이전 상태를 기준으로 객체 상태를 변경하는 동작(read-modify-write)

### 2.2.1 경쟁 조건 (race condition)

UnsafeCountingFactorizer 는 경쟁 조건이 나타나기 때문에 결과를 신뢰할 수 없다. 경쟁 조건은 상대적인 시점이나, JVM이 여러 쓰레드를
교차해서 실행하는 상황에 따라 계산의 정확성이 달라질 때 나타난다. 가장 일반적인 경쟁 조건 형태는 점검 후 행동(check-then-act) 이다.

### 2.2.2 늦은 초기화 시 경쟁 조건

점검 후 행동하는 가장 흔한 예제는 늦은 초기화(lazy initialization) 가 있다. 늦은 초기화는 필요한 시점에 딱 한 번만 초기화 하기 위한 프로그래밍 기법.

```java
public class LazyInitRace {
    private ExepensiveObject instance = null;

    public ExepensiveObject getInstance() {
        if(instance == null) {
            instance = new ExepensiveObject();
        }
        return instance;
    }
}
```

여러 쓰레드가 getInstance 메소드에 접근하면 경쟁 조건 발생함.

### 2.2.3 복합 동작 (compound action)

> 작업 A를 실행 중인 쓰레드 관점에서 다른 쓰레드가 작업 B를 실행할 때 작업 B가 모두 수행됐거나 또는 전혀 수행되지 않은 두가지
상태로만 파악된다면 작업 A의 눈으로 볼 때 작업 B는 단일 연산이다. 단일 연산 작업은 자신을 포함해 같은 상태를 다루는 모든 작업이 단일 연산인 작업을 지칭한다.

- UnsafeCountingFactorizer 에서 ``++count`` 가 단일 연산이었다면? 경쟁 조건 생길 수 없음
- 점검 후 행동, 읽고 수정하고 쓰기 등과 같은 일련의 동작을 복합 동작이라고 함
- 쓰레드에 안전하기 위해선 단일 연산이 수반되어야 함

다음은 쓰레드 안전한 기존 클래스 이용해 Count 예제를 고친 것

```java
@ThreadSafe
public class CountingFactorizer implements Servlet {
    private final AtomicLong count = new AtomicLong(0);

    public long getCount() {return count.get();}

    public void service(ServletRequest req, ServletResponse resp) {
        BigInteger i = extractFromRequest(req);
        BigInteger[] factors = factor(i);
        count.incrementAndGet();
        encodeIntoResponse(resp, factors)
    }
}
```

- ``java.util.concurrent.atomic`` 패키지에는 숫자 및 객체 참조에 대해 상태를 단일 연산으로 변경할 수 있는 ``atomic variable`` class 가 있음
- servlet 의 상태는 count 이고 이 count가 쓰레드 안전하므로 servlet도 쓰레드 안전하다.

> 가능하면 클래스 상태는 ``AtomicLong`` 처럼 이미 안전하게 만들어 둔 것을 사용하는 것이 좋다.

#### concurrent.atomic 패키지 (jdk8)

```java
// AtomicBoolean, AtomicInteger, AtomicLong, AtomicReference<V>, AtomiStampedReference<V>, AtomicMarkableReference  //A-B-A 문제 풀기위해...
// AtomicIntegerArray, AtomicIntegerFieldUpdater<T>, AtomicLongArray, AtomicLongFieldUpdater<T>, AtomicReferenceArray, AtomicReferenceFieldUpdater<T,V>
// DoubleAdder, LongAdder, DoubleAccumulator, LongAccumulator
public class AtomicBoolean {
    boolean compareAndSet(boolean expected, boolean update); // expected와 맞아야지만 update 함
    boolean get();
    boolean getAndSet(boolean newValue);
    boolean lazySet(boolean newValue); // memory-model 에서 store- load 를 store-store 로 해서 퍼포먼스 향상...
    boolean set(boolean newValue);
    boolean weakCompareAndSet(boolean expected, boolean update); // 거의 안 씀..
}
```

## 2.3 락



## 2.4 락으로 상태 보호하기

## 2.5 활동성과 성능