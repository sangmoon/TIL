
class 내부에 class를 정의한 것을 nested class라고 한다.

1. inner class
2. method local inner class
3. anonymous inner class
4. static nested class 

4 종류가 있다. 1 ~ 3 은 non-static, 4는 static class 이다.

``inner class``(member inner class)의 경우 inner class를 private 로 선언하여도
outer class에서 inner에 접근이 가능하며, inner 에서도 outer의 private 멤버에 접근 가능하다.
```java
class Outer{
    //...
    class Inner{
        //...
    }
}
```
java compiler는 
https://www.tutorialspoint.com/java/java_innerclasses.htm
https://stackoverflow.com/questions/17799976/why-is-static-inner-class-singleton-thread-safe
https://stackoverflow.com/questions/17693828/difference-between-loading-a-class-and-instantiating-it
https://stackoverflow.com/questions/24538509/does-the-java-classloader-load-inner-classes