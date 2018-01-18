2018/10/17

``Spring security``에서의 custom validator pattern

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

```java
@Target({ElementType.TYPE, ElementType.FIELD, ElementType.ANNOTATION_TYPE})
@Retention(value = RetentionPolicy.RUNTIME)
@Constraint(validatedBy = EmailValidator.class)
@Documented
public @interface ValidEmail {

}
```

```java
public class EmailValidator implements ConstraintValidator<ValidEmail, String> {
	
	private Pattern pattern;
	private Matcher matcher;
	private static final String EMAIL_PATTERN = "^[_A-Za-z0-9-+]+ (.[_A-Za-z0-9-]+)*@" + 
	"[A-Za-z0-9-]+(.[A-Za-z0-9]+)*(.[A-Za-z]{2,})$";
	@Override
	public void initialize(ValidEmail constriantAnotation) {
		
	}
	
	@Override
	public boolean isValid(String email, ConstraintValidatorContext context) {
		return (validateEmail(email));
	}
	
	private boolean validateEmail(String email) {
		pattern = Pattern.compile(EMAIL_PATTERN);
		matcher = pattern.matcher(email);
		return matcher.matches();
	}
}
```