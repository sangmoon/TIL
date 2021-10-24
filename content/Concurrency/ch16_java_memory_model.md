---
title: Java memory model
date: 2021-10-23T08:47:11+01:00
summary: 자바 메모리 모델에 대해 알아보자
draft: false
---


# ch16 자바 메모리 모델

## 16.1 자바 메모리 모델은 무엇이며, 왜 사용해야 할까?

```java
//특정 쓰레드에서 변수에 값을 할당
aVailable = 3;
```

자바 메모리 모델: "쓰레드가 aVariable에 할당도니 3이란 값을 사용할 수 있으려면 어떤 조건이 돼야 하는가?"
동기화 기법을 사용하지 않으면, 영언히 3을 읽어가지 못하는 여러 상황 존재.

- 컴파일러에서 소스코드에 적힌 내용을 명확하게 구현하는 코드를 생성 못할 가능성
- 변수 값을 메모리가 아닌 CPU 레지스터에 보관할 수 있음
- CPU 프로세서는 프로그램을 순차실행 하거나, 병렬 실행할 수 있고 따라서 사용하는 캐시 형태에 다라 할당된 값이  메모리에 보관되는 시점에 차이가 있을 수 있으며 CPU 내부 캐시 값이 다른 CPU에는 안 보일 수 있다.

싱글 쓰레드 일 때는 이런 현상이 가려져 보이지 않음. JVM 명세에 싱글 스레드 일 경우, 순차실행과 같은 결과를 보장하도록 하고 있음. 결과만 같으면 어떤 식으로 하든 상관없음.

### 16.1.1 플랫폼 메모리 모델

- 메모리 공유 멀티 프로세서 시스템은 보통 프로세서 내에 캐시가 있음
- 캐시의 내용을 주기적으로 메인 메모리와 동기화
- 하드웨어 프로세서 아키텍처는 저마다 다른 캐시 일관성(cache coherence)를 지원
- 멀티 프로세서에서 모두 동기화처리하는 것은 부하가 큼. 대부분 성능을 위해 캐시 일관성을 일부  포기함.
- 시스템 구조의 메모리 모델은 기본 정보를 제공하고, 메모리 내용을 공유하고자 할 때 특별한 명령어(memory barrier나 fence) 를 어떻게 사용해야 하는지 제공
- 자바 개발자가 하드웨어 신경 쓰지 않도록 JVM은 JMM(java memory model) 을 통해 이를 추상화.

### 16.1.2 재배치

- JMM은 서로 다른 쓰레드가 각자 상황에 맞게 명령어를 실행할 수 있도록 허용
- 동기화되지 않은 부분의 실행 순서 예측은 힘듬
- 특정 작업이 지연되거나 다른 순서로 실행되는 것처럼 보이는 문제는 ``재배치(reorder)`` 로 표현

```java
//예제16.1
public class PossibleReordering {
    static int x = 0, y = 0;
    static int a = 0, b = 0;

    public static void main(String[] args) throws InterruptedException {
        Thread one = new Thread(new Runnable(){
            public void run() {
                a = 1;
                x = b;
            }
        });
        Thread other = new Thread(new Runnable() {
            public void run() {
                b = 1;
                y = a;
            }
        });

        one.start(); other.start();
        one.joint(); other.join();
        System.out.println(x + " , " + y);
    }
}
```

결과 예측은 어려움. (1,0) (0,1) (1,1) (0,0) 다 가능

### 16.1.3 자바 메모리 모델을 간략히 설명한다면

- JMM 은 프로그램 내부 모든 작업을 대상으로 ``미리 발생(happens-before)`` 라는 ``부분 재배치(partial reordering)`` 연산을 정의
- 작업 A가 실행된 결과를 작업B에서 볼수 있다는 점을 보장하기 위해(동일 쓰레드는 다른 쓰레드든) 작업 A와 작업B 사이에는 미리 발생 관계가 갖춰져야 한다
- 관계가 없아면 JVM은 지멋대로 작업을 재배치
- 하나의 변수를 2개이상 쓰레드가 읽고, 최소 하나 이상 쓰레드에서 쓰기 작업을 하는데 미리 발생 관계가 갖춰져 있지 않다면 ``데이터 경쟁(data race)`` 가 발생
- 이런 데이터 경쟁이 발생하지 않는 프로그램을 ``올바른 동기화 프로그램(correctly synchoronized program)`` 이라고 함.

