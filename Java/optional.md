# Optional API

Java는 c나 c++에 있는 포인터를 대부분 숨겼다.
하지만 하나 못 숨긴게 있었으니 바로 null pointer 이다.
null 인 변수에 접근하려고 하면 NPE(Null Pointer Exception) 이 여지없이 떨어지기 때문에
항상 방어적 코드를 작성해야 했다.

```java
if( val == null){
    return "";
} else {
    return val;
}
```

val이 단순히 객체면 상관없지만, 만약 reference를 계속 따라가는 형태라면?

```java
Object4 obj4 = obj1.getObject2().getObject3().getObject4();

// 방어적 코드

if(obj1 != null){
    if(obj1.getObject2() != null){
        if(obj1.getObject2().getObject3() != null){
            obj4 = obj1.getObject2().getObject3().getObject4();
        }
    }
}
```

이러면 각 method 호출 직전마다 null check를 해주어야 한다. 마치 js의 callback 지옥과 같은 형태가 될 것이다.
조금 수정해보면

```java
if (obj1 != null && obj1.getObject2() != null && obj1.getObject2().getObject3() != null)
    obj4 = obj1.getObject2().getObject3().getObject4();
```

와 같이 if문 하나에서 다 체크 할 수 있다. 헬퍼 메소드를 활용한다면

```java
private boolean isValidObject(Obj1 obj1){
    return obj1 != null && obj1.getObject2() != null && obj1.getObject2().getObject3() != null;
}

if (isValidObject(obj1))
    obj4 = obj1.getObject2().getObject3().getObject4();
```

와 같이 만들 수 있다.

## optional

optional은 object를 감싼 wrapping 객체이다. 그래서 외부에서 null 체크를 보이지 않게 한다.
위의 코드를 바꿔보면

```java
Optional<Obj1> op = Optional.ofNullable(obj1);
Obj4 obj4 = op.map(Object1::getObject2).map(Object2::getObject3).map(Object3::getObject4).orElse(null)
```

와 같이 짤 수 있다. get을 3번 실행하는데 그 중 npe가 발생하면 orElse가 실행되어 null value로 obj4를 채워준다.