## Item 19: 상속을 고려해 설계하고 문서화해라. 그러지 않았다면 상속을 금지하라

**상속용 클래스는 재정의할 수 있는 메서드들을 내부적으로 어덯게 이용하는지 문서로 남겨야 한다**.
클래스를 안전하게 상속할 수 있도록 하려면 내부 구현 방식을 설명해야 한다.

**상속용 클래스를 시험하는 방법은 직접 하위 클래스를 만들어보는 것이 '유일'하다**.

### 상속용 클래스의 생성자는 재정의 가능 메서드를 호출해서는 안 된다

```java
// 상속 시 문제 발생 가능한 클래스
public class Super {
    public Super() {
        overrideMe();
    }

    public void overrideMe() {}
}
```

```java
public final class Sub extendss Super {
    private final Instant instant;
    Sub() {
        instant = Instant.now();
    }

    @Override pubic void overrideMe() {
        System.out.println(instant);
}
```

> private, final, static method 는 재정의가 불가능하니 안심하고 호출해도 된다.

### Cloneable, Serializable 을 구현한 클래스는 상속하기 어렵다.

- clone, readObject 모두 재정의 가능 메소드를 호출해서는 안 된다.
- Serializable 구현한 상속용 클래스가 readResolve 나 writeReplace 를 구현했다면 이 메소드는 private 가 아니라 protected 로 구현되어야 한다.

### 상속용으로 설계하지 않은 클래스는 상속을 금지

- class 를 final 로 선언
- 모든 생성자를 private 나 packge-private 로 선언하고 public 정적 팩토리를 만들어주는 방법

### 요약

> 상속용 클래스는 자기사용 패턴을 모두 문서로 남겨두어야 한다. <br>
> 효율적으로 하위 클래스를 만들 수 있도록 일부 메소드는 protected 로 제공해야 할 수도 있다. <br>
> 명확한 이유가 없다면 상속을 금지해야 한다.

### 예제

`OrderStateTransitionException`
