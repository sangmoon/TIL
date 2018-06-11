다음과 같은 test code를 돌려보자
```java
public void printClassLoaders() throws ClassNotFoundException {
 
    System.out.println("Classloader of this class:"
        + PrintClassLoader.class.getClassLoader());
 
    System.out.println("Classloader of Logging:"
        + Logging.class.getClassLoader());
 
    System.out.println("Classloader of ArrayList:"
        + ArrayList.class.getClassLoader());

    // result
    // Class loader of this class:sun.misc.Launcher$AppClassLoader@18b4aac2
    // Class loader of Logging:sun.misc.Launcher$ExtClassLoader@3caeaf62
    // Class loader of ArrayList:null
}
```
- Bootstrap class loader (c로 구현) jvm 구동 시킬 때 작동함 getClassLoader() 시에 null 로 나옴
- Extension class loader
- Application class loader (system class loader)

java 에서 class 들은 java.lang.ClassLoader의 instance에 의해 loading 된다. 그런데 class loader 또한 class 이다.
그럼 class loader는 누가 load 할까? 바로 bootstrap class loader 이다. 이 것은 rt.jar나 $JAVA_HOME/jre/lib 에 있는
core library를 loading 할 책임이 있다.또한 다른 class loader의 부모의 역할도 한다. bootstrap loader는 JVM의 core 역할을 하고,
native code로 쓰여 있다.

Extension loader는 bootstrap loader의 child이며 core java class의 extension 들을 loading 하는 역할을 한다.
$JAVA_HOME/lib/ext 에 있거나 java.ext.dirs system property에 등록된 것들을 이 loader가 loading 한다.

application level class는 application class loader가 관리한다. -classpath 나 -cp 옵션으로 주어지는 classpath에서 찾는 모든 file을 load한다.
또한 Extension loader의 child 이다.

class-loader의 동작을 살펴보자.
``delegation principle``
`` java.lang.ClassLoader.loadClass()``  method는 runtime에  class definition을 loading 책임이 있다.
1. 이미 loading 되어 있는지 확인하고(``findLoadedClass(name)``)
2. loading 안 됐으면 부모 loader에게 위임한다. (``parent.loadClass(name, false)``)
3. recursive하게 부모의 부모에게 가는데, 부모에게 서 찾을 수 없으면 자기 자신의 classpath에서 찾아 본다.(``finClass(name)``)
찾지 못할 경우 ``ClassNotFoundException``을 뱉어낸다.

``visibility principle``
> Child classloader는 부모 classloader가 load한 class를 볼 수 있지만, 반대는 안 된다.

``uniqueness principle``
> 부모 class loader가 load한 class는 자식 class loader가 load 하면 안된다.

코너 케이스로 JNDI의 경우 core class 는  bootstrap loader 에 의해 load 되지만, 이 core class들이 JNDI provider 를 load 해야 할 수 있습니다. JNDI provider는 
보통 classpath에 등록되어 application class loader의 담당이므로 부모 loader가 자식 class loader에서 class를 찾아야 합니다.
일반적인 delegation model로는 풀 수 없으며 이 경우 thread context loader를 이용하여 hierachy 를 tunneling 합니다.  