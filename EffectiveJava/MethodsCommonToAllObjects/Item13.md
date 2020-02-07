## Item 13: Override clone judiciusly

``Cloneable`` 인터페이스는 복사를 허용하기 위해 만들어졌다. 하지만 ``Object``의 clone method를 쓸 수 없기 때문에
 목적 달성에 실패했다.

 ```java
public class Employee {
  
   private String name;
  
   public Employee(String name) {
    this.name = name;
   }
  
   public String getName() {
    return name;
   }
     
   public static void main(String[] args) {
    Employee emp = new Employee("Abhi");
    try {
        Employee emp2 = (Employee) emp.clone();
        System.out.println(emp2.getName());
    } catch (CloneNotSupportedException e) {
        e.printStackTrace();
    }
   }
}

// return CloneNotSupportedException...
 ```

그럼 Cloneable 인터페이스는 무슨 역할을 할까?  그것은 Object의 clone 메소드의 동작을 정한다.
만약 한 클래스가 Cloneable을 구현했다면 Object.clone() 메소드는 field-by-field copy 객체 를 반환한다.
구현하지 않았다면 CloneNotSupportedException을 반환한다. 이건 매우 드문 인터페이스의 사용이다. 보통 인터페이스
구현은 클라이언트에게 그 클래스가 할수 있는 것을 말해준다. 이 경우 인터페이스는 부모클래스의 보호된 메소드 동작을 허용하게 한다.
실제 상황에서 Cloneable을 구현한 클래스는 적절한 public clone method를 반환해야 한다. 하지만 생성자를 호출하지 않고
객체를 생성하기 때문에 매우 위험하다.

clone 메소드에선 ``super.clone()`` 을 호출해야 한다. 꼭... 이걸 하지 않고 부모 클래스의 생성자를 호출하면 컴파일러는 문제를 일으키지 않지만 실제 JVM 동작에서 원치 않는 동작을 할 것이다. 예외적으로 Cloneable을 구현한 클래스가 final이면 sub클래스가 없기 때문에 이런 걱정을 할 필요가 없다. 하지만 super.clone() 을 호출하지 ㅇ낳으면 굳이 Cloneable을 구현할 필요가 없다, Object의 clone 구현에 의존할 필요가 없으니까!

잘 동작하는 clone 메소드를 제공하는 부모클래스를 가진 클래스에서 Cloneable을 구현한다고 생각해보자. 우선 ``super.clone``을 호출하자. 반환되는 객체는 완벽한 replica 이다.
모든 필드를 primitive나 immutable 객체로 선언했다면 더 처리할 필요가 없다. 

```java
//Item 11의 PhoneNumber 예제
@Override public PhoneNumber clone() {
    try {
        return (PhoneNumber) super.clone();
    } catch(CloneNotSupportedException e) {
        throw new AssertionError(); // Can't happen.. !
    }
}
```
return 타입을 자기 자신 클래스로 하는게 바람직하다. 클라이언트의 불필요한 캐스팅도 막고 java에서 covariant return type을 지원하기 때문에!

만약 field에 mutable object 가 있으면 대재앙이 일어난다. 예를 들어 Item 7의 스택을 생각해보자
이 클래스를 cloneable 하게 만들기 위해 단순히 super.clone() 을 한다면 copy stack 객체는 size 필드는 같지만 elements field는 original 객체의 array와
같은 array를 바라보게 된다. 따라서 original을 변경하면 NPE가 발생할 가능성이 아주 많다.
결과적으로 clone 메소드는 생성자처럼 기능한다. 따라서 original 객체에 영향을 주지 않게 만들어야 한다.
위 예제에서 stack이 적절히 동작하게 만드려면  stack의 내부도 copy 해야 한다. 가장 쉬운 방법은 elements array도 copy 하는 것이다.

```java
Override public Stack clone() {
    try {
        Stack stack = (Stack)super.clone();
        result.elements = elements.clone();
        return result;
    } catch (CloneNotSupportedException e) {
        thorw new AssertionError();
    }
}
```

근데 위의 예제는 stack.elements 가 final 필드면 불가능하다. 이건 근본적인 문제인데, serialization 처럼 mutable objects를 final 필드로 갖고 있는 형태와 사용할 수 없다.
cloneable 하려면 final을 없애야 한다.

단순 recursive copy 만으로는 부족할 수 있다. hashtable을 생각해보자

