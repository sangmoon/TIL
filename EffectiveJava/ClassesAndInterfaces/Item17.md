## Item 17: Minimize mutability

``immutable class`` 는 변경될 수 없는 인스턴스들의 클래스 이다. String, boxed primitive type, BigInteger 나 BigDecimal 등이 immutable class의 예이다.
mutable class 보다 설계하기 쉽고 에러도 적고 더 안전하다.
immutable class 만들기 위해 다음 5개 규칙을 따르라.

1. 객체의 상태를 바꾸는 메소드를 제공하지마라(Mutator라고 부르는)
2. 클래스를 상속할 수 없게 만들어라. 기본적으로 final로 선언하면 되는데, 다른 방법은 이따가 알려줄께!
3. 모든 필드를 final로 선언해라. 이를 통해 java가 보장하는 방식으로 당신의 의도를 표현할 수 있다. 또한 synchronization 없이 다른 쓰레드로 객체 레퍼런스를 건내줘도 정상 동작을 보장하기 위해 이 방식이 필요하다.
4. 모든 필드를 private로 만들어라.이건 client가 mutable objects에 접근해서 바로 수정하는걸 막는다. 기술적으로 immutable class가 primitive나 immutable object 필드를 public final로 가지는건 허용되지만 추천하지 않는다.
5. mutable object에 대한 접근 제한을 확실히 해라. 클래스가 mutable object 가지고 있으면 client는 절대 접근할 수 없게 해야 한다. client가 제공하는 객체로 초기화하지말고, field를 반환해서도 안된다.생성자나 accesor, readObject(Item 88)에서 defensive copy(Item 50)를 사용하자.

```java
// Immutable complex number class
public final class Complex {
    private final double re;
    private final double im;

    pubic Complex(double re, double im) {
        this.re = re;
        this.im = im;
    }

    public double realPart() {return re;}
    public double imaginaryPart() {return im;}

    public Complex plus(Complex c) {
        return new Complex(re + c.re, im + c.im);
    }

    public Complex minus(Complex c) {
        return new Complex(re - c.re, im - c.im);
    }

    public Complex times(Complex c) {
        return new Complex(re * c.re - im * c.im,
                            re * c.im + im * c.re);
    }

    public Complex dividedBy(Complex c) {
        double tmp = c.re * c.re + c.im * c.im;
        return new Complex((re * c.re + im * c.im) / tmp
                            (im * c.re - re * c.im) / tmp);
    }

    @Override public boolean equals(Object o) {
        if(o == this)
            return true;
        if(!(o instanceof Complex))
            return true;
        Complex c = (Complex) o;

        return Double.compare(c.re, re) == 0
            && Double.compare(c.im, im) == 0
    }

    @Override public int hashCode() {
        return 31 * Double.hashCode(re) + Double.hashCode(im);
    }

    @Override public String toString() {
        return "(" + re + " + " + im + "i)" ;
    }
}
```

복소수를 표현하는 클래스이다. 기본적인 Object의 메소드(equals, hashcode, toString) 에 더불어 접근자와 기본 연산 4가지 메소드를 제공하고 있다. 연산 내부에서 새로운 Complex 객체를 반환하는데 이는 Functonal 한 방식이라고 알려져있다. 객체를 변경시키기 보다 단순히 인자에 함수를 적용하는 것이기 때문이다. Immutable Object는 단순하다. Immuatable Object는 만들어질 때의 상태만을 갖는다. 반면 mutable object는 여러 상태를 가질 수 있다. 상태 변화에 대해 알지 못하면 사용하기 매우 어렵다.

Immutable Object는 기본적으로 thread-safe 하다. 이 녀석들은 synchronization이 필요 없다. 멀티 쓰레드가 동시에 접근해 state를 오염시킬 수 없다. 이게 thread 안전성을 확보하는 가장 쉬운 방법이다.

Immutable Objects는 자유롭게 공유할 수 있다. 따라서 클라이언트가 가능한한 갖고 있는 객체를 재사용하도록 해야 하낟. 가장 쉬운 방법은 public static final constants 를 제공하는 것이다. 예를 들어 Complex class는 다음 과 과 같은 상수를 제공할 수 있다.

