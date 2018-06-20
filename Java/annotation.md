# Annotation

``@`` 골뱅이를 통해서 추가 정보를 전달하는 방식을 annotation 이라고 한다. class에 대한 meta data를 저장하는 방식이다.
과거에는 XML을 통해 meta data를 많이 저장하였으나, 더 java 스러운 방식으로 현재 annotation을 표준 명세에 정의하였다.
java.lang의 reflection을 통해 runtime에 annotation 에 접근할 수 있다.

```java
@Target()
@Retention()
public @interface MyAnnotation {
    int value();
    int otherValue();
}
```

Target 과 Retention은 annotation 을 위한 built-in annotation 이다.
Target은 Type, Field, Method, Parameter, Constructor, Local variable, AnnotationType, Package, Type parameter, Type use로 할 수 있다.
즉 이 annotation을 붙이는 대상을 method로 할지, field로 할지 정하는 annotation이다.
retention의 경우 Source, Class, Runtime 3가지 옵션이 있다.  java 파일을 source 단계 -> 컴파일 후 .class 단계 -> JVM 위의 runtime 단계로 나눠볼 수 있는데,
Source의 경우 컴파일러만 참고하고 bytecode에는 남지 않는 정보이고 ``@Override``, Class는 컴파일 단계까지는 존재하며 runtime에서 사라지는 정보( 이것이 default 이다)
마지막으로 Runtime은 끝까지 살아남는 정보들이다. RUNTIME의 경우 reflection 을 통해 값을 runtime에 확인할 수 있다.