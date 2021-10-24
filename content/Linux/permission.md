## unix file permission
3 가지 permission 종류가 있다.

- r - read
- w - write
- x - execute

그리고 file 일 때와 directory 일 때 다른 의미를 갖는다.
``File``
- read - you can open, read and copy the file.
- write - you can modify the file.
- execute - you can execute the file if it's executable.

``directory``
- read - you can ``ls`` the directory and see the contents.
- write - you can make and removes files in the directory.
- execute - you can ``cd`` into that directory.

``ls -l`` 을 하면 파일의 permission을 볼 수 있다.
총 10개의 구분자로 되어 있다.
[-  ---  ---  --- ]    [owner]   [group]
맨 앞은 directory인지 구분.
다음 3개씩의 구분은 rwx 를 표현하는 3 쌍이다.
맨 처음은 owner의 권한, 그 다음은 group에 대한 권한, 마지막은 나머지 모두에 대한 권한이다.

권한을 바꾸고 싶을 경우 ``chmod`` 키워드를 사용한다.
- read : 4
- write: 2
- execute: 1
의 값으로 계산해서 더한 것을 권한으로 한다. 즉
```shell
chmod 777 /myfolder
```
라는 명령어는 myfolder에 owner, group에 상관없이 모든 권한을 주겠다는 뜻이다.
