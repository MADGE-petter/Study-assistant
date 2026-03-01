# 📚 Study Assistant - Ứng dụng học tập thông minh

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://python.org)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.4+-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Study Assistant là ứng dụng desktop giúp bạn quản lý thời gian học tập, ghi chú, nhiệm vụ và theo dõi tiến độ học tập một cách hiệu quả.

## ✨ Tính năng chính

### 🎯 Giao diện chính
- **📊 Dashboard** - Thống kê tổng quan thời gian học, số buổi học, ghi chú, nhiệm vụ
- **📝 Ghi chú** - Quản lý ghi chú học tập với tìm kiếm và phân loại
- **⏰ Timer học tập** - Đếm thời gian học tập với thông báo
- **📋 Nhiệm vụ** - Quản lý công việc cần hoàn thành
- **📈 Thống kê** - Biểu đồ và báo cáo tiến độ học tập

### 🔐 Bảo mật
- **🔑 Login system** - Đăng nhập với mật khẩu bảo vệ
- **🎮 Konami Code** - ALT x3 để đặt lại mật khẩu khẩn cấp
- **🛡️ SHA256 encryption** - Bảo mật mật khẩu với hash

### 📦 Build & Deploy
- **🚀 Standalone exe** - Build thành file .exe độc lập
- **📱 No dependencies** - Không cần cài Python để chạy
- **💾 Database** - SQLite tự động quản lý dữ liệu

## 🚀 Cài đặt

### Yêu cầu hệ thống
- **Windows 10/11** (64-bit)
- **RAM tối thiểu** 4GB
- **Dung lượng** 200MB

### Cách 1: Download exe (Khuyên dùng)
1. Tải file `StudyAssistant.exe` từ [releases](https://github.com/MADGE-petter/Study-assistant/releases)
2. Chạy file exe
3. Sử dụng ngay!

### Cách 2: Build từ source
```bash
# Clone repository
git clone https://github.com/MADGE-petter/Study-assistant.git
cd Study-Assistant

# Cài dependencies
pip install -r requirements.txt

# Build exe
python build.py

# Chạy app
python main.py
```

## 🔐 Admin Panel

### Truy cập Admin Panel
- **Mật khẩu mặc định**: `123`
- **Konami Code**: Nhấn ALT 3 lần để đặt lại mật khẩu
- **Quản lý database**: Xem, sửa, xóa dữ liệu học tập

### Build Admin Panel
```bash
cd Study-Assistant-Admin
python admin_panel.py
```

## 📖 Hướng dẫn sử dụng

### Bắt đầu
1. **Mở ứng dụng** - Chạy StudyAssistant.exe
2. **Tạo buổi học** - Click "Bắt đầu học tập"
3. **Ghi chú** - Thêm ghi chú trong quá trình học
4. **Xem thống kê** - Theo dõi tiến độ học tập

### Timer học tập
- **Bắt đầu**: Click "Bắt đầu học tập"
- **Tạm dừng**: Click "Tạm dừng"
- **Kết thúc**: Click "Kết thúc buổi học"
- **Tự động lưu**: Dữ liệu được lưu tự động

### Ghi chú
- **Thêm mới**: Click "Thêm ghi chú"
- **Tìm kiếm**: Sử dụng ô tìm kiếm
- **Phân loại**: Tags và categories
- **Xuất file**: Export ra file text

### Nhiệm vụ
- **Thêm nhiệm vụ**: Title, description, due date
- **Priority**: High, Medium, Low
- **Status**: Pending, In Progress, Completed
- **Theo dõi**: Auto-track completion

## 🛠️ Công nghệ

### Backend
- **Python 3.12+** - Ngôn ngữ lập trình chính
- **SQLite** - Database quản lý dữ liệu
- **NLTK** - Xử lý ngôn ngữ tự nhiên
- **Sumy** - Tóm tắt văn bản

### Frontend
- **PyQt6** - GUI framework
- **QSS** - Stylesheet cho giao diện
- **Custom widgets** - Components riêng

### Build Tools
- **PyInstaller** - Build exe standalone
- **Custom hooks** - Fix NLTK/Scipy issues
- **Optimized size** - 127MB final exe

## 📊 Cấu trúc project

```
Study-Assistant/
├── main.py                 # Entry point
├── src/                    # Source code
│   ├── ai/                # AI features
│   ├── database/          # Database management
│   ├── notes/             # Notes management
│   ├── timer/             # Timer functionality
│   ├── tasks/             # Task management
│   ├── statistics/        # Statistics & charts
│   └── utils/             # Utilities
├── build.py               # Build script
├── requirements.txt       # Dependencies
├── .gitignore            # Git ignore
└── dist/                  # Build output

Study-Assistant-Admin/
├── admin_panel.py         # Admin Panel GUI
├── admin_database.py     # Database manager
└── .gitignore           # Git ignore
```

## 🔧 Tùy chỉnh

### Đổi mật khẩu admin
1. Mở Admin Panel
2. Nhấn ALT 3 lần (Konami Code)
3. Nhập mật khẩu mới
4. Xác nhận và lưu

### Custom style
- Edit `src/utils/styles.py`
- Modify QSS stylesheets
- Restart application

### Database location
- Default: `study_assistant.db`
- Custom: Edit database path in `src/database/db_manager.py`

## 🐛 Troubleshooting

### Common issues
- **"Không tìm thấy file"**: Kiểm tra đường dẫn cài đặt
- **"Database error":** Xóa file .db và khởi động lại
- **"Build failed":** Cài đặt đầy đủ dependencies

### Get help
- **Issues**: [GitHub Issues](https://github.com/MADGE-petter/Study-assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/MADGE-petter/Study-assistant/discussions)

## 📝 Changelog

### v2.0 (2025-03-01)
- ✨ Thêm Admin Panel với bảo mật
- 🔐 Login system với SHA256 encryption
- 🎮 Konami Code (ALT x3) để reset mật khẩu
- 📦 Build standalone exe (127MB)
- 🗑️ Loại bỏ NLTK/Scipy dependencies
- 🎨 Cải thiện UI/UX

### v1.0 (2025-02-01)
- 🚀 Phiên bản đầu tiên
- 📚 Basic features: Timer, Notes, Tasks
- 📊 Statistics dashboard
- 💾 SQLite database

## 🤝 Đóng góp

### Cách đóng góp
1. Fork repository
2. Tạo branch mới
3. Commit changes
4. Push lên fork
5. Tạo Pull Request

### Guidelines
- Code style: PEP 8
- Comments: Tiếng Việt
- Testing: Test trước khi PR
- Documentation: Cập nhật README

## 📄 License

MIT License - xem file [LICENSE](LICENSE) để biết chi tiết.

## 🙏 Credits

- **PyQt6** - GUI framework
- **NLTK** - Natural Language Processing
- **SQLite** - Database engine
- **PyInstaller** - Build tool

## 📞 Liên hệ

- **GitHub**: [@MADGE-petter](https://github.com/MADGE-petter)
- **Email**: [your-email@example.com]
- **Website**: [your-website.com]

---

⭐ **Star repository** nếu bạn thích project này!

🔄 **Share** với bạn bè của bạn!

📝 **Feedback** giúp cải thiện sản phẩm!
