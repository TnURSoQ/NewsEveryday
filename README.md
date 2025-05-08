# VietNamNet News - Tự động lấy tin tức lúc 6h sáng mỗi ngày
hello
Đây là một project nhỏ dùng để lấy tin tức từ trang chủ VietnamNet bằng Python. Nó sẽ mở trình duyệt (tự động bằng Selenium), chọn ngẫu nhiên một mục tin tức, và lấy thông tin như: tiêu đề, mô tả, hình ảnh… rồi lưu vào file Excel.

---

## Cách cài đặt

### 1. Clone project

```bash
git clone https://github.com/TnURSoQ/NewsEveryday.git
cd VietNamNetNews

### 2. Cách cài thư viện
pip install -r requirements.txt
#hoặc cài thủ công
pip install selenium beautifulsoup4 pandas schedule