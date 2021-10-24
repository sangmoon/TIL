## Observer Pattern

### Intent <br>
>> 상태를 가지고 있는 subject 와  변경을 알아야하는 observer 가 존재하며 이들의 관계는 1:1, 1:N 이 될수 있다.
publisher-subscriber 관계라 볼 수 있다.
- 한 객체가 다른 객체에 의존적일 때
- 한 객체의 변화가 다른 객체의 변화를 일으킬 때
- 한객체가 다른객체에게 notify 날리고 싶을 때
### Implementation <br>
```java
public interface Subject{
	public void attach(Observer observer);
	public void detach(Observer observer);
	public void notify();
}

public interface Observer{
	public void update();
}


```
### Consequences <br>
