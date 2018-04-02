

1. /etc/environment

시스템 단계에서 설정하는 파일

모든 유저들에게 적용됨

왠만하면 건들지 말자.

 
2. ~/.profile

각 사용자마다 개별적으로 가지고있는 스크립트 파일

 
3. /etc/profile 아니면 /etc/profile.d/*.sh

~/.profile과 유사하지만 전역 스크립트.

이게 먼저 실행되고 개별 ~/.profile이 실행된다.

( /etc/profile이 /etc/profile.d/ 안에 있는 모든 *.sh 스크립트들을 실행시킴)


