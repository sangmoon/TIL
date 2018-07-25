# Generics

## Item 26: Don't use raw types

## Item 27: Eliminate unchecked warnings

## Item 28: Prefer lists to arrays

## Item 29: Favor generic types

## Item 30: Favor generic methods

클래스가 generic 일 수 있는 것 처럼 method 도 generic 할 수 있다.
예를 들어 collections 에 있는 알고리즘 관련 method(sort, binarysearch) 는 generic 하다.

```java
// use raw types - unacceptable!
//@SuppressWarnings("unchecked")
public static Set union(Set s1, Set s2) {
    // Warning! HashSet(Collection<? extends E>)
    Set result = new HashSet(s1);
    // Warning! result.addAll(Collections<? extends E>)
    result.addAll(s2);
    return result;
}
```

``type parameter list`` 는 접근 제어자와 return type 사이에 위치 합니다.

```java
public static <T> Set<T> union(Set<T> s1, Set<T> s2) {
    Set<T> result = new HashSet(s1);
    result.addAll(s2);
    return result;
}
```

아래와 같은 프로그램은 cast 없고, error 나 warning 없이 컴파일 된다.

```java
    public static void main(String[] args){
        Set<String> guys = new HashSet<>(Arrays.asList("Tom", "Dean", "Harry"));
        Set<String> stooges = new HashSet<>(Arrays.asList("Larry", "Moe", "Curly"));
        Set<String> aflCio = union(guys, stooges);
        System.out.println(aflCio);
    }
}
```
위의 union의 단점은 input set 2개와 output이 정확히 같은 타입이라는 것(``T``)
``bounded wildcard type`` 을 사용해서 좀 더 유연하게 구연 가능 뒤에 나옴

### type parameter에 대한 convention

- ``T`` (임의의 타입)
- ``E`` (collection의 element)
- ``K,V`` (key, value)
- ``X`` (exception)
- ``R`` (function의 return type)
- ``T, U, V`` || ``T1, T2, T3`` (연속된 임의의 타입)

### 제너릭 싱클톤 패턴

변경이 불가능하지만 많은 자료형에 적용 가능한 객체를 만들어야 할 때가 있다.
모든 필요한 형인자화 과정에서 동일 객체를 활용할 수 있는데, 그러려면 우선 필요한 형인자화 과정 마다 같은 객체를 나눠주는 정적 팩토리 메서드를 작성해야 한다.

항등 함수는 stateless 하므로 새 함수를 만드는 것은 낭비

```java
private static UnaryOperator<Object> IDENTITY_FN = t -> t;

//IDENTITY_FN 은 stateless 객체이고 형인자는 unbounded 이므로 모든 자료형이 같은 객체를 공유해도 된다.
@SuppressWarnings("unchecked")
public static <T> UnaryOperator<T> identityFunction() {
    return (UnaryOperator<T>) IDENTITY_FN;
}
```

``UnaryOperator<Object>`` 를  ``UnaryOperator<T>`` 로 캐스팅 하는 부분에서 warning 발생하지만
항등함수는 특별히 인자를 수정없이 반환하므로 형 안정성이 보장

```java
public static void main(String[] args) {
    String [] strings = {"jute", "hemp", "nylon"};
    UnaryOperator<String> sameString = identityFunction();
    for(String s: strings){
        System.out.println(sameString.apply(s));
    }

    Number[] numbers = {1, 2.0, 3l};
    UnaryOperator<Number> sameNumber = identityFunction();
    for(Number n: numbers) {
        System.out.println(sameNumber.apply(n));
    }
}
```

### 재귀적 자료형 한정(rescursive type bound)

형인자가 포함된 표현식으로 형인자를 한정할 수 있다.
``Comparable`` 인터페이스와 흔히 쓰인다

```java
public interface Comparable<T> {
    int compareTo(T o);
}
```

정렬, 탐색, 최대 최소값 method 들은 Comparable을 구현한 원소들의 컬랙션을 인자로 받는다.
이러한 작업이 가능하려면 컬렉션 내 원소들이 서로 비교 가능해야 한다.
아래 표현은 "자기 자신과 비교가능한 모든 자료형 T" 를 나타낸다.
> E 는 ``compareTo(E o)`` 를 구현했음을 보장한다.
```java
public static <E extends Comparable<E>> E max(Collection<E> c){...}
```

