# FastAPIの認証サンプル


## FastAPIの起動

```shell
# 起動
uvicorn api.main:app --reload
```

## フォームログイン

```
# フォーム送信
curl -X POST -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=admin@example.com&password=password" \
    http://localhost:8000/form-login
```
