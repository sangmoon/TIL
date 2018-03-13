## Builder Pattern

### Intent <br>
인스턴스를 생성할 때 ``생성자`` 만을 통해서 생성하는데에는 어려움이 있다.
생성자 인자가 너무 많은 경우 어떠한 인자가 어떠한 값을 나타내는지 확인하기 힘들다. 또 어떠한 인스턴스는 특정인자만으로
생성해야 하는 경우가 발생한다. ``telescoping constructor pattern``은 클래스가 지저분해진다.
``java bean pattern``은 일관성이 깨지고, immutable한 객체 생성이 불가능하다.

### Implementation <br>
``telescoping constructor pattern`` 과 ``java bean pattern``을 조합한다.
앱들이를 만드는 클래스를 생성한다.
```java
//AppleMan.java
public class AppleMan{
	private String name;
	private int age;
	private String phone;
	private String notebook;
	private String tablet;

	public student(){}

	public static class Builder {
		private String name;
		private int age;
		private String phone;
		private String notebook;
		private String tablet;

		public Builder(String name, int age){
			this.name = name;
			this.age = age;
		}

		public Builder phone(String phone){
			this.phone = phone;
			return this;
		}

		public Builder notebook(String notebook){
			this.notebook = notebook;
			return this;
		}

		public Builder tablet(String tablet){
			this.tablet = tablet;
			return this;
		}

		public AppleMan build(){
			return new AppleMan(this);
		}

		private Appleman(Builder builder){
			this.name = builder.name;
			this.age = builder.age;
			this.phone = builder.phone;
			this.notebook = builder.notebook;
			this.tablet = builder.tablet;
		}
	}
}
```
```java
//main.java
AppleMan man = new AppleMan.Builder("sangmoon", 26)
							.phone("iphone se")
							.notebook("macbook pro")
							.tablet("ipad pro")
							.build();
```


### Consequences <br>
1. 클래스 내부 표현을 다양화 할 수 있다.
2. 객체 생성과 표현을 분리할 수 있다.
3. 객체 생성에 대해 더 멋지게 조절 할 수 있다.
