---
title: Test pararrel program
date: 2021-10-23T08:47:11+01:00
summary: 병렬 프로그램을 테스트하자
draft: false
---

# Ch12 병렬 프로그램 테스트

- 정확성 테스트
  - 원하는 동작을 항상 한다.
  - 원치 않는 동작을 항상 안한다.

- 활동성 테스트
  - 데드락
  - 처리량(throughput)
  - 응답성(responseiveness)
  - 확장성(scalability)

## 12.1 정확성 테스트

- 설계대로 작동하는지 테스트

```java
/*
 * 간단한 큐 구현(LinkedBlockingQueue나 ArrayBlockingQueue 하위 호환)
 */
public class BoundedBuffer<E> {
    private final Semaphore availableItems, availableSpaces;
    private final E[] items;
    private int putPosition = 0, takePosition = 0;

    public BoundedBuffer(int capacity) {
        availableItems = new Semaphore(0);
        availableSpaces = new Semaphore(capacity);
        items = (E[]) new Object[capacity];
    }
    public boolean isEmpty() {
        return availableItems.availablePermits() == 0;
    }

    public boolean isFull() {
        return availableSpaces.availablePermits() == 0;
    }

    public void put(E x) throws InterruptedException {
        availableSpaces.acquire();
        doInsert(x);
        availableItems.release();
    }

    public E take() throws InterruptedException {
        availableItems.acquire();
        E item = doExtract();
        availableSpaces.release();
        return item;
    }

    private synchronized void doInsert(E x) {
        int i = putPosition;
        items[i] = x;
        putPosition = (++i == items.length) ? 0 : i;
    }

    private synchronized E doExtract() {
        int i = takePosition;
        E x = items[i];
        items[i] = null;
        takePosition = (++i == items.length) ? 0 : i;
        return x;
    }
}
```

### 12.1.1 가장 기본적인 단위 테스트

```java
public class BoundedBufferTest {
    private static final long LOCKUP_DETECT_TIMEOUT = 10 * 1000;

    /*만들 때 비어있는지*/
    void testIsEmptyWhenConstructed() {
        BoundedBuffer<Integer> bb = new BoundedBuffer<Integer>(10);
        assertTrue(bb.isEmpty());
        assertFalse(bb.isFull());
    }

    /*꽉 차는지*/
    void testisFullAfterPuts() throws InterruptedException {
        BoundedBuffer<Integer> bb = new BoundedBuffer<Integer>(10);
        for(int i=0;i<10;i++) {
            bb.put(i);
        }
        assertTrue(bb.isFull());
        assertFalse(bb.isEmpty());
    }


```

### 12.1.2 블로킹 메소드 테스트

- 병렬 동작 테스트하려면 2개 이상 쓰레드 테스트해야함.
- 만약 특정 메소드가 반드시 대기상태로 들어가야만 한다면 해당 쓰레드는 더 이상 실행되지 않고 멈춰야 테스트 성공.
- 인터럽트를 거는 것이 가장 확실한 방법. 대기 메소드가 인터럽트 걸리면 리턴되거나, InterruptedException 을 던지는 행동하도록 만들어져야 한다.
- JOIN 쓰면 되기 때문에 Thread 상속받는게 편함.
- Thread.getState() 는 JVM 에 따라 구현이 달라서 믿을만하지 않음.


```java
    /*비어있을 때 못 빼내는지*/
    void testTakeBlocksWhenEmpty() {
        final BoundedBuffer<Integer> bb = new BoundedBuffer<Integer>(10);
        Thread taker = new Thread() {
            public void run() {
                try {
                    int unused = bb.take();
                    fail(); // 여기 들어오면 오류!
                } catch(InterruptedException success) {
                }
            }
        };
        try {
            taker.start();
            Thread.sleep(LOCKUP_DETECT_TIMEOUT);
            taker.interrupt();
            taker.join(LOCKUP_DETECT_TIMEOUT);
            assertFalse(taker.isAlive());
        } catch(Exception unExpected) {
            fail();
        }
    }
}
```

