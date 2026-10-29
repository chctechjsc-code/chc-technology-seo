# CHC Technology SEO

Bộ skill SEO song ngữ cho khách Việt Nam và quốc tế. Bản đầy đủ được cài dưới dạng **Claude Code plugin**. ZIP Upload a skill của Claude giới hạn 200 file; bản này có 479 file, vì vậy không dùng ZIP skill cho bản đầy đủ.

## Thành phần

- 25 cặp hướng dẫn CHC Việt–Anh trong `skills/chc-seo/references/`.
- 26 hướng dẫn chuyên sâu nguồn gốc trong `skills/chc-seo/skills/`, đổi tên thành `GUIDE.md` để chỉ skill CHC hiện trong preview.
- Hơn 60 script Python và launcher trong `skills/chc-seo/scripts/`, cùng dữ liệu, schema, assets, agents và mã extension tùy chọn. Các script giữ đường dẫn nội bộ cần thiết cho runtime.
- CLI CHC công khai: `python skills/chc-seo/scripts/chc_seo.py page <url>` hoặc `audit <url>` (kiểm tra nhanh một trang, robots và sitemap).

## Sử dụng

Đọc `skills/chc-seo/SKILL.md`; chọn ngôn ngữ và chế độ. Với script chuyên sâu, kiểm tra `python skills/chc-seo/scripts/runtime.py doctor --json`. Môi trường quản lý và Chromium cần setup riêng trước khi chạy các script phụ thuộc; các API Google, vendor và extension cần quyền, khóa hoặc connector của tài khoản dùng. Đóng gói mã không tự cấp quyền hay tạo dữ liệu trả phí.

Nguồn gốc và bản quyền được ghi tại `THIRD-PARTY-NOTICES.md` và các file license đi kèm. Không có kho `legacy-source.zip` trong folder này.

## Cài bản đầy đủ vào Claude Code

Đẩy **toàn bộ folder repo này** lên GitHub của CHC. Người cài dùng repo CHC, không dùng URL của bản gốc:

```powershell
git clone --depth 1 https://github.com/<owner>/chc-technology-seo.git
powershell -ExecutionPolicy Bypass -File .\chc-technology-seo\install.ps1
```

`install.ps1` kiểm tra plugin, cài từ repo vừa clone và chạy `runtime.py setup` để cài môi trường Python. Nếu chỉ muốn kiểm tra, dùng `-ValidateOnly`; nếu đã cài runtime, dùng `-SkipSetup`.

Cách cài trực tiếp trong Claude Code, không cần chạy `install.ps1` trước:

```text
/plugin marketplace add <owner>/chc-technology-seo
/plugin install chc-technology-seo@chc-technology-seo
```

Sau đó dùng `/chc-technology-seo:chc-seo` và yêu cầu `setup` nếu runtime chưa sẵn sàng. Chạy `python skills/chc-seo/scripts/runtime.py doctor --json` trong repo để xem trạng thái. Dịch vụ Google, vendor và extension cần quyền, khóa API hoặc connector riêng.

Để thử trước khi có GitHub, chạy `powershell -ExecutionPolicy Bypass -File .\install.ps1 -ValidateOnly` tại folder này, hoặc `claude plugin install chc-technology-seo --marketplace .`.
