# Lambda Expression

Java 8 부터 람다 표현식을 지원한다.
핵심은 지울 수 있는 건 다 지우고 컴파일러에게 맡기자! 이다.

```java
interface Flyable
    void fly()

class Bird implements Flyable{
    @Override
    public void fly(){
        System.out.println("I believe I can fly");
    }
}

Flyable fly = new Flyable(){
    @Override
    public void fly(){
        System.out.println("I believe I can fly");
    }
}
```

Flyable 이라는 interface를 구현한다고 해보자. 이를 구현한 ``Bird``라는 클래스를 만드는게 일반 방법이고,
재사용성이 없다면 아래 방식으로 익명 inner class를 활용할 수도 있다. 그런데 단순히 method 하나 사용하려고
객체를 새로 생성하고 Override 해주는 게 귀찮게 느껴진다. 위의 코드는 다음과 같이 수정할 수 있다.

```java
Flyable fly = () -> System.out.println("I believe I can fly");
```

- 이미 변수 선언에서 Type을 알고 있으므로 new 를 할 필요가 없다.
- 구현하려는 method가 1개 이므로 이름 없어도 된다.
- method를 알고 있으니까 parameter 도 간소화 할 수 있다.

## FunctionalInterface

java는 method를 1급객체로 취급하지 않기 때문에 다른 언어들 처럼 바로 lambda를 사용하지는 못한다.
구현해야할 method가 1개인 functional interface를 사용하여 hint를 주게 된다.

```java
@FunctionalInterface
interface Flyable{
    void fly()
}
```

이는 인터페이스에 method가 1개 가 아니면 컴파일 에러를 발생시켜 오류를 줄여준다.
또한 실제 class를 만드는 것이 아니기 때문에 메모리 부담이 줄어든다(익명 inner class의 경우 class를 만드는 것이기 때문에 메모리 부담 가중)
그럼 java built-in functionalInterface를 찾아보자.

1. ``Runnable``

thread 생성할 때 보통 사용하는 interface 이다.
void 타입의 parameter 또한 없다.
2. ``Supplier<T>``

인자는 받지 않고, T type을 리턴한다. 순수함수는 input parameter에만 영향을 받으므로
항상 같은 값을 리턴한다.
3. ``Consumer<T>``

void type 이며 T를 인풋 parameter로 받는다.
4. ``Function<T, R>``

하나의 인자와 리턴타입을 갖는다.
5. ``Predicate<T>``

하나의 인자를 받고 리턴 타입은 boolean으로 고정이다.
6. ``UnaryOperator<T>``

인자와 리턴 타입이 같다.
7. ``BinaryOperator<T>``

동일한 타입의 인자 2개를 받아서 역시 동일한 타입으로 리턴한다.
8. ``BiPredicate<T, U>``

인자 2개를 받아서 boolean으로 리턴한다.
9. ``BiConsumer<T, U>``

인자 2개를 받는 void 타입
10. ``BiFunction<T, U, R>``

인자 2개를 받고 리턴한다.
11. ``Comparator<T>``

자바 전통적인 인터페이스로 객체간 비교 때 사용된다.
12. ``Callable<T>``

runnable에 대응되는 interface로 Future 객체를 사용할 때 사용된다.

[참조사이트](http://multifrontgarden.tistory.com/125?category=471239)

## clousure

자유 변수! unbound variable, free variable

## currying

argument가 1개인 anonymous function이 multi arg를 지원하는가

## Mixin

다른 class의 method를 가지고 있는 class. 상속 외에 다른 방식으로 reuse 함. 
이를 java 에서 받기 위해 default 생김.

## Default Method

provides a default impl for any class that implements the interface without overriding the method.
기존 interface 수정하지 않고 새로운 기능성 구현. 다중상속처럼 구현됨
다만 state(멤버 변수) 를 선언할 수 없고, 오로지 동작(method) 만 가능

## Java 8 lambda

- functional interface
- default method
- streams
- invokeDynamic
- java.util.Spliterator