# Serialization

## 규칙 76 readObject 메서드는 방어적으로 구현하라

변경 불가능 클래스 조차, 직렬화를 통해 불변식이 깨질 수 있다.
1. ``불변식 깨짐`` -> readObject 유효성 검사
2. ``악의적 객체 참조`` -> readObject 에서 방어적 복사

### immutable class

```java
// 규칙 39 Period 클래스
public final class Period {
    private final Date start;
    private final Date end;

    public Period(Date start, Date end) {
        this.start = new Date(start.getTime());
        this.end = new Date(end.getTime());
        // 방어적 규칙
        if (this.start.compareTo(this.end) > 0) {
            throw new IllegalArgumentException(
                    start + " after " + end
            );
        }
    }

    public Date start() {
        return new Date(start.getTime());
    }

    public Date end() {
        return new Date(end.getTime());
    }

    @Override
    public String toString() {
        return start + " - " + end;
    }
}
```

### 방어 규칙
1. 내부 주소는 공개하지 않는다
2. start  <= end  이어야 한다.

### 공격1. 악의적인 바이트 스트림 공격

```java
public class BogusPeriod {
    // Byte stream could not have come from real Period instance!
    private static final byte[] serializedForm = new byte[] { (byte) 0xac,
            (byte) 0xed, 0x00, 0x05, 0x73, 0x72, 0x00, 0x06, 0x50, 0x65, 0x72,
            0x69, 0x6f, 0x64, 0x40, 0x7e, (byte) 0xf8, 0x2b, 0x4f, 0x46,
            (byte) 0xc0, (byte) 0xf4, 0x02, 0x00, 0x02, 0x4c, 0x00, 0x03, 0x65,
            0x6e, 0x64, 0x74, 0x00, 0x10, 0x4c, 0x6a, 0x61, 0x76, 0x61, 0x2f,
            0x75, 0x74, 0x69, 0x6c, 0x2f, 0x44, 0x61, 0x74, 0x65, 0x3b, 0x4c,
            0x00, 0x05, 0x73, 0x74, 0x61, 0x72, 0x74, 0x71, 0x00, 0x7e, 0x00,
            0x01, 0x78, 0x70, 0x73, 0x72, 0x00, 0x0e, 0x6a, 0x61, 0x76, 0x61,
            0x2e, 0x75, 0x74, 0x69, 0x6c, 0x2e, 0x44, 0x61, 0x74, 0x65, 0x68,
            0x6a, (byte) 0x81, 0x01, 0x4b, 0x59, 0x74, 0x19, 0x03, 0x00, 0x00,
            0x78, 0x70, 0x77, 0x08, 0x00, 0x00, 0x00, 0x66, (byte) 0xdf, 0x6e,
            0x1e, 0x00, 0x78, 0x73, 0x71, 0x00, 0x7e, 0x00, 0x03, 0x77, 0x08,
            0x00, 0x00, 0x00, (byte) 0xd5, 0x17, 0x69, 0x22, 0x00, 0x78 };

    private static Object deserialize(byte[] sf) {
        try {
            return new ObjectInputStream(new ByteArrayInputStream(sf)).readObject();
        } catch (IOException | ClassNotFoundException e) {
            throw new IllegalArgumentException(e);
        }
    }

    public static void main(String [] args) {
        Period p = (Period) deserialize(serializedForm);
        System.out.println(p);
        // Sat Jan 02 05:00:00 KST 1999 - Mon Jan 02 05:00:00 KST 1984
        // 불변식 깨짐 ...!
    }
}
```

### 해결책1. readObject에서 유효성 검사 구현

Serializable 만 implements 하면 직렬화는 되지만 불변식 깨진다. <br>
``readObject `` 메소드 는 실질적으로 생성자나 마찬가지(byte stream을 인자로 받는 생성자)

유효성 검사하는 readObject 메소드를 추가한다.
```java
private void readObject(ObjectInputStream s) throws IOException, ClassNotFoundException {
    s.defaultReadObject(); // non-static, non-transient field 채워줌

    if (start.compareTo(end) > 0) {
        throw new InvalidObjectException(start + " after " + end);
    }
}
```

