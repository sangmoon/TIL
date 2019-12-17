## Item 1: Consider static factory methods instead of constructors

기본적으로 클라이언트는 어떤 객체의 퍼블릭 생성자를 얻을 수 있다. 하지만 ``static factory method``를 제공할 수도 있다.
```java
// Boolean Class 에서 사용하는 static factory method 예제
public static Boolean vaoueOf(boolean b) {
    return b ? Boolean.TRUE: Boolean.FALSE;
}
```
> ``static factory method``와 ``Factory Method Pattern``은 다르니 주의!

이제 클라이언트에게 퍼블릭 생성자를 주는 대신, 팩토리 메서드를 제공한다.

장점
1. 생성자와 다르게 이름이 있다. 

```java
BigInteger(int, int, Random); // 퍼블릭 생성자
BigInteger.probablePrime(int, int, Random) // 스태틱 팩토리 생성자
```

위와 같이 이름을 명시함으로 써 직관적으로 이해할 수 있다. 클래스는 생성자 이름을 하나 밖에 할 수 없다. 여러 생성자가 필요한 경우 static factory method를 써서 이름간 차이를 둘 수 있다.

2. 호출될 때마다 새로운 객체를 생성할 필요가 없다.

이 방식으로 immutable class(Item 17) 가 미리 만들어 놓은 객체를 사용하거나,  객체를 미리 캐시해두어서 여러번 소비할 수 있도록 한다.
```java
Boolean.valueOf(boolean);
```
위의 메소드는 절대 객체를 만들지 않는다. 디자인 패턴의 ``Flyweight Pattern``과 유사하다. 같은 객체가 자주 사용될 때 성능을 높이고 비용을 절감할 수 있다.
이렇게 불릴 때마다 같은 객체를 돌려주어 언제나 객체를 엄격히 제어 하는 클래스를  ``instance-controlled`` 되어있다고 한다. 이 instance-controlled 방식은 해당 클래스가 ``Singleton``(Item 3) 이거나 ``noninstantiable``(Item 4) 함을 보장한다. 또한 immutable value class (Item 17) 에서 동일한 2개의 객체가 존재하지 않음을 가능케 한다(a.equals(b) if and only if a == b). 이것이 Flyweight pattern의 기초이고 Enum type(Item 34) 가 이것을 제공한다.

3. 반환 타입의 어떤 자식 클래스도 반환할 수 있다.

API가 public 하지 않은 객체를 제공하게 할 수 있다. 이런 기술은 interface-based framework(Item 20) 을 만들 수 있다. 더 나아가 사용자가 구상 객체가 아닌 인터페이스로 작업하게 강제할 수 있다(Item 64)

4. 반환 타입으로 여러 객체를 섞어 쓸 수 있다.

위의 3번에서 확장된 의미로, 상황에 따라 interface를 구현한 여러 객체를 알맞게 제공할 수 있다.

5. 팩토리 메소드를 작성할 때 리턴 객체가 존재할 필요가 없다.

이런 장점은 JDBC같은 Service provider framework를 가능케 해준다. 실제 DB에 따른 구현체는 reflection(Item 65)을 통해 사용자가 설정한 내용에 따라 채워지게 된다.

단점

1. 퍼블릭 또는 프로텍티드 생성자가 없는 클래스는 상속될 수 없다.

팩토리 메소드 내에서 해당 생성자를 호출해 주어야 하기 때문에 불가능하다. 하지만 이 때문에 오히려 상속보다 composition을 사용케 하고(Item 18), Immutable type 도 강제하는 효과가 있다(Item 17).

2. 개발자가 찾기 힘들다.

팩토리 메서드는 찾기가 어렵다. 직접 문서를 뒤져야 하기 때문에. 그래서 다음과 같은 네이밍 컨벤션을 통해 API 를 만들도록 한다.

- **from** : 1개의 parameter를 받아 해당 객체를 반환한다.

    `` Date d = Date.from(instant);``

- **of** : 여러 parameter를 받아 해당하는 객체를 반환한다.

    `` Set<Rank> faceCards = EnumSet.of(JACK, QUEEN, KING);``

- **valueOf** : from이나 of의 장황한 버전

    `` BigInteger prime = BigInteger.valueOf(Intger.MAX_VALUE);``

- **instance** or **getInstance** : 매개변수로 설명되어있으나 동일한 값을 가질 수 없는 객체를 반환한다.

    `` StackWalker luke = Stackwalker.getInstance(options);``

- **create** or **newInstance** : 매번 새로운 객체를 반환함을 보장하는 것 말고는 instance와 같다.

    `` Object newArray = Array.newInstance(classObject, arrayLen);``

- **getType** : getInstance와 같으나 팩토리 메소드와 클래스가 다른 경우 사용한다. Type은 반환되는 클래스를 지칭한다.

    ``FileStore fs = Files.getFileStore(path);``

- **newType** : newInstance와 같으나 팩토리 메소드와 클래스가 다른 경우 사용한다. Type은 반환되는 클래스를 지칭한다.

    ``BufferedReaderbr = Files.newBufferedReader(path);``

- **type** : getType과 newType의 간편형

    ``List<Complaint> litany = Collections.list(legacyLitany);``

요약하자면, 스태틱 팩토리 메소드와 퍼블릭 생성자는 함께 쓰이며 상대적으로 장점이 있다.
대부분 스태틱 팩토리 메소드가 좋으므로, 단순하게 퍼블릭 생성자를 만들지 않도록 하자.