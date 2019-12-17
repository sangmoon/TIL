## Item 3 Enforce the singleton property with a private constructor or an enum type

싱글톤은 오직 단 1번만 생성되는 객체이다. 상태가 없는 function(Item 24) 나 시스템 컴포넌트가 여기에 해당한다.
싱클톤은 Mock을 만들기 어렵기 때문에 테스트 하기에 어려운 점이 있다. 

보통 2가지 방식이 존재한다. 둘 다 생성자를 private으로 보호하고, 접근자를 public하게 만들어 유일한 객체에 접근하도록 허용한다.

```java
// 인스턴스를 final로 해 접근하는 방식
public class Elvis {
    public static final Elvis INSTANCE = new Elvis();
    private Elvis() {}
}
```

protected나 public 생성자가 없기 때문에 elvis 객체는 오직 1번만 클래스가 초기화 될 때 생성됨을 보장한다.

reflection을 통해 우회할 수 있는데, 이를 막기 위해선 생성자내에서 이미 생성 됐다면 Error를 throw하게 하면 된다.

2번째 방법은 INSTANCE도 private로 하고 접근메소드를 정의하는 것이다.

```java
public clas Elvis {
    private static final Elvis INSTANCE = new Elvis();
    private Elvis(){}
    public static Elvis getInstance() { return INSTANCE};
}
```

이 방식의 장점은 API가 해당 클래스가 싱글톤이란 것을 단순히 보여준다는 점이다.
2번째 방식이 팩토리 메소드를 사용해 좀 더 좋다. 첫번째 장점은 메소드로 추상화시킴으로써 추후 변경에 용이하다는 점이다.
두번째는 필요하다면 Generic singleton factory 로 사용할 수 있다는 점이다. 마지막으로는  method reference를 이용해 supplier를 사용할 수 
있다는 점이다. 예를 들어 Elvis::instance 는 Supplier\<Elivis\> 가 될 수 있다.
이런 것과 관계없으면 public field가 간편하다.

serializable(Chapter 12) 를 생각해보면 이것만으로는 충분하지 않다. 모든 필드를 transient로 바꾸고 readResolve method를 제공해야 한다.(Item 89) 그렇지 않으면 디시리얼라이즈할 때마다 새로운 객체가 만들어 질 것이다.

```java
private Object readResolve() {
    return INSTANCE;
}
```

3번째 방식은 Enum으로 싱글톤 클래스를 생성하는 것이다.
```java
public enum Elvis {
    INSTANCE;

}
```

이 방식은 public field와 유사하지만 더 간결하고, serialization에 대해서도 자유로우며 reflection에도 대응할 수 있다. 다만 상속을 해야한다면 이 방식은 사용할 수 없다.