# Stream IO

java.io package 에 선언되어 있다.

- ByteStream 은 말 그대로 Byte 단위의 입출력을 담당한다.
    InputStream/OutputStream

- CharacterStream 은 Java char, 2Byte 단위로 작동한다.

Reader/Writer 가 두 Stream 간의 interface 역할을 한다.

ByteStream -> CharacterStream 해주는게 InputStreamReader
CharacterStream -> ByteStream 해주는게 OutputStreamWriter

## NIO

stream IO 는 non-blocking IO가 없다. 다 blocking임. 대용량 처리 같은 거할 때 critical 하다.
그래서 java.nio package 사용.
stream이 아니라 buffer 기본으로 사용.

Channel 사용 (FileChannel, SocektChannel)
Selector (epoll 로 구현)
Multiplexing/Nonblocking 에 유리

NIO Direct Buffer

- ByteBuffer.allocateDirect
  java heap에 할당하지 않고 그냥 malloc 호출
  내부적으로 요청한 크기만큼 할당
