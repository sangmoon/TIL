## memento pattern

### Intent <br>
>> 예전 상태를 기억하기 용이한 패턴. 주로 현재 상태를 기억했다가 롤백이 필요한 시점에서 쉽게 돌아가는 방식이다.
>> 바둑 장기등의 되돌리기, editor의 undo, browser의 뒤로가기 등이 있다.

참가자 : ``memento``, ``originator``, ``careTaker``
- originator: 객체 본래의 기능에 출실
- memento: 내부 상태를 저장
- careTaker: memento 들을 관리



### Implementation <br>
```java
public class Memento{
	private String state;

	public Memento(String state){
		this.state = state;
	}

	public String getState(){
		return this.state;
	}
}

public class CareTaker{
	private List mementoList = new ArrayList();

	public void add(Memento memento){
		this.mementoList.add(memento);
	}

	public Memento get(int idx){
		return this.mementoList.get(idx);
	}
}

public class Originator{
	private String state;

	public void setState(String state){
		this.state = state;
	}

	public String getState(){
		return this.state;
	}

	public Memento saveStateToMemento(){
		return new Memento(this.state);
	}

	public void getStateFromMemento(Memento memento){
		setState(memento.getState());
	}
}

public class MementoMain{
	public static void main(String[] args){
		Originator originator = new Originator();
		CareTaker careTaker = new CareTaker();

		originator.setState("state 1");
		careTaker.add(originator.saveStateToMemento()); // state 1 저장
		originator.setState("state 2");

		originator.getStateFromMemento(careTaker.get(0)); //state 1 불러오기
	}
}
```


### Consequences <br>
1. 상태정보와 관리를 기능과 분리해서 독립적으로 관리할 수 있다.
2. 오리지널 객체는 상태 관리의 부담을 덜면서 본래 기능에 충실 할 수 있다.
3. 메멘토 클래스로 들어오는 상태가 커지면 메멘토 클래스의 부담이 커진다.