### 12.1.3 안전성 테스트

- 위 테스트들은 공유 데이터 경쟁에서 나올 수 있는 오류는 테스트하지 못함
- 병렬처리 환경에서 ``높은 확률``로 잘못된 속성을 찾음과 동시에 병렬성을 ``인위적``으로 재현해서는 안 됨
- BnoudedBuffer와 같이 프로듀서-컨슈머 패턴을 사용하는 클래스는 큐나 버퍼에 추가된 항목을 모두 그대로 뽑아낼 수 있는지 확인하는 방법이 좋음
  - 아무 생각없이 만들면 input 리스트 만들고 queue에 넣을 때 output 리스트 에 넣고, 뺄 때 output 리스트에서 제거해서 마지막에 텅비었는지 확인
    - 추가적인 동기화 작업이 필요하기 때문에 꼬여버릴 가능성 있음
  - 들어가고 나오는 항목의 체크섬을 확인하는 방법
    - 프로듀서 1개, 컨슈머 1개로 항상 순서가 유지되는 구조에서 효과가 좋음
    - 여러 프로듀서, 컨슈머로 확장하려면 체크섬의 순서와 상관없이 최종 체크섬을 비교해야함
    - 사용하는 체크섬이 랜덤한지도 봐야함. 적당히 규칙이 있다면, 컴파일러가 최적화해서 미리 계산해버릴 수 있음
    - 이런 경우 난수발생기 사용하면 됨

```java
// 싼 값에 중급의 품질을 제공하는 난수 발생기..
    static int xorShift(int y) {
        y ^= (y<<6);
        y ^= (y>>>21);
        y ^= (y<<7);
        return y;
    }
```

- 쓰레드 생성하는 것에 부하가 있기 때문에, 최초 쓰레드가 대부분의 작업을 다 담당할 가능성 존재
  - ``CountDownLatch`` 나 ``CyclicBarrier`` 이용하면, 모든 쓰레드가 준비될 때까지 기다릴 수 있음
- 테스트가 끝났음을 쓰레드간 통신으로 하지말고 종료 조건을 정하면 동기화 안해도 되서 편함

```java
public class PutTakeTest {
    private static final ExecutorService pool = Executors.newCachedThreadPool();
    private final AtomicInteger putSum = new AtomicInteger(0);
    private final AtomicInteger takeSum = new AtomicInteger(0);
    private final CyclicBarrier barrier;
    private final BoundedBuffer<Integer> bb;
    private final int nTrials, nPairs; // 쓰레드당 시도 횟수, 쓰레드 수

    public static void main(String[] args) {
        new PutTakeTest(10, 10, 100000).test();
        pool.shutdown();
    }

    PutTakeTest(int capacity, int npairs, int ntrials) {
        this.bb = new BoundedBuffer<Integer>(capacity);
        this.nTrials = ntrials;
        this.nPairs = npairs;
        this.barrier = new CyclicBarrier(npairs*2+1);
    }

    void test() {
        try {
            for(int i=0;i<nPairs;i++) {
                pool.execute(new Producer());
                pool.execute(new Consumer());
            }
            barrier.await();
            barrier.await();
            assertEquals(putSum.get(), takeSum.get());
        } catch(Exception e) {
            throw new RuntimeException(e);
        }
    }

    class Producer implements Runnable {
        @Override
        public void run() {
            try {
                int seed = (this.hashCode() ^ (int)System.nanoTime());
                int sum = 0;
                barrier.await();
                for(int i = nTrials; i>0; --i) {
                    bb.put(seed);
                    sum+=seed;
                    seed=xorShift(seed);
                }
                putSum.getAndAdd(sum);
                barrier.await();
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        }
    }

    class Consumer implements Runnable {
        @Override
        public void run() {
            try {
                barrier.await();
                int sum=0;
                for(int i =nTrials;i>0;--i) {
                    sum += bb.take();
                }
                takeSum.getAndAdd(sum);
                barrier.await();
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        }
    }
}
```

