# Database Steganography Project

Dự án giấu tin trong cơ sở dữ liệu sử dụng kỹ thuật Case-based Steganography, được xây dựng với Python, Streamlit và SQLite.

## 🚀 Tính năng

- 💫 Giấu tin trong database sử dụng kỹ thuật thay đổi case
- 🔍 Trích xuất tin nhắn bí mật
- 📊 Phân tích và thống kê dữ liệu
- 📈 Biểu đồ trực quan
- 💾 Export dữ liệu (CSV/Excel)

## 🛠 Yêu cầu hệ thống

- Python 3.10
- pip (Python package installer)
- Git

## ⚙️ Cài đặt

1. **Clone repository**

```bash
git clone https://github.com/baolamabcd13/khoi.git
cd khoi
```

2. **Tạo môi trường ảo**

````bash
# Windows
python -m venv venv
venv\Scripts\activate


3. **Cài đặt các thư viện**
```bash
pip install -r requirements.txt
````

## 🚀 Chạy ứng dụng

1. **Kích hoạt môi trường ảo**

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

2. **Chạy ứng dụng**

```bash
streamlit run app.py
```

3. **Truy cập ứng dụng**

- Mở trình duyệt web
- Truy cập: http://localhost:8501

## 📝 Hướng dẫn sử dụng

1. **Giấu tin**

   - Chọn tab "Hide Message"
   - Điền thông tin employee
   - Nhập text gốc và tin nhắn cần giấu
   - Nhấn "Hide Message"

2. **Trích xuất tin**

   - Chọn tab "Extract Message"
   - Chọn record cần trích xuất
   - Nhấn "Extract" để xem tin nhắn

3. **Xem dữ liệu**
   - Chọn tab "View Data"
   - Sử dụng các filter để lọc dữ liệu
   - Xem biểu đồ thống kê
   - Export dữ liệu nếu cần

## 🔧 Troubleshooting

1. **Lỗi môi trường ảo**

```bash
# Xóa và tạo lại môi trường ảo
rm -rf venv
python -m venv venv
```

2. **Lỗi thư viện**

```bash
pip install --upgrade -r requirements.txt
```

3. **Lỗi database**

```bash
# Xóa file database.db để tạo mới
rm database.db
```
