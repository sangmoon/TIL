## Item 5 Prefer dependency injection to hardwiring resources

Static utility 클래스와 싱글톤은 리소스에 따라 달라져야하는 클래스에는 적합하지 않다.
static utility 와 싱글톤은 테스트와도 어울리지 않는다.
바람직한 방식은 생성자에 인자로써 건내주는 것이다. 이는 Dependency Injection의 한 형태이다.

```java
// static utility
public class SpellChecker {
    private static final Lexicon dictionary = ...;
    private SpellChecker(){}
}
```

```java
// singleton
public class SpellChecker {
    private final Lexicon dictionary = ...;
    private SpellChecker(){}
    public static INSTANCE = new SpellChecker(...);
}
```

```java
// DI gives flexibility and testability
public class SpellChecker {
    private final Lexicon dictionary = ...;
    public SpellChecker(Lexicon dictionary){
        this.dictionary = Objects.requireNonNull(dictionary);
    }
}
```

Depenency Injection은 Immutability(Item 17) 도 만족하기에 client가 같은 객체를 공유할 수 있다.
도한 생성자, static factories(Item 1), builder(Item 2) 에도 적용할 만하다.

이 패턴의 또 다른 사용 방식은 생성자에 ``resource factory`` 를 넘기는 것이다. java8의 ``Supplier<T>`` 를 사용하면 딱 좋다. 보통 API에서는 parameterized Type으로 bounded wild card(Item 31) 를 사용하는데, 이는 사용자가 해당 T type을 상속해서 사용할 수 있게 하기 위함이다.

```java
Mosaic create(Supplier<? extends Tile> tileFactory){}
```

Dependency Injection이 유연성과 테스트성을 엄청 좋게 하긴하는데, 프로젝트가 커지면 어수선해질 수가 있습니다. 이런 경우 DI framework를 사용하면 모두 제거할 수 있습니다. Dagger, Guice, Spring 같은 녀석이 Framework의 예시입니다.

요약하면 다른 resource나 클래스의 영향을 받는 녀석들은 Static Util이나 싱글톤으로 만들지 말고 생성자에 인자를 넘기는 방식으로 하는게 좋습니다.