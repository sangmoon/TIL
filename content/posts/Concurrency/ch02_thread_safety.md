# 쓰레드 안전성

- 객체의 상태(object's state) = 인스턴스나 static 변수 같은 상태 변수에 저장된 객체의 데이터
- 공유되었다(shared) = 여러 쓰레드가 특정 변수에 접근할 수 있다
- 변경할 수 있다(mutable) = 해당 변수 값이 변경될 수 있다
- 쓰레드 안전성(Thread safety) = 데이터에 제한 없이 동시에 접근하는걸 막으려는 것

- 하나 이상의 쓰레드가 상태 변수에 접근하고, 하나라도 변수에 값을 쓰면 해당 변수에 접근할 때 관련 쓰레드는 동기화 사용해야 함

- 자바에서 동기화 수단: ``synchronized``, ``volaitile``, ``명시적 락``, ``atomic variable``

> 여러 쓰레드가 동기화 없이 변경 가능한 하나의 상태 변수에 접근하면 잘못된 프로그램임.<br> 이를 고치려면 </br>
상태 변수를 쓰레드 간 공유하지 않거나(thread-local, single-threaded) </br>
상태 변수를 변경 불가능하게 하거나(immutable)</br>
상태 변수를 접근할 땐 언제나 동기화 한다(synchronization)</br>

>  쓰레드 안전한 클래스를 설계할 때 , 캡슐화, 불변 객체를 잘 활용하고 불변 조건을 명확히 기술해야 한다.

## 2.1 쓰레드 안전성(thread safety)이란

> 여러 쓰레드가 한 클래스에 접근할 때, 실행 환경(OS..?)이 해당 쓰레드들을 어떻게 스케줄하든 <br>호출하는 쪽(Caller)에서 추가적인 동기화나 다른 조율 없이도 ***정확하게*** 동작하면 해당 클래스는 쓰레드 안전하다고 말한다. ('정확하게' 라는건 클래스가 명세대로 동작함을 의미한다.)

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
> Stateless Objects 는 항상 Thread-safe 하다

## 2.2 단일 연산 (Atomicity)

위 클래스에 요청 횟수를 기록하는 접속 카운터를 추가.

```java
@NotThreadSafe
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

- ``++`` 연산은 내부적으로 3개의 단일 연산의 시퀀스로 구성( 현재 값 가져오기/1더하기/새 값 저장하기) (load, add, mov 아마도..?)
- 이 부분에서 여러 쓰레드가 접근하면 문제 발생 가능
- 경쟁 조건(race condition) 생김. 

### 2.2.1 경쟁 조건 (race condition)

UnsafeCountingFactorizer 는 경쟁 조건이 나타나기 때문에 결과를 신뢰할 수 없다. 경쟁 조건은 상대적인 시점이나, 런타임이 여러 쓰레드를 교차해서 실행하는 상황에 따라 계산의 정확성이 달라질 때 나타난다. 가장 일반적인 경쟁 조건 형태는 점검 후 행동(``check-then-act``) 이다.
(점검 후 행동은 stale data가 다음 행동을 결정하는 형태)

### 2.2.2 늦은 초기화 시 경쟁 조건

점검 후 행동하는 가장 흔한 예제는 늦은 초기화(``lazy initialization``) 가 있다. 늦은 초기화는 필요한 시점에 딱 한 번만 초기화 하기 위한 프로그래밍 기법.

```java
@NotThreadSafe
public class LazyInitRace {
    private ExpensiveObject instance = null;

    public ExpensiveObject getInstance() {
        if(instance == null) { //critical seciton
            instance = new ExpensiveObject();
        }
        return instance;
    }
}
```
쓰레드 A, B가 같은 LazyInitRace 객체에 접근해서 getInstance()를 호출하면 문제 발생할 수 있음 
여러 쓰레드가 getInstance 메소드에 접근하면 경쟁 조건 발생함.

**UnsafeCountingFactoriezer** 은 도 따른 형턔의 race-condition 이다. ``read-modify-write``
는 이전 상태를 기준으로 객체 상태를 변경하는 동작이다.

race condition은 항상 실패하진 않는다. 하지만 치명적인 문제를 야기할 수 있다.

### 2.2.3 복합 동작 (compound actions)

> 작업 A를 실행 중인 쓰레드 관점에서 다른 쓰레드가 작업 B를 실행할 때 작업 B가 모두 수행됐거나 또는 전혀 수행되지 않은 두가지 state 로만 파악된다면 작업 A의 눈으로 볼 때 작업 B는 단일 연산이다. 단일 연산은 자신을 포함해 같은 state를 다루는 모든 작업이 단일 연산인 작업을 지칭한다.

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
    boolean lazySet(boolean newValue); // memory-model 에서 store-load 를 store-store 로 해서 퍼포먼스 향상...  GC 위한 nullable 할 때 많이 쓴다고 함
    boolean set(boolean newValue);
    boolean weakCompareAndSet(boolean expected, boolean update); // 거의 안 씀..
}
```

```java
//https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/atomic/package-summary.html
The memory effects for accesses and updates of atomics generally follow the rules for volatiles, as stated in section 17.4 of The Java™ Language Specification.

get has the memory effects of reading a volatile variable.

set has the memory effects of writing (assigning) a volatile variable.

lazySet has the memory effects of writing (assigning) a volatile variable except that it permits reorderings with subsequent (but not previous) memory actions that do not themselves impose reordering constraints with ordinary non-volatile writes. Among other usage contexts, lazySet may apply when nulling out, for the sake of garbage collection, a reference that is never accessed again.

weakCompareAndSet atomically reads and conditionally writes a variable but does not create any happens-before orderings, so provides no guarantees with respect to previous or subsequent reads and writes of any variables other than the target of the weakCompareAndSet. compareAndSet and all other read-and-update operations such as getAndIncrement have the memory effects of both reading and writing volatile variables.
```

## 2.3 락

- 인수분해 결과를 캐시하려함
- 가장 마지막 인수분해한 숫자를 ``lastNumber``, 그 결과를 ``lastFactors`` 에 담는다.

```java
@NotThreadSafe
public class UnsafeCachingFactorizer implements Servlet {
    private final AtomicReference<BigInteger> lastNumber
        = new AtomicReference<>();
    private final AtomicReference<BigInteger[]> lastFactors
        = new AtomicReference<>();

    public void service(ServletRequest req, ServletResponse resp) {
        BigInteger i = extractFromRequest(req);

        // 첫번째 취약점
        if (i.equals(lastNumber.get())) {
            encodeIntoResponse(resp, lastFactors.get());
        } else {
            BigInteger[] factors = factor(i);
            // 두번째 취약점
            lastNumber.set(i);
            lastFactors.set(factors);
            encodeIntoResponse(resp, factors);
        }
    }
}
```

- 참조 자체는 쓰레드 안전하지만 결과는 틀릴 수 있다.
- set() 과 get() 이 2개의 메소드이기 때문에 Atomic하지 않다.

> 상태를 일관성 있게 유지하려면 관련 있는 변수들을 하나의 단일 연산으로 갱신해야 한다.

### 2.3.1 암묵적인 락(intrinsic lock)

- 자바에서는 단일 연산 보장 위해 ``synchronized`` 키워드 제공
- 락으로 사용될 객체의 참조와 락으로 보호하려는 코드 블록으로 구성
- 메소드 선언에 synchronized 를 지정하면 매소드 내부 전체를 포함하며 메소드가 포함된 클래스의 인스턴스를 락으로 사용(static method는 클래스 객체를 락으로 사용)

```java
synchronized (lock) {
    // lock으로 보호된 영역
}
```

- 모든 자바 객체는 락으로 사용 가능
- 락은 thread 가 synchronized 블록 들어가기 전에 자동으로 확보되어 해당 블록 벗어날 때 자동으로 해제됨
- 자바의 경우 mutex로 구현

```java
@Threadsafe
public class SnchronizedFactorizer implements Servlet {
    @GuardedBy("this") private BigInteger lastNumber;
    @GuardedBy("this") private BigInteger[] lastFactors;

    public synchronized void service(ServletRequest req, ServletResponse resp) {
               BigInteger i = extractFromRequest(req);

        if (i.equals(lastNumber.get())) {
            encodeIntoResponse(resp, lastFactors.get());
        } else {
            BigInteger[] factors = factor(i);
            lastNumber.set(i);
            lastFactors.set(factors);
            encodeIntoResponse(resp, factors);
        }
    }
}
```

- 메소드에 synchronized 달아서 쉽게 고칠 수 있음.
- 성능 매우 떨어질 수 있음

### 2.3.2 재진입성(reentrant)

- 암묵적인락은 재진입 가능하기 때문에 자기가 이미 획득한 락을 다시 확보할 수 있음
- 락 동작을 쉽게 캡슐화 가능
- 재진입성 없으면 자식 class 에서 override 한 후 부모 class 메소드 호출하면 데드락 걸릴 수 있음

```java
public class Widget {
    public synchronized void doSomething(){}
}

public class LoggingWidget extents Widget {
    pbulic synchronized void doSomething() {
        super.doSomething();
    }
}
```

## 2.4 락으로 상태 보호하기

> 여러 쓰레드에서 접근할 수 있고 변경 가능한 모든 변수를 대상으로 해당 변수에 접근할 때는 항상 동일한 락을 먼저 확보한 상태여야 한다. 이 경우 해당 변수는 확보된 락에 의해 보호된다고 한다.

- 객체의 암묵적인 락과 그 객체의 상태에는 특별한 관계는 없음
- 쓰기 쉬워서 default로 해놓은 것일 뿐임
- 공유 상태에 안전하게 접근할 수 있도록 락 규칙이나 동기화 정책을 만들고 프로그램 내에서 규칙과 정책을 일관성 있게 따르는 건순전히 개발자에게 달림

> 모든 변경할 수 있는 공유 변수는 정확하게 단 하나의 락으로 보호해야 한다. 유지 보수하는 사람이 알 수 있게 어느 락으로 보호하고 있는지를 명확하게 표시하라(``@GuardedBy``)

- synchronized 동기화의 해법은 아님
- ``Vector`` 는 모든 메소드가 단순 동기화되어 있음. 여러 메소드를 섞으면 또 다른 락이 필요함

```java
if (!vector.contains(element)) {
    vector.add(elements);
}
```

- 동기화를 통해 메소드 각각을 단일 연산화 시킬 수 있지만,여러 메소드를 복합으로 사용하려면 추가 동기화 필요.
- 모든 메소드를 동기화 하면 성능에 문제 생길 수 있음

## 2.5 활동성과 성능

- 동기화를 단순하고 큰 단위로 접근하면 안전하지만 성능 감소가 매우 큼
- ``SynchronizedFactorizer`` 예제의 경우 service 실행을 한번에 한 쓰레드만 할 수 있음
- 병렬처리 능력이 떨어지게 됨

```java
@ThreadSafe
public class CachedFactorizer implements Servlet {
    @GuardedBy("this") private BigInteger lastNumber;
    @GuardedBy("this") private BigInteger[] lastFactors;
    @GuardedBy("this") private long hits;
    @GuardedBy("this") private long cacheHits;

    public synchronized long getHits() {return hits;}
    public synchronized double getCacheHitRatio() {
        return (double) cacheHits / (double) hits;
    }

    public void service(ServletRequest req, ServletResponse resp) {
        BigInteger i = extractFromRequest(req);
        BigInteger[] factors = null;
        synchronized (this) {
            ++hits;
            if (i.equals(lastNumber)) {
                ++cacheHits;
                factors = lastFactors.clone();
            }
        }

        if (factors == null) {
            factors = factor(i);
            synchronized(this) {
                lastNumber = i;
                lastFactors = factors.clone();
            }
        }
        encodeIntoResponse(resp, factors);
    }
}
```

- 접속카운터(``hits``) 를 AtomicLong 대신 long으로 사용. 이미 synchronized 블럭 내에서 처리하기 때문에 성능이나 안전성 측면에서 이득이 없음
- 단순성(전체 메소드 동기화) 병렬 처리 능력(짧은 부분만 동기화) 사이에 균형을 맞춤
- 락을 잡고 놓는 것 자체도 부하가 있음. 너무 짧게 sync 블럭을 나누는 것도 좋지 않음
- 위의 경우 오래 걸릴 가능성이 높은 인수분해 시에는 락을 놓는다. 이렇게 하므로써 병렬 처리 능력에 영향을 주지 않으면서 쓰레드 안전성 확보.
- 각 sync block 은 충분히 짧다(어떻게 계산하지..?)

> 종종 단순성과 성능이 서로 상출할 때가 있다. 동기화 정책을 구현할 때는 성능을 위해 조급하게 단순성(잠재적으로 안전성을 훼손하면서)을 희생하고픈 유혹을 버려야 한다.

- 락을 사용할 땐 블록 안 코드가 수행하는 일과 수행 예측 시간을 파악해야 함. 계산량이 많거나 쓰레드가 잠들 수 있는 작업을 하느라 락을 오래 잡고 있으면 성능 문제가 야기 될 수 있다.

> 복잡하고 오래 걸리는 계산 작업, 네트워크 작업, 사용자 입출력 작업과 같이 빨리 끝나지 않을 수 있는 작업을 하는 부분에서는 가능한 락을 잡지 마라