## Proxy Pattern

### Intent <br>
>> 일반적으로 프록시는 다른 무언가와 이어지는 인터페이스의 역할을 하는 클래스이다. 프록시는 어떠한 것(이를테면 네트워크 연결, 메모리 안의 커다란 객체,
>> 파일, 또 복제할 수 없거나 수요가 많은 리소스)과도 인터페이스의 역할을 수행 할 수 있다. 

참가자 : ``client``, ``subject``, ``real subject``, ``proxy``

- 같은 인터페이스를 상속 받기 때문에 실제 client는 real subject와 proxy 를 구분하지 않는다.
- proxy 는 real subject에 대한 reference를 가지고 있다.
- proxy 는 real subject에 대한 접근을 통제하고 생성,제거할 책임이 있다.

- ``remote proxy``: 다른 주소 공간에 있는 real subject로 request를 중계한다.
- ``virtual proxy``: real subject에 대한 추가 정보를 cache 해서 real object 생성을 최대한 연기한다.
- ``protection proxy``: caller가 권한이 있는지 체크한다. ``real subject``는 기능에만 충실

### Implementation <br>
```java
interface Image {
    public void displayImage();
}

// On System A
class RealImage implements Image {

    private String filename = null;
    /**
     * Constructor
     * @param filename
     */
    public RealImage(final String filename) {
        this.filename = filename;
        loadImageFromDisk();
    }

    /**
     * Loads the image from the disk
     */
    private void loadImageFromDisk() {
        System.out.println("Loading   " + filename);
    }

    /**
     * Displays the image
     */
    public void displayImage() {
        System.out.println("Displaying " + filename);
    }

}

// On System B
class ProxyImage implements Image {

    private RealImage image = null;
    private String filename = null;
    /**
     * Constructor
     * @param filename
     */
    public ProxyImage(final String filename) {
        this.filename = filename;
    }

    /**
     * Displays the image
     */
    public void displayImage() {
        if (image == null) {
           image = new RealImage(filename);
        }
        image.displayImage();
    }

}

class ProxyExample {

   /**
    * Test method
    */
   public static void main(final String[] arguments) {
        final Image image1 = new ProxyImage("HiRes_10MB_Photo1");
        final Image image2 = new ProxyImage("HiRes_10MB_Photo2");

        image1.displayImage(); // loading necessary
        image1.displayImage(); // loading unnecessary
        image2.displayImage(); // loading necessary
        image2.displayImage(); // loading unnecessary
        image1.displayImage(); // loading unnecessary
    }
}
```
### Consequences <br>
1. remote proxy는 real object가 다른 address space에 있다는 것을 숨긴다.
2. virtual proxy는 객체 생성을 최적화 할 수 있다.(on demand)
3. real object에 접근할 때 추가적인 작업을 할 수 있게 해준다.