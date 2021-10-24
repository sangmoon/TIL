# java.util.Collection

- List 중복 허용
- Set, SortedSet, NavigableSet 중복 불가
- Queue, Deque concurrency 위해서..

- Map, SortedMap, NavigableMap

equals/hashCode
Iterator(한 방향)/ListIterator(양 방향)
Collections class(cf. Arrays class)
Vector, Hashable, Enumeration => legacy! 쓰지마셍...
Wrappers: unmodifiable, synchronized, checked

## java.util.concurrent

- BlockingQueue
 > 모든 큐 기반 동시 콜렉션의 기본에있는 인터페이스. BlockingQueue에 요소를 추가하는 동안, 공간이 없으면 사용 가능하게 될 때까지 기다릴 수 있고 검색 할 때 요소가 비어있을 때까지 사용할 수있을 때까지 대기합니다.
- ArrayBlockingQueue
 > Array를 기반으로 한 blocking queue 입니다. 일단 인스턴스화되면 사이즈를 조정할 수 없다.
- SynchronousQueue
 > 용량이 9인 blocking queue입니다.
- PriorityBlockingQueue
 > blocking queue에 기반한 우선순휘 큐. unbounded 입니다.
- LinkedBlockingQueue
 > 선택적으로 bounded 할 수 있는 queue이다.
- DelayQueue
 > 일정 기간이 지난 element 만 빼낼 수 있다. unbounded queue 이다.
- BlockingDeque
 > blockingqueue 에 deque 의 명세가 있는 인터페이스 이다.
- LinkedBlockingDeque
 > linked node로 blockingdeque 구현했다.
- TransferQueue
 > producer 가 Element를 넣고 consumer가 receive 할 때 까지 기다리는 method가 있는 blocking queue.
- LinkedTransferQueue
 > transferqueue 구현체.
- ConcurrentMap
 > thread safety 와 atomicity 가 보장된 map interface
- ConcurrentHashMap
 > concurrent map 구현체
- ConcurrentNavigableMap
 > a Java concurrent collection interface that extends ConcurrentMap and adds operations of NavigableMap.
- ConcurrentSkipListMap
 > ConcurrentNavigableMap 구현체.