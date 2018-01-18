2018/01/18

``OS``에서 Cache 정책

읽기 정책은 둘다  같다. 가장 가까운 캐시에 있으면 hit, 없으면 miss로 아래 단계 cache 또는 memory에 접근하여 hit 할 때 까지 반복한다.

쓰기의 경우 다음 2가지 정책이 존재한다.

1. ``write-through``
  cache에 write 하고, 다음 cache에 또 write하고 .. 메모리까지 한번에 write한다.

  장점은 로직이 매우 단순하다. 반면 write 작업의 overhead가 커진다. 같은 메모리를 지속적으로 변경하는 작업을 수행한다면,

  모든 level의 cache,memory를 write해야하기 때문에 불필요한 자원소모가 생긴다.  

2. ``write-back``
  우선 cache에 write를 하고, dirty bit를 assgin한다. 하위 계층으로 넘어가지 않는다.

  그리고 dirty bit이 할당된 cache block을 cache에서 제거해야 할 때, 그 때 하위 계층으로 write 작업을 진행한다.

  단점은 로직이 상대적으로 복잡하다. dirty bit를 고려해야 하며 data가 통일되지 않은 state가 오래 존재하기 때문에 이를 생각해야한다.

  또한 멀티 코어의 경우 다른 코어에서는 코어 내부의 cache가 unvisible 하기 때문에 이를 관리하는 장치가 필요하다.

  장점으로는 write 오버헤드가 낮아서 성능상 이득이 있다.

