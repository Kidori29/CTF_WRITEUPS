# # {"role": "admin"}

## Challenge Information
- **Category**: Web Exploitation
- **Points**: hide
- **Difficulty**: level 1
- **Event**: hide
- **Author**: [liasdfio](https://dreamhack.io/users/82496)
- **Tags**: #web #JWT #JWTInjection
---
## 1. Description
> Can you gain admin access?
## 2. Overview
Đây là một bài JWT Injection điển hình khi quá tin tưởng vào input của người dùng mà không có bước làm sạch nào.
## 3. Reconnaissance
Trang web chỉ có chức năng login và register cơ bản:

![](images/Pasted%20image%2020260216172832.png)

![](images/Pasted%20image%2020260216172839.png)

Sau khi tạo thử account và login thì ta sẽ có giao diện như thế này:

![](images/Pasted%20image%2020260216172940.png)

Các mục còn lại cũng chưa khai thác được nhiều:

![](images/Pasted%20image%2020260216173742.png)

![](images/Pasted%20image%2020260216173745.png)

Vì mô tả đã chỉ ra việc phải bypass để login vào account `admin` nên ta sẽ kiểm tra Cookie trước:

![](images/Pasted%20image%2020260216173844.png)

Đây là một JWT code -> decode xem sao:

![](images/Pasted%20image%2020260216173922.png)

Bây giờ ta sẽ xem source code phía server:

![](images/Pasted%20image%2020260216174005.png)

Đoạn code lấy thẳng username của người dùng cho vào `raw-user` mà không hề có biện pháp làm sạch nào -> 99% dính JWT injection
## 4. Exploitation
Ta sẽ exploit chall này bằng cách inject một đoạn mã cho phép nâng quyền lên admin.
Trong chuẩn JSON (và cách thư viện `json` của Python hoạt động), nếu một key xuất hiện 2 lần trong một object, **giá trị của key xuất hiện sau cùng sẽ được ưu tiên**.
-> Dựa vào điều này ta tạo một tài khoản mới và inject username như sau:
```
test1", "role": "admin
```

![](images/Pasted%20image%2020260216174359.png)

Đăng nhập thành công và role bây giờ đã là `admin`
-> Vào mục Flag để lấy và submit thôi

![](images/Pasted%20image%2020260216174447.png)