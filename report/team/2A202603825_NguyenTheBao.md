# Báo cáo cá nhân — NguyenTheBao-2A202603825

## 1. Thông tin thành viên

- Họ tên: Nguyễn Thế Bảo
- MSSV: 2A202603825
- Email:
- Nhóm: AI20K5aeBanCuoi (Lớp L3B)

---

## 2. Phần việc phụ trách

Trong bài làm nhóm Day 03 (*Research Agent Tool Eval*), tôi phụ trách xây dựng giao diện Streamlit cho Research Agent (CP5) trong [`starter_v0/app.py`](../../starter_v0/app.py), tập trung vào trải nghiệm demo hội thoại, cấu hình model và quan sát các lượt gọi công cụ.

---

## 3. Đóng góp cụ thể

- Xây dựng giao diện web theo phong cách xanh tím than, gồm tiêu đề, thanh cấu hình bên cạnh và khu vực chat.
- Tạo tùy chọn provider và model; cấu hình mặc định trên giao diện là Groq với model `openai/gpt-oss-120b`.
- Thêm các câu hỏi mẫu để demo tra cứu arXiv, chính sách công ty và ranh giới xác nhận trước khi gửi tin.
- Kết nối giao diện với vòng lặp hội thoại và gọi công cụ trong [`starter_v0/chat.py`](../../starter_v0/chat.py).
- Hiển thị các bước suy luận do vòng lặp trả về, nội dung phản hồi và chi tiết lời gọi công cụ (tên, tham số, kết quả); bổ sung nút xóa lịch sử trò chuyện.
- Tạo transcript theo phiên với thông tin phiên bản artifact, provider, model và nội dung các lượt hội thoại.
- Khởi chạy app tại `http://localhost:8501` và xác nhận endpoint kiểm tra sức khỏe trả về `HTTP 200` (`ok`).

---

## 4. Bằng chứng

### Mã nguồn và tích hợp

- Giao diện Streamlit: [`starter_v0/app.py`](../../starter_v0/app.py)
- Vòng lặp chat, gọi công cụ và ghi transcript: [`starter_v0/chat.py`](../../starter_v0/chat.py)
- Danh sách dependency hiện tại: [`starter_v0/requirements.txt`](../../starter_v0/requirements.txt)

### Kiểm tra chạy

- Lệnh chạy: `streamlit run app.py`
- URL: `http://127.0.0.1:8501`
- Kết quả kiểm tra: `http://127.0.0.1:8501/_stcore/health` trả về `200 ok`.
- Việc kiểm tra trên xác nhận ứng dụng khởi động và phản hồi health check; chưa thay thế cho kiểm thử tương tác đầy đủ qua giao diện hoặc xác nhận toàn bộ luồng gọi model trực tiếp.

### Công cụ hỗ trợ và lưu ý

- Sử dụng Copilot trong VS Code để hỗ trợ rà soát mã nguồn và cách khởi chạy ứng dụng; kiểm tra kết quả trực tiếp trong workspace.
- Môi trường `.venv` của workspace cần cài `streamlit` để chạy app. [`starter_v0/requirements.txt`](../../starter_v0/requirements.txt) hiện chưa khai báo dependency này, nên cần bổ sung nếu muốn tái tạo môi trường chạy trên máy mới.
- Giao diện có hiển thị nhãn `summarize_paper (Mới)`, nhưng cần xác nhận tool tương ứng đã được triển khai và đăng ký trong hệ thống trước khi giới thiệu đó là chức năng hoạt động.

---

## 5. Tự đánh giá

Tôi đã hoàn thành giao diện chat và các thành phần hỗ trợ demo chính, đồng thời xác nhận ứng dụng có thể khởi động và phản hồi health check. Phần cần hoàn thiện tiếp theo là khai báo dependency Streamlit để dễ cài đặt trên máy khác, kiểm thử tương tác end-to-end qua giao diện và chỉ giới thiệu những tool đã được đăng ký, tích hợp thực sự.
