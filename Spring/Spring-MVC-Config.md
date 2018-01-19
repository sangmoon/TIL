2018/01/19

스프링은 기본적으로 xml 기반의 설정파일은 관리한다.<br>
라이브러리 dependency 및 예약어 들을 관리하는 ``pom.xml.`` 가 있고<br>
``root-context.xml`` 은 모든 SERVICE나 DAO layer bean을 담고 있다. compunent-scan을 통해 해당 경로의 Bean들을 찾는다.<br>
``web-context.xml`` 은 servlet 정보들을 담고 있는데, 해당 servlet이 담당할 resolver나 handler 정보를 가지고 있다.<br>
``web.xml``에는 위에 ``web-context.xml``에 등록한 servlet들 정보와, ``root-config.xml``에 등록한 정보를 등록해서 <br>
``dispatcherServlet`` 을 생성한다. 

하지만 xml파일은 가독성이 떨어지고 디버깅이 어려운 단점이 있다. 그래서 Spring3.1 이후로 java-based 설정이 추가되었다.

```xml
<!-- web-servlet.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:mvc="http://www.springframework.org/schema/mvc"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-3.2.xsd http://www.springframework.org/schema/mvc http://www.springframework.org/schema/mvc/spring-mvc-3.2.xsd http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-3.2.xsd">
 
    <!-- Scan for spring annotated components -->
    <context:component-scan base-package="com.luckyryan.sample"/>
 
    <!-- Process annotations on registered beans like @Autowired... -->
    <context:annotation-config/>
 
    <!-- This tag registers the DefaultAnnotationHandlerMapping and
         AnnotationMethodHandlerAdapter beans that are required for Spring MVC  -->
    <mvc:annotation-driven/>
 
    <!-- Exception Resolver that resolves exceptions through @ExceptionHandler methods -->
    <bean class="org.springframework.web.servlet.mvc.method.annotation.ExceptionHandlerExceptionResolver"/>
 
    <!-- View Resolver for JSPs -->
    <bean class="org.springframework.web.servlet.view.InternalResourceViewResolver">
        <property name="prefix" value="/WEB-INF/pages/"/>
        <property name="suffix" value=".jsp"/>
    </bean>
 
    <!-- This tag allows for mapping the DispatcherServlet to "/" -->
    <mvc:default-servlet-handler/>
 
    <!-- resources exclusions from servlet mapping -->
    <mvc:resources mapping="/assets/**" location="classpath:/META-INF/resources/webjars/"/>
    <mvc:resources mapping="/css/**" location="/css/"/>
    <mvc:resources mapping="/img/**" location="/img/"/>
    <mvc:resources mapping="/js/**" location="/js/"/>
 
</beans>
```
이렇다고 하자. 이 설정을 config.java로 옮긴다면;
```java
@EnableWebMvc //<mvc:annotation-drvien> 과 같다.
@ComponentScan(basePackages = {"com.luckyryan.sample"}) //<context:component-scan base-package="com.luckyryan.sample"/> 과 같다.
@Configuration // Bean 을 갖고 있음을 알려줌.
public class appConfig extends WebMvcConfigurerAdapter {
 
    @Override // static resource handler
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        registry.addResourceHandler("/assets/**").addResourceLocations("classpath:/META-INF/resources/webjars/").setCachePeriod(31556926);
        registry.addResourceHandler("/css/**").addResourceLocations("/css/").setCachePeriod(31556926);
        registry.addResourceHandler("/img/**").addResourceLocations("/img/").setCachePeriod(31556926);
        registry.addResourceHandler("/js/**").addResourceLocations("/js/").setCachePeriod(31556926);
    }
 
    @Override // <mvc:default-servlet-handler/> 와 같다.
    public void configureDefaultServletHandling(DefaultServletHandlerConfigurer configurer) {
        configurer.enable();
    }
 
    @Bean // View Resolver for JSPs bean과 같다
    public InternalResourceViewResolver getInternalResourceViewResolver() {
        InternalResourceViewResolver resolver = new InternalResourceViewResolver();
        resolver.setPrefix("/WEB-INF/pages/");
        resolver.setSuffix(".jsp");
        return resolver;
    }
}
```

이와 같은 방식으로 해당 ``bean`` 이나 기본 해당 config의 base object를 상속해서 설정을 구성 할 수 있다.
앞으로 설정 파일에 대해 하나씩 분석해보겠다...