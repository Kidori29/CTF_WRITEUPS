# 403-forbbiden

## Challenge Information
- **Category**: Web Exploitation
- **Difficulty**: level 1
- **Author**: 상현예
- **URL**: https://dreamhack.io/wargame/challenges/2786 
- **Tags**: #web #json
---
## 1. Description
>403 forbidden error
## 2. Overview
Đây là một bài cơ bản về POST, json
## 3. Reconnaissance
Giao diện bài này khá đơn giản và không có chức năng gì để khai thác:

![](images/Pasted%20image%2020260323160739.png)

Challenge chỉ có một file code python là `app.py`:

![](images/Pasted%20image%2020260323160517.png)

Nhìn vào đây ta có thể thấy để lấy được `flag` thì phải POST một cái gì đó lên có dạng JSON, trong data được post có trường `status`, và trường `status` này phải có giá trị là "200" lên `/flag`
## 4. Exploitation
Payload cho Burp:
```http
POST /flag HTTP/1.1
Host: host3.dreamhack.games:14918
Content-Type: application/json
Content-Length: 21

{"status": "200"}
```

![](images/Pasted%20image%2020260323161024.png)