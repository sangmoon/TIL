## Item 10: Obey the general contract when overriding equals

``equals``를 구현하는 건 쉽지 않다. 가장 쉬운 방법은 override 하지 않는 것이다.
다음 조건 중 하나라도 만족하면 구현하지 않는 것이 좋다.

1. Each instance of the class is inherently unique. ``Thread``와 같은 객체는 값보다 엔티티 자체를 표현한다. Object에서 제공하는 equals로 충분하다
2. There is no need for he class to provide a ``logical equality`` test.  Client가 해당 기능을 필요하지 않다고 생각한다면 굳이 구현할 필요가 없다.
3. A superclass has already overridden equals, and the superclass behavior is appropriate for this class. 예를 들어 Set은 AbstractSet, List 는 AbstractList, Map은 AbstractMap에서 미리 구현했다.
4. The class is private or package-private and your are certain that its equals method will never be invoked. 정말 위험을 감수하기 싫으면 다음과 같이 처리할 수도 있다.

```java
@Override public boolean equals(Object o) {
    throw new AssertionError();
}
```

정말 equlas 를 override 하고 싶으면 일반 규칙을 준수해야 한다. 다음과 같다.

- ``Reflexive``: for any Non-null reference value x, x.equals(x) must return true
- ``Symmetric``: for any non-null reference values x and y, x.equals(y) == y.equals(x)
- ``Transitive``: for any non-null reference values x,y,z, if x.equals(y) == true and y.equals(z) == true then x.equals(z) must return true
- ``Consistent``: equals가 여러번 불려도 x, y 가 변경되지 않았다면 항상 같은 값을 return 해야 한다.
- x.equals(null) must return false

... 갑자기 이산수학이.. 하나씩 살펴보자

- ``Reflexivity`` 이건 객체는 자기 자신과 항상 같아야 함을 뜻한다. 이걸 위반하는게 더 힘든데, 이 어려운 걸 해낸다면 collection에서 자기 자신을 찾을 수 없을 것이다.
- ``Symmetry`` 는  두 객체의 equals 값이 항상 같아야 한다는 것이다. 다음과 같이 만들면 위반할  수 있다.

```java
// violate sysmmetry
public final class CaseInsensitiveString {
    private final String s;

    public CaseInsensitiveString(String s) {
        this.s = Objects.requireNonNull(s)
    }

    @Override public boolean equals(Object o) {
        if(o instanceof CaseInsensitiveString) {
            return s.equalsInnoreCase(
                ((CaseInsensitiveString)o).s
            );
        }
        if(o instanceof String) {
            return s.equalsIgnoreCase(String o); // one-way interoperability!
        }
        return false;
    }
}
```
위의 경우 CaseInsensitiveString.equals(String s) 는 true 가 나올수 있지만 String.equals(CaseInsensitiveString cis) 는 항상 false가 나오게 된다.
이렇게 되면 이 객체의 행동을 예측할 수 없게 된다.
따라서 String과 통합하려는 시도는... 멍청하다고 할 수 있다.
```java
// 그냥 String 통합은 포기!
@Override public boolean equals(Object o) {
    return o instanceof CaseInsensitiveString && 
    s.equalsInnoreCase(((CaseInsensitiveString)o).s);
}
```

- ``Transitivity`` 이건 a와 b가 같고 b와 c 가 같으면 a와 c 가 같아야 함을 말한다. 위반하는걸 상상하기 어려운데... subclass가 equals에 영항을 주는 추가 정보를 담는 경우를 생각해보자.

```java
public class Point {
    private final int x;
    private final int y;

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    @Override public boolean equals(Object o) {
        if(!(o instanceof Point))
            return false
        Point p = (Point)o;
        return p.x == x && p.y == y;
    }
}
```
```java
public class ColorPoint extends Point {
    private final Color color;

    public ColorPoint(int x, int y, Color color) {
        super(x, y);
        this.color = color;
    }
}
```
이 상태로 두면 ColorPoint는 부모인 Point의 equals를 사용하게 된다. 당연히 color 정보는 무시되고, 이걸 의도하진 않았겠으니 override 해야 할 거다.

```java
// violates symmetry
@Override public boolean equals(Object o) {
    if(!(o instanceof ColorPoint)) {
        return false;
    }
    return super.equals(o) && ((ColorPoint)o).color == color;
}
```

문제는 Point와 ColorPoint를 비교할 때 생긴다. 전자는 color를 무시하고 비교하지만
후자는 항상 false가 나오기 때문이다. 따라서 symmetry 를 위반한다. 그래서 만약 다음과 같이 바꾼다면

```java
// violates transivity
@Override public boolean equals(Object o) {
    if(!(o instanceof Point)) {
        return false;
    }
    
    // o is norla Point
    if(!(o instanceof ColorPoint)) {
        return o.equals(this);
    }

    // o is ColorPoint
    return super.equals(o) && ((ColorPoint)o).color == color;

}
```

이러면 sysmmetry는 해결되지만, transitivity에서 문제가 생긴다.

```java
// what if?
ColorPoint p1 = new ColorPoint(1, 2, Color.RED);
Point p2 = new Point(1, 2);
ColorPoint p3 = new ColorPoint(1, 2, Color.BLUE);

p1.equals(p2) => true
p2.equals(p3) => true
p1.equals(p3) => false
```
왜냐하면 Point는 color를 무시하기 때문에 이런 결과가 나온다. 또한 다른 subclass가 있다고 한다면 무한 recursion에 빠질 수 있다.

``getClass``를 사용해서 해결할 수 있다는 사람들도 있다.
```java
@Override public boolean equals(Object o) {
    if(o == null || o.getClass() != getClass()) {
        return false;
    }
    Point p = (Point) o;
    return p.x == x && p.y == y;
}
```
같은 클래스여야만 equals를 확인한다. 그럴듯해보이지만 결과는 그렇지 않다. 상속을 완전 무시하는 결과이다. 따라서 지양해야하는 방향이다.

그럼 해결책은 무엇일까? 이건 객체지향 언어의 근본적인 동일성 문제이다. equals를 깨지 않으면서 클래스를 상속받아 값을 추가할 방법은 없다.

상속을 통한 방법은 없지만, 좋은 방법이 있다, ``Item 18: 상속보단 구성!``
ColorPoint가 Point를 상속하는 대신 필드를 갖게하고 view 메소드를 주는 것이다.

```java
public class ColorPoint {
    private final Point point;
    private final Color color;

    public ColorPoint(int x, int y, Color color) {
        point = new Point(x, y);
        this.color = Objects.requireNonNull(color);
    }

    public Point asPoint() {
        return point;
    }

    @Override public boolean equals(Object o) {
        if(!(o instanceof ColorPoint)) {
            return false;
        }
        ColorPoint cp = (ColorPoint)o;
        return cp.point.equals(point) && cp.color.equals(color);
    }
}
```

- ``Non-nullity``: ``instanceof`` keyword 가 인자가 null로 들어오면 false를 return하기 때문에 굳이 null check를 별도로 할 필요는 없다.

결론적으로 수준높은 equals를 짜기 위해 다음 과정이 필요하다.

1. Use the == operator to check if the argument is a reference to this object. 최적화를 위한 것
2. Use the instanceof operator to check if the argument has the correct type. interface 가 있다면 interface를 이용해라(Collection)
3. Cast the argument to the correct type
4. For each ``significant`` field in the class, check if that field of the argument matches the corresponding field of this object