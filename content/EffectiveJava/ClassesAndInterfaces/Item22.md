## Item22: 인터페이스는 타입을 정의하는 용도로만 사용하라

클래스가 인터페이스를 구현한다는 것은 자신의 인스턴스로 무엇을 할 수 있는지 클라이언트에게 알려주는 것.

Anti Pattern: 상수 인터페이스

```java
public interface PhysicalConstants {
    static final double AVOGADROS_NUMBER = 6.022_140_857e23;
}
```

**상수는 외부 인터페이스가 아니고 내부 구현이다.**

만약 클라이언트가 이런 상수들을 쓰고 있다면, 인터페이스에서 지우지도 못하게 된다.

이런 경우에는

- 클래스 자체에 추가한다(책에는 클래스나 인터페이스 자체에 추가한다... 는데 번역 오류인가..?)
- ENUM 을 사용한다(Item 34)
- 인스턴스화 못하는 유틸 클래스를 사용한다

```java
public class PhysicalConstants {
    private PhysicalConstants() {}

    public static final double AVOGADROS_NUMBER = 6.022_140_857e23;

}
```

예제: `MetricConstants`
