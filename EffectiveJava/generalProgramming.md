# 일반적인 프로그래밍 원칙들

## 규칙 53 리플렉션 대신 인터페이스를 이용하라

java.lang.reflect 를 활용하면 클래스 정보를 런타임에 가져 올 수 있다.

- Class 객체를 통해 생성자(Constructor), 메서드(Method), 필드(Field) 객체를 가져올 수 있다
-  멤버 이클래스의름, 필드 자료형, 메서드 시그니처 들을 알 수 있다.
- 객체를 생성할 수도 있고, 메서드를 호출할 수도 있으며 필드에 접근할 수도 있다.

단점도 많다.

- 컴파일 시점에서 자료형 검사함으로써 얻는 이점을 모두 포기해야 한다 (존재하지 않는, 접근 할 수 없는 method 호출하면 런타임 오류 발생)
- 리플렉션 코드는 보기 싫고 장황하다. 가독성 떨어진다
- 성능이 낮다 (저자 컴퓨터에서는 2 ~ 50 배 가량 느렸다)

### 일반적인 프로그램은 프로그램 실행 중 리플렉션을 통해 객체를 이용하려 하면 안 된다

리플렉션이 필요한 복잡한 프로그램 예시 (여기에 포함 안 되면 리플렉션 사용 ㄴㄴ)

- 클래스 브라우저
- 객체 검사도구
- 코드 분석 도구
- 해석적 내장형 시스템(interpretive embedded system) ???
- 스텁 컴파일러가 없는 원격 프로시저 호출(???)

### 리플렉션을 아주 제한적으로 사용하면 오버헤드는 피하면서 리플렉션의 장점을 누릴 수 있다.

- 객체 생성은 리플렉션으로, 참조는 인터페이스나 상위 클래스로

```java
// command line으로 받은 첫번째 인자의 클래스를 이용해 Set<String> 을 만드는 프로그램. 나머지 인자는 해당 Set에 집어 넣음
// 생성은 리플렉션, 참조와 사용은 인터페이스

public static void main(String[] args) {
    Class<? extends Set<String>> cl = null;
    try {
        cl = (Class<? extends Set<String>>) Class.forName(args[0]); // unchecked cast
    } catch (ClassNotFoundException e) {
        System.err.println("Class not found.");
        System.exit(1);
    }

    // get constructor
    Constructor<? extends Set<String>> cons = null;
    try {
        cons = cl.getDeclaredConstructor();
    } catch (NoSuchMethodException e) {
        System.err.println("No parameterless constructor.");
        System.exit(1);
    }

    // Instantiate the set
    Set<String> s = null;  // Set으로 참조

    try {
        // cl.newInstance() 를 안쓰고 굳이 생성자 호출하는 이유는?
        s = cons.newInstance();
    } catch (IllegalAccessException e) {
        System.err.println("Class not accessible.");
        System.exit(1);
    } catch (InstantiationException e) {
        System.err.println("Class not instantiable");
        System.exit(1);
    } catch (InvocationTargetException e) {
        System.err.println("Constructor threw " + e.getCause());
        System.exit(1);
    } catch (ClassCastException e) {
        System.err.println("Class doesn't implements Set");
        System.exit(1);
    }

    s.addAll(Arrays.asList(args).subList(1, args.length));
    System.out.println(s);
    /// etc
}
```

- 어떤 클래스가 Set을 구현했는지 검증하는 검사도구로 사용 가능 (generic set tester)
- 일반적 집합 성능 분석 도구 (generic performance analysis tool) 로도 사용 가능

2개의 단점 존재

- 6 가지 런타임 오류 발생. 리플렉션 안 썼으면 컴파일 시점에서 다 감지 가능
- 클래스 객체 생성 위해 코드 엄청 많이 씀. 생성자 호출로 했으면 한 줄로 가능

하지만 객체 생성 부분에서만 나타나는 문제로 일단 객체 생성 후에는 Set<>으로 참조하기 때문에 아무 영향 없다.

리플렉션은 실행 시점에 존재하지 않는 클래스나 메서드, 필드에 대한 종속성 관리에 적합. <br> 
어떤 패키지의 버전이 여러가지 이고, 그 전부를 지원하는 또 다른 패키지를 구현해야 할 때 <br>
모든 버전을 지원하는 최소한의 환경만 컴파일하고, 새로운 클래스나 메서드는 리플렉션을 통해 접근

