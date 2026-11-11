# Team

## Thông tin nhóm

- Tên nhóm: AI20K5aeBanCuoi
- Lớp: L3B
- Repo nhóm: K5-L3B-DAY03-AI20K5aeBanCuoi-ResearchAgentToolEval
- URL repo, nhánh nộp, commit chốt: https://github.com/phucluo/K5-L3B-DAY03-AI20K5aeBanCuoi-ResearchAgentToolEval

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Lương Phúc | 2A202603889 | 26ai.phucnl@vinuni.edu.vn | phucluo | Team lead - Review merge PR, quản lý artifacts/version_log.csv, hoàn thiện mục Reflection và rà soát checklist trước khi nộp bài|
|   2 | Nguyễn Anh Quân | 2A202603892 |       | AnhQuanHANU| Phụ trách CP3 (Code Tool mới `summarize_paper`, viết Unit Test, tích hợp `GroqProvider`, xây dựng 10 test case CP4|
|   3 | Lê Ngọc Khánh | 2A202603804 | lekhanh2k5@gmail.com | lekhanh2k5-dotcom | Prompt & tool declaration (v0–v3), version log |
|   4 | Nguyễn Minh Thành | 2A202603884 | thanhhy98@gmail.com | thanhhy98 | Evaluation, Q&A (v7)|
|   5 | Nguyễn Thế Bảo | 2A202603825 |       | NTBao | Phụ trách xây dựng Streamlit UI, cấu hình `requirements.txt`|
|   6 |        |      |       |        |         |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## LeNgocKhanh-2A202603804

### Phần việc phụ trách

- System prompt và tool declaration (v0–v3); ghi `version_log.csv` (chuỗi trên nhánh `KhanhDay03`).

### Đóng góp cụ thể

- Cấu hình môi trường, provider Groq (`openai/gpt-oss-120b`) và key các tool (Tavily, Firecrawl, RapidAPI).
- Baseline v0 và phân tích 6 case FAIL; v1 (system prompt), v2 (`lookup` trong `tools.yaml`), v3 (mọi tool còn lại): case_accuracy 0.70 → 0.80 → 0.90 → 0.90.

### Bằng chứng

- Commit `c6c8578`, `d113030`, `1d403c6`; nhánh [`KhanhDay03`](https://github.com/phucluo/K5-L3B-DAY03-AI20K5aeBanCuoi-ResearchAgentToolEval/tree/KhanhDay03)
- Báo cáo cá nhân: [`report/team/2A202603804_LeNgocKhanh.md`](report/team/2A202603804_LeNgocKhanh.md)

## NguyenMinhThanh-2A202603884

### Phần việc phụ trách

- Evaluation và QA (CP7): rà soát kết quả eval, kiểm tra điều kiện hợp lệ của run, xác nhận contract tests và unit tests.

### Đóng góp cụ thể

- Đối chiếu run base v0–v3 trên cùng model Groq `openai/gpt-oss-120b`: case accuracy `0.70 → 0.90 → 0.90 → 0.90`; v1 tăng so với baseline, v2/v3 không tăng thêm metric này.
- Kiểm tra run group v3: 10/10 case pass, không có provider error, đủ measured cases; routing, argument và multi-turn accuracy đều `1.00`.
- Chỉ dùng run thỏa điều kiện rubric (`provider_error_cases == 0`, `measured_cases == total_cases`); loại các run lỗi xác thực/provider hoặc thiếu measured cases khỏi kết luận.
- Chạy QA suite: contract + TODO tool tests đạt 77 passed; toàn bộ pytest đạt 84 passed, 0 failed, 0 skipped.

### Bằng chứng

- Báo cáo cá nhân và chi tiết số liệu: [`report/team/2A202603884_NguyenMinhThanh.md`](report/team/2A202603884_NguyenMinhThanh.md)
- Run group: [`starter_v0/runs/v3_B_group_groq_20261110T181849672426.json`](starter_v0/runs/v3_B_group_groq_20261110T181849672426.json); bộ case: [`starter_v0/data/eval_group.json`](starter_v0/data/eval_group.json)
- Run base và hash/version log: [`starter_v0/artifacts/version_log.csv`](starter_v0/artifacts/version_log.csv); QA tests: [`starter_v0/tests/test_tool_contract.py`](starter_v0/tests/test_tool_contract.py), [`starter_v0/tests/test_tools_todo.py`](starter_v0/tests/test_tools_todo.py)
- Commit `bdb2f8c`, `e9e45a6` ; nhánh [`nguyen-minh-thanh`](https://github.com/phucluo/K5-L3B-DAY03-AI20K5aeBanCuoi-ResearchAgentToolEval/tree/nguyen-minh-thanh)


## HoVaTen-MSSV

### Phần việc phụ trách

-

### Đóng góp cụ thể

-

### Bằng chứng

-
