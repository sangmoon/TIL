spring에서 파일 업로드는 2가지 방식을 택할 수 있다
1. HTML ``FORM`` 사용하기
다음과 같은 형식으로 파일 업로드를 실행 할 수 있다.
```html
<form action="uploadfile" method="post" enctype="multipart/form-data">
	<input type="file" name="file"><input type="submit">
</form>
```

2. ajax 사용하기
drag-drop을 구현하려면 ajax를 이용한다.
우선 기본적으로 브라우저에 image를 드래그 하면 창으로 보여주기 때문에
이를 ``preventDefault`` 함수로 막는다
```js
<script>
	$(".fileDrop").on("dragenter dragdover", function(e){
		e.preventDefault()
		})

	$(".fileDrop").on("drop", function(e){
		e.preventDefault()
		})
</script>
```