```java
public class HashTable implements Cloneable {
    private Entry[] buckets = ...;

    private static class Entry {
        final Object key;
        Object value;
        Entry next;

        Entry(Object key, Object value, Entry next) {
            this.key = key;
            this.value = value;
            this.next = next;
        }
    }
}
```

Stack에서 했던 것 처럼 buckets array를 recursive 하게 clone 해보자

```java
@Override public HashTable clone() {
    try {
        HashTable result = (HashTable) super.clone();
        result.buckets = buckets.clone();
        return result;
    } catch (CloneNotSupportedException e) {
        thorw new AssertionError();
    }
}
```

Copy hashtable은  자신만의 bucket 이 있지만 링크드리스트는  오리지날과 같다. 따라서 비정상동작 할 것이다.
이걸 고치기 위해선 각각 bucket 마다 링크드리스트도 copy 해야 한다.

```java
public class HashTable implements Cloneable {
    ///...

        private static class Entry {
        final Object key;
        Object value;
        Entry next;

        Entry(Object key, Object value, Entry next) {
            this.key = key;
            this.value = value;
            this.next = next;
        }

        Entry deepCopy() {
            // recursively copy the linked list
            return new Entry(key, value, next == null? null : next.deepCopy());
        }
    }
    
    @Override public HashTable clone() {
        try {
            HashTable result = (hashTable)super.clone();
            result.buckets = new Entry[buckets.length];
            for (int i = 0; i < buckets.length; i++) {
                if(buckets[i] != null) {
                    results[i] = buckets[i].deepCopy();
                }
            }
            return result;
        } catch (CloneNotSupportedException e) {
        thorw new AssertionError();
    }
}
```

잘 동작하는데, deepCopy가 recursive라서 stackoverFlow 가 발생할 수 있다. 이를 iteration으로 바꾸면...

```java
Entry deepCopy() {
    Entry result = new Entry(key, vaule, next);
    for (Entry p = result; p.next != null; p = p.next) {
        p.next = new Entry(p.next.key, p.next.value, p.next.next);
    }
}
```
결국 복잡한 mutable  객체를 cloning 하는 최종 방법은 우선 super.clone을 불러서 필드를 초기화하고  original 객체의 state를 재생산하는 것이다.
따라서 HashTable 예제에서 클로닝이 제대로 된 후에 put 메소드가 불려서 복사된 객체에서 동작한다. 이 방식이 깔끔하긴 하지만 super.clone() 한 필드를
덮어써야 하기 때문에 느릴 수 있다.

생성자와 같이 clone 메소드 내에서는 override 가능한 메소드를 불려선 안된다. 이게 가능하게 되면 subclass가 제대로 필드 바꾸기 전에 original을 오염시킬 수 있다.
따라서 put(key, value) 는 final 이거나 private 여야 한다.

public clone 메소드는 ``CloneNotSupportedException``을 throw 해서는 안된다, check exception 을 사용하지 않는게 쓰기 편하기 때문에.

상속을 위한 클래스를 설계할 때에는 Cloneable을 implements 해서는 안된다. 만약 clone을 구현한다면
Object의 clone 메소드 처럼 CloneNotSupportedException을 throw 하는 protected 메소드로 구현해야 한다.
그래야 subclass 들은 마치  Object를 바로 상속받은 것 처럼 Cloneable을 구현할지 말지 자유를 얻을 수 있다.
반대로 clone 동작을 허용하지 않는 것을 택했다면 아예 막을 수 있다.

```java
@Override
public final Object clone() throws CloneNotSuportedException {
    throw new CloneNotSupportedException();
}
```

또 Objects의 clone() 메소드는 sync 하지 않기 때문에 병렬 프로그래밍을 한다면
synchronization을 고려해야 한다.

이런 복잡한 작업이 꼭 필요할까? 거의 아니다.copy 생성자나 copy factory를 구현하는게 더 좋은 방법이다.

```java
// Copy constructor
public Yum(Yum yum){};

// Copy factory
public static Yum newInstance(Yum yum){};
```

클론에 비해 위 방식들의 장점은 이상한 객체 생성을 하지 않아도 된다는 것이다.final field도 신경쓸 필요 없다.
불필요한 exception 던지지 않는다. casting도 필요 없다.
또한 자신이 속한 class의 인터페이스를 구현한 타입 클래스도 인자로 받을 수 있다.
예를 들어 TreeSet을 HashSet으로 바꾸려 한다면 clone은 지원하지 않지만, ``new TreeSet(hashSet);`` 으로 가능하다.

결론적으로 array 복사정도면 모를까 거의 쓰지 말자.. copy constructor 나 copy factory 쓰자