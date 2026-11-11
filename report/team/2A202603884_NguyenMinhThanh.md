# Báo cáo cá nhân — Nguyễn Minh Thành

## 1. Thông tin thành viên

- Họ tên: Nguyễn Minh Thành
- MSSV: 2A202603884
- Email: thanhhy98@gmail.com

## 2. Phần việc phụ trách

- CP7 — Evaluation và QA: rà soát bộ đánh giá nhóm, kiểm tra tính hợp lệ của run, đối chiếu kết quả theo từng version và xác nhận contract/unit tests.

## 3. Đóng góp cụ thể

- Đối chiếu 10 case trong `starter_v0/data/eval_group.json` với run group hợp lệ. Bộ case có 5 single-turn và 5 multi-turn, bao gồm routing tới `summarize_paper`, xử lý thiếu thông tin, out-of-scope và xác nhận gửi Telegram.
- Kiểm tra run v0–v3 trên cùng model `openai/gpt-oss-120b`: base case accuracy tăng từ 0.70 ở v0 lên 0.90 ở v1, rồi giữ ở 0.90 ở v2 và v3. Routing accuracy lần lượt là 0.80, 0.95, 0.95, 0.95; argument accuracy là 0.70, 0.90, 0.90, 0.90.
- Xác nhận từng run base được dùng có đủ 20/20 measured cases và 0 provider errors. Đối chiếu hash cho thấy v1 thay prompt, v2 thay tool declarations, v3 thay prompt.
- Xác nhận run group v3 đạt 10/10 case, `provider_error_cases=0`, `measured_cases=total_cases=10`; cả routing, argument và multi-turn accuracy đều là 1.00.
- Chạy contract tests và unit tests của tool mới; kiểm tra suite đầy đủ để bảo đảm thay đổi không làm hỏng regression tests.
- Loại khỏi kết luận các run có provider errors hoặc thiếu measured cases, ví dụ các run OpenRouter bị lỗi xác thực và run Groq gpt-oss-20b có provider error. Không so sánh chúng như thể cùng điều kiện với các run gpt-oss-120b hợp lệ.

## 4. Bằng chứng

- Eval nhóm: [`starter_v0/data/eval_group.json`](../../starter_v0/data/eval_group.json), [`starter_v0/runs/v3_B_group_groq_20261110T181849672426.json`](../../starter_v0/runs/v3_B_group_groq_20261110T181849672426.json).
- Base eval v0–v3: [`v0`](../../starter_v0/runs/v0_B_base_groq_20261110T175650792984.json), [`v1`](../../starter_v0/runs/v1_B_base_groq_20261110T180058765915.json), [`v2`](../../starter_v0/runs/v2_B_base_groq_20261110T180517362630.json), [`v3`](../../starter_v0/runs/v3_B_base_groq_20261110T180941997435.json); version/hash log: [`starter_v0/artifacts/version_log.csv`](../../starter_v0/artifacts/version_log.csv).
- QA tests: [`starter_v0/tests/test_tool_contract.py`](../../starter_v0/tests/test_tool_contract.py), [`starter_v0/tests/test_tools_todo.py`](../../starter_v0/tests/test_tools_todo.py).
- Lệnh kiểm tra từ `starter_v0/`: `.venv/bin/python -m pytest -q tests/test_tool_contract.py tests/test_tools_todo.py` — **77 passed**; `.venv/bin/python -m pytest -q` — **84 passed, 0 failed, 0 skipped**.
- Cách tự kiểm tra: đọc `summary` từ từng run JSON và chỉ tính run thỏa điều kiện rubric (`provider_error_cases == 0`, `measured_cases == total_cases`); chạy test offline với mock HTTP, không dùng API key thật.
- Công cụ hỗ trợ: Python/pytest và AI hỗ trợ tổng hợp; các số liệu được đối chiếu trực tiếp với run JSON và kết quả test.
- Commit cá nhân: chưa ghi nhận commit riêng trong lịch sử hiện có; không gán commit của thành viên khác làm bằng chứng cá nhân.

## 5. Tự đánh giá

- Hoàn thành phần kiểm tra tính hợp lệ và tổng hợp kết quả evaluation/QA có thể tái chạy. Kết quả cho thấy v1 cải thiện rõ so với baseline; v2 và v3 không tăng thêm base accuracy, nên không kết luận các vòng này có cải thiện metric đó.
- Bộ group eval đạt 10/10 nhưng chỉ gồm 10 case và dùng một model; đây là bằng chứng cho các tình huống đã kiểm thử, không đảm bảo agent đúng với mọi truy vấn thực tế. Cần bổ sung thêm biến thể đầu vào và chạy lặp để đo độ ổn định.
- Một cảnh báo `NotOpenSSLWarning` từ urllib3 xuất hiện do môi trường Python dùng LibreSSL; không làm thất bại tests hoặc thay đổi kết quả QA.