### 12.1.4 자원 관리 테스트

- 지금까지는 스펙에 맞게 동작하는지 확인하는 테스트
- 이번엔 하지말아야 할 일을 하지 않는지 테스트 ex) 자원 유출
- HEAP inspection 을 사용해 볼만 함
- 크기가 제한된 버퍼에 상당한 메모리 객체를 추가하고, 추가된 객체를 제거. 그러면 버퍼는 비어있기에 힙 사용량 크게 변화 없어야함

```java
    class Big{double[] data = new double[100000];}
    static final int CAPACITY = 1000;
    static final int THREHOLD = /*경험적인 값*/;
    void testLeak() throws InterruptedException {
        BoundedBuffer<Big> bb = new BoundedBuffer<Big>(CAPACITY);
        int heapSize1 = /*HEAP SNAP SHOT*/;
        for(int i=0; i< CAPACITY; i++) {
            bb.put(new Big());
        }
        for(int i=0; i<CAPACITY; i++) {
            bb.take();
        }
        int heapSize2 = /*HEAP SNAP SHOT*/;
        assertTrue(Math.abs(heapSize1 - heapSize2) < THRESHOLD);
    }
```

### 12.1.5 콜백 사용

- 콜백 구조를 적용하면 테스트 케이스 구현에 도움이 됨
- 콜백 함수는 중요 시점마다 객체 내부값을 확인하는 좋은 기회 제공
- 모든 기능을 새로 만들지 말고 Java에서 제공하는 기존 클래스들 활용하라는 뜻인듯...
- ThreadPool 예제

```java
public class TestingThreadFactory implements ThreadFactory {
    public final AtomicInteger numCreated = new AtomicInteger();            // 생성한 쓰레드의 수
    private final ThreadFactory factory = Executors.defaultThreadFactory(); // 쓰레드 팩토리

    @Override
    public Thread newThread(Runnable r) {
        numCreated.incrementAndGet(); // 쓰레드 새로 만드는 시점에 증가시킴
        return factory.newThread(r);
    }

        public void testPoolExpansion() throws InterruptedException {
        int MAX_SIZE = 10;
        TestingThreadFactory threadFactory = new TestingThreadFactory();
        ExecutorService exec = Executors.newFixedThreadPool(MAX_SIZE, threadFactory);

        for(int i=0; i<10 * MAX_SIZE; i++) {
            exec.execute(new Runnable() {
                public void run() {
                    try {
                        Thread.sleep(Long.MAX_VALUE);
                    } catch(InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }
            });
        }
        for (int i=0; i<20 && threadFactory.numCreated.get() < MAX_SIZE; i++) {
            Thread.sleep(100);
        }
        assertEquals(threadFactory.numCreated.get(), MAX_SIZE); // 제대로 동작했다면 10개 쓰레드 생성되고 90개는 queueing 되었어야함
        exec.shutdownNow();
    }
}
```

### 12.1.6 쓰레드 교차 실행량 확대

- 병렬프로그래밍의 오류는 concurrency 이슈가 많음. 이를 재현하기는 쉽지 않음
- 쓰레드의 컨택스트 스위칭을 의도적으로 높이면 이런 오류가 나올 확률을 높일 수 있음
  - ``Thread.yield()`` OS에 현재 Thread를 재 스케줄 해도 된다는 힌트를 줌. JVM에 따라 무시하기도 함
  - ``Thread.sleep()`` 강제로 현재 쓰레드를 sleep 상태로 빠지게함. 속도가 약간 느리지만 효과는 명확함
  - 테스트에만 사용하고 제품에서 빼고 싶을 때는 AOP 활용

```java
public synchronized void transferCredits(Account from, Account to, int amount) {
    from.setBalance(from.getBalance() - amount);
    if(random.nextInt(1000) > THRESHOLD) {
        Thread.yield();
    }
    to.setBalance(to.getBalance() + amount);
}
```

