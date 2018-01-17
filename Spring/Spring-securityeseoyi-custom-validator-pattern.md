2018/10/17
Spring security에서의 custom validator pattern
```java
// User.java

@Entity(name="user")
@PasswordMatches
public  class User {
  //중략..
  @ValidEmail
  @NotNull
  @NotEmpty
  private String email;
}
```
- ``PasswordMatches``의 경우 confirm field와 password field를 비교하기에 User 만들 때 사용..
- ``ValidEmail``의 경우 Email 형식인지 확인

```java
@Target({ElementType.TYPE, ElementType.ANNOTATION_TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = PasswordMatchesValidator.class)
@Documented
public @interface PasswordMatches {
	String message() default "Passwords don't match";
	Class<?>[] groups() default {};
	Class<? extends Payload>[] payload() default {};
}
```

```java
//PasswordMatchesValidator
public class PasswordMatchesValidator 
	implements ConstraintValidator<PasswordMatches, Object>{
		@Override
		public void initialize(PasswordMatches constrainAnnotation) {}
		
		@Override
		public boolean isValid(Object obj, ConstraintValidatorContext context) {
			User user = (User) obj;
			return user.getPassword().equals(user.getMatchingPassword());
		}
}
```