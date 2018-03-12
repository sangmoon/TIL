## odoo-install

어려운 작업이다. window에 python package를 설치한다는 것은...
git bash를 이용해 pip을 활용해서 많이 설치가 가능하다.

마지막으로 git bash에서
```bash
python ./odoo-bin --addons-path=addons -r sangmoon -w 1123 --db_host localhost --db_port 5432
```
하면 잘 된다.