# Proposal: TikTok Auto Upload Workflow

---

## 1. Tổng quan

Xây dựng tool tự động upload video lên nhiều tài khoản TikTok thông qua **Browser Automation** — dùng code điều khiển trình duyệt thay thế thao tác thủ công.

---

## 2. Công nghệ sử dụng

**Browser Automation** (Playwright hoặc Puppeteer): điều khiển Chrome tự động — mở trang, đăng nhập, upload video, chọn nhạc, chỉnh volume, và đăng bài — hoàn toàn không cần thao tác tay.

---

## 3. Cấu trúc Input (Google Drive)

```
📁 TikTok Upload/
   ├── 📁 queue/
   │   ├── acc1_001.mp4       ← video
   │   ├── acc1_001.txt       ← caption, link sfx, sfx_volume, original_volume
   │   ├── acc2_001.mp4
   │   ├── acc2_001.txt
   │   └── ...
   ├── 📁 done/               ← tool tự chuyển vào khi upload xong
   └── 📁 failed/             ← video bị lỗi
```

**Quy tắc đặt tên file:** `{tên_account}_{số_thứ_tự}.mp4/.txt`
Tool ghép cặp file `.mp4` + `.txt` cùng tên → xử lý thành 1 job.

---

## 4. Quy trình hoạt động

```
[1] Quét folder queue/
        │  (theo lịch: 30 phút / 1 ngày / thủ công)
        ▼
[2] Ghép cặp file
        │  acc1_001.mp4 + acc1_001.txt → Job #1
        │  acc2_001.mp4 + acc2_001.txt → Job #2
        ▼
[3] Đọc thông tin
        │  Tên file  → xác định account cần đăng
        │  File .txt → caption, link nhạc, sfx_volume, original_volume
        ▼
[4] Mở trình duyệt
        │  Đăng nhập account (dùng cookies đã lưu sẵn)
        ▼
[5] Upload & cấu hình video
        │  Upload file .mp4
        │  Chọn nhạc từ link SFX
        │  Chỉnh sfx_volume + original_volume
        │  Điền caption → Đăng
        ▼
[6] Xử lý kết quả
        │  ✅ Thành công → chuyển .mp4 + .txt vào done/
        └  ❌ Thất bại  → chuyển .mp4 + .txt vào failed/
```

---

## 5. Cấu hình file .txt

Mỗi video đi kèm 1 file `.txt` chứa các thông tin:

```
caption: Đây là caption của video #caption #hashtag
sfx_link: https://www.tiktok.com/music/...
sfx_volume: 80
original_volume: 20
```

---

## 6. Lịch chạy

Tool hỗ trợ 3 chế độ kích hoạt:

- **Thủ công:** nhấn Run khi cần
- **Định kỳ:** tự động chạy mỗi 30 phút / 1 giờ / 1 ngày
- **Theo dõi thư mục:** tự chạy ngay khi có file mới trong `queue/`

---

## 7. Phạm vi triển khai

| Hạng mục | Chi tiết |
|---|---|
| Ngôn ngữ | Python hoặc Node.js |
| Browser Automation | Playwright (khuyến nghị) |
| Lưu trữ input | Google Drive |
| Quản lý session | Cookies per account |
| Log lỗi | Ghi vào file log + chuyển vào `failed/` |
