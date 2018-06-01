## Abstract Factory Pattern

### Intent <br>
Provide an interface  for creating families of related or dependent objects without specifying their concrete classes.
제품군을 만들 때 사용한다.


### Implementation <br>
```java
// factory method 사용할 경우
public enum VenderID{LG, SAMSUNG, APPLE}


public class ScreenFactory{
	public static Screen createScreen(VendorID vendorID){
       Screen screen  = null;
       switch(vendorID){
           case LG:
             screen = new LGScreen();
             break;
          case SAMSUNG:
             screen = new SAMSUNGScreen();
             break;
          case APPLE:
          	screen = new APPLEScreen();
      }
      return screen;
   }
}

public class FrameFactory{
	public static Frame createFrame(VendorID vendorID){
		Frame frame = null;
		switch(vendorID){
			case LG:
				frame = new LGFrame();
				break;
			case SAMSUNG:
				frame = new SAMSUNGFrame();
				break;
			case APPLE:
				frame = new APPLEFrame();
				break;
		}
		return frame;
	}
}


public class client{
	public static void main(String[] args){
		Frame frame = FrameFactory.createFrame(VendorID.APPLE);
		Screen screen = ScreenFactory.createScreen(VendorID.APPLE);

		Phone phone = new PhoneBuilder().setFrame(frame).setScreen(screen).build();

		//...
	}
}
```
제조사에 화웨이나 소니 등 다른 업체가 추가되면 각각 팩토리의 switch 문을 수정해야 한다. 

```java
public enum VenderID{LG, SAMSUNG, APPLE}

public interface PhoneFactory{
	public Frame createFrame();
	public Screen createScreen();
}

public class LGPhoneFactory implements PhoneFactory{
	public Frame createFrame(){
		return new LGFrame();
	}
	public Screen createScreen(){
		return new LGScreen();
	}
}

public class SAMSUNGPhoneFactory implements PhoneFactory{
	public Frame createFrame(){
		return new SAMSUNGFrame();
	}
	public Screen createScreen(){
		return new SAMSUNGScreen();
	}
}

public class APPLEPhoneFactory implements PhoneFactory{
	public Frame createFrame(){
		return new APPLEFrame();
	}
	public Screen createScreen(){
		return new APPLESCreen();
	}
}

public class client{
	public static void main(String[] args){
		Frame frame = APPLEPhoneFactory.createFrame();
		Screen screen = APPLEPhoneFactory.createScreen();

		Phone phone = new PhoneBuilder(VendorID.APPLE).setFrame(frame).setScreen(screen).build();

		//...
	}
}
```
### Consequences <br>
1. concrete classes 들을 숨긴다.
2. product families 교환을 쉽게 한다.
3. 같은 상속을 받는 product 간 consistency를 증가시킨다.
4. 새로운 product의 추가는 어려워진다.
5. 새로운 factory의 추가는 쉽다.