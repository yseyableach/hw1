FROM python:3

WORKDIR /app

COPY . .

# 安装 Flask
RUN pip install --no-cache-dir flask

EXPOSE 5000

CMD [ "python", "app.py" ]
