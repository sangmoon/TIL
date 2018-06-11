
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
``method-local Inner class`` 는 외부 class의 method에 내부 class를 정의하여 사용 한다.
```java
class Outer{
    //...
    void my_method(){
        //...
        class Inner(){
            void my_method2(){
                //...
            }
        }
        Inner in = new Inner();
        in.my_method2();
    }
    //...
}
```
``anonymous Inner class``는 클래스의 선언과 초기화를 동시에 하는 방식이다. class나 interface의 method를 override 할 때 보통 사용한다.
Android 할 때 button eventListener 만들 때 이런 식으로 했던 것 같다.
```java
abstract class AnonymousInner {
   public abstract void mymethod();
}

public class Outer_class {

   public static void main(String args[]) {
      AnonymousInner inner = new AnonymousInner() {
         public void mymethod() {
            System.out.println("This is an example of anonymous inner class");
         }
      };
      inner.mymethod();	
   }
}
```

``static nested class`` 는 outer class의 static member이다. 초기화 없이 접근할 수 있다.
```java
public class Outer {
   static class Nested_Demo {
      public void my_method() {
         System.out.println("This is my nested class");
      }
   }
   
   public static void main(String args[]) {
      Outer.Nested_Demo nested = new Outer.Nested_Demo();	 
      nested.my_method();
   }
}
```

https://www.tutorialspoint.com/java/java_innerclasses.htm
