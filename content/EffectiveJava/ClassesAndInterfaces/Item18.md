## Item 18: 상속보다는 컴포지션을 사용해라

**상속은 캡슐화를 깨뜨린다**. 상위 클래스 구현에 따라 하위 클래스의 동작이 이상해 질 수 있다.

### 상속 사용

```java
public class InstrumentedHashSet<E> extends HashSet<E> {
    private int addCount = 0;

    public InstrumentedHashSet() {}

    public InstrumentedHashSet(int initCap, float loadFactor) {
        super(initCap, loadFactor);
    }

    @Override public boolean add(E e) {
        addCount++;
        return super.add(e);
    }

    @Override public boolean addAll(Collection<? extends E> c) {
        addCount += c.size();
        return super.addAll(c);
    }

    public int getAddCount() {
        return addCount;
    }


    InstrumentedHashSet<Stirng> s = new InstrumentedHashSet<>();
    s.addAll(List.of("일", "이", "삼"));

    print(s.getAddCount());
    // 6  (?!)
    // 3 이 아니다.
}
```

원인은 HashSet 의 `addAll` 이 `add` 를 사용해 구현되어 있기 때문이다.

- `InstrumentedHashSet.addAll` 에서 3이 추가됨
- `HashSet.addAll` 이 각각 인자에 대해 `add` 호출
- Override 된 `InstrumentedHashSet.add` 가 3번 호출되어 3이 또 더해짐
- 결론적으로 원소 당 2씩 추가됨

**이 문제는 결국 메소드 재정의 때문에 발생했다.**

### composition 사용

```java
// Wrapper class
public class InstrumentedSet<E> extends ForawrdingSet<E> {
    private int addCount = 0;

    public InstrumentedSet(Set<E> s) {
        super(e);
    }

    @Override public boolean add(E e) {
        addCount++;
        return super.add(e);
    }

    @Override public boolean addAll(Collection<? extends E> c) {
        addCount += c.size();
        return super.addAll(c);
    }
}
```

```java
// Forwarding class
public class ForwardingSet<E> implements Set<E> {
    private final Set<E> s;
    public ForwardingSet(Set<E> s) {this.s = s;}

    public void clear() {s.clear();}
    public boolean contains(Object o) {return s.contains(o);}
    public boolean isEmpty() {return s.isEmpty();}
    public int size() {return s.size();}
    public Iterator<E> iterator() {return s.iterator();}
    public boolean add(E e) {return s.add(e);}
    public boolean remove(Object o) {return s.remove(o)};
    public boolean containsAll(Collection<?> c) {
        return s.containsAll(c);
    }
    public boolean addAll(Collection<? extends E> c) {
        return s.addAll(c);
    }
    // 후략

}
```

이러면 기존 Set 에 영향을 주지 않고 기능을 확장할 수 있다. 디자인 패턴으로 보면 **Decorator pattern** 으로 볼 수 있다. Composition 과 Forwarding 은 넓은 의미로 **Deligation** 이라고 부른다.

wrapper class 의 단점은 거의 없는데, callback 프레임워크와 어울리지 않는다. callback framework 에서는 `this` 를 넘겨서 callback 호출 시 사용하도록 한다. 그런데 내부 객체는 wrapper 를 모르므로 wrapper 가 아닌 내부 객체 자신을 넘기게 된다(SELF problem).

### 요약

> 상속은 강력하지만 캡슐화를 해친다. <br>
> 상속 대신 composition 과 forwarding 을 사용하자.
