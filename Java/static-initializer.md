# initializer

enum을 조사하던 중 enum class를 컴파일 하면
``static {};`` block이 static 내부에 생기는 것을 발견하였다.

```java
public class Abc{
    static {
        // static initializer
    }

    {
        // instance initializer
    }

    Abc(){
        // constructor
    }
}
```
class 에서 크게 3가지의 초기화 method를 생각할 수 있다. ``constructor``, ``static initializer``, ``instance initializer`` 이다.
``static initializer``는 class가 불리는 시점 즉 class loader에서 불릴 때 호출 되는 method 이다.
Final static 변수를 초기화 해줄 때 로직이 필요하다면 여기서 해주어야 한다.

``instance initializer``의 경우 생성자와 비슷한데, 컴파일 과정에서 생성자 앞쪽으로 자동으로 복사가 된다. 여러 생성자가 있을 때
공통되는 로직을 instance initializer로 해놓을 경우 코드 중복을 막을 수 있다.
3가지 rule이 있는데

1. instance initializer는 instance 생성 시에 실행
2. super(); 뒤에 실행
3. ``{ }`` 이 여러 개가 있다면 차례 대로 실행

이다.