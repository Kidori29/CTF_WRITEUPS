# whoami

## Challenge Information
- **Category**: Web Exploitation
- **Points**: hide
- **Difficulty**: level 1
- **Event**: hide
- **Author**: toka
- **Tags**: #web #ip #XFF
---
## 1. Description
> The server knows who you are.  
> The question is… do you? 🤨
## 2. Overview
Đây là một bài sử dụng X-Forwarded-For để sử dụng ip `admin` đăng nhập
## 3. Reconnaissance
Web chỉ có chắc năng `Check` (xem phiên đăng nhập là ai) và `Go` (chỉ dành cho admin)

![](images/Pasted%20image%2020260216202727.png)

Chức năng Check sẽ trả về 1 JSON với 3 trường `ip`, `role` và `message`

![](images/Pasted%20image%2020260216203219.png)

Check source code để tìm xem có cách nào leo quyền lên `admin` không

![](images/Pasted%20image%2020260216203319.png)

Ta có thể thấy role phụ thuộc vào hàm `isLocal(ip)`, nếu hàm này trả về `true` thì ta thành công leo được admin, ta sẽ cùng check logic của hàm:

![](images/Pasted%20image%2020260216203431.png)

Dễ thấy chỉ cần ip là `"127.0.0.1"` hoặc `"::1"` thì hàm này sẽ trả về `true`
-> Nghĩ ngay đến dùng kỹ thuật chèn HTTP header `X-Forwarded-For` để  fake ip của `admin`
## 4. Exploitation
Sử dụng Burp Suit để bắt gói tin và sửa đổi (chèn thêm header `X-Forwarded-For: 127.0.0.1`):

![](images/Pasted%20image%2020260216203833.png)

Copy flag và submit