# atomic volatile synchronized

## Atomic

java 는 java.concurrent.atomic Class 가 있다. Lock이나 synchronized keyword가 없어도 병렬 수행의 안전성이 하드웨어에 의해 보장된다.
내부적으로 CAS(compare-and-swap) 을 활용한다. 한 method 인 incrementAndGet을 보면 다음과 같다.(JDK 7 기준)

```java
public final long incrementAndGet(){
    for(;;){
        long current = get();
        long next = current + 1;
        if (compareAndSet(current, next))
            reutrn next;
    }
}
```

get() 으로 현재 val을 가져오고, 2줄 아래 if 문에서 다시 memory의 값과 비교하여서 변동이 없으면 next value를 set하고,
변동이 있다면 다시 for문을 도는 형태이다. compareAndSet은 hardware 적으로 atomic을 보장한 native(assembly) 연산이다.
즉 lock을 사용하지 않고,다른 thread에 의한 변동이 없을 때까지 for 문을 도는 형태이다.

대표적으로 AtomicInteger, AtomicBoolean, AtomicLong, AtomicReference 가 있다.
JDK 8 에서는 LongAdder, LongAccumulator 등 이 추가되었다.

## volatile

volatile은 변수의 가시성(visibility)를 보장한다. 변수들은 Main memory 또는 CPU의 cache에 저장되는데,
멀티 쓰레딩 환경에서 해당 변수의 최신값이 다른 cpu에 있을 지, main memory에 있을지 보장할 수 없다.
따라서 volatile 키워드는 main memory에 값이 써지는 것을 보장합니다. 또 volatile 변수의 읽기 쓰기 연산은
JVM에 의해 재배치 되지 않는다.(????)

## synchronized

monitorlock 이나 intrinsic lock .. 재진입 가능한 락이다. 같은 락을 한 thread에서 여러번 얻을 수 있음.
