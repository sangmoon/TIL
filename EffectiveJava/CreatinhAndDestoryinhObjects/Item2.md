## Item 2 Consider a builder when faced with many constructor parameters

**Static factory** 와 **constructor** 는 같은 문제를 공유한다 - 많은 수의 optional parameter를 처리 하기 힘들다.
전통적으로 많은 파라미터를 같는 경우 ***telescoping constructor*** 패턴이 사용된다.

```java
// Telescoping constructor pattern - scale을 키우기 쉽지 않다
public class NutritionFacts {
    private final int servingSize;
    private final int servings;
    private final int calories;
    private final int fat;
    private final int sodium;
    private final int carbohydrate;

    public NutritionFacts(int servingSize, int servings) {
        this(servingSize, servings, 0);
    }

    public NutritionFacts(int servingSize, int servings, int calories) {
        this(servingSize, servings, calories, 0);
    }

    public NutritionFacts(int servingSize, int servings, int calories, int fat) {
        this(servingSize, servings, calories, fat, 0);
    }

    public NutritionFacts(int servingSize, int servings, int calories, int fat, int sodium) {
        this(servingSize, servings, calories, fat, sodium, 0);
    }

    public NutritionFacts(int servingSize, int servings, int calories, int fat, int sodium, int carbohydrate) {
       this.servingSize = servingSize;
       this.servings = servings;
       this.scalories = calories;
       this.fat = fat;
       this.sodium = sodium;
       this.carbohydrate = carbohydrate;
    }
}
```

새롭게 객체를 만들고 싶으면 다음과 같이 만든다.

```java
NutritionFacts cocaCola = new NutritionFacts(240, 8, 100, 0, 35, 27);
```

parameter가 6개면 위처럼 할 수 있지만 더 많아지면 생성자가 너무 많아진다. 또한 코드를 읽기도 어렵다.
같은 type의 변수를 여러개 나열하면 client가 사용시 순서를 뒤집어 런타임 오류를 발생 시킬 수도 있다.

두번째 방법은 ***JavaBeans Patten*** 이다. 파라미터 없는 생성자를 호출한 후 setter를 호출해 파라미터를 채워준다.

```java
public class NutritionFacts {
    private final int servingSize;
    private final int servings;
    private final int calories;
    private final int fat;
    private final int sodium;
    private final int carbohydrate;

    public NutritionFacts(){};

    public void setServingSize(int val) { servingSize = val }
    public void setServings(int val) { servings = val }
    public void setCalories(int val) { calories =  val}
    public void setFat(int val) { fat = val }
    public void setSodium(int val) { sodium = val }
    public void setCarbohydrate(int val) { carbohydrate = val }
}
```

이 패턴의 경우 텔레스코핑 패턴의 단점은 없다. 생성자는 단순 하나이며 원하는 값만 채워주면 된다.
그러나 심각한 단점은 객체 생성과 setter 호출 사이에 비정상적인 state가 존재한다는 것이다.
**Javabean 패턴은 imutable 한 class 를 만들 수 있는 가능성을 배제한다**(Item 17) 에서 볼 수 있듯
쓰레드 세이프한 클래스를 위해선 별도의 작업이 필요하다.

이러한 단점들을 보완한 Builder Pattern이 있다. 보통 해당 클래스의 static member class로 만든다.

```java
public class NutritionFacts {
    private final int servingSize;
    private final int servings;
    private final int calories;
    private final int fat;
    private final int sodium;
    private final int carbohydrate;

    public static class Builder() {
        private final int servingSize;
        private final int servings;
        private final int calories;
        private final int fat;
        private final int sodium;
        private final int carbohydrate;

        public Builder(int servingSize, int servings) {
            this.servingSize = servingSize;
            this.servings = servings;
        }

        public Builder calories(int val) {
            calroies = val;
            return this;
        }

        public Builder fat(int val) {
            fat = val
            return this;
        }

        public Builder sodium(int val) {
            sodium = val;
            return this;
        }

        pubic Builder carbohydrate(int val) {
            carbohydrate = val;
            return this;
        }

        public NutritionFacts build() {
            return new NutritionFacts(this);
        }



    }

    private NutritionFacts(Builder builder){
        servingSize = builder.servingSize;
        servings = builder.servings;
        calories = builder.calories;
        fat = builder.fat;
        sodium = builder.sodium;
        carbohydrate = builder.carbohydrate;
    };
}
```

이러한 빌더 패턴은 읽기 쉽다. 파이썬이나 스칼라의 optional named parameter와 유사하다. 또한 클래스 상속에서도 장점이 있다.

```java
public abstract class Pizza {
    public enum Topping { HAM, MUSHROOM, ONION, PEPPER, SAUSAGE }
    final Set<Topping> toppings;

    abstract static class Builder<T extends Builder<T>> {
        EnumSet<Topping> toppings = EnumSet.noneOf(Topping.class);
        public T addTopping(Topping topping) {
            toppings.add(Objects.requireNonNull(topping));
            return self();
        }

        abstract Pizza build(); 

        // Subclass는 자기 자신을 돌려주기 위해 반드시 이 메소드를 오버라이딩 해야 한다.
        protected abstract T self();
    }

    Pizza(Builder<?> builder) {
        toppings = builder.toppings.clone(); // See Item 50
    }
}
```

```java
public class NyPizza extends Pizza {
    public enum Size { SMALL, MEDIUM, LARGE }
    private final Size size;

    public static class Builder extends Pizza.Bulder<Builder> {
        private final Size size;

        public Builder(Size size) {
            this.size = Objects.requireNonNull(size);
        }

        @Overide public NyPizza() {
            return new NyPizza(this);
        }

        @Override protected Builder self() {return this;}
    }

    private NyPizza(Builder builder) {
        super(builder);
        size = builder.size;
    }
}

public class Calzone extends Pizza {
    private final boolean sauceInside;

    public static class Builder extends Pizza.Builder<Builder> {
        private boolean sauceInside = false;

        public Builder sauceInside() {
            sauceInside = true;
            return this;
        }

        @Override public Calzone build() {
            return new Calzone(this);
        }

        @Override protected Builder self() { return this; }
    }

    private Calzone(Builder builder) {
        super(builder);
        sacueInside = buider.sauceInsde;
    }
}
```

Pizza.Builder 는 recursive type parameter인 generic type(ITEM 30) 임을 기억하자.
이를 통해 캐스팅 없이 체이닝이 가능하다.(안한다면 다 Pizza의 Builder이므로 사용이 제한됨...)

빌더 패턴의 단점 중 나나느 빌더 객체를 꼭 만들어야 한다는 점이다. 퍼포먼스가 중요한 곳에선 문제를 야기할 수 있다. 텔레스코핑 만큼 verbose 하므로 최소 생성자 인자가 4개 이상인 상황에서 써야 한다.

요약하면 빌더 패턴은 생성자나 스태틱 팩토리의 인자가 많을 때 쓸 수 있는 좋은 방식이다.
