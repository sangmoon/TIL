## Item 4 Enforce noninstantiability with a private constructor

유틸 클래스들처럼 객체화 시키고 싶지 않은 클래스를 원할 때가 있다. 하지만 명시적 생성자가 없으면 컴파일러는 public default 생성자를 만들어준다.
따라서 private 생성자를 명시적으로 넣으므로써 이를 방지할 수 있다.

```java
public class UtilityClass {
    private UtilityClass() {
        throw new AssertionError();
    }
}
```

부과 효과로 이런 방식은 상속을 불가능하게 만든다. 모든 생성자는 부모 생성자를 호출해야 하기 때문에, private 생성자에 접근할 방법이 없다.

