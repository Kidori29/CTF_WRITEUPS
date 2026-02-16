# command-injection-1

## Challenge Information
- **Category**: Web Exploitation
- **Points**: hide
- **Difficulty**: Beginner
- **Event**: hide
- **Author**: Dreamhack
- **Tags**: #web #cmdi
---
## 1. Description
> A service that sends ping packets to specific hosts.  
> Obtain flags through Command Injection. The flag `flag.py` is located at
## 2. Overview
Bài này là một command injection điển hình với chức năng ping host, tuy giao diện đã chống cmdi bằng whitelist nhưng phía backend lại không lọc kỹ -> dẫn đến ta có thể inject thông qua request mà không cần đến giao diện.
## 3. Reconnaissance
Giao diện đầu tiên khi ta vào web là một trang bình thường với chức năng chính là ping host

![](images/Pasted%20image%2020260213210011.png)

![](images/Pasted%20image%2020260213210026.png)

Thử ping một ip chuẩn và 1 ip chứa ký tự lạ xem có thể phát hiện được gì không

![](images/Pasted%20image%2020260213210104.png)

![](images/Pasted%20image%2020260213210127.png)

Thử kiểm tra source phía client:
```html
<input type="text" class="form-control" id="Host" placeholder="8.8.8.8" name="host" pattern="[A-Za-z0-9.]{5,20}" required>
```
Thấy code dùng whitelist để lọc đầu vào (chỉ gồm chữ cái và số, độ dài từ 5 đến 20) -> kiểm tra phía backend xem sao:

![](images/Pasted%20image%2020260213222050.png)

Không hề có dòng nào để lọc đầu vào, đặc biệt hơn chương trình lại đưa thẳng biến `host` chưa được lọc vào câu lệnh gọi shell -> 99% command injection.
-> Dùng burp để bắt request và lấy flag.
## 4. Exploitation

Vì `host` được đưa vào cặp dấu "" nên ta sẽ thoát ra trước, sau đó dùng `;` để kết thúc lệnh ping và truyền vào lệnh lấy flag và comment toàn bộ chuỗi còn lại -> Payload sẽ như sau:
```shell
";cat flag.py #
```
Lúc này server sẽ thực hiện đọc nội dung của file `flag.py` và gửi response về
![](images/Pasted%20image%2020260213223223.png)