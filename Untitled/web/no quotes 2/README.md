# Cookie Monster Secret Recipe

## Challenge Information
- **Category**: Web Exploitation
- **Points**: hide
- **Difficulty**: hide
- **Event**: UofCTF 2026
- **URL**: [Link Challenge](https://play.uoftctf.org/challenges#No%20Quotes%202-18)
- **Author**: SteakEnthusiast
- **Tags**: #web #SQLi #SQLiQuine #HexEncode
---
## 1. Description
> Unless it's from "Go Go Squid!", no quotes are allowed here! Let this wholesome quote heal your soul:
> Ai Qing: "If you didn't know about robot combat back then, what would you be doing?"
> Wu Bai: "There's no if. As long as you're here, I'll be here."
> Now complete with a double check for extra security!
## 2. Overview
Bài này có một form đăng nhập, và challenge cung cấp source của trang đăng nhập này, khi khai thác sẽ phát hiện ra lỗ hổng SQLi và 1 hàm xử lý chuỗi đầu vào ngăn chặn `'` và `"`. Cách chặn này khá giống bài `no quotes` ([[Write-up CTF/Untitled/web/no quotes/README|README]]) nhưng ở bài này sẽ phức tạp hơn đôi chút vì có hàm so sánh giá trị input của người dùng với output của câu SQL query. Có thể bypass bằng cách dùng kỹ thuật `SQL Quine` kết hợp với cách bypass của bài trước ta sẽ lấy được flag của bài này.
## 3. Reconnaissance
Truy cập vào trang web và thấy form đăng nhập.
Nhập thử một username và password bất kỳ: `test`/`test.

![[Pasted image 20260113121405.png]]

Sau khi nhấn Login, trang web login thành công và hiện lên `Welcome, test`. Có lẽ đây là tài khoản challenge cung cấp sẵn để người chơi biết giao diện khi login thành công.

![[Pasted image 20260113121959.png]]

Thử nhập một account khác thì web trả về:

![[Pasted image 20260113121944.png]]

Để phân tích và khai thác sâu hơn ta sẽ mở source code và review xem có lỗi gì ở phía cấu hình server hay không. Sau khi đọc source trong file `app.py` thì ta phát hiện ra trang web lấy thẳng input của người dùng và đưa vào câu truy vấn.

```python
if waf(username) or waf(password):
        return render_template(
            "login.html",
            error="No quotes allowed!",
            username=username,
        )
    query = (
        "SELECT username, password FROM users "
        f"WHERE username = ('{username}') AND password = ('{password}')"
    )
```

>**Nghi vấn:** tiềm năng khá cao dính SQL Injection vì có sử dụng SQL query đến Database và chèn thẳng input người dùng vào câu query này.

Nhìn lên điều kiện đi kèm ta sẽ thấy user input được filter thông qua hàm `waf()`, cùng xem logic của hàm này có gì.

```python
def waf(value: str) -> bool:
    blacklist = ["'", '"']
    return any(char in value for char in blacklist)
```

Hàm này nhận input là string và trả về `true` nếu input chứa ký tự `'` hoặc `"`. Đến đây ta có thể nghĩ ra các hướng để bypass hàm này.

Để ý một chút ta sẽ thấy một câu điều kiện khá quan trọng:
```python
if not username == row[0] or not password == row[1]:
        return render_template(
            "login.html",
            error="Invalid credentials.",
            username=username,
        )
```

Ý nghĩa của việc kiểm tra điều kiện ở đây là phải bắt buộc input của user và output của sql query phải giống nhau, lúc này việc bypass sẽ khó khăn hơn.
## 4. Exploitation

Vì chall này có thêm điều kiện kiểm tra username và password khớp với output của sql query nên ta không thể nào dùng dấu '\' như ở chall trước để bypass. Phải tìm cách làm sao để khi ta nhập username và password đầu vào, database trả về dữ liệu cũng phải hoàn toàn khớp với input ta đã nhập này.

Lúc này nghĩ ngay đến kỹ thuật viết câu query SQL Quine, kỹ thuật này cho phép ta có thể viết 1 câu query mà output của nó in ra vẫn là chính nó (có thể tưởng tượng đến việc soi gương).

Dựa vào các dữ kiện ấy ta có thể viết payload như sau:

```mysql

```

### Script (Optional)
Một đoạn script Python nhỏ để tự động hóa việc này (nếu lười copy paste thủ công):

```python
import base64

part1 = "cGljb0NURntwcm94aWVzX2Fs"
part2 = "bF90aGVfd2F5XzI1YjMxYzYyfQ=="

flag = base64.b64decode(part1).decode() + base64.b64decode(part2).decode()
print("Flag found: " + flag)