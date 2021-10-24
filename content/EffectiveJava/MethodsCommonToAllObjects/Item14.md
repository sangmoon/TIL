## Item 14: Consider implementing Comparable

Comparable은 Object에 정의된 인터페이스가 아니고, 단독 인터페이스이다. equals와 비슷한데 순서를 정하게 해준다.
Comparable을 구현한 객체 배열은 다음과 같이 정렬할 수 있다.

```java
Arrays.sort(a);
```

기본적으로 java에서 값을 나타내는 클래스는 Comparable을 구현한다. 만약 알파벳 순서나, 수치 순서, 연대 순 등과 같은 natural ordering이 필요하다면
반드시 ``Comparable`` 인터페이스를 구현해야 한다.

```java
public interface Comparable<T> {
    int compareTo(T t);
}
```
compareTo의 일반적인 규약은 equals와 비슷하다.
> 이 객체가 비교하고자 하는 녀석보다 작으면 음수를 반환, <br>
> 같으면 0을 반환 <br>
> 크면 양수를 반환한다. <br>
> 비교할 수 없는 녀석이면 ``ClassCastException`` 을 반환한다.

- sgn() 은 signum function을 의미한다.
- sgn(x.compareTo(y)) == -sgn(y.compareTo(x)) for all x and y(이건 x.compareTo(y) 가 exception 나오면 y.compareTo(x) 도 exception 을 반환해야 한다는 것을 의미한다)
- ``transitive`` 함을 보장해야 한다.(x.compareTo(y) > 0 && y.compareTo(z) > 0 이면 x.compareTo(z) > 0 이여야 한다.)
- x.compareTo(y) == 0 이면 sgn(x.compare(z)) == sgn(y.compare(z)) 여야 한다.
- (x.compareTo(y) == 0) == (x.equals(y)) 는 강제는 아니지만 정말 추천한다. Comparable을 구현하면서 이 규약을 위반하는 경우 분명히 명시해야 한다. "이 클래스는 equals와 대치되는 순서를 갖고 있습니다."

보면 equals와 굉장히 닮아 있다, ``reflexivity`` ``symmetry`` ``transitivity`` 모두를 만족해야 한다. 따라서 같은 문제가 있다. 기존 compareTo 규약을 유지하면서 상속을 통해 확장할 방법이 없다. Comparable을 구현한 클래스에 값을 추가하고 싶다면 상속하지 마라. 구성을 통해 필드로 해당 객체를 사용하는 것이 유일한 방법이다.

마지막 규약은 compareTo의 equality 판단 값이 equals의 판단과 같아야 한다는 것이다.
둘이 다르면 일관성이 깨졌다고 표현하고, 동작은 하겠지만  Collection, Set, Map 에서 생각대로 동작하지 않을 수 있다. 왜냐하면 이런 인터페이스들은 equals 를 이용해 보통 정의되지만, sorted algorithm은 보통 compareTo를 이용하기 때문이다. 큰 재앙은 아니지만 주의해야 한다.

compareTo method에서는 필드를 비교하면 되는데 객체의 경우 recursive하게 compareTo를 불러주면 된다. 만약 객체가 Comparable을 상속하지 안았다면 Comparator를 대신 써라.

```java
public final class CaseInsensitiveString implements Comparable<CaseInsensitiveString> {
    public int compareTo(CaseInsensitiveString cis) {
        return String.CASE_INSENSITIVE_ORDER.compare(s, cis.s);
    }
}
```

이전 버전의 책에서는 비교에서 부등흐를 사용했는데 java6부터 static compare methods들이 모든 boxed primitive type에 추가되었다. 부등호 쓰지말고 static method 사용하자.

만약 중요한 필드가 여러개라면 비교하는 순서가 중요해진다. 가장 중요한 필드부터 차례대로 비교하고, 0이 아닌 값이 나오면 그 순간에 반환하면 된다.

```java
public int compareTo(PhoneNumber pn) {
    int result = Short.compare(areaCode, pn.areaCode);
    if (result == 0) {
        result = Short.compare(prefix, pn.prefix);
        if (result == 0) {
            result = Short.compare(lineNum, pn.lineNum);
        }
    }
    return result;
}
```

요약하면 값을 비교해야할 필요가 있을 땐 Comparable을 구현해서 쉽게 정렬하고 검색할 수 있게 해라. 부등호 사용은 피하고 static method를 사용하거나 Comparator를 구현한 Comparator를 이용해라.