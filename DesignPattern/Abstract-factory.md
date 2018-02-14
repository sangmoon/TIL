## Abstract Factory Pattern

### Intent <br>
Provide an interface  for creating families of related or dependent objects without specifying their concrete classes.

인스턴스의 생성과정을 숨긴 채 다 만들어진 인스턴스를 반환해주어야 한다.<br>
생설할 객체를 추상화 해야한다. 생성과정에서 추상화된 객체를 반환하게 하여야 상속받는 모든 자식 클래스를 다룰 수 있다.
여기에 생성을 담당하는 팩토리 또한 추상화 시켜서 그 내용을 숨긴다.

예를 들어 아이폰과 안드로이드를 만드는 제조 공장이 두 곳 있다고 하자. 그럼 우선 핸드폰과 공장이라는 것을 추상화 할 수 있다.

```java
public interface Factory<T>{
	public Phone createPhone(Class<T> implements Phone type);
```

```java
public interface Phone{
	public String getPhoneType();
}
```
그럼 이를 구현하는 concrete 클래스를 구현해보자

```java
public class AFactory<T> implements Factory {
	@Override
	public Phone createPhone(Class<T> type){
		Class<T> claz = (Class<T>); 
		return (Phone)abc;
	}
}
```

```java
public class Iphone implements Phone{
	@Override
	public String getPhoneType(){
		return "Iphone";
	}
}
```

```java
public class Android implements Phone{
	@Override
	public String getPhoneType(){
		return "Android";
	}
}
```