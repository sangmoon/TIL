loading, linking 그리고 initialization은 ``.class`` 인 바이트 코드가 jvm으로 불리면서 시작하는 초기 프로세스 이다.
(instantiation, GC, finalization은 중간 단계이고 unloading 을 끝 프로세스라고 볼 수 있다)
- loading
이 단계 에서는 특정 이름을 가진 클래스나 인터페이스의 .class 파일을 찾고 이 것을 해석하여 JVM 내부 데이터 구조에 맞게 바꿉니다.
 ``class loader``  가 이러한 역할을 수행한다. class loader는 기본적으로 ``.class`` 파일들을 cache하기 때문에
 한 번만 load하면 됩니다.
요약하면 loading 단계에서는 다음과 같은 3가지 일을 합니다.
  1. Create a binary stream of data from the class file
  2. Parse the binary data according to the internal data structure
  3. Create an instance of java.lang.Class

- linking
링킹에서는 class나 interface를 가져와서 JVM의 run-time state와 합치는 일을 합니다.
링킹은 verification, preparation, resolution 3 단계로 구성됩니다.
``verification`` 과정에서는  semantic을 체크하고 JVM 무결성을 방해하는지 검증합니다.
``preparation`` 과정에서 JVM은 클래스 변수에 메모리를 할당하고 type에 따라 default value로 초기화 합니다.
그러나 실제 초기화(user가 define 한)는 initialization phase 까지 실행되지는 않습니다.
``resolution`` 단계에서 JVM은 참조되는 class, interface, field 그리고 method 를 constant pool(symbolic table)에 위치 시키고
symbolic 참조에서 구체적인 값을 결정합니다.

- initialization
``initialization`` class 나 interface의 initialization method를 실행합니다.
static value나 static initializer에 정의한 값으로 class variable을 초기화합니다. 그리고 초기화가 안 됐다면 super-class를 initialization 해줍니다.