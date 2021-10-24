## Item24: 멤버 클래스는 되도록 static 으로 만들어라

중첩 클래스는 다음 4개가 존재

- static member class
- member class
- anonymous class
- local class

### static Member Class

클래스 안에 선언되고, 바깥 클래스 private 멤버 접근 가능. 보통 public 도우미 클래스로 쓰임

### (Non-static) Member Class

바깥 클래스 인스턴스와 암묵적으로 연결되어 있음.
정규화된 this 로 참조 가능.

```java
class A {
    public class C {
        public void run() {
            System.out.println("Run C: " + A.this.a);
        }
    }
```

어댑터 패턴에서 자주 쓰임

### 왠만하면 static member class

멤버 클래스가 바깥 인스턴스에 접근하지 않는다면 무조건 static 을 붙여 static member 클래스가 되게 하자. 그냥 member class 는 외부 인스턴스로의 숨은 참조를 갖게 되고 이는 시간과 공간을 소비함. GC 가 안될 수도 있음
