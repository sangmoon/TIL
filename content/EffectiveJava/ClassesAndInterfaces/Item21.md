## Item21: 인터페이스는 구현하는 쪽을 생각해서 설계해라

### 모든 상황에서 불변식을 해치지 않은 default 메소드는 작성하기 어렵다

```java
// Java8 에 추가된 Collection dml removeIf

default boolean removeIf(Predicate<? super E> filter) {
    Objects.requireNonNull(filter);
    boolean result = false;
    for (Iterator<E> it = iterator(); it.hashNext();) {
        if (filter.test(it.next())) {
            it.remove();
            result = true;
        }
    }
    return result;
}
```

굉장히 범용적이지만 못 쓰는 경우도 있다. (ex) 아파치의 SynchronizedCollection)

컴파일 에러가 발생하지 않아도 런타임 에러가 발생할 수도 있다.

**기존 인터페이스에 default method 를 추가하는 건 최대한 자제하자.**
