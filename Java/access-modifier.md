java 에는 4개의 access modifier 가 있다.
1. public ()
2. protected
3. default(package private)
4. private

위의 순서대로 public에 가까울 수록 제한이 적고, private에 갈수록 제한이 커진다.

```java
            | Class | Package | Subclass | Subclass | World
            |       |         |(same pkg)|(diff pkg)| 
————————————+———————+—————————+——————————+——————————+————————
public      |   +   |    +    |    +     |     +    |   +     
————————————+———————+—————————+——————————+——————————+————————
protected   |   +   |    +    |    +     |     +    |         
————————————+———————+—————————+——————————+——————————+————————
default     |   +   |    +    |    +     |          |    
————————————+———————+—————————+——————————+——————————+————————
private     |   +   |         |          |          |    

+ : accessible
blank : not accessible
```

https://stackoverflow.com/questions/215497/in-java-difference-between-package-private-public-protected-and-private