> 미리 발생 현상 규칙
>> ``프로그램 순서 규칙``: 특정 스레드를 놓고 봤을 때 프로그램된 순서에서 앞서 있는 작업은 동일 스레드에서 뒤에 실행되도록 프로그램된 작업보다 미리 발생한다  
>> ``모니터 잠금 규칙``: 특정 모니터 잠금 작업이 뒤이어 오는 모든 모니터 잠근 작업보다 미리 발생한다  
>> ``volatile 변수 규칙``: volatile 변수에 대한 쓰기 작업은 이후에 따라오는 해당 변수에 대한 모든 읽기 작업보다 미리 발생한다  
>> ``쓰레드 시작 규칙``: 특정 스레드에 대한 Thread.start 작업은 시작된 스레드가 갖고 있는 모든 작업보다 미리 발생한다  
>> ``스레드 완료 규칙``: 스레드 내부의 모든 작업은 다른 스레드에서 해당 스레드가 완료됐다는점을 파악하는 시점보다 미리 발생한다. 특정 스레드가 완료됐는지 판단하는 것은 Thread.join 메소드가 리턴되거나 Thread.isAlive가 false를 리턴하는지 확인하는 방법을 말한다  
>> ``인터럽트 규칙``: 다른 스레드를 대상으로 interrupt 메소드를 호출하는 작업은 인터럽트 당한 스레드에서 인터럽트를 당했다는 사실을 파악하는 일보다 미리 발생한다. 인터럽트를 당했다는 사실을 파악하려면 InterruptedException을 받거나 isInterrupted 메소드 또는 interrupted 메소드를 사용할 수 있다  
>> ``완료 메소드(finalizer) 규칙``: 특정 객체에 대한 생성 메소드가 오나료되는 시점은 완료메소드가 시작하는 시점보다 미리 발생한다  
>> ``전이성(transitivity)``: A가 B보다 미리 발생하고, B가 C보다 미리 발생한다면, A는 C보다 미리 발생한다

** 특정 Lock 객체 잠그거나 해제하는 연산은 암묵적락과 동일한 메모리 현상을 보여준다  
** 단일 연산 변수에 대한 읽기 쓰기 연산은 volatile 변수에 대한 작업과 동일한 메모리 현상을 보여준다.

작업이 부분적으로만 순서가 정해져 있어도, 동기화 작업(락 확보 및 해제, vilatile 변수 읽기 쓰기 작업)은 항상 완전하게 순서가 정해져 있다.

### 16.1.4 동기화 피기백

- ``피기백(piggyback)``: 현재 사용 중인 동기화 기법의 가시성(visiblity)에 얹혀가는 방법 락으로 보호돼 있지 않은 변수에 모니터락이나 volatile 변수 규칙 같은 미리 발생 규칙을 함께 적용해 순서를 정의하는 방법. 오류가 나기 쉬워 성능 튜닝이 정말 중요할 때만 써야함

- AQS는 FutureTask가 맡은 작업의 진행 상태(실행 중, 완료, 취소 여부를 정수형으로 보관) 및 결과 관리
- 외부에서는 set()으로 실행 결과를 보관하고, get()으로 결과 값을 가져옴
- 결과 값 보관 변수를 volatile로 선언해도 되겠지만, 기존 동기화 잘 이용하면 적은 자원으로 동일한 결과 얻을 수 있음
- FutureTask 메소드에서 ``tryReleaseShared()`` 메소드가 ``tryAcquireShared()`` 보다 항상 먼저 실행되도록 되어 있음...

```java
// AbstractQueuedSynchronizer 내부
private volatile Thread runner;

protected boolean tryReleaseShared(int ignore) {
    runner = null;
    return true;
}

protected int tryAcquireShared(int ignore) {
    return innerIsDone() ? 1 : -1;
}

boolean innerIsDone() {
    return ranOrCancelled(getState()) && runner == null;
}
```