```java
    public static <E extends Comparable<E>> E max(Collection<E> c) {
        if (c.isEmpty())
            throw new IllegalArgumentException("Empty collection");

        E result = null;
        for (E e : c){
            if(result == null || e.compareTo(result) > 0) {
                result = e;
            }
        }
        return result;
    }
```
이 보다 복잡한 건 뒤에서...

### 요약

- 제네릭 자료형과 마찬가지로 제네릭 메서드는 클라이언트가 직접 형변환 해야하는 메서드 보다 사용하기 쉽고 안정성 높음
- 새로운 메서드 고안할 때는 형변환 없이도 사용할 수 있는지 판단해라
- 시간 날 때 기존 메서드 제네릭하게 바꾸면 기존 클라이언트와 호환되면서 더 좋은 API 제공 가능


## Item 31: Use bounded wildcards to increase API flexibility

앞에서 했다시피 형인자 자료형(prameterized types) 는 불변형이다.
상-하위 관계 가 성립하지 않는다.List<Object> 가 하는 걸 List<String> 이 다 할 수 없기 때문에 List<String> 은 List<Object> 의 하위 자료형이 아니다.

### 와일드카드

```java
// 스택 API
public class Stack<E> {
    public Stack();
    public void push(E e);
    public E pop();
    public boolean isEmpty();
}
```

엘리먼트 집합 받아서 다 stack 에 넣는 pushAll 을 생각해보자

```java
// producer.. 문제!
public void pushAll(Iterable<E> src){
    for(E e: src){
        push(e);
    }
}
```

실제 하려고 하면 컴파일 에러...

```java
public static void main(String[] args) {
    WildcardStack<Number> ws = new WildcardStack<>();
    Iterable<Integer> integers = Arrays.asList(1,2,3,4,5);
    ws.push(1); //OK
    ws.pushAll(integers); //compile error incompatible types..
}
 ```

Integer 는 Number의 하위 타입이지만 Iterable<Integer> 는 Iterable<Number> 의 하위 타입(subtype)이 아니기 때문
``한정적 와일드카드 자료형 (bounded wildcard type)`` 을 활용하면 해결

- ``Iterable<E>``  -> E 의 Iterable
- ``Iterable<? exends E>`` -> E 의 하위 자료형의 Iterable 

```java
public void pushAll(Iterable<? extends E> src){
    for(E e: src){
        push(e);
    }
}

```java
// consumer... 문제!
public void popAll(Collection<E> dst) {
    while(!isEmpty()) {
        dst.add(pop());
    }
}
```

```java
public static void main(String[] args) {
    WildcardStack<Number> ws = new WildcardStack<>();
    Iterable<Integer> integers = Arrays.asList(1,2,3,4,5);

    Collection<Object>  objects = new ArrayList<>();
    ws.popAll(objects); // 컴파일 에러
}
```

Collection<Number> 자리에 Collcection<Object> 가 들어가려 해서 발생. 

이 때는 E의 컬렉션이 아니라 E의 상위 자료형(supertpye) 컬렉션 이라고 해야 한다.
- ``Collection<E>``  -> E의 컬렉션
- ``Collection<? super E>`` -> E의 상위 타입의 컬렉션

```java
public void popAll(Collection<? super E> dst) {
    while(!isEmpty()) {
        dst.add(pop());
    }
}
```

- 객체의 생산자나 소비자 역할을 하는 메서드 인자의 자료형은 와일드카드로 해라
- 둘을 동시에 하는 메서드 인자는 와일드 카드 무쓸모 자료형이 정확히 일치해야 하기 때문

### PECS (Produce - Extends, Consumer - Super)

- 인자가 T 생산자 라면 ``<? extends T>``, T 소비자라면 ``<? super T>``

Stack 예를 들자면 pushAll의 인자 src 는 스택에 사용될 E 형의 객체 만드는 생산자이므로 extends
``public void pushAll(Iterable<? extends E> src)``
popAll 의 인자 dst 는 스택 내의 객체를 소비하므로 super..
``public void popAll(Collection<? super E> dst)``

앞서 했던 ``union(Set<E> e1, Set<E> e2)`` method 는 producer 이므로
``union(Set<? extends E> e1, Set<? extends E> e2)`` 로 하는게 좋다.

### return type 으로  와일드 카드를 쓰지 말 것

반환형으로 와일드카드가 나가면 사용자가 명시적 형변환을 해주어야 한다. 적절히만 쓰면 와일드 카드 자료형이 쓰인 것은 
사용자에게 거의 노출되지 않음. 
> 사용자가 와일드카드에 대해 고민한다면 클래스 API 설계가 잘못된 것이다.

### 명시적 형인자

위의 union 함수를 실제로 쓰면 컴파일 에러 발생 (java8 부턴 컴파일러 똑똑해져서 됨)

```java
Set<Integer> integers = ...;
Set<Double> doubles = ...;
Set<Number> numbers = union(integers, doubles);
// return type 추측을 못함...

