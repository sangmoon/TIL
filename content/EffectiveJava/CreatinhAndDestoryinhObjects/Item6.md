## Item 6 Avoid creating unnecessary objects

기능적으로 동일한 객체를 매번 생성하는 것 보다 객체 하나를 재사용하는게 적절한 상황이 있다.
재사용은 더 빠르고 읽기 쉽다. ``immutable(Item 17)`` 해야만 재사용 할 수 있다.

```java
String s = new String("bikini"); //제발 이렇게 사용하지 말 것!
```

위 처럼 하게 되면 매번 새로운 String 객체를 생성하게 된다.

```java
String s = "bikini";
```

이 버전은 같은 string literal은 매번 같은 객체를 사용함을 JVM이 보장한다.

특히 다른 객체보다 만들 때 자원을 더 소모하는 녀석들을 ``expensive object`` 라고 한다.
``String.matches(String pattern)`` 메소드는 Pattern 객체를 내부적으로 만들고, pattern은 정규식을 FSM으로 바꿔야 해서 굉장히 expensive 한 객체이다.

```java
static boolean isRomanNumeral(String s) {
    return s.matches("^(?=.)M*(C[MD]|D?C{0,3})"
            + "(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})$");
}
```

성능 개선을 위해 미리 Pattern 객체를 만들어 놓고 cache 해서 재사용할 수 있다.

```java
public class RomanNumerals {
    private static final pattern ROMAN = Pattern.compile("^(?=.)M*(C[MD]|D?C{0,3})"
            + "(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})$");

    static boolean isRomanNumeral(String s) {
        return ROMAN.matcher(s).matches();
    }
}
```

유사한 경우는 Map.keySet() 에서도 볼 수 있다. 항상 같은 객체를 반환해서, 한군데에서만 바꾸면 다른 곳들도 영향을 받는다.
또한 사례는 ``Autoboxing``을 들 수 있다. primitive 대신 boxed primitive를 쓰면 객체 생성을 해야해서 속도면에서 느려질 수 있다.

반면 private Object Pool을 구성하는 건 위험하다. 현대 JVM은 GC에 최적화되어있기 때문에 차라리 새로 생성하는게 나을 수 있다.
Item 50에 지금 이야기와는 반대로 "새로 만들어야 할 땐 재사용하지 말자" 라고 말한다. 이는 security와 버그 를 유발할 가능성을 막기 위함이다.
단순히 성능면에선 객체 생성을 할 필요가 없다.