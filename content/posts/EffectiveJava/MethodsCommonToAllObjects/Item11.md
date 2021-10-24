## Item 11: Always override hashCode when you override equals

equals를 구현한 클래스는 항상 hashcode 를 구현해야 한다. 그렇지 않으면 HashMap 이나 HashSet 같은 collection을 제대로 사용할 수 없다.
다음과 같은 규약이 있다.

1. 한 객체에 반복적으로 hashcode 가 호출될 때, 항상 같은 값을 반환해야 한다.
2. equals로 true로 판단되는 객체는 같은 hashcode를 반환해야 한다.
3. equals로 false가 나올 때 다른 hashcode가 나올 필요는 없다. 하지만 다른 값 나오게 하는게 hashtable 성능을 향상 시킨다.

가장 많이 실수하는게 2번째 규칙이다. 2 개의 다른 객체는 equals를 통해 같게 할 수 있지만 Object의 hashcode로는 그냥 다른 2개의 객체이다.
예를 들어 다음과 같은 HashMap 예제를  생각해보자

```java
Map<PhoneNumber, String> m = new HashMap<>();
m.put(new PhoneNumber(707, 867, 5309), "Jenny");
m.get(new PhoneNumber(707, 867, 5309));
```

이러면 "Jenny"를 돌려주기를 기대하겠지만 실상은 null을 반환한다. 왜냐하면 새로운 객체를 만들어 넣기 때문에 hashcode 값이 다르기 때문이다.
해결 방법은 적절한 hashcode() 함수를 구현하는 것이다.

방법은 다음과 같다

1. result 란 이름의 int 변수를 선언해서 중요 변수들ㅇ릐 값을 2.1 방식으로 계산해 초기화한다.
2. 모든 중요 변수들에 대해 다음 작업을 진행한다.
    1. 필드에 대해 int hashcode 를 계산한다.
        1. 필드가 primitive type이면 Type.hashcode(f) 를 이용해 값을 계산한다.
        2. 필드가 객체이고, 이 클래스의 equals 메소드가 해당 객체의 equals를 이용한다면 해당 필드의 hashCode 메소드를 이용해라. 더 복잡한 비교가 필요하면 ``canonical representation`` 을 이용해서 hashCode를 구해라. 만약 필드가 null이면 0 을 쓰는 것이 전통적이다.
        3. 필드가 array라면 각각의 중요한 element 가 분리된 필드인 것처럼 적용해라. array가 중요하지 않은 녀석이면 0이 아닌 상수를 써도 된다. 모든 element가 중요하면 Arrays.hashCode()를 써라
    2. 위의 작업을 통해 구해진 hashcode를 result와 합친다.
    > result = 31 * result + c;
    3. result 를 반환한다.

equals에 쓰이지 않는 필드는 사용해서는 안된다. 2.2의 과정을 반복적으로 수행하면 필드 순서에 따라 다른 hashcode가 나오게 되어 더 좋은 hash function이 된다. 31은 홀수 소수이기 때문에 선택되었는데, 만약 짝수라면 overflow 발생 했을 때 정보가 사라지게 되는 단점이 있다. 소수를 쓰는 이유는 덜 명확한데 그냥 그렇게 써왔다. 31의 장점은 최적화를 위해 쉬프트 연산과 뺄샘으로 대체할 수 있다는 것이다.
> 31 * i = (i<<5) - i 

모던 JVM은 이 작업을 자동으로 진행한다.

```java
// 전형적인 hashcode
@Override public int hashCode() {
    int result = Short.hashCode(areaCode);
    result = 31 * result + Short.hashCode(prefix);
    result = 31 * result + Short.hashCode(lineNum);
    return result;
}
```

```java
// 좀 더 느리고 평범한 hashcode
@Override public int hashCode() {
    return Objects.hash(lineNum, prefix, areaCode);
}
```

만약 클래스가 immutable 하고 hashcode 계산하는 비용이 크다면 캐싱을 생각해볼 수 있다.
```java
private int hashCode;

@Override public int hashCode() {
    int result = hashCode;
    if( result == 0) {
        result = 31 * result + Short.hashCode(prefix);
        result = 31 * result + Short.hashCode(lineNum);
        hashCode = result;
    }
    return result;
}
```

요약하면 equlas 쓸 땐 항상 hashcode를 오버라이딩 해야 한다.