Set<Number> numbers = Uniom.<Number>union(integers, doubles); // 명시적 형인자 전달
```

앞서 했던 max 는 다음과 같이 고칠 수 있다.
```java
    public static <T extends Comparable<? super T>> T max(Collection<? extends T> c) {
        if (c.isEmpty())
            throw new IllegalArgumentException("Empty collection");

        T result = null;
        for (T t : c){
            if(result == null || t.compareTo(result) > 0) {
                result = t;
            }
        }
        return result;
    }
```

2번 PECS 적용

- argument c에 적용한 것은 직관적. T 객체의 생산자 이므로
- ``Comparable<T>`` 는 언제나 T 인자를 소비해서 int 값을 반환함  따라서 consumer 니까 super 로 해야 함 . Comparable 과 Comparator는 모두 comsumer!
책의 예시로는 ``ScheduledFuture<?>`` 나옴. 이 인터페이스는 Future와 Delayed 인터페이스를 상속받는데
Delayed 인터페이스가 Comparable 을 extends 하고 있음. 즉 
``<T extends Comparable<T>>`` 이거로는 ``<ScheduledFuture extends Comparable<ScheduledFuture>>`` 이걸 추론할 수 있고
``<T extends Comparable<? super T>>`` 이거로는 ``<ScheduledFuture extends Comparable<Delayed (super ScheduledFuture)>>``
를 추론 할 수 있다.

### 형인자 vs 와일드카드 에선 와일드카드를 쓰자

```java
public static <E> void swap(List<E> list, int i, int j);
public static void swap(List<?> list, int i ,int j);
```
많은 method 가 형인자 형태와 와일드카드 형태 두가지로 표현 가능
public API 에서는 와일드카드가 좋음. 간단하기 때문에.

> 형인자가 메소드 선언에서만 나타나면 와일드카드로 바꾸자

```java
// 문제 있음
public static void swap(List<?> list, int i, int j){
    list.set(i, list.set(j, list.get(i)));
}
```

컴파일 에러 발생.  List<?> 에는 null 말고 어떤 것도 넣을 수 없기 때문
해결 방법으로 helper method 에서 타입 추론 도와주도록 함

```java
public static void swap(List<?> list, int i, int j) {
    swapHelper(list, i, j);
}

private static <E> void swapHelper(List<E> list, int i, int j) {
    list.set(i, list.set(j, list.get(i)));
}
```

### 요약

- 와일드카드 쓰면 좀 더 유연한 API 구현 가능
- 널리 쓰일 라이브러리라면 필수적으로 고려해야 한다
- PECS 암기하자 암기하자
- 모든 Comparable 과 Comparator 는 Consumer 이다

## Item 32: Combine generics and varargs judiciously

varargs 는 method args 를 다인자로 받을 수 있게 한 것
```java
static void func(int... ints);

//client
func(1,2,3,4);
```

내부적으로 인자를 ``array`` 에 보관. 인자가 generic 이면 ....
Heap Pollution 문제 생길 수 있다.
```java

```


## Item 33: Consider typesafe heterogeneous containers

Generic은 Set 이나 Map 같은 collection 이나 ThreadLocal 이나 AtomicReference 같은 하나의 원소만을 담는 컨테이너에
많이 쓰인다. 이 때 형인자를 받는 부분은 컨테이너임. 보통은 컨테이너당 type parameter 가 정해져 있다. 
이것을 유연하게 하나의 컨테이너에 여러 Type 이 담기면서도 형안정성을 유지할 수 있게 해보자.
즉 컨테이너가 아니라 key 값에 형인자를 지정하자. 

```java
// Typesafe heterogeneous container pattern 형 안전 다형성 컨테이너
public class Favorites {
    private Map<Class<?>, Object> favorites = new HashMap<>();

    public <T> void putFavorite(Class<T> type, T instance) {
        favorites.put(Objects.requireNonNull(type), instance);
    }

