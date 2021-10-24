## Chain of responsibility
어떤 프로세스가 일어 났을때 그 책임을 적당한 대상한테 넘겨주게 됩니다.
이 패턴은 하나의 클래스의 인스턴스들 간의 체인이라기보다는 여러 클래스 간에 걸쳐 이루어지는 일이기 때문에 구조가
다른 클래스에 대해서 낮은 결합도로 동일한 이벤트에 대한 핸들링을 가능하게 한다는 점에서 주목할 만합니다.
사슬에 들어가는 객체를 바꾸거나 순서를 바꿈으로써 역할을 동적으로 추가/제거 할 수 있습니다.

### Intent <br>
둘 이상의 오브젝트에 요청을 처리 할 수있는 기회를 주면 요청 송신자와 수신자를 연결하지 마십시오. 
수신 객체를 연결하고 객체가 처리 할 때까지 체인을 따라 요청을 전달합니다.

### Implementation <br>
class Handler{
	private int id;
	private Handler nextChain;

	public Handler add(Handler next) {
		if (!nextChain){
			nextChain = next;
		} else {
			nextChain.add(next);
		}
	}
}
// main(client) 에서는 handler의 종류를 알 필요가 없으므로
// manager class를 두어 chain을 생성하거나, 맨 앞 chain만 외부로 노출시킨다. 
// 하지만 여기선 복잡해져서 그런건 생각하지 않았다
### Consequences <br>
1. 결합도를 감소시킨다. 이 패턴은 어떤 object가 request를 처리하는지 몰라도 된다.
모든 object에 대한 참조를 갖지 않고, 하나의 successor에 대한 참조만 하면 된다.
2. 객체에 책임을 주는데 유연성이 생긴다.
3. 요청이 수행된다는 보장이 없다.
4. 처리하는데 걸리는 시간을 정확히 예측할 수 없다.