```java
public static final Complex ZERO = new Complex(0, 0);
public static final Complex ONE  = new Complex(1, 0);
public static final Complex I    = new Complex(0, 1);
```
여기서 한 걸음 더 나아가면 immutable class는 static factory 를 사용해 자주 사용하는 instance를 캐시함으로써 존재하는 객체를 새로 만드는 것을 피할 수 있다. 모든 bobxed primitive class와 BigInteger는 이 방식을 사용한다. 이 방식을 통해 client 메모리 사용량과 GC 부하를 줄일 수 있다. public 생성자 대신에 static factory method를 사용하는 방식은 cache를 나중에 추가할 수 있는 유연성을 준다.

자유롭게 공유가능한 immutable Object의 특징은 결과적으로 ***depensive copy***(Item 50) 을 하지 않아도 되게 만든다. 따라서 clone method 나 copy 생성자를 만들 필요가 없다.

immuatble 객체 자체를 공유할 수 있을 뿐 아니라 내부 객체도 공유 할 수 있다.
예를 들어 BigInteger의 경우 부호를 나타내는 ``int`` 와 크기를 나타내는 ``int[]`` 로 구성되는데 ``negate`` method는  크기는 같고 부호만 다른 BigInteger를 반환한다. 이 때 array를 copy 할 필요 없다. 새로운 BigInteger 객체는 original과 같은 array를 갖고 있어도 된다.

이러한 특성을 안다면 immutable Object는 map의 key나 set의 elements로 충분히 사용할 수 있다. 

immutable objects의 가장 큰 문제는 별도의 값을 가진다는 것이다. 객체 생성이 충분히 비쌀 수 있기에 이는 성능 저하로 이어질 수 있다. 거기에 생성 과정에서 여러 step을 밟는 다면 치명적인 속도 저하로 이어질 수 있다. 이를 해결하기 위해 2개의 copy 접근이 있다. 첫번째 방법은 어떤 연산이 공통으로 필요한지 찾고 해당 부분을 primitives로 제공하는 것이다. 만약 어떤 작업이 primitive로 제공되면 immutable class는 각 단계별로 새로운 객체를 만들 필요가 없다. 예를 들어 BigInteger의 경우 package-private mutable ``companion class`` 가 있어서 modular 연산같은 경우에 속도를 증가시켜준다. 우리가  정확히 속도를 올릴 수 있는 부분을 알고 있으면 package-private mutable class를 활용할 수 있지만 그렇지 않다면 public mutable companion class를 사용하는 것이 최선이다.  가장 흔한 예는 String 과 StringBuilder class 이다.

immutability를 만족하기 위해서 subclass가 없도록 강제했었다. 하지만 좀 더 유연한 다른 방식이 있다. 바로 생성자를 모두 private 나 package-private로 만들고 public static factory를 사용하는 것이다.

```java
public class Complex {
    private final double re;
    private final double im;

    private Complex(double re, double im) {
        this.re = re;
        this.im = im;
    }

    public static Complex valueOf(double re, double im) {
        return new Complex(re, im);
    }
}
```

이렇게 하면 client에겐 immutable class는 효과적인 final이다(같은 패키지가 아니므로).
여러 구현체를 쓸 수 있는 유연함과 더불어 이 방식으로 추후 성능 튜닝(cache 등을 통해) 이 무리 없이 제공될 수 있다.

지금까지 immutable class는 어떤 메소드도 객체를 바꿀 수 없고, 모든 필드는 final이어야 한다고 말했다.  사실 이러한 제약은 실제 필요보다 더 강화된 것이며 성능 향상을 위해 조금 느슨히 할 수 있다. 실제로 어떤 메소드도 외부로 보이는 상태 변화를 만들어선 안 된다.
하지만 몇몇 immutable class 는 하나 이상의 non-final field를 갖고 있어 비싼 계산 결과를 캐시하고 있다. 같은 요청이 들어오면 cache 한 결과를 반환해 속도를 높인다. 해당 객체는 immutable 하기 때문에 항상 같은 결과다 나옴을 보장한다. 따라서 캐시해도 문제가 없다.

하나 문제점은 ``serializability`` 에 관한 것이다.만약 immutable 객체를 serializable 하게 선언했고 해당 객체에 mutable objects 에 대한 reference가 있다면 반드시 readObject나 readResolve 메소드를 명시하거나, ``ObjectOutputStream.writeUnshared`` 와 ``ObjectInputStream.readUnshared`` 를 사용해야 한다.

요약 하면 setter를 모두 만드려고 하지 마라. 클래스는 필요가 없는한 immutable 해야 한다.
만약 immutable 하게 할 수 없다면 최대한 변경할 수 없도록 제한해라. 생성자는 모든 불변 변수를 초기화 할 수 있게 잘 설계해야 한다.