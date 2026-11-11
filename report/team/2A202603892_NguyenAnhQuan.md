# Báo cáo cá nhân — Nguyễn Anh Quân - 2A202603892

## 1. Thông tin thành viên

- Họ tên: Nguyễn Anh Quân
- MSSV: 2A202603892
- Email: (Điền email trường / cá nhân của bạn)
- Nhóm: AI20K5aeBanCuoi (Lớp L3B)

---

## 2. Phần việc phụ trách

Trong bài làm nhóm Day 03 (*Research Agent Tool Eval*), tôi đảm nhận vai trò **Kỹ sư Tích hợp Mô hình & Phát triển Công cụ (Model Integration & Tooling Engineer)** với các nhiệm vụ cụ thể:

1. **Tích hợp Model Provider (Groq API)**:
   - Xây dựng module kết nối `GroqProvider` dựa trên nền tảng OpenAI-compatible endpoint và model `openai/gpt-oss-120b`, thay thế provider ban đầu nhằm đảm bảo tốc độ phản hồi cao, hỗ trợ tool calling chuẩn xác và đạt `provider_error_cases == 0` tuyệt đối qua tất cả các lượt chạy.
   - Quản lý cấu hình bí mật môi trường `.env`, đảm bảo tuân thủ nguyên tắc bảo mật không lộ credential lên Git.

2. **Thiết kế & Triển khai Tool Mới (CP3)**:
   - Phát triển công cụ mới `summarize_paper` trong `tools/summarize_paper/` hỗ trợ agent trích xuất có cấu trúc các phát hiện nghiên cứu (findings), phương pháp (methodology) và giới hạn (limitations) từ nội dung bài báo khoa học.
   - Soạn thảo tài liệu đặc tả `TOOL.md` chuẩn hóa frontmatter metadata theo đúng quy ước của bài lab.

3. **Hiện thực hóa Bộ Unit Test cho Tool (CP3 Challenge)**:
   - Viết toàn bộ các test case unit test trong `tests/test_tools_todo.py`, bao gồm ≥ 3 unit test cho tool mới `summarize_paper` (happy path, bad/empty input, failure path) và các test cho toàn bộ công cụ hệ thống (`clarify`, `format`, `send`, `lookup`, `fetch`, `timeline`, `social_search`, `policy`).
   - Đảm bảo toàn bộ test suite `pytest` đạt **84 passed, 0 failed, 0 skipped** (đạt yêu cầu Test Challenge).

4. **Xây dựng Test Case Đánh giá Nhóm & Thực thi Đo lường (CP4 & Vòng lặp v0–v3)**:
   - Đóng góp xây dựng các test case kiểm thử trong `data/eval_group.json` (bao phủ tool mới và các tình huống ranh giới đa lượt).
   - Thực thi các lệnh đo lường base eval và group eval, ghi nhận dữ liệu vào `artifacts/version_log.csv`.

---

## 3. Đóng góp cụ thể

- **Code Base**:
  - Viết module `starter_v0/providers/groq_provider.py` và đăng ký provider trong `starter_v0/providers/__init__.py`, `starter_v0/run_eval.py`, `starter_v0/chat.py`.
  - Viết mã nguồn công cụ `starter_v0/tools/summarize_paper/tool.py` xử lý phân tích logic, bắt lỗi an toàn trả về dict `err` thay vì raise exception, đăng ký vào `starter_v0/tools/__init__.py` và `starter_v0/artifacts/tools.yaml`.
  - Hoàn thiện toàn bộ các hàm test stubs trong `starter_v0/tests/test_tools_todo.py` sử dụng mock `fake_http` và fixture độc lập, không phụ thuộc mạng bên ngoài.
- **Dữ liệu đánh giá (Eval Cases)**:
  - Soạn thảo các test case kiểm tra khả năng route tới tool mới `summarize_paper` và kiểm tra ranh giới xác nhận hai bước trong `starter_v0/data/eval_group.json`.
- **Thực nghiệm & Đo lường**:
  - Chạy baseline `v0` đạt 70% accuracy (14/20 passed, 0 provider errors), lưu log tại `runs/v0_B_base_groq_20261110T175650792984.json`.
  - Thực hiện các vòng lặp cải tiến `v1` $\rightarrow$ `v3` nâng accuracy lên 90% (18/20 passed, 0 provider errors).
  - Chạy đánh giá bộ test case nhóm `--suite group` đạt **100% accuracy (10/10 passed, 0 provider errors)** tại `runs/v3_B_group_groq_20261110T181849672426.json`.
  - Thực hiện phiên chat trực tiếp đa lượt để xuất transcript thật tại `transcripts/v3_groq_20261110T181940006104.transcript.json`.

---

## 4. Bằng chứng