### 요약

- 리플렉션은 특정 종류의 복잡한 시스템 프로그래밍에 필요한 강력한 도구
- 단점 매우 많음
- 사용하고 싶다면 객체를 만들 때만 사용하고 참조할 때는 컴파일 시에 알고 있는 인터페이스나 상위 클래스만 사용할 것

## 규칙 54 네이티브 메서드는 신중히 사용하라

JNI(java native interface) 는 C나 C++로 작성된 native method 호출하는 데 이용되는 기능.

3가지 용도로 쓰임

1. 레지스트리나 파일락 같은 특정 플랫폼에 고유한 기능을 이용
2. 이미 구현되있는 라이브러리를 이용할 수 있음
3. 성능 상 중요한 부분을 네이티브 언어에 맡길 수 있음

### 네이티브 메서드를 통해 성능을 개선하는 것을 추천 안함

- 현재 JVM은 네이티브에 필적하는 성능을 낸다.
- 네이티브 메서드는 심각한 문제 1. 안전하지 않다. memory corruption error 발생 가능
- 플랫폼 종속적
- 디버깅 어려움
- 네이티브와 jvm 넘나드는 코드 때문에 오히려 성능 떨어질 수 있음
- 이해하기 어렵고 작성하기 난감한 접착 코드 작성해야 함

### 요약

- 네이티브 메서드 쓰지 마라
- 퍼포먼스 향상 될 일 거의 없다
- 굳이 써야 한다면 네이티브 코드를 최소화 하고 전체를 다 테스트 해야한다. 작은 버그가 어플리케이션을 다 망침.

## 규칙 55 신중하게 최적화하라

최적화 관련 명언 3개가 있다.

> 맹목적인 어리석음을 비롯한 다른 어떤 이유보다도, 효율성이라는 이름으로 저질러지는 죄악이 더 많다. - 윌리엄 울프

> 작은 효율성에 대해서는, 말하자면 97% 정도에 대해서는, 잊어버려라. 섣부른 최적화는 모든 악의 근원이다. - 도널드 커누스

> 최적화 할 때는 아래 두 규칙을 따르라. <br>
> 규칙 1: 하지 마라 <br>
> 규칙 2: (전문가들만 따를 것) 아직은 하지 마라 - 완벽히 명료한, 최적화되지 않은 해답을 얻을 때까지는 - M.A. 잭슨 M

### 중간 요약

``최적화 하지마라``

- 성능 때문에 구조적인 원칙을 희생하지 마라. 빠른 프로그램이 아닌, 좋은 프로그램을 만드려 노력하라. 좋은 프로그램이라면 좋은 구조를 갖추었기 때문에 최적화의 여지도 충분.
 

- 설계 할 때는 성능을 제약할 가능성이 있는 결정들은 피하라. 가장 까다로운 부분은 모듈간의 상호작용이나 외부와의 상호작용을 명시하는 부분, 즉 ``API``, ``통신 프로토콜``, ``지속성 데이터 형식`` 등 이다. 이런 부분은 성능 문제가 발견된 후 수정이 어렵다.

- API를 설계할 때 내리는 결정들이 성능에 어떤 영향을 끼칠지 생각하라. 
  - public 자료형을 변경 가능하게 만들면 방어적 복사를 많이 해야한다. 
  - composition이 적절할 public class에 상속을 적용하면 해당 클래스는 영원히 상위 클래스에 묶이게 되서 하위 클래스 성능에 제약 가해질 수 있다. 
  - 인터페이스가 적당한 API 에 구현자료형 사용하면 해당 API가 특정 구현에 종속되어 나중에 더 빠른 구현이 나와도 개선할 수 없다.

- 성능을 위해 API를 급진적으로 바꾸는 건 바람직하지 않다.
  - 너무 많이 변경된 API를 지원하는건 개발자가 너무 힘들다.

- 최적화를 시도할 때마다 전후 성능을 측정하고 비교하라
  - JVM 마다, 릴리스 마다, 프로세서 마다 차이가 크다.

### 요약

- 빠른 프로그램 만들고자 애쓰지 마라
- 대신 좋은 프로그램 짜기 위해 노력하면 성능은 따라 온다
- 시스템 설계할 때 API, 통신 프로토콜, 지속성 데이터 형식을 성계할 때 성능 문제를 따져봐라.
- 성능 문제 있을 때 처음 해야 할건 구현에 쓰인 알고리즘 검토. 이게 잘못되면 저수준 최적화 의미없음.