### 공격2. 악의적 객체 참조

```java
public class MutablePeriod {
    public final Period period;
    public final Date start;
    public final Date end;

    public MutablePeriod() {
        try {
            ByteArrayOutputStream bos = new ByteArrayOutputStream();
            ObjectOutputStream out = new ObjectOutputStream(bos);

            out.writeObject(new Period(new Date(), new Date()));

            /*
             * 악의적 "previous object refs" 를 추가
             * Period 내부 Date 필드에 대한 것
             */
            byte[] ref = {0x71, 0, 0x7e, 0, 5};
            bos.write(ref); // start field
            ref[4] = 4; // {0x71, 0, 0x7e, 0, 4}
            bos.write(ref); // end field

            // Period 와 훔친 Date 참조 역직렬화
            ObjectInputStream in = new ObjectInputStream(new ByteArrayInputStream(bos.toByteArray()));

            period = (Period) in.readObject();
            start = (Date) in.readObject();
            end = (Date) in.readObject();

        } catch (IOException | ClassNotFoundException e) {
            throw new AssertionError(e);
        }
    }
}
```
```java
    public static void main(String[] args) {
        MutablePeriod mp = new MutablePeriod();
        Period p = mp.period;
        Date pEnd = mp.end;

        pEnd.setYear(78);
        System.out.println(p);

        pEnd.setYear(69);
        System.out.println(p);
    }
// 결과
// Mon Oct 08 18:04:19 KST 2018 - Sun Oct 08 18:04:19 KST 1978
// Mon Oct 08 18:04:19 KST 2018 - Wed Oct 08 18:04:19 KST 1969
```

Period 역직렬화 과정에서 객체 참조가 노출됨.
방어적 복사를 readObject() 에서도 해야 한다.

### 해결책2 방어적 복사
```java
private void readObject(ObjectInputStream s) throws IOException, ClassNotFoundException {
    s.defaultReadObject(); // non-static, non-transient field 채워줌

    start = new Date(start.getTime()); // start랑 end final 빼줘야 함
    end = new Date(end.getTime());

    if (start.compareTo(end) > 0) {
        throw new InvalidObjectException(start + " after " + end);
    }
}
```

java 1.4부터 위 처럼 방어적 복사 안해도 되도록 ``writeUnshared``와 ``readUnshared`` 메소드 추가되었는데, 뒤에 나올 규칙77에 취약하므로 그냥 방어적 복사 사용할 것. <br>
readObject 에서 override 가능한 메소드 호출하지 말 것. 보장 못함.

### 요약
- readMobject 를 구현 할 때는 public 생성자 구현하듯이 해야 한다.
- 어떤 바이트스트림이 주어지더라도 유효한 객체가 생성될 수 있게 해야 한다.
- 안전한 메서드 구현은 다음 지침들을 따르자
  - private 로 남아야 하는 객체 참조 필드를 가진 클래스는 해당 객체를 방어적으로 복사해야 한다.
  - 불변식을 검사해서 위반되면 InvalidObjectException을 던저야 한다. 불변식 검사는 방어적 복사 끝난 후에 실행되어야 한다.
  - 객체 완전 역직렬화 한 다음 유효성 검사해야 한다면 ObjectInputValidation 인터페이스를 이용해라
  - 직-간접적으로 override 가능 메소드 호출하지 말 것


```java
// ObjectInputValidation 사용법
// readObject가 다 끝나고 return 되기 직전에 validation 해줌
interface ObjectInputValidation {
    public void validateObject() throws InvalidObjectException;
}

public class ObjectInputStreamDemo {
    public static void main(String[] args) {
        try {
            ObjectInputStream ois = new ObjectInputStream(new FileInputStream("test.txt"));

            Example a = (Example) ois.readObject();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    static class Example implements Serializable, ObjectInputValidation {
        private String s = "Hello World!";

        private void readObject(ObjectInputStream in)
                throws IOException, ClassNotFoundException {
            in.defaultReadObject();
            in.registerValidation(this, 0); // 콜백 등록
        }

        @Override
        public void validateObject() throws InvalidObjectException {
            if (this.s.equals("Hello World!")) {
                System.out.println("Validated.");
            } else {
                System.out.println("Not validated.");
                throw new InvalidObjectException("Not validated.");
            }
        }
    }
}
```

