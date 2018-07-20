# Chapter2

## Item 1 - Consider static factory methods instead of constructors

### Pros

- unlike constructors, they have name
- They are not required to create a new objevt each time they're invoked
- they can return an object of any subtype of their return type
- the class of the returned object can  vary from call to call as a function of the input parameters
- the class of the returned object need not exist when te class containing the method written

### Cons

- classess without public or protected constructors cannot be subclassed
- they are hard for programmers to find

## Item 2 - Consider a builder when faced with many constructor parameters

```java
// telescopnig pattern - does not scale well
public class NutritionFacts {
    private final int servingSize;
    private final int servings;
    private final int calories;
    private final int fat;
    private final int sodium;
    private final int carbohydrate;

    public NutritionFacts(int servingSize, int servings) {
        this(servingSize, servinigs, 0);
    }

    public NutritionFacts(int servingSize, int servings, int calories) {
        this(servingSize, servings, calories, 0);
    }

    public NutritionFacts(int servingSize, int servings,
            int calories, int fat) {
        this(servingSize, servings, calories, fat, 0);
    }

    public NutritionFacts(int servingSize, int servings,
            int calories, int fat, int sodium) {
        this(servingSize, servings, calories, fat, sodium ,0);
    }

    public NutritionFacts(int servingSize, int servings,
            int calories, int fat, int sodium, int carbohydrate) {
        this.servingSize = servingSize;
        this.servings = servings;
        this.calories = calories;
        this.fat = fat;
        this.sodium = sodium;
        this.carbohydrate = carbohdrate;
    }
}

NutritionFacts cocaCola = new NutiritionFacts(240, 8, 100, 0, 35, 27);
```

> In the Telescoping pattern, it is hard to write client code when there are many parameters, and hareder still to read it.

```java
// javabean pattern - allows inconsistency, mandates mutability
public class NutritionFacts {
    private int servingSize = -1;
    private int serving = -1;
    private int calories = 0;
    private int fat = 0;
    private int sodium = 0;
    private int carbohydrate = 0;

    public NutritionFacts() {}

    public setServingSize(int val) { servingSize = val; }
    public setServings(int val) { servings = val; }
    public setCalories(int val) { calories = val; }
    public setFat(int val) { fat = val; }
    public setSodium(int val) { sodium = val; }
    public setCarbohydrate(int val) { carbohydrate = val; }
}

NutritionFacts cocaCola = new NutritionFacts();
cocaCola.setServingSize(240);
cocaCola.setServings(8);
cocaCola.setCalories(100);
cocaCola.setSodium(35);
cocaCola.setCarbohydrate(27);
```

> a JavaBean may be in an inconsistent state partway through its construction.
> It precludes the possibility of marking a class immutable.

```java
//builder pattern
public class NutritionFacts {
    private final int servingSize;
    private final int servings;
    private final int calories;
    private final int fat;
    private final int sodium;
    private final int carbohydrate;

    public static class Builder {
        private final int servingSize;
        private final int servings;

        private int calories = 0;
        private int fat = 0;
        private int sodium = 0;
        private int carbohydrate = 0;

        public Builder(int servingSize, int servings) {
            this.servingSize = servingSize;
            this.servings = servings;
        }

        public Builder calories(int val) { calories = val; return this; }
        public Builder fat(int val) { fat = val; return this; }
        public Builder sodium(int val) { sodium = val; return this; }
        public Builder carbohydrate(int val) { carbohydrate = val; return this; }

        public NutritionFacts build() {
            return new NutritionFacts(this);
        }
    }

    private NutritionFacts(Builder builder) {
        this.servingSize = builder.servingSize;
        this.servings = builder.servings;
        this.calories = builder.calories;
        this.fat = builder.fat;
        this.sodium = builder.sodium;
        this.carbohydrate = builder.carbohdrate;
    }
}

NutritionFacts cocaCola = new NutritionFacts.Builder(240, 8)
    .calrories(100).sodium(35).carbohydrate(27).build();
```

> The builder pattern simulates named optional parameters as found in Python and Scala

```python
# optional named parameter example in python
def func(object, optional_param1=1, optional_param2=10):
    pass

func("A")    # func("A", 1, 10)
func("A", 2) # func("A", 2, 10)
func("A", optional_param2=2)  # func("A", 1, 2)
func(optional_param1=2, object="B")  # func("B", 2, 10)
```

> The builder pattern is well suited to class hierarchies

```java
public  abstract class Pizza {
    public enum Topping { HAM, MUSHROOM, ONION, PEPPER, SAUSAGE }
    final Set<Topping> toppings;

    abstract static class Builder<T extends Builder<T>> {
        EnumSet<Topping> toppings = EnumSet.noneOf(Topping.class);
        public T addTopping(Topping  topping) {
            toppings.add(Objects.requireNotNull(topping));
            return self();
        }

        abstract Pizza build();

        protected abstract T self();
    }
    Pizza(Builder<?> builder) {
        toppings = builder.toppings.clone();
    }
}
```

```java
public class NyPizza extends Pizza {
    public enum Size { SMALL, MEDIUM, LARGE }
    private final Size size;

    public static class Builder extends Pizza.Builder<Builder> {
        private final Size size;

        public Builder(Size size) {
            this.size = Objects.requireNotNull(size);
        }

        @Override public NyPizza build() {
            return new NyPizza(this);
        }

        @Override protected Builder self(){ return this; }
    }

    private NyPizza(Builder builder) {
        super(builder);
        size = builder.size;
    }
}

NyPizza pizza = new NyPizza.Builder(SMALL).addTopping(SAUSAGE).addTopping(ONION).build();
```

> builders can have multiple varargs parameters because each parameter is specified in its own method
> the builder pattern is quite flexible. single builder can be used repeatedly to buld multiple objects.
> builder can fill in some fields automatically

```java
void multiVarargs(String... params1, String... params2); //not allowed
```

### Pros

- client code is much easier to read and write than telescoping
- builder are much safer than javaBean
- well suited to class hierarchies
- can simulate optional named parameters
- can have multiple varagrs parameters

### Cons

- must first create its builder
- it is verbose somehow. there are enough parameters to make it worthwhile

### 결론

> the builder pattern is a good c hoice when designing classes whose constructors or 
> static factories whould have more than a handful of parameters.

## Item 3 - Enforce the singleton property with a private constructor or an enum type

- 싱글톤은 클라이언트에서 테스팅 하기 어렵다. mock 하는게 불가능해서.
