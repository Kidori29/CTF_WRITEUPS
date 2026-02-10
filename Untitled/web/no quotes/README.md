# Cookie Monster Secret Recipe

## Challenge Information
- **Category**: Web Exploitation
- **Points**: hide
- **Difficulty**: Medium
- **Event**: picoCTF 2023
- **URL**: [Link Challenge](https://play.picoctf.org/practice/challenge/349)
- **Author**: SteakEnthusiast
- **Tags**: #web #SQLi #HexEncode
---
## 1. Description
> Unless it's from "Go Go Squid!", no quotes are allowed here! Let this wholesome quote heal your soul:
> Ai Qing: "If you didn't know about robot combat back then, what would you be doing?"
> Wu Bai: "There's no if. As long as you're here, I'll be here."
## 2. Overview
Bài này có một form đăng nhập, và challenge cung cấp source của trang đăng nhập này, khi khai thác sẽ phát hiện ra lỗ hổng SQLi và 1 hàm xử lý chuỗi đầu vào ngăn chặn `'` và `"` nhưng ta có thể bypass dễ dàng bằng kỹ thuật `hexa encode` và dùng `UNION` để lấy flag.
## 3. Reconnaissance
Truy cập vào trang web và thấy form đăng nhập.
Nhập thử một username và password bất kỳ: `test`/`test.

![[Pasted image 20260110015756.png]]

Sau khi bấm Login, trang web sẽ hiện ra thông báo gợi ý cho ta tìm flag.

![[Pasted image 20260110015923.png]]

> **Nghi vấn:** Có thể Flag nằm trong cookie mà trang web cung cấp trong response của request này.

-> Mở Burp Suite để đọc rõ hơn

Bắt request login và xem response windown, bôi đen đoạn mã sau `secret_recipe=` và nhìn sang bên phải ô *Decoded from Base64* ta tìm được flag

![[Pasted image 20260110020305.png]]

## 4. Analysis & Exploitation

Để bắt được các request chuyển hướng, mình có 2 cách: dùng **Burp Suite** (HTTP History) hoặc dùng **Developer Tools** của trình duyệt. Ở đây mình dùng Developer Tools cho đơn giản.

### Bước 1: Monitor Network
1. Mở F12 -> Tab **Network**.
2. Tích vào ô **Preserve log** (Giữ lại log). *Bước này cực quan trọng, nếu không khi trang load lại, các request cũ chứa Flag sẽ biến mất.*
3. Thực hiện Login lại.

### Bước 2: Phân tích Request
Mình quan sát thấy có 2 request `GET` lạ xuất hiện trước khi load trang `/home`. Chúng có dạng:

1. `GET /next-page/id=cGljb0NURntwcm94aWVzX2Fs`
2. `GET /next-page/id=bF90aGVfd2F5XzI1YjMxYzYyfQ==`

![Screenshot Network Tab showing redirects](link_to_image_here)
*(Chỗ này bạn chèn ảnh chụp tab Network khoanh đỏ 2 dòng request trên)*

### Bước 3: Decode
Dữ liệu trong tham số `id` nhìn giống **Base64** (kết thúc bằng dấu `=` và gồm các ký tự a-z, A-Z, 0-9).

Mình tiến hành ghép 2 chuỗi này lại và decode:

**Part 1:** `cGljb0NURntwcm94aWVzX2Fs` -> Decode: `picoCTF{proxies_al`
**Part 2:** `bF90aGVfd2F5XzI1YjMxYzYyfQ==` -> Decode: `l_the_way_25b31c62}`

### Script (Optional)
Một đoạn script Python nhỏ để tự động hóa việc này (nếu lười copy paste thủ công):

```python
import base64

part1 = "cGljb0NURntwcm94aWVzX2Fs"
part2 = "bF90aGVfd2F5XzI1YjMxYzYyfQ=="

flag = base64.b64decode(part1).decode() + base64.b64decode(part2).decode()
print("Flag found: " + flag)