### File mã nguồn & Tài liệu
- Provider: [`starter_v0/providers/groq_provider.py`](file:///e:/AI/K5-L3B-DAY03-AI20K5aeBanCuoi-ResearchAgentToolEval/starter_v0/providers/groq_provider.py)
- Tool mới: [`starter_v0/tools/summarize_paper/tool.py`](file:///e:/AI/K5-L3B-DAY03-AI20K5aeBanCuoi-ResearchAgentToolEval/starter_v0/tools/summarize_paper/tool.py)
- Tài liệu tool: [`starter_v0/tools/summarize_paper/TOOL.md`](file:///e:/AI/K5-L3B-DAY03-AI20K5aeBanCuoi-ResearchAgentToolEval/starter_v0/tools/summarize_paper/TOOL.md)
- Unit test hoàn chỉnh: [`starter_v0/tests/test_tools_todo.py`](file:///e:/AI/K5-L3B-DAY03-AI20K5aeBanCuoi-ResearchAgentToolEval/starter_v0/tests/test_tools_todo.py)
- Nhật ký version: [`starter_v0/artifacts/version_log.csv`](file:///e:/AI/K5-L3B-DAY03-AI20K5aeBanCuoi-ResearchAgentToolEval/starter_v0/artifacts/version_log.csv)
- Test case nhóm: [`starter_v0/data/eval_group.json`](file:///e:/AI/K5-L3B-DAY03-AI20K5aeBanCuoi-ResearchAgentToolEval/starter_v0/data/eval_group.json)

### Log đo lường thực tế (Runs & Transcripts)
- Baseline `v0`: [`starter_v0/runs/v0_B_base_groq_20261110T175650792984.json`](file:///e:/AI/K5-L3B-DAY03-AI20K5aeBanCuoi-ResearchAgentToolEval/starter_v0/runs/v0_B_base_groq_20261110T175650792984.json)
- Run `v1`: [`starter_v0/runs/v1_B_base_groq_20261110T180058765915.json`](file:///e:/AI/K5-L3B-DAY03-AI20K5aeBanCuoi-ResearchAgentToolEval/starter_v0/runs/v1_B_base_groq_20261110T180058765915.json)
- Run `v2`: [`starter_v0/runs/v2_B_base_groq_20261110T180517362630.json`](file:///e:/AI/K5-L3B-DAY03-AI20K5aeBanCuoi-ResearchAgentToolEval/starter_v0/runs/v2_B_base_groq_20261110T180517362630.json)
- Run `v3`: [`starter_v0/runs/v3_B_base_groq_20261110T180941997435.json`](file:///e:/AI/K5-L3B-DAY03-AI20K5aeBanCuoi-ResearchAgentToolEval/starter_v0/runs/v3_B_group_groq_20261110T181849672426.json)
- Group Eval Run: [`starter_v0/runs/v3_B_group_groq_20261110T181849672426.json`](file:///e:/AI/K5-L3B-DAY03-AI20K5aeBanCuoi-ResearchAgentToolEval/starter_v0/runs/v3_B_group_groq_20261110T181849672426.json)
- Transcript Live Chat: [`starter_v0/transcripts/v3_groq_20261110T181940006104.transcript.json`](file:///e:/AI/K5-L3B-DAY03-AI20K5aeBanCuoi-ResearchAgentToolEval/starter_v0/transcripts/v3_groq_20261110T181940006104.transcript.json)

### AI và Công cụ đã dùng
- **Antigravity AI**: Được sử dụng như một cộng sự lập trình (pair-programmer) để hỗ trợ cấu trúc hóa code, soạn thảo nhanh các mẫu test mock và kiểm tra đối chiếu schema JSON.
- **Phương pháp tự kiểm tra độc lập**: 
  - Chạy kiểm tra tĩnh contract: `pytest tests/test_tool_contract.py`.
  - Chạy toàn bộ unit test độc lập: `pytest tests/ -v` (kết quả 84/84 test passed, 0 skipped, 0 failed).
  - Soát lỗi rò rỉ bảo mật qua `git status --ignored` để xác nhận file `.env` được bảo vệ tuyệt đối.

---

## 5. Tự đánh giá

- Mức độ hoàn thành công việc: **10/10** (Hoàn thành vượt tiến độ các cam kết kỹ thuật, mã nguồn chuẩn chỉ, kiểm thử tự động toàn diện).
- Tuân thủ liêm chính học thuật: **10/10** (Không can thiệp sửa đổi `eval_base.json`, đo đạc bằng chứng trung thực dựa trên log JSON thật từ API, bảo vệ tuyệt đối API key).
- Đóng góp vào thành công chung của nhóm: Cung cấp giải pháp chạy mô hình Groq ổn định, mang lại bộ công cụ và bài test hoàn chỉnh giúp cả nhóm có bằng chứng xác thực để tự tin thuyết trình và hoàn thành báo cáo chung.
