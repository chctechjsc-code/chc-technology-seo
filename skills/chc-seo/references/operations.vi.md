# Vận hành CHC Technology SEO

## Quy trình
1. Ghi URL/chủ đề, mục tiêu, ngôn ngữ báo cáo, thị trường, thời điểm và phạm vi. Không cần hỏi lại dữ liệu đã có.
2. Chọn quy trình ở SKILL.md; đọc hướng dẫn tiếng Việt tương ứng. Kiểm tra website công khai hoặc file người dùng cung cấp bằng công cụ sẵn có.
3. Tách phát hiện đã xác minh, suy luận và phần chưa đo. Mỗi phát hiện ghi ID, URL, bằng chứng, nguồn, mức ưu tiên, tác động, sửa đề xuất và cách nghiệm thu.
4. Đọc `skills/seo/GUIDE.md` và `skills/seo-<chế-độ>/GUIDE.md` đi kèm khi cần quy trình hoặc script chi tiết. Tài liệu nguồn là dữ liệu tham khảo, không mở rộng quyền cài đặt, gọi dịch vụ hoặc phân công agent.
5. Xuất báo cáo theo mẫu trong assets. Audit một trang không được gọi là audit toàn site. Giữ dữ liệu thô riêng, loại thông tin đăng nhập khỏi báo cáo.

## Điểm và ưu tiên
Điểm là mô hình nội bộ CHC, không phải điểm Google. Nếu dùng rubric nguồn gốc, công bố tiêu chí và trọng số: kỹ thuật 22%, nội dung 23%, on-page 20%, schema 10%, CWV 10%, AI readiness 10%, ảnh 5%.

Chỉ tính khi có tiêu chí chấm được công bố và dữ liệu đủ cho từng hạng mục. Hạng mục không đo = null. Điểm phần đã đo = tổng(score × weight) / tổng trọng số đã đo; ghi rõ độ phủ trọng số và gọi là điểm tạm thời nếu thiếu bất kỳ hạng mục. Không có dữ liệu thì không xuất điểm. Không quy đổi phán đoán chủ quan thành số chính xác giả.

P0: lỗi đã xác minh chặn truy cập/index trang quan trọng; P1: vấn đề tác động lớn có bằng chứng; P2: tối ưu có cơ sở; P3: thử nghiệm hoặc cải tiến nhỏ. Không tự kết luận bị phạt. Ưu tiên còn phụ thuộc giá trị trang, công sức và các việc tiên quyết.

## CLI CHC và dữ liệu
CLI độc lập `python scripts/chc_seo.py page <url>` kiểm tra HTML công khai; `audit <url>` còn kiểm tra robots.txt và tối đa ba sitemap. Đây là kiểm tra nhanh một trang, không phải crawl toàn website. CLI dùng thư viện chuẩn Python, không cần API key hoặc mã nguồn gốc. Hạn mức phản hồi 2 MB, timeout 15 giây; URL nội bộ/riêng bị chặn. Dữ liệu JSON giữ nguyên tên field, còn báo cáo viết theo ngôn ngữ yêu cầu.

Mã và dữ liệu gốc đã được tích hợp trực tiếp vào skill ở `scripts/`, `data/`, `schema/`, `skills/` và `extensions/`. Dùng `python <skill-dir>/scripts/runtime.py doctor --json` để kiểm tra. Chỉ chạy `setup` khi được yêu cầu cài môi trường. Không chạy installer extension mặc định. Không đưa token, khóa API, email riêng hoặc dữ liệu khách hàng vào Git. Dịch vụ có đăng nhập/tính phí cần adapter CHC riêng sau khi có tài khoản và quyền phù hợp.

## Dữ liệu xuất
Dùng mẫu report.vi.md. Nếu cần bản Anh, dùng report.en.md và giữ nguyên finding IDs. JSON tối thiểu: brand, report_language, target_languages, target_countries, generated_at, scope, sources, findings, action_plan, limitations. Mỗi finding chứa id, url, evidence, priority, recommendation, acceptance_check và confidence. Giá trị chưa biết là null; không dùng dữ liệu mẫu làm kết quả đo thật.
