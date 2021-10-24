## Always override toString

``Object`` 가 default toString 메소드를 제공하지만 사람이 읽기에 충분치 한다.
[해당 클래스이름]@[Hexa hashcode] 형태를 이루고 있다. 따라서 모든 하위 클래스에서
toString을 override 하는게 좋다. 그리고 특정 포멧을 결정하든 말든 주석으로 의도를 명확히 써놓아야 한다.
