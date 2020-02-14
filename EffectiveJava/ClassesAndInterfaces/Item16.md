##  Item 16: In public classes, use accessor methods, not public fields

가끔 필드 조합의 모음 정도의 클래스를 쓸 때가 있다.
```java
class Point {
    public double x;
    public double y;
}
```
 이 때 필드는 ``public`` 이어선 안된다. 필드에 직접 접근이 가능해서 캡슐화의 이점을 전혀 얻을 수 없다.
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
 클래스가 패키지 밖에서도 접근이 가능하다면 accessor method를 제공해라. 하지만 클래스가 package-private 거나 inner private class 라면 필드를 노출해서 손해볼 건 없다.
 public class가 필드를 노출해선 안되지만, field가 immutable 하다면 덜 영향을 끼칠 것이다.

 요약하자면 public 클래스는 mutable field를 외부에 노출해선 안된다. 하지만 package-private나 private nested class의 경우 노출하는게 바람직 할 수도 있다.