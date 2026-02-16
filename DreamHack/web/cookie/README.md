# cookie

## Challenge Information
- **Category**: Web Exploitation
- **Points**: hide
- **Difficulty**: Beginner
- **Event**: hide
- **Author**: Dreamhack
- **Tags**: #web #cookie
---
## 1. Description
> A simple login service that uses cookies to manage authentication status.  
> If you successfully log in with an admin account, you can obtain a flag.
> The flag format is DH {...} This is it.
## 2. Overview
Bài này đưa ra một form đăng nhập và yêu cầu phải đăng nhập vào bằng tài khoản admin để lấy được flag. Ta sẽ thay đổi cookie để đánh lừa và bypass.
## 3. Reconnaissance
Giao diện là một page chức năng chính là đăng nhập:

![](images/Screenshot%202026-02-11%20165220.png)

Mở source trong devtools ta sẽ thấy tài khoản mặc định là `guest/guest`

![](images/Pasted%20image%2020260211172426.png)

-> Đăng nhập xem sao

![](images/Pasted%20image%2020260211172530.png)

Trang web chỉ hiện thông báo này và không có gì khác. Ta sẽ kiểm tra source code chall cung cấp.

```Python
@app.route('/')
def index():
    username = request.cookies.get('username', None)
    if username:
        return render_template('index.html', text=f'Hello {username}, {"flag is " + FLAG if username == "admin" else "you are not admin"}')

    return render_template('index.html')
```
Ở source có một đoạn rất khả nghi là phía backend chỉ xác thực user có phải là admin hay không thông qua nội dung của cookie. Lấy `username` ở cookie sau đó so sánh nếu đó là "admin" thì sẽ hiện FLAG và ngược lại sẽ là "you are not admin" -> dựa vào đây ta có thể bypass được.
## 4. Exploitation
Vì bài này liên quan đến cookie nên ta sẽ mở devtools để xem có thể sửa nội dung cookie để đánh lừa phía server hay không:

![](images/Screenshot%202026-02-11%20165152.png)

Ở phần cookie ta có thể thấy trường `username` hiện tại đang có giá trị là `guest`, bây giờ cùng thử sửa thành `admin` xem sao.

![](images/Screenshot%202026-02-11%20165159.png)

Reload trang web và nhận flag.

![](images/Screenshot%202026-02-11%20165138.png)
