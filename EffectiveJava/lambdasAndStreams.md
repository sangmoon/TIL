# Chapter 7 Lambdas and Streams

자바8에 함수형 인터페이스, 람다 메서드 참조 등이 추가됨. <br>
Stream API 또한 추가되어서 이러한 언어변화에 맞는 데이터 요소 처리를 돕는다.

## 규칙 42 익명 클래스 보다 람다를 쓰자
오래전부터 1개의 추상 메소드를 갖는 인터페이스는 function type 으로 쓰여옴. <br>
이 인터페이스를 구현한 ``function objects`` 는 함수를 나타냄. <br>
JDK1.1 부터 함수 객체를 만드는 가장 대표적인 수단은 익명 클래스였음 <br>
```java
// 글자 길이로 정렬하는 함수 객체
Collections.sort(words, new Comparator<String>() {
    public int compare(String s1, String s2) {
        return Integer.compare(s1.length(), s2.length());
    }
})
```

```java
// java8 부터
Collections.sort(words,
    (s1,s 2) -> Integer.compare(s1.length(), s2.length()));
```

### 람다의 특징
- lambda의 타입(Comparator<String>)
- parameter (String s1, String s2)
- return value (int)
코드에 표시 안됨. 컴파일러가 컨텍스트를 보고 다 추론함. 특정 경우는 컴파일러가 추론 못하고 프로그래머가 타입을 지정해야 할 수도 있음. <br>
추론 규칙을 자세히 이해하기는 어려운데, 일단 가능한 한 다 생략해버려도 된다.

컴파일러가 추론할 때 Generic을 많이 이용하기 때문에 잘 쓰는게 좋다. <br>
위 예제에서 words 가 List<String> 아니라 List 로 선언 되었으면 컴파일 되지 않는다.

Comparator 가 제공하는 snippet 메서드를 이용하면 더 짧게 할 수 있다.
```java
Collections.sort(words, comparingInt(String::length));
```

java8 부터 List에 추가된 메소드를 이용하면 더 줄 일 수 있다.
```java
words.sort(comparingInt(String::length));
```

앞서 enum type 에 나왔던 Operation을 람다로 리팩토링하면 다음과 같다

```java
// lambdas 적용 전
public enum Operation {
    PLUS("+") {
        public double apply(double x, double y) {return x + y;}
    },
    MINUS("-") {
        public double apply(double x, double y) {return x - y;}
    },
    TIMES("*") {
        public double apply(double x, double y) {return x * y;}
    },
    DIVIDE("/") {
        public double apply(double x, double y) {return x / y;}
    };

    private final String symbol;
    Operation(STring sysmbol) {this.symbol = symbol;}
    public abstract double apply(double x, double y);
}
```

```java
public enum Operation {
    PLUS("+", (x, y) -> x + y),
    MINUS("-", (x, y) -> x - y),
    TIMES("*", (x, y) -> x * y),
    DIVIDE("/", (x, y) -> x / y);

    private final String symbol;
    private final DoubleBinaryOperator op;

    Operation(String symbol, DoubleBinaryOperator op) {
        this.symbol = symbol;
        this.op = op;
    }

    public double apply(double x, double y) {
        return op.applyAsDouble(x, y);
    }
}
```
``DoubleBinaryOperator`` 는 java.util.function에 정의된 함수형 인터페이스 중 하나. 2개의 double을 인자로 받아서 하나의 double을 반환한다.

### 주의할 점
람다는 이름과 설명이 없기 때문에 코드가 그 내용을 설명해주지 못하거나 또는 두 세 줄이 넘어가면 안쓰는 게 좋다. <br>
한 줄이 이상적이고 최대 3줄이 허용범위임.

### 익명 클래스가 람다보다 좋은 점
- 객체를 생성할 수 있다??(lambda는 객체가 아닌가?)
- 여러 추상 메소드가 있는 경우에도 쓸 수 있다
- 람다는 자기 자신의 참조를 얻을 수 없다 (lambda 에서 this 는 감싸고 있는 instance 를 의미. 익명 클래스는 클래스 자기 자신을 의미)

- 람다와 익명클래스 둘 다 직렬화 역직렬화 믿을 수 없음. (JVM 따라 달라서 인 듯)
- 가급적 람다와 익명 클래스 직렬화 하지 말 것. 
- 정말 하고 싶으면 private static nested class의 객체를 이용할 것 (Comparator 처럼)

### 요약
- 람다는 함수 객체를 이용하는 최고의 방법
- 진짜 클래스 객체가 필요하지 않으면 익명 클래스보단 람다 쓰자
- 람다 쓰면 함수형 프로그래밍 입문 하는 거다 어서 쓰자

## 규칙 43 람다보다 메소드 참조를 쓰자
람다의 장점은 간결함임. 자바는 람다보다 더 간견한 방식을 추가함: ``method reference``