```java 
(byte) 0xac, (byte) 0xed,                                               //STREAM_MAGIC. Specifies that this is a serialization protocol.
0x00, 0x05,                                                             // STREAM_VERSION. The serialization version.
0x73,                                                                   // TC_OBJECT. Specifies that this is a new Object.
0x72,                                                                   // TC_CLASSDESC. Specifies that this is a new class.
0x00, 0x06,                                                             // Length of the class name.
0x50, 0x65, 0x72, 0x69, 0x6f, 0x64,                                     // the name of the class 'P e r i o d'
0x40, 0x7e, (byte) 0xf8, 0x2b, 0x4f, 0x46, (byte) 0xc0, (byte) 0xf4,    // SerialVersionUID, the serial version identifier of this class.
0x02,                                                                   // Various flags. This particular flag says that the object supports serialization.
0x00, 0x02,                                                             // Number of fields in this class.
0x4c,                                                                   // ?? field type
0x00, 0x03,                                                             // Length of the field name
0x65, 0x6e, 0x64,                                                       // e n d
0x74,                                                                   // TC_STRING. Represents a new string.
0x00, 0x10,                                                             // Length of the string.
0x4c, 0x6a, 0x61, 0x76, 0x61, 0x2f, 0x75, 0x74, 0x69, 0x6c, 0x2f, 0x44, 0x61, 0x74, 0x65, 0x3b, // Ljava/util/Date;
0x4c,                                                                   // ?? field type
0x00, 0x05,                                                             // Length of the field name
0x73, 0x74, 0x61, 0x72, 0x74,                                           // s t a r t
0x71,                                                                   // TC_REFERENCE. Reference to an object already written into the stream.
0x00, 0x7e, 0x00, 0x01,                                                 // 1번째 참조..?
0x78,                                                                   // TC_ENDBLOCKDATA, the end of the optional block data for an object.
0x70,                                                                   //TC_NULL, which represents the fact that there are no more superclasses because we have reached the top of the class hierarchy.
0x73,                                                                   // TC_OBJECT. Specifies that this is a new Object.
0x72,                                                                   // TC_CLASSDESC. Specifies that this is a new class.
0x00, 0x0e,                                                             // Length of the class name.
0x6a, 0x61, 0x76, 0x61, 0x2e, 0x75, 0x74, 0x69, 0x6c, 0x2e, 0x44, 0x61, 0x74, 0x65, // java.util.Date
0x68, 0x6a, (byte) 0x81, 0x01, 0x4b, 0x59, 0x74, 0x19,                  // serialVersionUID of the java.util.Date class
0x03,                                                                   // Varius flags. SC_WRITE_METHOD. 
0x00, 0x00,                                                             // Number of fields in this class.
0x78,                                                                   // TC_ENDBLOCKDATA, the end of the optional block data for an object.
0x70,                                                                   //TC_NULL, which represents the fact that there are no more superclasses because we have reached the top of the class hierarchy.
0x77,                                                                   //TC_BLOCKDATA
0x08, 0x00, 0x00, 0x00, 0x66, (byte) 0xdf, 0x6e,
0x1e, 0x00, 0x78, 0x73, 
0x71, 
0x00, 0x7e, 0x00, 0x03,                                                 // 3번 째 참조..?
0x77, 
0x08,0x00, 0x00, 0x00, (byte) 0xd5, 0x17, 0x69, 0x22, 0x00, 
0x78 };
```