## 12.2 성능 테스트

- 성능테스트는 특정 사용환성 시나리오를 정하고, 시나리오를 통과하는데 얼마만큼의 시간이 걸리는지 측정
- 의미있는 사용환경을 가정해야함
- 하드웨어의 영향도 많이 받음(CPU의 수, 메모리 용량, CPU 종류)

### 12.2.1 PutTakeTest의 시간 측정

- 기존 PutTakeTest에 시간 측정을 넣으려 함
- Barrier 적용 부분에 타이머 구현

```java
public class BarrierTimer implements Runnable {
    private boolean started;
    private long startTime, endTime;

    @Override
    public void run() {
        long t = System.nanoTime();
        if(!started) {
            started= true;
            startTime = t;
        } else {
            endTime = t;
        }
    }
    public synchronized void clear() {
        started = false;
    }

    public synchronized long getTime() {
        return endTime - startTime;
    }
}
```

```java
public class TimedPutTakeTest {
    /*배리어 기반 타이머 사용 테스트*/
    private static final ExecutorService pool = Executors.newCachedThreadPool();
    private final AtomicInteger putSum = new AtomicInteger(0);
    private final AtomicInteger takeSum = new AtomicInteger(0);
    private final CyclicBarrier barrier;
    private final BoundedBuffer<Integer> bb;
    private final int nTrials, nPairs;
    private finnal BarrierTimer timer;

    public TimedPutTakeTest(int capacity, int npairs, int ntrials) {
        this.bb = new BoundedBuffer<Integer>(capacity);
        this.nTrials = ntrials;
        this.nPairs = npairs;
        this.timer = new BarrierTimer();
        this.barrier = new CyclicBarrier(npairs*2+1, timer); // Runnable을 생성자에 넣어줌
    }

    public void test() {
        try {
            timer.clear();
            for(int i=0; i<nPairs; i++) {
                pool.execute(new Producer());
                pool.execute(new Consumer());
            }
            barrier.await();
            barrier.await();
            long nsPerItem = timer.getTime() / (nPairs * (long)nTrials);
            System.out.println("Throughput: " + nsPerItem + " ns/item");
            assertEquals(putSum.get(), takeSum.get());
        }catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    public static void main(String[] args) throws Exception	{
        int tpt = 100000; //쓰레드별 실행횟수
        for(int cap=1; cap<=1000; cap*=10) { //버퍼 용량
            System.out.println("Capacity: "+cap);
            for(int pairs=1; pairs<=128; pairs*=2) { // 쓰레드 수
                TimedPutTakeTest t = new TimedPutTakeTest(cap, pairs, tpt);
                System.out.println("Pairs: " + pairs);
                t.test();
                System.out.println("");
                Thread.sleep(1000);
                t.test();
                System.out.println("");
                Thread.sleep(1000);
            }
        }
        pool.shutdown();
    }
}
```

- 테스트 결과는 책 참조...
- 버퍼가 크기가 크면 선능 증가
- 쓰레드 수는 오히려 성능 악화

12.2.2 다양한 알고리즘 비교

- ArrayBlockingQueue나 LinkedBlockingQueue 에 비하면 BoundedBuffer는 성능 떨어짐
- 가장 큰 이유는 put과 take 모두 쓰레드 경쟁하기 때문
- 잘 튜닝된 알고리즘은 큐의 처음과 끝에 동시에 접근 할 수 있음(put과 take가 별개의 락을 가짐)

### 12.2.3 응답성 측정

- 앞에서는 처리량을 봄
- 단일작업을 처리하는데 걸리는 시간 측정이 중요할 수도 있다.
- 또 분산도 측정해야 한다. 평균은 오래걸리지만 균일한 시간을 보장하는게 중요할 수도.. ex) "100ms 내에 끝나는 작업의 비율이 몇 %인가", QOS
- 공정 세마포어, 불공정 세마포어 는 13.3절에서 다룸 PASS~

## 12.3 성능 측정의 함정 피하기

