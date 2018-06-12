# Thread

기본적으로 ``main`` thread 존재(java launcher에 의해 실행되는 사용자 thread. public static void miain(String[]) 실행)

시작
creator thread에서 start() 호출하면 새로 thread 만들어서 해당 thread에서 run() 실행

종료
run() method가 종료되면 thread가 종료

다른 방식으로 thread를 제어하는 method는 모두 금지

- stop()
- destroy()
- suspend()
- resume()

why?
쓰레드가 임의의 lock을 잡은 상태에서 stop하거나 suspend 했을 때 답이 없다.
JVM이 오버헤드가 너무 커진다.

남은 방법은  interrupt를 해당 thread에 notification 하는 것 뿐.
사용자 코드에서 flag를 활용하여 직접 종료/일시중지/재개 등을 구현해야 한다.

java interrupt는 Object.wait(), Thread.sleep(), Thread.join() 을 깨울 수 있다.
InterruptedException이 발생하면서 해당 thread의 interrupted flag가 ``clear`` 된다.
(thread는 내부적으로 interrupted 당했는지 알고 있다) 다른 blocking operation 진행 중이었다면
interrupted flag가 ``set`` 된다. interruptible channel은 interrupt 되면 바로 종료하면서
ClosedByInterruptedException을 리턴하지만, 그렇지 않으면 계속 block 되어 있다.(flag만 ``set`` 되고)

> 주의사항 : thread 에서 loop를 돌면 매번 flag를 체크해서 interrupted를 체크해야 한다.

interrupt 상태 체크

- public static boolean interrupted(); 현재 쓰레드의 interrupted flag를 알려주고 reset
- public boolean isInterrupted(); Thread 객체가 가리키는 thread의 현재 interrupted flag를 알려줌

Thread의 상태

- NEW (start 호출 전)
- RUNNABLE (run 실행 상태)
- BLOCKED (synchronized lock을 기다리는 상태)
- WAITING (Object.join, Thread.join, LockSupport.park 를 실행 중인 상태)
- TIMED_WAITING (time 인자를 줘서 wait, join, park를 실행하였거나 thread.sleep 인 상태)
- TERMINATED (thread가 종료한 상태)

ContextClassLoader
thread 별로 특별한 의미를 가진 classLoader를 지정함
쓰레드를 만들 때 creator thread로 부터 copy(상속) 받음
main thread의 context classloader는 null
thread pool 을 고려한 api

Lock and Conditions
monitor 객체: lock &n unlock의 대상
wait으로 기다리고, notify로 wait하고 있는 놈 중 하나를 깨운다.

Spurious wakeup
notify가 없어도 wait이 깨어날 수 있다.

1. interrupt 발생한 경우
2. wait_timeout 발생시
3. spurious wakeup

항상 condition check를 해야 한다.

