## Item 15: Minimize the accessibility of classess and members

컴포넌트를 잘 설계하려면 중요한 것중 하나가 내부 데이터와 구현을 숨기는 것이다.
잘 설계된 컴포넌트는 상세 구현을 숨기고 API와 완벽히 분리해야 한다.
``Information hiding or encapsulation``으로 알려진 이 생각은 소프트웨어 디자인의 기본이다.

이를 통해 컴포넌트 간 결합도를 줄일 수 있다. 이를 통해 개발을 병렬적으로 할 수 있다.
또한 쉽게 디버깅할 수 있고 수정할 수 있어 유지의 부담도 줄여준다.

룰은 간단하다.각 클래스와 멤버들은 점근하기 힘들게 만들자. 다른 말로하면 access level을 최대한 낮추는 것이다.

top-level class와 interface에서는 package-private와 public만 가능하다.
package-private로 하면 그건 노출된 API 라기 보다 구현에 가깝다. 따라서 client 유무에 상관없이 수정 가능하다. 만약 packge-private class나 인터페이스가 한 클래스에서만 쓰인다면 private nested class 를 고려해봐라.

다음은 java에서 가능한 access level을 정리한 것이다.

- **private**: 멤버들은 오직 해당 클래스에서만 접근 가능하다
- **package-private**:  멤버는 해당 클래스가 선언되어 있는 패키지에서 접근 가능하다(접근자를 안쓰면되는데, interface는 기본 public 이라 예외)
- **protected**: 패키지 내와 상속받은 클래스에서만 접근 가능하다
- **public**: 어디서든 접근 가능하다

public class의 객체 필드는 거의 public일 일이 없다. 만약 해당 필드가 final이 아니고 mutable 객체라면 넌 제어권을 포기하는 것이다. 특히 해당 필드 변경에 대해 어떠한 동작도 할 수 없기 때문에 해당 클래스는 thread-safe하지 않게 된다. static 필드에 대해서도 같은 원리가 적용된다(final static 제외하고)

다음과 같은 코드는 보안의 구멍이 된다.
```java
public static final Thing[] VALUES = {...};
```

2가지 해결책이 있다. 하나는 private array를 immutable list로 만들어서 반환할 수 있다.
```java
private static final Thing[] PRIVATE_VALUES = {...};
public static final List<Thing> VALUES = Collections.unmodifiableList(Arrays.asList(PRIVATE_VALUES));
```

두번재는 array의 copy를 반환하는 public method를 둘 수 있다.
```java
private static final Thing[] PRIVATE_VALUES = {...};
public statif final Thing[] values() {
    return PRIAVTE_VALUES.clone();
}
```

> 나라면 첫번째 방법을 택하겠다. 호출마다 clone 하는 부하가 크다고 판단.
> 반환 타입도 array보다는 list가 좋다.

요약하면 public API는 최대한 줄이자. 접근성을 최대한 줄여라. public static final 필드가 immutable인지 꼭 확인해라.