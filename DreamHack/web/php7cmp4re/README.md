# php7cmp4re

## Challenge Information
- **Category**: Web Exploitation
- **Points**: hide
- **Difficulty**: Beginner
- **Event**: Dreamhack CTF Season 5 Round #2 (🌱Div2) 
- **Author**: Dreamhack
- **Tags**: #web #PHPcmp #PHP74 #TypeJuggling
---
## 1. Description
> This page is written in php 7.4.
> Enter an appropriate Input value and obtain a flag.
> The flag format is`DH{}`.
## 2. Overview
Bài này là whitebox một đoạn code với các điều kiện so sánh chuỗi và số, từ đó viết input phù hợp để bypass và lấy flag.
## 3. Reconnaissance
Giao diện là một page có 2 vị trí để điền input1 và input2:

![](images/Pasted%20image%2020260211161315.png)

Source code bao gồm 3 file: `check.php`, `index.php` và `flag.php`
Đọc source code ta sẽ thấy chỉ file `check.php` chứa logic ta có thể bypass được. Để ý phần check điều kiện của POST request:

![](images/Pasted%20image%2020260211162431.png)

Đoạn code này yêu cầu input1 và input2 phải thỏa mãn tất cả các điều kiện if thì mới hiện flag -> ta sẽ viết payload để thỏa mãn.
## 4. Exploitation
- if dòng số 25: Chương trình sẽ kiểm tra request cho vào có phải là POST không, sau đó kiểm tra input1 và input2 có tồn tại không.
- if dòng số 30: Ở đây sẽ kiểm tra input1 và input2 có rỗng hay không, nếu không sẽ đi tiếp.
- if dòng số 31: Độ dài của input1 phải < 4
- if dòng số 32: input1 phải < chuỗi "8", < chuỗi "7.A" và > chuỗi "7.9"
- if dòng số 33: Độ dài input2 phải = 2
- if dòng số 34: input2 < 74 và > chuỗi "74"

Dựa vào những phân tích đó ta có đánh giá như sau:
1. input1 phải có độ dài là 3 và 2 ký tự đầu phải là "7.", ký tự cuối cùng phải < "A" và > "9" trong bảng ascii.
2. input2 phải có độ dài là 2, < 74 và > "74", điều này nghe có vẻ vô lý nhưng với PHP 7.4, việc so sánh giữa chuỗi và số rất lỏng lẻo. Trong PHP 7.4, khi sử dụng toán tử so sánh không nghiêm ngặt (như `<`, `>`, `==`), PHP sẽ tự động ép kiểu dữ liệu (Type Juggling) để thực hiện phép so sánh -> Ta sẽ tận dụng điều này để bypass.

Payload sẽ là: `input1 = 7.:` và `input2 = ab`

Cơ chế xử lý của PHP 7.4 trong trường hợp này như sau:
- **So sánh chuỗi (`$input2 > "74"`)**: PHP so sánh theo thứ tự từ điển. Với `$input2 = "ab"` -> ĐÚNG
- **So sánh số (`$input2 < 74`)**: Khi so sánh một chuỗi không bắt đầu bằng số với một số nguyên, PHP 7.4 sẽ ép kiểu chuỗi đó về `0`. Vì `0 < 74` -> ĐÚNG

> **Note**: Từ PHP 8.0 trở đi, logic này đã được thay đổi để trở nên an toàn hơn.

![](images/Pasted%20image%2020260211163343.png)

Lấy được flag và hoàn thành chall.