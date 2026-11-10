# Báo cáo cá nhân — LeNgocKhanh-2A202603804

## 1. Thông tin thành viên

- Họ tên: Lê Ngọc Khánh
- MSSV: 2A202603804
- Email:

## 2. Phần việc phụ trách

- System prompt (`starter_v0/artifacts/system_prompt.md`) và tool declaration (`starter_v0/artifacts/tools.yaml`) qua các version v0–v3.
- Ghi `starter_v0/artifacts/version_log.csv` và các bảng B1, B2 trong group report.

## 3. Đóng góp cụ thể

- **Setup:** tạo venv, cài dependency, cấu hình `.env` với provider Groq (`openai/gpt-oss-120b`, dùng lại provider `openrouter` qua `OPENROUTER_BASE_URL`) và key Tavily / Firecrawl / RapidAPI. Preflight pass; smoke test `lookup`, `fetch`, `timeline`, `social_search` đều trả dữ liệu thật. `pytest`: 62 passed, 17 skipped (TODO stub).
- **v0 (baseline):** case_accuracy 0.70, routing 0.80, args 0.70, multiturn 0.83. Phân loại 6 case FAIL: R10, R11 (`missing_info`), R12 (`wrong_boundary`), R13 (`wrong_tool`), R03, M02 (`wrong_arg_value`).
- **v1:** giả thuyết — các lỗi R10–R13 do prompt starter cố ý khuyến khích đoán, gửi ngay và chỉ dùng 1 tool. Viết lại `system_prompt.md`: thiếu thông tin → `clarify`; trước `send` phải xin xác nhận; được gọi nhiều tool. Kết quả: case_accuracy 0.80, routing 0.95; R10, R11 chuyển PASS; R12 tiến bộ (không còn tự gửi) nhưng sai `response_type`; R13 chưa sửa được.
- **v2:** giả thuyết — R03/M02 sai `query` vì mô tả param của `lookup` quá sơ sài. Viết lại khối `lookup` trong `tools.yaml` (khi nào dùng/không dùng; `query` chỉ chứa chủ đề cốt lõi; tin tức/hôm nay qua `topic`/`timeframe`). Kết quả: case_accuracy 0.80 → 0.90, multiturn 0.83 → 1.00; R03, M02 chuyển PASS, không case nào bị FAIL lại.
- **v3:** giả thuyết — đặt quy ước `yes_no` ngay trong mô tả param `clarify.response_type` và boundary trong `send` sẽ sửa R12 (vì v2 cho thấy mô tả param hiệu quả hơn prompt). Viết lại mô tả mọi tool còn lại trong `tools.yaml` (khi nào dùng/không dùng + convention args). Kết quả: metric không đổi (0.90), không regression; R12, R13 vẫn FAIL → giả thuyết bị bác bỏ, đối chiếu với nhánh của Anh Quân (sửa prompt cũng thất bại) cho thấy nhiều khả năng là giới hạn của model. Phát hiện và loại một run v3 bị lệch `prompt_hash` do git chuyển line ending sang CRLF.

## 4. Bằng chứng

- File/commit/PR:
  - Commit `c6c8578` (prompt v1, version_log v0/v1, run JSON)
  - [`starter_v0/runs/v0_B_base_openrouter_20261110T180108907998.json`](../../starter_v0/runs/v0_B_base_openrouter_20261110T180108907998.json)
  - [`starter_v0/runs/v1_B_base_openrouter_20261110T181455132429.json`](../../starter_v0/runs/v1_B_base_openrouter_20261110T181455132429.json)
  - [`starter_v0/runs/v2_B_base_openrouter_20261110T183035054608.json`](../../starter_v0/runs/v2_B_base_openrouter_20261110T183035054608.json)
  - [`starter_v0/runs/v3_B_base_openrouter_20261110T185950990970.json`](../../starter_v0/runs/v3_B_base_openrouter_20261110T185950990970.json)
  - Commit `d113030` (v2), nhánh `KhanhDay03`
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - Claude Code (Claude Opus 5.5): hỗ trợ setup môi trường, chạy eval, đọc run JSON, đề xuất giả thuyết và soạn nháp prompt/báo cáo.
  - Tự kiểm tra: đối chiếu mọi metric trong báo cáo với `summary` của run JSON; kiểm tra `provider_error_cases == 0` và `measured_cases == total_cases`; đọc `failures` + `actual_tool_calls` của từng case FAIL để xác nhận nguyên nhân; chạy `pytest` trước khi commit.

## 5. Tự đánh giá

- **Mức độ hoàn thành:** Hoàn thành đầy đủ phần việc được giao (CP1 và CP2): thiết lập môi trường chạy provider thật không lỗi (`provider_error_cases == 0`), đo baseline v0, phân tích lỗi và thực hiện trọn vẹn 3 vòng lặp tối ưu v1–v3 đúng nguyên tắc mỗi version kiểm chứng một giả thuyết độc lập, nâng `case_accuracy` từ `0.70` lên `0.90` và `multiturn` từ `0.83` lên `1.00` mà không làm gãy contract test (`pytest tests/test_tool_contract.py` luôn pass).
- **Bài học rút ra:**
  - Phân biệt rõ vai trò giữa `system_prompt.md` và `tools.yaml`: các quy tắc hành vi tổng quát (như hỏi lại bằng `clarify` khi thiếu thông tin, xin xác nhận trước khi `send`, cho phép gọi nhiều tool) đặt ở `system_prompt.md` giúp cải thiện mạnh `routing` (`0.80` → `0.95` ở v1); trong khi quy ước truyền tham số (như giữ `query` ngắn gọn, tách `topic`/`timeframe`) đặt trực tiếp tại mô tả từng parameter trong `tools.yaml` lại hiệu quả hơn hẳn để sửa lỗi `wrong_arg_value` (`args` tăng từ `0.70` lên `0.90` ở v2).
  - Việc giữ kỷ luật "một giả thuyết mỗi version" và kiểm tra `prompt_hash`/`tools_hash` giúp cô lập chính xác nguyên nhân thay đổi điểm số (kể cả khi giả thuyết bị bác bỏ như ở v3) và phát hiện sớm sai lệch kỹ thuật (như lỗi đổi line ending CRLF làm lệch hash).
- **Điểm hạn chế & hướng cải thiện:** Hai case R12 (`wrong_boundary` / sai `response_type` ở bước xác nhận) và R13 (`wrong_tool`) vẫn chưa vượt qua được sau v3 dù đã thử can thiệp ở cả tool declaration lẫn system prompt. Hướng cải thiện tiếp theo là thử nghiệm few-shot ngắn cho tình huống xác nhận `yes_no` hoặc đối chiếu thêm trên các model khác để tách bạch rõ giới hạn của model `openai/gpt-oss-120b` với cách diễn đạt schema.