[오라클 스펙](https://docs.oracle.com/javase/7/docs/platform/serialization/spec/protocol.html)

[serialization 알고리즘 참조](https://www.javaworld.com/article/2072752/the-java-serialization-algorithm-revealed.html)

## 규칙77 개체 통제가 필요하다면 readResolve 대신 enum 자료형을 사용해라
 
 앞서 다룬 싱글톤 패턴은 "implements Serializable" 을 붙이는 순간 깨진다.

 ```java
public class Elvis {
    public static final Elvis INSTANCE = new Elvis();
    private Elvis(){}
}
 ```

- 기본 직렬화 형태, 사용자 정의 직렬화 형태 상관 없이
- 클래스에 명시적 readObject 있든 없든 상관 없다
- 모든 readObject 메서드는 새로 생성된 객체를 반환하는데 이 객체는 클래스가 초기화될 때 만들었던 객체가 아니다

### readResove 통한 싱글톤

readResolve 는 역직렬화 끝나서 만들어진 객체에 대해 호출된다. 새로 만들어진 객체 대신 이 메서드가 반환하는 객체가 사용자에게 간다.
```java
public class Elvis {
    public static final Elvis INSTANCE = new Elvis();
    private Elvis(){}

    private Object readResolve() {
        return INSTANCE;
    }
}
```
- 역직렬화된 객체는 무시. 싱글톤 객체 그냥 반환함
- 따라서 객체의 모든 필드는 transient 어야 한다
- 개체 통제를 위해 readResolve 쓸 때는 모든 객체 필드를 transient로 해야 한다
안 그러면 MutablePeriod 처럼 참조 가로채기 가능

### 비-transient 필드 통한 참조 가로채기

싱글톤 객체에 비-transient 필드가 있는 경우, 해당 필드의 내용은 객체의 readResolve가 실행되기 전에 역직렬화 되어야 한다. <br>
따라서 이 부분을 바이트 스트림 조작을 통해 다른 객체로 갈아 끼면, 참조 필드가 역직렬화 되는 순간 원래 객체를 "훔칠 수" 있다. (원래는 참조를 잃고 GC 되어야 할...)

- 먼저 도둑이 숨을 직렬화된 싱글턴 객체를 참조하는 객체 필드와 readResolve 메서드를 갖춘 도둑 클래스를 만듬
- 직렬화 스트림에서 싱글턴의 비-transient 필드가 참조하는 대상을 도둑 객체로 바꿔놓는다
- 이러면 참조 순환이 발생함(싱글턴은 도둑객체 포함, 도둑객체는 싱글턴 참조)
- 싱글턴이 도둑객체 포함하므로 싱글턴 역직렬화될 때 도둑 객체의 readResolve() 가 먼저 실행됨.
- 이 때 싱글톤 객체의 참조를 static 필드에 복사한다
- 그 다음 원래 대로 도둑 객체 숨겼던 원래 필드 자료형에 맞는 값을 반환한다. 안 그러면 ClassCastExecption 발생

```java
// 잘못된 싱글톤
public class Elvis implements Serializable {
    public static final Elvis INSTANCE = new Elvis();
    private Elvis(){}

    private String[] favoriteSongs = {"Hound Dog", "Heartbreak Hotel"};

    public void printFavorites() {
        System.out.println(Arrays.toString(favoriteSongs));
    }

    private Object readResolve() {
        return INSTANCE;
    }
}
```

```java
//도둑 클래스
public class ElvisStealer implements  Serializable {
    static Elvis impersonator;
    private Elvis payload;

    private Object readResolve() {
        // 아직 relosve 되지 않은 Elvis 객체 저장
        impersonator = payload;

        //favoriteSongs 필드 자료형에 맞는 객체 반환
        return new String[] {"A Fool Such as I"};
    }
    private static final long serialVersionUID = 0;
}
```

```java
public class ElvisImpersonator {
    private static final byte[] serializedForm = new byte[]{
            (byte) 0xac, (byte) 0xed, 0x00, 0x05, 0x73, 0x72, 0x00, 0x05, 0x45, 0x6c, 0x76, 0x69, 0x73, (byte) 0x84,
            (byte) 0xe6, (byte) 0x93, 0x33, (byte) 0xc3, (byte) 0xf4, (byte) 0x8b, 0x32, 0x02, 0x00, 0x01, 0x4c, 0x00,
            0x0d, 0x66, 0x61, 0x76, 0x6f, 0x72, 0x69, 0x74, 0x65, 0x53, 0x6f, 0x6e, 0x67, 0x73, 0x74, 0x00, 0x12, 0x4c,
            0x6a, 0x61, 0x76, 0x61, 0x2f, 0x6c, 0x61, 0x6e, 0x67, 0x2f, 0x4f, 0x62, 0x6a, 0x65, 0x63, 0x74, 0x3b, 0x78,
            0x70, 0x73, 0x72, 0x00, 0x0c, 0x45, 0x6c, 0x76, 0x69, 0x73, 0x53, 0x74, 0x65, 0x61, 0x6c, 0x65, 0x72, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x01, 0x4c, 0x00, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f,
            0x61, 0x64, 0x74, 0x00, 0x07, 0x4c, 0x45, 0x6c, 0x76, 0x69, 0x73, 0x3b, 0x78, 0x70, 0x71, 0x00, 0x7e, 0x00, 0x02
    };

    private static Object deserialize(byte[] sf) {
        try {
            InputStream is = new ByteArrayInputStream(sf);
            ObjectInputStream ois = new ObjectInputStream(is);
            return ois.readObject();
        } catch (Exception e) {
            throw new IllegalArgumentException(e);
        }
    }

    public static void main(String[] args) {
        // ElvisStealer.impersonator 를 초기화 하고
        // 진짜 Elvis 객체를 반환 한다 (Elvis.INSTANCE)
        Elvis elvis = (Elvis) deserialize(serializedForm);
        Elvis impersonator = ElvisStealer.impersonator;
        
        elvis.printFavorites();
        impersonator.printFavorites();
    }

    //[Hound Dog, Heartbreak Hotel]
    //[A Fool Such as I]
}
```

### 해결책

대신 직력화 가능 클래스를 enum 으로 구현하면 확실히 싱글톤 보장이 됨. <br>
JVM이 보장해주고 프로그래머는 신경 쓸 필요 없음.

```java
public enum Elvis {
    INSTANCE;
    privates String[] favoriteSongs = {"Hound Dog", "Heartbreak Hotel"};
    //...
}
```
하지만 직렬화 가능 클래스의 객체수를 컴파일 시점에서 알 수 없는 경우 enum을 통해 구현 할 수 없음. readResolve 써야함

### readResove와 접근 권한
- readResolve 메서드를 final 클래스에 두는 경우엔 반드시 private으로 선언해야 한다.
- final 클래스가 아닐 때, readResolve가 private이면 하위 클래스에는 적용되지 않는다. 
- final 클래스가 아닐 때, readResolve가 protected나 public이면, readResolve를 재정의하지 않은 모든 하위 클래스에 적용이 될 텐데 이러면 직렬화된 하위 클래스 객체를 deserialize 하면 상위 클래스 객체가 만들어져 ClassCastException이 발생할 것이다.

### 요약
- 개체 수 관련 불변식 강제하고 싶으면 enum 쓰자
- 그런 상황이 아니면 반드시 readResolve 를 구현해야하고 모든 객체 필드는 기본 자료형이나 transient로 선언해야 한다.

## 규칙78 직렬화된 객체 대신 직렬화 프락시를 고려해 보라

직렬화를 사용하면 버그나 보안 결함 생길 가능성 높음 <br>
일반 생성자 대신 언어 외적인 매커니즘을 이용하기 때문

이에 대안으로  ``직렬화 프록시 패턴``이 있다.
- private static nested class (== serialization proxy)를 만든다. (outer class 객체의 논리적 상태를 간결하게 표현하는)
- 바깥 클래스를 인자 자료형으로 사용하는 생성자 하나 (일관성 검사 필요 없음, 방어적 복사 필요 없음)
- 바깥 클래스에 writeReplace 메서드 구현
-  proxy 클래스에 자기와 논리적으로 동일한 바깥 클래스객체 반환하는 readResolve 메서드 추가

```java
private static class SerializationProxy implements Serializable {
    private final Date start;
    private final Date end;

    SerializationProxy(Period p) {
        this.start = p.start;
        this.end = p.end;
    }

    private static final long serialVersionUID = 1241142L;
}
```

다음과 같이 바깥 클래스에 writeReplace() 구현하면 직렬화 시스템은 바깥 클래스를 직렬화된 객체 만들지 않음
```java
private Object writeReplace() {
    return new SerializationProxy(this);
}
```

근데 공격자는 앞선 바이트스트림 공격처럼 만드려 시도 할 수 있다. 그걸 막으려면 readObject를 바깥 클래스에 추가하면 된다.
```java
private void readObject(ObjectInputStream stream) throws InvalidObjectException {
    throw new InvalidObjectException("Proxy require!");
}
```

마지막으로 SerializationProxy 클래스에 readResolve를 추가. <br>
Public API만 이용하기 때문에 아름답다. (직렬화 특성 거의 제거)
```java
private Object readResolve() {
    return new Period(start, end);
}
```

장점
1. 방어적 복사 접근법 처럼 바이트 스트림 통한 공격 방지
2. 내부 필드 탈취 공격도 저절로 중단
3. 외부 클래스 필드를 final로 선언할 수 있어서 진정한 immutable class 구현 가능
4. 직렬화 도중 유효성 검사도 필요 없음
5. 역직렬화된 객체가 애초에 직렬화된 객체와 다른 클래스가 되도록 할 수 있음(?? 장점인가..??)

EnumSet의 경우 생성자가 없고 팩토리 메서드로 EnumSet 객체를 얻는데, 실제로는 자료형 크기가 64 이하면 RegularEnumSet, <br>
64 보다 크면 JumboEnumSet을 반환한다. 만약 64개 원소를 갖는 enumSet 객체를 직렬화 한다음 enum 자료형에 다섯 개의 원소를 더 추가하고, <br>
방금 직렬화한 객체를 역직렬화 하면? 처음엔 RegularEnumSet Type 이었겠지만 나중엔 JumboEnumSet Type으로 변환 될 것이다.

```java
// EnumSet 의 직렬화 프록시
// EnumSet's serialization proxy
   private static class SerializationProxy <E extends Enum<E>>
           implements Serializable {
       // The element type of this enum set.
       private final Class<E> elementType;

       // The elements contained in this enum set.
       private final Enum[] elements;

       SerializationProxy(EnumSet<E> set) {
           elementType = set.elementType;
           elements = set.toArray(EMPTY_ENUM_ARRAY);  // (Item 43)
       }

       private Object readResolve() {
           EnumSet<E> result = EnumSet.noneOf(elementType);
           for (Enum e : elements)
               result.add((E)e);
           return result;
       }

       private static final long serialVersionUID = 362491234563181265L;
}
```

```java
    // 팩토리 메소드 내부
    public static <E extends Enum<E>> EnumSet<E> noneOf(Class<E> elementType) {
        Enum<?>[] universe = getUniverse(elementType);
        if (universe == null)
            throw new ClassCastException(elementType + " not an enum");

        if (universe.length <= 64)
            return new RegularEnumSet<>(elementType, universe);
        else
            return new JumboEnumSet<>(elementType, universe);
    }
```

### 직렬화 프록시 단점ㅅ는 ㅡㅋㄹ래스에는 적용 불가
- 클라이언트가 확장할 수 있는 클래스에는 적용 불가.
- 객체 그래프에 순환이 있으면 사용 불가. 어떤 객체의 메서드를 해당 객체의 직렬화 프록시의 readResolve 에서 호출하면 ClassCastException 이  뜬다. 아직 실제 객체를 가진것이 아니기 때문.
- 직렬화 프고시는 방어적 복사 기법에 비해 비용이 더 많이 듬

### 요약
- 클라이언트가 확장할 수 없는 클래스에 readObject나 writeObject를 구현해야 할 때는 직렬화 프록시 패턴 도입을 고려. 단순하지 않은 불변식을 만족해야 하는 객체를 안정적으로 직렬화하는 가장 쉬운 방법