## Decorator Pattern

### Intent <br>
상속을 받아 기능성을 확장하는 것 말고, 다른 방식으로 객체에 추가적 기능을 부여한다. (상속의 단점 보완)<br>
Wapper라고도 불린다. 직장인 클래스를 기준으로 해보자...

### Implementation <br>
```java
public interface Employee{
	public int getSalary();	
}

public class Researcher implements Employee{

	private int year;
	@Override
	public int getSalary(){
		return 10 + year;
	}
}

abstract public class EmployeeDecorator implements Employee{
	protected Emplyee decoratedEmployee;

	public EmplyeeDecorator(Employee decoratedEmployee){
		this.decoratedEmplyee = decoratedEmployee;
	}

	public int getSalary(){
		return decoratedEmployee.getSalary();
	}
}

public class 팀장 extends EmployeeDecorator{
	public 팀장(Employee decoratedEmployee){
		super(decoratedEmployee);
	}

	public int getSalary(){
		return super.getSalary() + 1;
	}
}

public class 실장 extends EmployeeDecorator{
	public 실장(Employee decoratedEmployee){
		super(decoratedEmployee);
	}

	public int getSalary(){
		return super.getSalary() + 5;
	}
}

public class 세자녀부모 exntends EmployeeDecorator{
	public 세자녀부모(Employee decoratedEmployee){
		super(decoratedEmployee);
	}

	public int getSalary(){
		return super.getSalary() + 10;
	}
}

```
### Consequences <br>
1. 단순 상속보다 더 유연하다.
2. 단순 기능 추가를 위해 클래스 설계를 쉽게 할 수 있다.
3. decorator와 component 는 같지 않다.(object 관점에서)
4. 작은 오브젝트들이 매우 많이 생성된다...