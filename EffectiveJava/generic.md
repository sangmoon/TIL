# Generics

## 2판의 경우 27, 28 ,29 로 되어 있음

## Item 30: Favor generic methods 가능하면 제네릭 메서드로 만들 것

클래스가 generic 일 수 있는 것 처럼 method 도 generic 할 수 있음 </br>
예를 들어 collections 에 있는 알고리즘 관련 method(sort, binarysearch) 는 generic 하다.

```java
// use raw types - 문제 있음
public static Set union(Set s1, Set s2) {
    // Warning! HashSet(Collection<? extends E>)
    Set result = new HashSet(s1);
    // Warning! result.addAll(Collections<? extends E>)
    result.addAll(s2);
    return result;
}
```
- ``형인자 목록(type parameter list)`` 는 접근 제어자와 return type 사이에 위치

```java
public static <T> Set<T> union(Set<T> s1, Set<T> s2) {
    Set<T> result = new HashSet(s1);
    result.addAll(s2);
    return result;
}

// client 잘 동작함!
public static void main(String[] args){
    Set<String> guys = new HashSet<>(Arrays.asList("Tom", "Dean", "Harry"));
    Set<String> stooges = new HashSet<>(Arrays.asList("Larry", "Moe", "Curly"));
    Set<String> aflCio = union(guys, stooges);
    System.out.println(aflCio);
}
```
위의 union의 단점은 input set 2개와 output이 정확히 같은 타입이라는 것(``T``) </br>
``bounded wildcard type`` 을 사용해서 좀 더 유연하게 구연 가능 뒤에 나옴

### type parameter에 대한 convention

- ``T`` (임의의 타입)
- ``E`` (collection의 element)
- ``K,V`` (key, value)
- ``X`` (exception)
- ``R`` (function의 return type)
- ``T, U, V`` || ``T1, T2, T3`` (연속된 임의의 타입)

### 제너릭 싱클톤 패턴

변경이 불가능하지만 많은 자료형에 적용 가능한 객체를 만들어야 할 때가 있다. </br>
모든 필요한 형인자화 과정에서 동일 객체를 활용할 수 있는데, 그러려면 우선 필요한 형인자화 과정 마다 같은 객체를 나눠주는 정적 팩토리 메서드 필요 </br>

```java
private static UnaryOperator<Object> IDENTITY_FN = t -> t;

//IDENTITY_FN 은 stateless 객체이고 형인자는 unbounded 이므로 모든 자료형이 같은 객체를 공유해도 된다.
// 팩토리 메소드
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
    UnaryOperator<String> sameString = identityFunction(); //같은 IDENTITY_FN 객체 사용
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

이 패턴은 함수객체 구현에 많이 쓰임
```java
//Collections.java
// 예시 Arrays.sort(a, Collections.reverseOrder());
@SuppressWarnings("unchecked")
public static <T> Comparator<T> reverseOrder() {
    return (Comparator<T>) ReverseComparator.REVERSE_ORDER;
}

/// 중략 ...

