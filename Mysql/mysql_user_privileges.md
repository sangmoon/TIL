2018/01/29

이번에 컴퓨터 ip 변경으로 인해 새로운 작업 환경을 구축하던 중 mysql connection이 튕겨서 문제 발생. <br>
```sql
select user, host from mysql.users
```
를 통해 보니 user name과 host가 구분되어 있어 host ip가 달라지면 접속이 안되는 현상임을 알았다. <br>
기존 유저에 변경하려다가 잘 안되서 그냥 현재 ip에 새로운 유저를 등록하고 권한을 주기로 함.
```sql
mysql -u root -p
mysql> CREATE USER 'username'@'1.2.3.4' IDENTIFIED BY 'password';
    -> GRANT ALL PRIVILEGES ON *.* TO 'username'@'1.2.3.4' WITH GRANT OPTION;
```
[참조 stackoverflow](https://stackoverflow.com/questions/7864276/cannot-connect-to-database-server-mysql-workbench)