    public <T> T getFavorite(Class<T> type) {
        return type.cast(favorites.get(type));
    }
}

// client 부분
public static void main(String[] args) {
    Favorites f = new Favorites();
    f.putFavorite(String.class, "Java");
    f.putFavorite(Integer.class, 12345);

    String favoriteString = f.getFavorite(String.class);
    String favoriteInteger = f.getFavorite(Integer.class);
}
```
Favorites 객체는 형 안전(type 에 맞게 캐스팅해서 돌려줌 ``Class.cast``), 다형성(하나의 type 이 아닌 여러 type을 컨테이너 내부에 보관 ``Class<?>``)

- ``private Map<Class<?>, Object> favorites`` 여기서 map에 unbounded wildcard 쓰면 아무것도 못하지 않나요?

> 여기서 와일드 카드는 map의 타입이 아니라 key에 사용된다. 그래서 가능

- favorites 의 value가 그냥 Object 인데 괜찮나?

> type은 ``key`` 이고 해당 해당 type으로 알아서 ``value``를 캐스팅해주면 좋겠지만 java type system 이 그렇게 강력하진 않다. 하지만 우리는 그걸 알고 있으니 꺼내올 때 적용 해주면 됨

현재 Favorites 2가지 문제 있음

1. 악의적인 클라이언트가 형 안전성을 꺠뜨릴 수 있다.
```java
// client 부분
public static void main(String[] args) {
    Favorites f = new Favorites();
    Class a = String.class; // use raw type Class!
    f.putFavorite(a, 1234); // putFavorite 잘 작동함... key: String.class value: Integer
}
```
raw type을 사용하면 generic 을 passing 하기 때문에 문제 발생. dynamic type checking 을 해주어야 한다.
```java
    public <T> void putFavorite(Class<T> type, T instance) {
        favorites.put(Objects.requireNonNull(type), type.cast(instance));
    }
```
같은 전략을 쓰는 컬랙션 wrapper class: checkedSet, checkedList, checkedMap
```java
List safeList = Collections.checkedList(new ArrayList(), String.clss);
safeList.add(123); // ClassCastException 발생
```

2. 실체 불가능한 자료형(non-reifiable type) 에는 쓰일 수 없다.
- ``reifiable type`` : type 정보를 runtime 에서 전부 사용 가능. ex) primitive, non-generic, raw type, invocations of unbound wildcards
- ``non-reifiable type`` :  type erasure 에 의해 type 정보가 compile time 에서 지워짐 ex) unbound wildcard 를 제외한 generic

따라서 key로 ``String`` ``String[]`` 은 쓰일 수 있지만 List<String> 은 쓰일 수 없다. List<String> 의 class 객체를 얻을 수 없기 때문.
List<String> 이랑 List<Integer> 는  같은 class 객체 List.class를 공유한다.  만일 자료형 리터럴(List<String>.class)이 가능하면 Favorites 객체는 올바르게 동작 못할 것

### 해결책 
- 상위 자료형 토큰(super type token) 
상속과 reflection 사용해서 구현

``String.class``(클래스 리터럴) -> ``Class<String>`` (타입 토큰)
``???`` -> ``Class<List<String>>`` 얻을수 있다면  가능

#### Class.getGenericSuperClass()

- 바로 위 수퍼 클래스의 타입을 반환
- 수퍼 클래스가 parameterized type 이면 실제 타입 파라미터를 반영한 타입을 반환 

#### ParameterizedType.getActualTypeArguments()

- 실제 파라미터 정보를 구한다.

즉 다음과 같이 실제 타입을 구할 수 있다
```java
class Super<T> {}
class Sub extends Super<List<String>> {}
Sub sub = new Sub();
Type typeOfGenericSuperclass = sub.getClass().getGenericSuperclass(); //Super<List<String>>
Type actualType = ((ParameterizedType) typeOfGenericSuperclass).getActualTypeArguments()[0]; // List<String>
```

### 한정적 자료형 토큰(bound type parameter)
Favorites 가 사용하는 자료형 토큰은 비한정적(unbound). get put 에 전달되는 argument를 제한 하고 싶을 때에는 한정적 자료형

annotation API: 한정적 자료형 토큰 많이 씀
```java
public <T extends Annotation> T getAnnotation(Class<T> annotationType)
```

- getAnnotation
이따 추가