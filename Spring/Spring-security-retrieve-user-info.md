2018/01/25

# 스프링 시큐리티로 유저 정보 얻기! 

1. Bean으로 부터 유저 정보 얻기
``SecurityConytextHolder``  로 부터 현재 인증된 principal을 얻을 수 있다.
```java
Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
String currentPrincipalName = authentication.getName();	
```
체크하기 전에 유저가 있는지 체크할 수 있다.
```java
Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
if (!(authentication instanceof AnonymousAuthenticationToken)) {
    String currentUserName = authentication.getName();
    return currentUserName;
}
```
하지만 static call은 좋지 않다... 

2. 컨트롤러에서는 ``(@Controller)`` 추가적인 방법이 가능하다. ``Principal`` 에 method argument로 접근이 가능하다.
```java
import java.security.Principal;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;
 
@Controller
public class SecurityController {
 
    @RequestMapping(value = "/username", method = RequestMethod.GET)
    @ResponseBody
    public String currentUserName(Principal principal) {
        return principal.getName();
    }
}
```
``authentication`` token 으로 접근 할 수도 있다.
```java
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;
 
@Controller
public class SecurityController {
 
    @RequestMapping(value = "/username", method = RequestMethod.GET)
    @ResponseBody
    public String currentUserName(Authentication authentication) {
        return authentication.getName();
    }
}
```
HTTP request로 부터 직접 접근도 가능하다.
```java
import java.security.Principal;
 
import javax.servlet.http.HttpServletRequest;
 
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;
 
@Controller
public class SecurityController {
 
    @RequestMapping(value = "/username", method = RequestMethod.GET)
    @ResponseBody
    public String currentUserNameSimple(HttpServletRequest request) {
        Principal principal = request.getUserPrincipal();
        return principal.getName();
    }
}
```

3. Spring의 DI를 이용하면 컨트롤러가 아니어도 어디서든 접근이 가능하다! 이를 위해 간단한 인터페이스를 구성하자.
```java
public interface IAuthenticationFacade {
    Authentication getAuthentication();
}
@Component
public class AuthenticationFacade implements IAuthenticationFacade {
 
    @Override
    public Authentication getAuthentication() {
        return SecurityContextHolder.getContext().getAuthentication();
    }
}
```
DI를 활용해 다음과 같이 decoupled 시켜서 스프링의 장점을 활용할 수 있다.
```java
@Controller
public class SecurityController {
    @Autowired
    private IAuthenticationFacade authenticationFacade;
 
    @RequestMapping(value = "/username", method = RequestMethod.GET)
    @ResponseBody
    public String currentUserNameSimple() {
        Authentication authentication = authenticationFacade.getAuthentication();
        return authentication.getName();
    }
}
```

4. JSP 에서는 어떻게 가져오지?

현재 인증 정보는 JSP에서 접근 할 수도 있다.

우선 ``spring-security-taglib``를 pom.xml에 추가하고

```jsp 
<%@ taglib prefix="security" uri="http://www.springframework.org/security/tags" %>
```

라고 jsp에 include하면 된다.

```jsp
<security:authorize access="isAuthenticated()">
    authenticated as <security:authentication property="principal.username" /> 
</security:authorize>
```

그러면 위와 같이 접근 할 수 있다.

다음 두 곳을 참조하였다.

[Baeldung](http://www.baeldung.com/get-user-in-spring-security)

[github-project](https://github.com/eugenp/tutorials/tree/master/spring-security-rest-custom#readme)