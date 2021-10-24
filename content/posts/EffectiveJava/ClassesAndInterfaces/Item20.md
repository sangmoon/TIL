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

### Default Method

Interface 의 default method 를 사용하려면, 꼭 `@implSpec` 을 붙여서 문서화해야 한다.

default method 의 제약 사항

- Object의 메소드는 제공해선 안 된다
- 필드를 가질 수 없어 functional 한 기능만 수행

### 인터페이스와 추상 클래스

둘을 함께 쓰면 장점만 추릴 수 있음. 이러한 것을 템플릿 메서드 패턴이라고 함

### 네이밍 컨밴션

관례상 인터페이스 이름이 **_Interface_** 라면 추상클래스는 **_AbstractInterface_** 로 짓는다.

### 요약

> 인터페이스는 정말 좋음 <br/>
> 너무 복잡해지면 골격 구현 클래스를 고려 <br/>

예제: `AbstractDynamoDBJacksonConverter`
