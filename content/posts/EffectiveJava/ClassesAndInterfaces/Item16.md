## Item 16: In public classes, use accessor methods, not public fields

가끔 필드 조합의 모음 정도의 클래스를 쓸 때가 있다.

```java
class Point {
    public double x;
    public double y;
}
```

이 때 필드는 `public` 이어선 안된다. 필드에 직접 접근이 가능해서 캡슐화의 이점을 전혀 얻을 수 없다.
API를 바꾸지 않고는 아무것도 변경할 수 없다. getter와 setter로 바꿔야 한다.

```java
class Point {
   private double x;
   private double y;

   public Point(double x, double y) {
       this.x = x;
       this.y = y;
   }

   public double getX() {return x;}
   public double getY() {return y;}

   public void setX(double x) {this.x = x;}
   public void setY(double y) {this.y = y;}
}
```

### immutable 한 필드도 public 은 좋지 않다.

```java
public final class Time {
    public final int hour;
    public final int minute;
}
```

불변성은 유지하겠지만, 추후 해당 필드 읽을 때 부수 작업을 할 수 없다.

### 요약

> public 클래스는 mutable field를 외부에 노출해선 안된다. <br>
> immutable field 도 노출 하지 말자.
