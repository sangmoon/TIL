# docker의 기본 명령어를 정리하자

도커 이미지 빌드

```shell
docker build -t cholsoo22001/orly .
```

container 실행

```shell
docker run \
    --env AZURE_ACCOUNT_NAME="" \
    --env AZURE_ACCOUNT_KEY="" \
    -p 8080:8080 \
    cholsoo22001/orly
```

Docker Hub에 이미지 배포

```shell
docker push cholsoo22001/orly
```

Docker images 확인

```shell
docker images
```

Docker image 삭제

```shell
docker rmi [image id]
```

모든 Container 확인

```shell
docker ps -a
```

Container 삭제

```shell
docker rm [container id | container name]
```

Container shell로 들어가기

```shell
docker exec -it [container id| container name] /bin/bash
```