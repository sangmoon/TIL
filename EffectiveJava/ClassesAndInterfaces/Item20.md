## Item 20: 추상 클래스보다는 인터페이스를 우선하라

> 추상 클래스는 1개만 상속 가능하지만, 인터페이스는 여러개 구현할 수 있다.

1. 기존 클래스에도 손쉽게 새로운 인터페이스를 구현해넣을 수 있다.
2. 인터페이스는 Mixin 정의에 안성맞춤이다.
3. 인터페이스는 계층 구조가 없는 타입 프레임워크를 만들 수 있다.

```java
public interface Singer {
    AutidoCLip sing(Song s);
}

public interface Songwriter {
    Song compose(int chartPosition);
}

public interface SingerSongWriter extends Singer, SongWriter {
    AudioCLip strum();
    void actSensitive();
}
```
