# Thread Excecutor

Executor는 thread 생성 및 관리를 해주는 클래스이다. thread 를 직접 생성 하고 제어 하는 데에서 나올 수 있는
복잡성을 줄여준다. ``Executors`` 라는 Factory class 를 활용하거나 또는 직접 생성해줄 수도 있다.

```java
ExecutorService executor = Executors.newFixedThreadPool(10); // by Executors

ExecutorService executor = new ThreadPoolExecutor(1, 1, 0L, TimeUnit.MILLISECONDS, 
                                new LinkedBlockingQueue<Runnable>()); // directly 
```

ExecutorService 는 interface 이다.

- newFixedThreadPool : 고정된 갯수의 thread를 유지하는 executor이다.
- newSingleThreadExecutor : 1개의 thread만 유지하는 executor이다.
- newCachedThreadPool : thread 를 적당한 시간 동안만 cache 하는 executor이다.
- newScheduledThreadPool : 일정 기간이나, 주기적으로 작업하는 thread pool 을 생성한다.
- newSingleThreadScheduledExecutor :  thread가 1개인 scheduledThreadPool 이다.

## Runnable

ExecutorService 에서 thread 들이 할 일을 queue에 넣는다. 이 일을 Runnable 또는 Callable interface 로 만들 수 있다.

```java
Runnable runnableTask = () -> {
    try {
        TimeUnit.MILLISECONDS.sleep(1000);
    } catch (InterruptedExecption e) {
        e.printStackTrace();
    }
};

Callable<String> callableTask = () -> {
    TimeUnit.MILLISECONDS.sleep(1000);
    return "Task's execution";
}
```

ExecutorService의 API를 살펴보면

- execute()
- submit()
- invokeAny()
- invokeAll()

등이 있다. ``execute`` 는 void 타입으로, task가 실행 중인지 끝났는지 확인 할 방법이 없다.
``submit`` 은 Callable 이나 Runnable task 를 받아서 Future type을 return 한다. 이 Future을 통해 진행 상황을 알 수 있다.
``invokeAny`` 와 ``invokeAll`` 의 경우 ``Collection<Callable>`` 를 input으로 받아서 any의 경우 아무거나 1개의 return 값을 return 해주고
all은 모든 callable의 future를 return 해준다.

## Shutdown Executor

Executorservice는 기본적으로 GC되지 않는다. 그래서 필요할 때는 명시적으로 destory 해야 한다.
``shutdown`` 과 ``shutdownNow`` 가 있는데, 둘 다 바로 thread가 꺼짐을 보장하지는 않는다.
따라서 다음과 같은 방법을 추천한다.

```java
executorService.shutdown();
try {
    if (!executorService.awaitTermination(800, TimeUnit.MILLISECONDS)) {
        executorService.shutdownNow();
    }
} catch (InterruptedException e) {
    executorService.shutdownNow();
}
```

## Future interface

