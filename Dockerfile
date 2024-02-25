FROM python:3

WORKDIR /app

# 複製程式碼到工作目錄
COPY . .

# 安裝所需的 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 開放容器的 5000 端口
EXPOSE 5000

# 執行應用程式
CMD [ "python", "app.py" ]