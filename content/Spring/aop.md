## AOP
> 개발의 핵심적인 비즈니스 로직을 개발하는 데에만 집중하고, 나머지 부가적인 기능은 설정을 통해서 조정하라

### 관련 용어
- Aspect: 공통 관심사에 대한 추상적 명칭. 로깅이나 보안, 트랜잭션 같은 기능 자체
- Advice: 실제로 Aspect를 구현한 객체
- Join points: Advice를 적용할 수 있는 대상. Spring에서는 각 객체의 method
- Pointcuts: 여러 메소드 중 실제 Adivce가 적용될 대상 메소드
- target: pointcuts을 갖는 객체
- Proxy: Advice가 적용될 때 만들어지는 객체
- Introduction: target엔느 없는 새로운 메소드나 인스턴스 변수를 추가하는 기능
- Weaving: Advicd와 target이 결합하여 프록시 객체를 만드는 과정

### Advice의 종류
- Before Advice: target의 메소드 호출 전에 사용
- After returning: target의 메소두 호출 이후에 적용
- After throwing: target의 예외 발생 후 적용
- After: target의 메소드 호출 후 예외발생에 관계없이 적용
- Around: target의 메소드 호출 이전 이후 모두 적용

