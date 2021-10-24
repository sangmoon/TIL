# Stream

stream은 java의 자료구조(List, Map, Set ...) 들을 선언적으로 다룬다.
자료 구조들은 util.collection에 대부분 있는데, stream과 collection의 차이는
collection의 경우 자료 구조의 구현체이고, stream은 collection 들이 보관하고 있는 data를
다루는 API 라는 것이다.

예를 들어 String List에서 h로 시작하는 문자열만 뽑아낸다고 하자.
기존 방식은 List 에서 1개 씩 get을 해온 후 문자열 체크를 할 것이다.

```java
for (String str: inputList){
    if(str.startWith("h")){
        outputList.add(str);
    }
}
```

대략 위와 같은 코드가 된다. collection은 data의 추가, 삭제, 순회 API만 제공하기 때문에
나머지를 직접 구현해야 한다.

반면 Stream 을 사용하면 다음과 같이 구현할 수 있다.

```java
List<String> outputList = inputList.stream()
                                    .filter(str -> str.startWith("h"))
                                    .collect(Collectors.toList());
```

stream 은

- ``source`` : collection, array, generator, ftn, IO,
- ``intermediate op`` : filter, map,
- ``terminal op`` : forEach, reduce, sum,

로 구성되어 있다.

API 몇 가지를 보면

```java
//중간연산
Stream<R> map(Function<A, R>)
Stream<T> filter(Predicate<T>)
Stream<T> peek(Consumer<T>)

//최종연산
R collect(Collector)
void forEach(Consumer<T>)
Optional<T> reduce(BinaryOperator<T>)
boolean allMatch(Predicate<T>)
boolean anyMath(Predicate<T>)
```

등이 있다.