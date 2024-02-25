## 使用說明

這個應用程序包含了兩個API端點，用於管理使用者帳戶的創建和驗證。以下是如何使用這兩個端點的簡要說明：
若要對api進行測試，可以在啟動後端後，在瀏覽器輸入以下url，就能夠透過Swagger對API進行測試
```
http://127.0.0.1:5000/apidocs
```

### 啟動服務

- 透過以下指令將dockerhub的image pull下來
    ```
    docker pull jayyyyyyu/hw1:v1
    ```
- 利用以下指令執行後端
    ```
    docker run -p 5000:5000 myflaskapp
    ```


### 1. 創建帳戶

- **端點路徑**: `/create_account`
- **HTTP方法**: POST
- **描述**: 此端點用於創建新的使用者帳戶。
- **參數**:
  - `username` (必填): 新帳戶的使用者名稱。
  - `password` (必填): 新帳戶的密碼。
- **回應**:
  - 成功: 返回JSON格式的成功訊息。

    樣本請求:
    ```json
    {
    "username": "AAA",
    "password": "aaaaaaaaaaaA1"
    }
    ```
    樣本響應 (成功):
    ```json
    {
    "success": true
    }
    ```
  - 失敗:密碼缺少數字
      樣本請求:
    ```json
    {
    "username": "AAAA",
    "password": "aaaaaaaaaaaA"
    }
    ```
    樣本響應 (失敗:密碼缺少數字):
    ```json
    {
    "reason": "Password should contain at least one digit",
    "success": false
    }
    ```

  - 失敗:密碼太短
    ```json
    {
    "username": "AAAA",
    "password": "aaa"
    }
    ```


    樣本響應 (失敗:密碼太短):
    ```json
    {
    "reason": "Password length should be between 8 and 32 characters",
    "success": false
    }
    
    ```

  - 失敗:密碼缺少大寫字元 
    ```json
    {
    "username": "AAAA",
    "password": "aaaaaaaaaa1"
    }
    ```


    樣本響應 (失敗:密碼太短):
    ```json
    {
    "reason": "Password should contain at least one uppercase letter",
    "success": false
    }
        
    ```


### 2. 驗證帳戶

- **端點路徑**: `/verify_account`
- **HTTP方法**: POST
- **描述**: 此端點用於驗證使用者帳戶。
- **參數**:
  - `username` (必填): 要驗證的帳戶的使用者名稱。
  - `password` (必填): 要驗證的帳戶的密碼。
- **回應**:
  - 成功: 返回JSON格式的成功訊息。
  - 失敗: 返回JSON格式的錯誤訊息，包含失敗的原因。
  - 多次錯誤: 如果連續多次輸入錯誤密碼，系統將暫時禁止登錄，需等待一分鐘後再試。
  -
    樣本請求:
    ```json
    {
    "username": "AAA",
    "password": "aaaaaaaaaaaA1"
    }
    ```
    樣本響應 (成功):
    ```json
    {
    "success": true
    }
    ```

  - 失敗(無此帳號)
    ```json
    {
    "username": "QQQQQQQQQQQQQQ",
    "password": "aaaaaaaaaaaA1"
    }
    ```

    樣本響應 (失敗):
    ```json
    {
    "reason": "Username does not exist",
    "success": false
    }
    ```
  - 失敗(連續失敗5次)
    ```json
    {
    "message": "Too many failed attempts. Please try again later and wait for one minutes."
    }
    ```