### 12.3.1 가비지 컬렉션

- GC는 언제 실행될지 알 수 없음
- 테스트 동안 GC가 일어날 수 있다는 점을 감안해야 함

### 12.3.2 동적 컴파일

- 최근 JVM들은 바이트코드 인터프리트와 동적 컴파일을 혼용해 사용함
- 처음에는 클래스의 바이트코드를 이너프리터해서 실행하고, 해당 메소드 호출이 잦아지면 그 때 기계어로 동적 컴파일함
- 역시 언제 실행될지 알 수 없음
- 컴파일 과정에서 CPU 상당부분 소모
- 컴파일된 후에는 인터프리트 속도는 의미 없음
- 어떤 경우에는 컴파일된 코드를 다시 디컴파일해서 인터프리트하기도 함
- 간단한 해결책은 긴 시간(최소 몇분 이상) 프로그램을 실행시켜 미리 컴파일을 시켜놓는 것(워밍업 스테이지)
- Hotspot JVM은 ``--XX:=PrintCompilation`` 옵션으로 동적 컴파일시 메세지 출력하게 할 수 있음

### 12.3.3 비현실적인 코드 경로 샘플링

- 런타임 컴파일러는 자기 맘대로 최적화함. 그래서 문제 발생할 수 있음

### 12.3.4 비현실적인 경쟁 수준

- 병렬 어플리케이션은 두 종류의 작업을 번갈아 실행하는 구조(프로듀서, 컨슈머)
- 예를 들어 N개 쓰레드가 공유하는 작업 큐에서 작업을 가져다 실행한다 했을 때
  - 각 작업이 CPU 중심이며 오래 걸리는 작업이라면 쓰레드 경쟁은 거의 발생하지 않음. 실행시간은 CPU 성능에 의존
  - 개별 작업이 아주 빠르게 끝나는 작업이라면 쓰레드 경쟁이 높아지고 동기화 방법에 따라 실행시간 좌우
- 병목이 어디인지 파악하는게 중요. 쓰레드 경쟁 vs CPU 작업

### 12.3.5 의미없는 코드 제거

- 컴파일러는 의미없어 보이는 코드를 그냥 제거해버린다.
- 정적 컴파일언어는 기계어 코드 보면 되지만(?) 동적 컴파일 언어는 이런 정보 얻기 힘들다.
- 핫스팟 JVM 클라이언트 모드보다 서버 모드가 실행 결과 좋음(최적화 능력이 좋기 때문에)
- 예를 들어 PutTakeTest에서 체크썸 합하는 부분도 하는일이 없기 떄문에 최적화될 가능성 존재
- 해당 체크썸을 출력해서 사용값이라는 걸 알려줄 수 있음.. 하지만 IO 부하 들어감
- 그럴 땐 아래 처럼 거의 실행되지 않을 코드를 넣어서 최적화를 막아보자

```java
if(foo.x.hashCode() == System.nanoTime())
    System.out.print(checkSum);
```

- 매번 정적인 값들을 넣고 실행하는 경우 컴파일러가 최적화할 수도 있음

## 12.4 보조적인 테스트 방법

### 12.4.1 코드 리뷰
  
- 테스트 보다 좋을 때가 있음....
- 주석 자세히 달면서 유지보수 비용 낮출 수 있음

### 12.4.2 정적 분석 도구

- 대표적인 기능들
  - 일관적이지 않은 동기화
  - Thread.run 호출
  - 해제되지 않는 락
  - 빈 Synchronized 블럭
  - 더블 체크 락(16장 참조)
  - 생성자에서 쓰레드 실행
  - 조건부 대기 오류
  - Lock과 Condition의 오용
  - 락 확보하고 대기상태 진입
  - 스핀 반복분

### 12.4.3 관점 지향 테스트 방법

- AOP 쓰자!

### 12.4.4 프로파일러 모니터링 도구

- 프로파일러 제품 써서 CPU나 쓰레드양 실시간 체크 하는 것도 좋은 방법