private static class ReverseComparator
    implements Comparator<Comparable<Object>>, Serializable {

    private static final long serialVersionUID = 7207038068494060240L;

    static final ReverseComparator REVERSE_ORDER
        = new ReverseComparator();

    public int compare(Comparable<Object> c1, Comparable<Object> c2) {
        return c2.compareTo(c1);
    }

    private Object readResolve() { return Collections.reverseOrder(); }

    @Override
    public Comparator<Comparable<Object>> reversed() {
        return Comparator.naturalOrder();
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

정렬, 탐색, 최대 최소값 method 들은 컬렉션 내 원소들이 서로 비교 가능해야 한다.
이러한 작업이 가능하려면 Comparable을 구현한 원소들의 컬랙션을 인자로 받아야 한다.
아래 표현은 "자기 자신과 비교가능한 모든 자료형 T" 를 나타낸다.

```java
public static <E extends Comparable<E>> E max(Collection<E> c){...}
```
> E 는 ``compareTo(E o)`` 를 구현했음을 보장한다.

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


## Item 31: Use bounded wildcards to increase API flexibility 한정적 와일드카드를 써서 API의 유연성을 높여라

앞에서 했다시피 형인자 자료형(prameterized types) 는 불변형. </br>
때로는 불변 자료형 보다 유연한 자료형이 필요 할 수 있다. 이때 와일드 카드를 사용하자.

### 한정적 와일드카드

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

#### 생산자 문제

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
    // Iterable<Integer> is not subtype of Iterable<Number> ...
}
 ```

Integer 는 Number의 하위 타입이지만 Iterable<Integer> 는 Iterable<Number> 의 하위 타입(subtype)이 아니기 때문 </br>
``한정적 와일드카드 자료형 (bounded wildcard type)`` 을 활용하면 해결

- ``Iterable<E>``  -> E 의 Iterable
- ``Iterable<? exends E>`` -> E 의 하위 자료형의 Iterable 

```java
public void pushAll(Iterable<? extends E> src){
    for(E e: src){
        push(e);
    }
}
```

#### 소비자 문제

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
    // Collection<Object> is not subtype of Collection<Number>
}
```

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

Stack 예를 들자면 pushAll의 인자 src 는 스택에 사용될 E 형의 객체 만드는 생산자이므로 extends </br>
``public void pushAll(Iterable<? extends E> src)`` </br>
```java
E a = ? producer;
```

popAll 의 인자 dst 는 스택 내의 객체를 소비하므로 super.. </br>
``public void popAll(Collection<? super E> dst)`` </br>
```java
? consumer = E a;
```

앞서 했던 ``union(Set<E> e1, Set<E> e2)`` method 는 producer 이므로 </br>
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
Delayed 인터페이스가 Comparable 을 extends 하고 있음. 즉  ``<T extends Comparable<T>>`` 이거로는 ``<ScheduledFuture extends Comparable<ScheduledFuture>>`` 
이걸 추론할 수 있고 ``<T extends Comparable<? super T>>`` 이거로는 ``<ScheduledFuture extends Comparable<Delayed (super ScheduledFuture)>>``
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

## Item 32: Combine generics and varargs judiciously generic 과 다인자변수를 잘 조합하자

varargs 는 method args 를 다인자로 받을 수 있게 한 것
```java
static void func(int... ints);

//client
func(1,2,3,4);
```

내부적으로 인자를 ``array`` 에 보관. 인자가 generic 이면 Heap Pollution 문제 생길 수 있다.

- Heap Pollution : 형인자 자료형 변수가 형인자 자료형이 아닌 객체를 참조할 때 상황.. runtime 에서 ``ClassCastException`` 날 가능성 높음.
```java
static void dangerous(List<String>... stringLists){ // 형인자 자료형 array 가 생겨서 heap pollution
    List<Integer> intList = Arrays.asList(42, 11);
    Object[] objects = stringLists;
    objects[0] = intList;
    String s = stringLists[0].get(0); // ClassCastException 발생
}

// client
public static void main(String... args){
    dangerous(Arrays.asList("a", "b"), Arrays.asList("c", "d"));
}
```
- generic varargs array parameter 에 값 저장하는 건 좋지 않다.

의문 1 : generic array 만드는 건 못하게 하면서 method 에 generic varargs parameter 허용하는 이유는??
```java
List<String>[] = new ArrayList<String>[10]; // 불가능 error
static void dangerous(List<String>... stringLists){ ...} //가능 warning
```
위험을 감수하고 서라도 유용할 때가 있어서 java 언어 설계자들이 남겨둠 </br>
Java library 들은 generic + varargs 이미 많이 쓰고 있다. Arrays.asList(T... a), Collections.addAll(Collection<? super T> c) 등등.
이 Method 들은 typesafe 하다.

method를 typesafe 하게 만들었어도 java 7 이전에는 warning 무시하던지, 호출할 때마다 ``@SuppressWarnings("unchecked")`` 붙여야 했다. </br>
java7 에 ``@SafeVarags`` 어노테이션 나와서 method 선언부에 붙여주면 warning은 안 뜬다. 중요한 건 정말 typesafe 할 때만 붙여주어야 한다는 것. </br>

#### typesafe 조건

1. generic varargs array에 아무 것도 새로 저장하지 말 것(overwrite 하지 말 것)
2. 그 array의 reference 를 method 밖으로 노출시키지 말 것(해당 method 외의 다른 code 가 1번을 위반할 수 있다)

typesafe 의 예 </br>
input 으로 들어온 리스트의 배열의 원소들을 하나의 리스트로 만들어서 내보냄. </br>
```java
@SafeVarargs
static <T> List<T> flatten(List<? extends T>... Lists) {
    List<T> result = new ArrayList<>();
    for(List<? extends  T> list : lists){
        return.addAll(list);
    }
    return result
}
```

중요한게 Override 안 될 메소드에만 ``@SafeVarargs`` 다는게  중요 </br>
가능한 모든 override된 method 들이 safe 한 지 보장하는 것은 불가능하기 때문 </br>
Java8 에서는 static method나 final instance method 에만 저 annotation을 달 수 있고, </br>
Java9 에서는 private instance method 도 가능해졌다.

또 다른 대안은 varargs 사용하지 않고 List parameter를 사용하는 것 
```java
static <T> List<T> flatten(List<List<? extends T>> Lists) {
    List<T> result = new ArrayList<>();
    for(List<? extends  T> list : lists){
        result.addAll(list);
    }
    return result
}
```

#### 요야야야약
-  varargs 랑 generic은 잘 안 맞는다
- generic varargs parameter 는 typesafe 하지는 않지만, 문법적으로는 맞다.
- method의 parameter 로 generic varargs parameter 쓸 꺼면 typesafe 한지 확인하고 ``@SafeVarargs`` 꼭 달아라 

## Item 33: Consider typesafe heterogeneous containers 형 안전 다형성 컨테이너를 쓰면 어떨지 따져보라

Generic은 Set 이나 Map 같은 collection 이나 ThreadLocal 이나 AtomicReference 같은 하나의 원소만을 담는 컨테이너에 </br>
많이 쓰인다. 이 때 형인자를 받는 부분은 컨테이너임. 보통은 컨테이너당 type parameter 가 정해져 있다. </br>
이것을 유연하게 하나의 컨테이너에 여러 Type 이 담기면서도 형안정성을 유지할 수 있게 해보자.</br>
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

> 여기서 와일드 카드는 map(컨테이너)이 아니라 key에 사용된다. 모든 키가 상이한 형인자 자료형 가질 수 있다는 의미.

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

따라서 key로 ``String`` ``String[]`` 은 쓰일 수 있지만 ``List<String>`` 은 쓰일 수 없다. ``List<String>`` 의 class 객체를 얻을 수 없기 때문. </br>
``List<String>`` 이랑 ``List<Integer>`` 는  같은 class 객체 ``List.class``를 공유한다.  </br>
만일 자료형 리터럴(``List<String>.class``)이 가능하면 Favorites 객체는 올바르게 동작 못할 것 </br>

### 해결책 
- 상위 자료형 토큰(super type token) 
상속과 reflection 사용해서 구현

``String.class``(클래스 리터럴) -> ``Class<String>`` (타입 토큰)
``???`` -> ``Class<List<String>>`` 얻을 수 있다면  가능

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

코드 구현도 찾아서 했는데 복잡해서...

### 한정적 자료형 토큰(bound type parameter)
Favorites 가 사용하는 자료형 토큰은 비한정적(unbound). get put 에 전달되는 argument를 제한 하고 싶을 때에는 한정적 자료형

annotation API: 한정적 자료형 토큰 많이 씀
```java
public <T extends Annotation> T getAnnotation(Class<T> annotationType)
```

- ``getAnnotation`` : 프로그램 실행 중에 어노테이션을 읽은 메소드. ``AnnotatedElement`` 인터페이스에 있음
- ``AnnotatedElement`` : 클래스나 메서드, 필드 등 프로그램 요소들, 즉 리플렉션 객체를 표현하는 리플렉션 자료형들이 구현하는 인터페이스

```java
// 컴파일 시점에는 자료형을 알 수 없는 어노테이션을 실행시간에 읽어내는 메서드
// 방식 1 무점검 형변환
static Annotation getAnnotation(AnnotatedElement element, String annotationTypeName) {
    Class<?> annotationType = null;
    try {
        @SuppressWarnings("unchecked")
        annonationType = (Class<? extends Annotation>) Class.forName(annotationTypeName); //무점검 형변환 이므로 warning 발생
    } catch (Exception ex) {
        throw new IllegalArgumentException(ex);
    }
    return element.getAnnotation(annotationType);
}
```

클래스 Class 는 이런 종류 형변환 안전하게 동적으로 처리해주는 객체 메서드 ``asSubclass`` 가 이미 있다. 특정 객체를 하위 클래스의 class 객체로 형변환시켜줌. 

```java
// 컴파일 시점에는 자료형을 알 수 없는 어노테이션을 실행시간에 읽어내는 메서드
// 방식 2 dynamic 형변환 메서드 사용
static Annotation getAnnotation(AnnotatedElement element, String annotationTypeName) {
    Class<?> annotationType = null;
    try {
        annonationType = Class.forName(annotationTypeName);
    } catch (Exception ex) {
        throw new IllegalArgumentException(ex);
    }
    return element.getAnnotation(
        annotationType.asSubclass(Annotation.class);
    )
}
```

```java
//asSubclass 구현 ..
@SuppressWarnings("unchecked")
public <U> Class<? extends U> asSubclass(Class<U> clazz) {
    if (clazz.isAssignableFrom(this))
        return (Class<? extends U>) this;
    else
        throw new ClassCastException(this.toString());
}
```

### 요오오오약
- 컨테이너 대신 키를 제네릭으로 하면 형인자 개수의 제약이 없는 형 안전 다형성 컨테이너를 만들 수 있다.
- 그런 컨테이너는 Class 객체를 키로 쓰는데 그러한 객체를 자료형 토큰(type token) 이라고 한다.
- 키 자료형을 직접 구현하는 것도 가능하다. 예를 들어 DB 레코드를 표현하는 DataBaseRow 클래스(컨테이너) 는 제네릭 자료형 Column<T> 를 키로 사용할 수 있다.