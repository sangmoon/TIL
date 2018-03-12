## Singleton Pattern

### Intent <br>
Class에 대해 하나의 instance만 가지고 싶을 때...


### Implementation <br>
1. 기본구현
2. getInstance 를 ``synchronized``로 구현
3. 인스턴스를 처음부터 만들어버림
4. DCL을 활용하여 ``volatile`` 로 싱클톤 인스턴스 선언을 하고  getInstance에서 싱글톤 클래스를 synchronized 해서 동기화 한다.


### Consequences <br>
