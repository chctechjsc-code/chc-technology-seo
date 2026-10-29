# CHC Technology SEO

**Bộ công cụ SEO song ngữ Việt–Anh cho Claude Code.** Kiểm tra website, giải thích bằng chứng và lập kế hoạch sửa lỗi cho thị trường Việt Nam hoặc quốc tế.

[English](README.en.md) · [Hướng dẫn skill](skills/chc-seo/SKILL.md) · [Danh mục API](API-INVENTORY.md) · [Nguồn và giấy phép](THIRD-PARTY-NOTICES.md)

> **Cài dưới dạng plugin từ GitHub.** Repo đầy đủ có hơn 500 file; mục **Upload a skill** của Claude giới hạn 200 file và không nhận ZIP lồng nhau.

## Cài nhanh bằng Claude Code

Trong Claude Code, chạy lần lượt:

```text
/plugin marketplace add chctechjsc-code/chc-technology-seo
/plugin install chc-technology-seo@chc-technology-seo
/chc-technology-seo:chc-seo setup
```

`setup` tạo môi trường Python riêng và chuẩn bị các thư viện cần thiết. Kiểm tra trạng thái bằng `/chc-technology-seo:chc-seo doctor`. Một số phép kiểm tra trình duyệt còn cần Chromium được cài thành công.

### Windows: clone repo và chạy bộ cài

```powershell
git clone --depth 1 https://github.com/chctechjsc-code/chc-technology-seo.git
powershell -ExecutionPolicy Bypass -File .\chc-technology-seo\install.ps1
```

Hãy xem nội dung `install.ps1` trước khi chạy. Script xác thực cấu trúc plugin, cài plugin từ bản clone và chạy setup runtime. Dùng `-ValidateOnly` để chỉ kiểm tra hoặc `-SkipSetup` nếu đã có runtime. Trên macOS/Linux, dùng ba lệnh Claude Code ở trên; repo hiện chưa có installer shell riêng.

## Bắt đầu sử dụng

```text
/chc-technology-seo:chc-seo audit https://example.com lang=vi
/chc-technology-seo:chc-seo page https://example.com/product lang=en
/chc-technology-seo:chc-seo hreflang https://example.com lang=both
/chc-technology-seo:chc-seo schema https://example.com
```

Skill nhận yêu cầu bằng tiếng Việt hoặc tiếng Anh. `lang=both` yêu cầu hai phần báo cáo tương đương; ngôn ngữ báo cáo và thị trường mục tiêu được xác định riêng. URL ví dụ ở trên chỉ minh họa cú pháp.

## Chức năng có trong repo

| Nhóm | Nội dung |
|---|---|
| Kiểm toán | Toàn site, một trang, SEO kỹ thuật, sitemap, hình ảnh, tốc độ và thay đổi theo thời gian |
| Nội dung | Chất lượng nội dung, E-E-A-T, đề bài viết, cụm từ khóa, trang so sánh, SXO |
| Tìm kiếm mới | GEO, khả năng truy cập của tác nhân AI, dữ liệu có cấu trúc |
| Thị trường | SEO địa phương, bản đồ, thương mại điện tử, hreflang và đa quốc gia |
| Dữ liệu | Google, backlink và các nhà cung cấp tùy chọn khi tài khoản được cấu hình |

Repo cung cấp **một skill CHC** để điều phối 25 chế độ song ngữ, 26 hướng dẫn kỹ thuật chi tiết, 19 agent chuyên môn và hơn 60 script. Chín thư mục extension chứa mã tích hợp tùy chọn; việc có mã trong repo không tự kích hoạt dịch vụ đó.

Mỗi kết luận SEO nên nêu URL/phạm vi kiểm tra, thời điểm, bằng chứng, mức độ chắc chắn và cách xác nhận sau khi sửa. Nếu không đo được dữ liệu, báo “Chưa đo” thay vì điền số 0 hoặc suy đoán.

## API và dữ liệu

- **Có thể bắt đầu với nguồn công khai:** HTML, robots.txt, sitemap và các kiểm tra không cần tài khoản, sau khi runtime phù hợp đã sẵn sàng.
- **Cần quyền của website/tài khoản:** Search Console, Analytics, Bing Webmaster và các nguồn tương tự cần xác thực hợp lệ.
- **Nhà cung cấp tùy chọn:** Ahrefs, DataForSEO, SE Ranking, Profound và các dịch vụ khác có thể cần hợp đồng, khóa API hoặc phí riêng. Không có khóa của nhà cung cấp trong repo.

Xem [API-INVENTORY.md](API-INVENTORY.md) trước khi kết nối dịch vụ. Các tích hợp riêng chưa được cấu hình hoặc kiểm thử bằng tài khoản CHC thì không được coi là đã hoạt động.

## Cấu trúc

```text
.claude-plugin/                 plugin.json và marketplace.json
skills/chc-seo/SKILL.md        điểm vào CHC duy nhất
skills/chc-seo/references/     hướng dẫn Việt–Anh
skills/chc-seo/skills/         quy trình kỹ thuật chi tiết
skills/chc-seo/scripts/        runtime và công cụ kiểm tra
skills/chc-seo/extensions/     mã tích hợp tùy chọn
agents/                        19 agent Claude Code
install.ps1                    bộ cài Windows
```

Kiểm tra trước khi dùng hoặc đóng góp:

```powershell
claude plugin validate .
powershell -ExecutionPolicy Bypass -File .\install.ps1 -ValidateOnly
python .\skills\chc-seo\scripts\runtime.py doctor --json
```

## Giới hạn hiện tại

Đã kiểm tra cấu trúc plugin, liên kết tài liệu và cú pháp script. Việc chạy đủ từng API, trình duyệt và extension phụ thuộc môi trường cùng quyền truy cập thực tế. Plugin không bảo đảm thứ hạng, lượng truy cập hay kết quả kinh doanh. Claude Code và các dịch vụ bên ngoài áp dụng điều khoản riêng của họ.

## Nguồn và bản quyền

Bản CHC được biên soạn lại cho luồng làm việc Việt–Anh và phân phối từ repo này. Phần mã và tài liệu có nguồn gốc bên thứ ba được ghi trong [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md), [LICENSE](LICENSE) và các giấy phép đi kèm. Vui lòng giữ các thông báo đó khi phân phối tiếp.
