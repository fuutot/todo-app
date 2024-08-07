# 元となるDockerイメージを指定
FROM python:3.10

# 作業ディレクトリの指定
WORKDIR /app/

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Gunicornでアプリを実行
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "main:app"]