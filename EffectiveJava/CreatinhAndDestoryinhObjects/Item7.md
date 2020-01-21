## Eliminate obsolete object references

```java
pubic class Stack {
    private Object[] elements;
    private int size=0;
    private static final int DEFAULT_INITIAL_CAPACITY = 16;

    public Stack() {
        elements = new Object[DEFAULT_INITIAL_CAPACITY];
    }

    public void push(Object e) {
        ensureCapacity();
        elements[size++] = e;
    }

    public Object pop() {
        if(size == 0) {
            thorw new EmptyStackException();
        }
        return elements[--size];
    }

    private void ensureCapacity() {
        if(elements.length == size) {
            elements = Arrays.copyOf(elements, 2* size + 1);
        }
    }
}
```

문제가 없어보이지만, pop 하고 난 후 내보낸 객체에 대한 reference를 stack이 갖고 있는게 문제다. 이러면 GC 가 되지 않아 메모리 누수가 발생한다.

```java
public Object pop() {
    if (size == 0) {
        trow new EmptyStackExecption();
    }

    Object result = elements[--size];
    elements[size] = null;
    return result;
}
```

근데 null 하는게 정상적인 프로그래밍 방식은 아니다. 그럼 언제 해야할까? 스택은 자신만의 메모리 공간을 관리하기 때문이다.
즉  클래스가 자신만의 메모리 공간을 관리하면, 프로그래머는 메모리 누수를 항상 염두해야 한다.
또 다른 흔한 메모리 누수 경우는 캐시이다. 이 경우 ``WeakHashMap``이 좋은 대안이 된다.

3번째 요인은 listener && callback의 경우 발생한다. callback이 언제 실행될지 모르기에 항상 메모리에 올려두고 있으며 이는 메모리 누수로 이어진다.
하나의 해결책은 해당 callback을 WeakHashMap에 넣는 것이다.