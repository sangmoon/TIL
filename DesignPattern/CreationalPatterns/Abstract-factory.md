## Abstract Factory Pattern

### Intent <br>
Provide an interface  for creating families of related or dependent objects without specifying their concrete classes.
제품군을 만들 때 사용한다.


### Implementation <br>
```java
//StarBucksFactory.java
public interface StarBucksFactory{

}

public class KoreaStarBucksFactory implements StarBucksFactory{

}

public class JapanStartBucksFactory implements StarBucksFactory{

}

public interface Coffee{
	
}

```
### Consequences <br>
1. concrete classes 들을 숨긴다.
2. product families 교환을 쉽게 한다.
3. 같은 상속을 받는 product 간 consistency를 증가시킨다.
4. 새로운 product의 추가는 어려워진다.