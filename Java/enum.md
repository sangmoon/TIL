# enum

다음과 같은 enum class 가 있다고 하자.

```java
public enum Season{
  Spring("March through May"),
  Summer("Jun throuh August"),
  Fall("September through November"),
  Winter("Decomber through Febnruary");

  private String span;

  Season(String months){
    this.span = months;
  }

  public String getSpan() {
    return this.span;
  }
}
```

이를 컴파일 할 경우 

```java
public final enum Season {
  

  public static final enum Season Spring;
  public static final enum Season Summer;
  public static final enum Season Fall;
  public static final enum Season Winter;

  private java.lang.String span;

  private static final synthetic Season[] ENUM$VALUES;
  
  static {};

  private Season(java.lang.String arg0, int arg1, java.lang.String months);

  public static Season[] values();

  public static Season valueOf(java.lang.String arg0);
}
```

이런 코드가 나온다.

enum은 Enum class를 상속받게 된다.

```java
public abstract class Enum<E extends Enum<E>>
extends Object
implements Comparable<E>, Serializable
```

즉

```java
public final class Season extends Enum<Season>{
    //...
}
```

라고 볼 수 있다.
enum은 결국 final class가 되므로 상속이 불가능하고, 선언한 변수들 또한 static final이기 때문에 ``static{}``  이 부분에서 초기화되고
수정이 불가능하다. instance가 1개로 제한되므로 오류의 경우가 줄어든다.

참조: https://docs.oracle.com/javase/7/docs/api/java/lang/Enum.html