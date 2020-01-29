## Item 9: Prefer try-with-resources to try-finally

InputStream이나 sql.Connection 등은 close() 를 꼭 불러주어야 한다.
전통적으로는 try, catch 문이 이를 지원하였다.

```java
static String firstLineOfFile(String path) throws IOException {
    BufferedReader br = new BufferedReader(new FileReader(path));
    try {
        return br.readLine();
    } finally {
        br.close();
    }
}
```

하지만 자원이 여러개가 되면 굉장히 이상해진다.

```java
static void copy(String src, String dst) throws IOException {
    InputStream in = new FileStream(src);
    try {
        OutputStream out = new FileOutputStream(dst);
        try {
            byte[] buf = new byte[BUFFER_SIZE];
            int n;
            while((n = in.read(buf) >= 0)) {
                out.write(buf, 0, n);
            }
        } finally {
            out.close();
        }
    } finally {
        in.close();
    }
}
```
위 예제에서 device 문제로 Exception이 발생하면 첫번째 Exception은 먹히게 된다. 디버깅에 굉장히 안 좋음...

java7에 나온 try-with-resources 를 이용하면 이 문제는 해결된다. 이를 위해 해당 자원은 AutoCloseable 인터페이스를 구현해야 한다.

```java
static void copy(String src, String dst) throws IOException {
    try (InputStream in = new FileInputStream(in);
        OutputStream out = new FileOutputStream(dst)) {
        byte[] buf = new byte[BUFFER_SIZE];
        int n;
        while((n = in.read(buf) >= 0)) {
            out.write(buf, 0, n);
        }
    }
}
```

더 간결하고 읽기 쉬워졌다.