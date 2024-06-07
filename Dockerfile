# 元となるDockerイメージを指定
FROM python:3.10

# 作業ディレクトリの指定
WORKDIR /app/

# ファイル、ディレクトリのコピー
COPY ./src/ /app/

RUN pip install --upgrade pip
# 実行
CMD ["/bin/bash"]