## Item 17: Minimize mutability

`immutable class` 는 변경될 수 없는 인스턴스들의 클래스 이다. String, boxed primitive type, BigInteger 나 BigDecimal 등이 immutable class의 예이다.
mutable class 보다 설계하기 쉽고 에러도 적고 더 안전하다.

### immutable class 만들기 위한 규칙

1. 객체의 상태를 바꾸는 메소드(Mutator)를 제공하지마라
2. 클래스를 상속할 수 없게 만들어라
3. 모든 필드를 final로 선언해라
4. 모든 필드를 private로 만들어라.
5. mutable object에 대한 접근 제한을 확실히 해라. 클래스가 mutable object 가지고 있으면 client는 절대 접근할 수 없게 해야 한다. client 가 제공하는 객체로 초기화하지말고, field 를 반환해서도 안된다. 생성자나 accesor, readObject(Item 88)에서 defensive copy(Item 50)를 사용하자.

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

    @Override
    public boolean equals(Object o) {
        if(o == this)
            return true;
        if(!(o instanceof Complex))
            return true;
        Complex c = (Complex) o;

        return Double.compare(c.re, re) == 0
            && Double.compare(c.im, im) == 0
    }

    @Override
    public int hashCode() {
        return 31 * Double.hashCode(re) + Double.hashCode(im);
    }

    @Override
    public String toString() {
        return "(" + re + " + " + im + "i)" ;
    }
}
```

### Immutable Object 장점

**Immutable Object는 기본적으로 thread-safe 하다**. 멀티 쓰레드가 동시에 접근해 state를 오염시킬 수 없다. 이게 thread 안전성을 확보하는 가장 쉬운 방법이다.

**Immutable Objects는 자유롭게 공유할 수 있다**. 따라서 클라이언트가 가능한한 갖고 있는 객체를 재사용하도록 해야 한다. 가장 쉬운 방법은 public static final constants 를 제공하는 것이다. 예를 들어 Complex class는 다음 과 과 같은 상수를 제공할 수 있다.

```java
public static final Complex ZERO = new Complex(0, 0);
public static final Complex ONE  = new Complex(1, 0);
public static final Complex I    = new Complex(0, 1);
```

여기서 한 걸음 더 나아가면 **immutable class는 static factory 를 사용해 자주 사용하는 instance를 캐시함으로써 존재하는 객체를 새로 만드는 것을 피할 수 있다**. 모든 boxed primitive class와 BigInteger는 이 방식을 사용한다. 이 방식을 통해 client 메모리 사용량과 GC 부하를 줄일 수 있다. public 생성자 대신에 static factory method를 사용하는 방식은 cache를 나중에 추가할 수 있는 유연성을 준다.

자유롭게 공유가능한 immutable Object의 특징은 결과적으로 **_depensive copy_**(Item 50) 을 하지 않아도 되게 만든다. 따라서 clone method 나 copy 생성자를 만들 필요가 없다.

**immuatble 객체 자체를 공유할 수 있을 뿐 아니라 내부 객체도 공유 할 수 있다**.
예를 들어 BigInteger의 경우 부호를 나타내는 `int` 와 크기를 나타내는 `int[]` 로 구성되는데 `negate` method는 크기는 같고 부호만 다른 BigInteger를 반환한다. 이 때 array를 copy 할 필요 없다. 새로운 BigInteger 객체는 original과 같은 array를 갖고 있어도 된다.

### Immutable Object 단점

**immutable objects의 가장 큰 문제는 값이 다르면 별도의 객체를 생성해야 한다는 점이다**. 객체 생성이 충분히 비쌀 수 있기에 이는 성능 저하로 이어질 수 있다. 거기에 생성 과정에서 여러 step을 밟는 다면 치명적인 속도 저하로 이어질 수 있다.

immutability를 만족하기 위해서 subclass가 없도록 강제했었다. 하지만 좀 더 유연한 다른 방식이 있다. 바로 생성자를 모두 private 나 package-private로 만들고 `public static factory`를 사용하는 것이다.

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
여러 구현체를 쓸 수 있는 유연함과 더불어 이 방식으로 추후 성능 튜닝(cache 등을 통해)이 무리 없이 제공될 수 있다.

### 요약

요약 하면 setter를 모두 만드려고 하지 마라. 클래스는 가능한 한 immutable 해야 한다.
만약 immutable 하게 할 수 없다면 최대한 변경할 수 없도록 제한해라. 생성자는 모든 불변 변수를 초기화 할 수 있게 잘 설계해야 한다.