## 규칙 56 일반적으로 통용되는 작명 관습을 따르라

1. 철자에 관한 것

- package
  - 마침표를 구분자로 하는 계층적 이름
  - 소문자 사용
  - 숫자 거의 사용 X
  - 앞에 2개는 조직의 인터넷 도메인을 따온다 (``com.tmax``)
  - 나머지 부분은 어떤 패키지 인지 설명하는 하나이상의 컴포넌트로 구성
  - 의미가 확실한 약어면 좋음(utilities 보다 util)

- enum, class, interface 
  - 첫 글자는 대문자
  - 널리 쓰이는 약어(max, min)을 제외하면 약어는 피한다

- 메서드, 필드
  - 첫 글자는 소문자
  - 상수 필드의 경우 모두 대문자로 쓰며  ``_``   로 구분한다.

- 지역 변수
  - 메서드, 필드와 같은 규칙
  - 약어를 많이 사용

- 자료형 인자
  - 보통 하나의 대문자
  - 임의 자료형 T
  - 컬렉션의 요소 자료형 E
  - 맵의 키와 값은 K, V
  - 예외인 경우 X
  - 임의 자료형의 연속은 T, U, V or T1, T2, T3

|식별자 자료형 | 예제| 
|----|       ----|
|패키지 | com.tmax.proobject|
|클래스나 인터페이스 |ChannelEventHandler, BodyParser|
|메서드나 필드 | remove, ensureCapacity |
|상수 필드 | MIN_VALUE, NEGETIVE_INFINITY|
|지역 변수 | i, xref, houseNumber|
|자료형 인자 | T, E, K, V, X, T1, T2|
 
 2. 문법에 관한 것

철자 관습보다 가변적이고 논쟁 여지가 많다.

- 패키지는 문법 관습 없음
- 클래스나 enum 은 단수형 명자나 명사구 붙는다 (Timer, BuffedWriter, ChessPiece)
- 인터페이스도 클래스와 비슷하며 able이나 ible 같은 형용사격 어미가 붙기도 한다 (Collection, Comparator, Runnable, Iterable, Accessible)
- 어노테이션은 쓰임새가 너무 다양해 지배적인 규칙이 없다. 명사, 동사, 전치사, 형용사 다 쓰인다 (BindingAnnotation, Inject, ImplementedBy, Singleton)
- 어떤 동작을 수행하는 메서드는 동사나 동사구를 이름으로 한다(append, add)
- boolean 값을 반환하는 method는 보통 is, 가끔 has 로 시작한다 (isDigit, isEmpty, hasSiblings)
- boolean 이외의 속성을 반환하는 메서드는 보통 명사나 명사구, get으로 시작한다 (size, hashCode, getTime)
- bean 클래스에 속한 메서드이름은 반드시 get으로 시작해야 한다. 속성을 설정하는 건 set으로 시작해야 한다.
- 객체의 자료형을 변환하는 메서드, 다른 자료형의 ``독립적 객체``를 반환하는 메서드는 보통 toType 형태를 붙인다 (toString, toArray)
- 인자로 전달받은 객체와 다른 자료형의 ``View 객체``를 반환하는 메서드는 asType 형태의 이름을 붙인다 (asList)
- 호출 객체와 동일한 기본 자료형 값을 반환하는 경우 typeValue 로 붙인다 (intValue)
- 정적 팩토리 메서드는 valueOf, of, getInstance, newInstance, getType, newType 등을 붙인다
- 필드는 특별한 관습 없고 별로 중요하지 않다 (잘 설계된 API는 외부로 필드를 거의 공개 안하기 때문)
- boolean field는 메서드와 같은 이름을 붙이거나 is를 생략한다 (initialized, composite)
- 다른 필드는 보통 명사나 명사구를 쓴다 (height, digits, bodyStyle)
- 지역 변수는 더 중요하지 않다.

### 요약

- 표준 작명 관습을 내면화 시켜서 제2의 천성인 것 처럼 사용하자
- 철자 관습은 직관적이며 모호한 부분이 없다
- 문법 관습은 좀 더 복잡하고 느슨하다