innerSet() 은 releaseShared() 하기 전에 결과를 set 하고 innerGet()은 acquireShared() 하고 결과 얻어오므로... 락 없으나 result 쓰는 일이 result 읽는 것보다
먼저 일어나도록 조절하고 있음

```java
// FutureTask 내부의 AbstactQueuedSynchronizer class
private final class Sync extends AbstactQueuedSynchorizer {
    private static final int RUNNING = 1, RAN = 2, CANCELLED = 4;
    private V result;
    private Exception exception;

    void innnerSet(V v) {
        while(true) {
            int s = getState();
            if(RanOrCancelled(s))
                return;
            if(compareAndSetState(s, RAN)) 
                break;
        }
        result = v;
        releaseShared(0);
        done();
    }

    V innerGet() throws InterruptedException, ExecutionException {
        acquireSharedInerruptibly(0);
        if(getState() == CANCELLED)
            throw new CancellationException();
        if(exception != null)
            throw new ExecutionException(exception);
        return result;
    }
}
```

이처럼 객체 값 공개할 미리 발생 규칙 따로 정의하지 않고, 다른 목적으로 만들어 놓은 미리 발생 순서를 가져다가 사용하는 것을 피기백이라고 함

## 16.2 안전한 공개

## 16.2.1 안전하지 못한 공개

```java
public class UnsafeLazyInitialization {
    private static Resource resource;

    public static Resource getInstance() {
        if(resource == null) {
            resource = new Resource();
        }
        return resource;
    }
}
```

- 경쟁 조건 생길 수 있음
- 심한 경우, 참조는 최신화되지만 내부 초기화는 재배치 될 수 있음

락을 쓰거나 volatile을 쓰면 미리 발생 관계가 보장됨..

## 16.2.2 안전한 공개



### 16.2.3 안전한 초기화를 위한 구문

- Syncronized
- Static (static 변수가 아니어도 static block에서 초기화하면 같은 효과)

```java
// 스레드 안전 초기화
public class SafeLazyInitialization {
    private static Resource resource;

    public synchronized static Resource getInstance() {
        if(resource == null) {
            resource = new Resource();
        }
        return resource;
    }
}
```
```java
// 성질 급한 초기화
public class SafeLazyInitialization {
    private static Resource resource = new Resource();

    public synchronized static Resource getInstance() {
        return resource;
    }
}
```
```java
public class ResourceFactory {
    private static class ResourceHolder {
        public static Resource resource = new Resource();
    }

    public static Resource getResource() {
        return ResourceHolder.resource;
    }
}
```

### 16.2.4 Double Checked Lock

```java
public class DoubleCheckedLocking {
    private static Resource resource;

    public static Resource getInstance() {
        if(resource == null) {
            synchronized(DoubleCheckedLocking.class) {
                if(resource == null) {
                    resource = new Resource();
                }
            }
        }
        return resource;
    }
}
```
- 가독성 떨어짐...
- 부분 구성된 Resource 객체를 가져올 가능성 있음
- volatile 쓸 것

## 16.3 초기화 안전성

``초기화 안전성(initialization safety)`` : 올바르게 생성된 불변객체를 어떤 방법으로건 공개해도 별다른 동기화 구문 없이 안전하게 쓸 수 있다.

- final 로 선언된 변수를 갖고 있는 클래스는 초기화 안전성 조건 때문에 인스턴스 참조 최초 생성 때 재배치가 일어나지 않는다

```java
public class SafeStates {
    private final Map<String, String> status;

    public SafeStates() {
        states = new HashMap<String, String>();
    }

    public String getAbbreviation(String s) {
        return states.get(s);
    }
}
```

이 클래스는 스레드 안전하지만..

- states 가 final이 아니거나
- 생성자가 아닌 곳에서 states를 변경하거나
- SafeStates class에 final로 선언되지 않은 다른 변수가 더 있다면 해당 변수들은
다른 쓰레드에서는 올바르게 못 볼 수 있다.
- 생성자 완료되기 전에 객체를 외부에 노출하는 경우에도..

## 요약

JMM은 어렵다.