## Item 15: Minimize the accessibility of classess and members

잘 설계된 컴포넌트는 상세 구현을 숨기고 API와 완벽히 분리해야 한다.
`Information hiding` or `encapsulation` 으로 알려진 이 생각은 소프트웨어 디자인의 기본이다.

### 캡슐화의 장점

- 병렬 개발을 통한 개발 속도 증가
- 독립적인 컴포넌트 분리로 인한 관리 비용 감소
- 성능 최적화에 도움
- 재사용성 증가
- 제작 난이도 감소

룰은 간단하다. **모든 클래스와 멤버의 접근성을 가능한 한 좁혀야 한다.**

### java에서 가능한 access level

- **private**: 멤버들은 오직 해당 클래스에서만 접근 가능하다
- **package-private**: 멤버는 해당 클래스가 선언되어 있는 패키지에서 접근 가능하다(접근자를 안쓰면 되는데, interface는 기본 public 이라 예외)
- **protected**: 패키지 내와 상속받은 클래스에서만 접근 가능하다
- **public**: 어디서든 접근 가능하다

| total           | In the class | Same package | Extended class | Another area |
| --------------- | ------------ | ------------ | -------------- | ------------ |
| private         | O            | X            | X              | X            |
| package-private | O            | O            | X              | X            |
| protected       | O            | O            | O              | X            |
| public          | O            | O            | O              | O            |

**public class의 객체 필드는 public 이어선 안 된다.**

### pubic array 의 허점

```java
public static final Thing[] VALUES = {...};
// client 가 배열 필드 참조를 받아서 수정할 수 있다.
```

#### 해결책 1. immutable list

```java
private static final Thing[] PRIVATE_VALUES = {...};
public static final List<Thing> VALUES = Collections.unmodifiableList(Arrays.asList(PRIVATE_VALUES));
```

#### 해결책 2. array copy

```java
private static final Thing[] PRIVATE_VALUES = {...};
public static final Thing[] values() {
    return PRIAVTE_VALUES.clone();
}
```

### Java9 부터 나온 Module system

`class` 모음은 `packages`, `packages` 의 모음이 `module`

외부에 노출할 패키지는 명시적으로 `export` 해주어야 함.
외부 패키지에서 참조할 패키지는 명시적으로 `require` 해주어야 함. (java script 의 모듈화 방식과 유사하다..?)

JDK 에서는 많이 쓰이고 있는데 실제 어플리케이션에는 아직 시기상조라고...

### 요약

> API 설계 시 public 은 최소화 하자. <br>
> public class 는 public static final 외 에는 public 필드를 가져서는 안 된다. <br>
> public static final 필드도 immutable 인지 확인하자.
