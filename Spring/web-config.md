2018/01/19

``WebConfig`` 설정을 알아보자. WebConfig가 상속받는 abstract class는 다음 ``WebMvcConfigurerAdapter`` 이다. <br>
이 abstract class는 ``WebMvcConfigurer`` 라는 interface를 구현했는데 이는 원하는 method만 override하면 실행되도록 하기 위함이다. <br>
해당 method가 어떤 설정에 해당하는지 알아보자.
[spring docs](http://docs.spring.io/spring/docs/4.3.0.RC2/spring-framework-reference/htmlsingle/#mvc-config-enable)

```java
public abstract class WebMvcConfigurerAdapter implements WebMvcConfigurer {

	@Override
	public void configurePathMatch(PathMatchConfigurer configurer) {
	}
	@Override
	public void configureContentNegotiation(ContentNegotiationConfigurer configurer) {
	}
	@Override
	public void configureAsyncSupport(AsyncSupportConfigurer configurer) {
	}
	@Override
	public void configureDefaultServletHandling(DefaultServletHandlerConfigurer configurer) {
	}
	@Override
	public void addFormatters(FormatterRegistry registry) {
	}
	@Override
	public void addInterceptors(InterceptorRegistry registry) {
	}
	@Override
	public void addResourceHandlers(ResourceHandlerRegistry registry) {
	}
	@Override
	public void addCorsMappings(CorsRegistry registry) {
	}
	@Override
	public void addViewControllers(ViewControllerRegistry registry) {
	}
	@Override
	public void configureViewResolvers(ViewResolverRegistry registry) {
	}
	@Override
	public void addArgumentResolvers(List<HandlerMethodArgumentResolver> argumentResolvers) {
	}
	@Override
	public void addReturnValueHandlers(List<HandlerMethodReturnValueHandler> returnValueHandlers) {
	}
	@Override
	public void configureMessageConverters(List<HttpMessageConverter<?>> converters) {
	}
	@Override
	public void extendMessageConverters(List<HttpMessageConverter<?>> converters) {
	}
	@Override
	public void configureHandlerExceptionResolvers(List<HandlerExceptionResolver> exceptionResolvers) {
	}
	@Override
	public void extendHandlerExceptionResolvers(List<HandlerExceptionResolver> exceptionResolvers) {
	}
	@Override
	public Validator getValidator() {
		return null;
	}
	@Override
	public MessageCodesResolver getMessageCodesResolver() {
		return null;
	}
}
```

``public void configurePathMatch(PathMatchConfigurer configurer)`` 는 ``<mvc:path-matching>`` 태크와 같은 역할을 한다.<br>
suffix-pattern, trailing-slash, registered-suffixes-only, path-helper, path-matcher 등을 등록할 수 있다.

``public void configureContentNegotiation(ContentNegotiationConfigurer configurer)`` 는 <br>
``<mvc:annotation-driven content-negotiation-manager="??"/>`` tag를 대신한다. <br>
content-negotiation은 어떤 type의 content를 보내줄지 클라이언트에게 위임하는 것이다.

``public void configureAsyncSupport(AsyncSupportConfigurer configurer)``는 <br>
spring 내에서 async한 task를 하고자 할 때 thread pool과 타임아웃, taskexecuter등을 설정한다.

``public void configureDefaultServletHandling(DefaultServletHandlerConfigurer configurer)`` 는 어떤 servlet과도 match가 안될때 갈 deafultServlet을 설정한다.

``public void addFormatters(FormatterRegistry registry)`` 는 ``<mvc:annotation-driven conversion-service="??"/>`` 태그 역할을 한다.

``public void addInterceptors(InterceptorRegistry registry)`` 는 interceptor 를 등록하는 부분이다.

``public void addResourceHandlers(ResourceHandlerRegistry registry)``는 html, css, js 같은 static resources 들을 처리하는 handler를 등록한다.

``public void addCorsMappings(CorsRegistry registry)``는 cross origin resource sharing을 위한 메소드로 이곳에서의 설정은 global하게 적용된다.

``public void addViewControllers(ViewControllerRegistry registry)`` static한 view를 등록하는 곳인데 잘 안 쓴다.

``public void configureViewResolvers(ViewResolverRegistry registry)`` view template를 처리하는 resolver를 등록한다. suffix나 prefix처리를 할 수 있다.

``public void addArgumentResolvers(List<HandlerMethodArgumentResolver> argumentResolvers)`` user로 부터 넘어온 값을 바로 model이나 Object로 받을 수 있다. <br>
	하지만 Model과 1:1 parameter mapping 이 안되거나, form object가 아니거나, request body에 값이 없으면 mapping이 제대로 안될 수 있다<br>
	이런 경우 addArgumentResolvers를 이용해 특정 행동을 하는 argumentResolver를 추가할 수 있다.

``public void addReturnValueHandlers(List<HandlerMethodReturnValueHandler> returnValueHandlers)`` 컨트롤러에서 특정 타입의 value를 반환 할 때 이를 처리하는  handler이다.

``public void configureMessageConverters(List<HttpMessageConverter<?>> converters)``  특정 mime에 대한 converter를 등록한다. jackson이 많이 쓰인다.. 이걸 쓰면 기존 default들이 다 turn off된다.

``public void extendMessageConverters(List<HttpMessageConverter<?>> converters)``  default를 냅두고 custom 한가지만 집어 넣는다.

``public void configureHandlerExceptionResolvers(List<HandlerExceptionResolver> exceptionResolvers)``  Exception 발생시 어떻게 해야할지 알려준다. default들은 turn off 시킨다. 

``public void extendHandlerExceptionResolvers(List<HandlerExceptionResolver> exceptionResolvers) `` 기존 default handler 를 확장한다.

``public Validator getValidator()`` validator 등록

``public MessageCodesResolver getMessageCodesResolver()`` 에러 방생시 error code와 Object name으로 사용할 message code를 리턴한다.






