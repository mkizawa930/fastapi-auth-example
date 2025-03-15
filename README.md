# README.md


## FastAPIの起動


```shell
# 起動
uvicorn app.main:app --reload

# 他のディレクトリから実行させるにはアプリケーションルートで次を実行する
PYTHON_PATH=. uv run python <path/to/file>
```
