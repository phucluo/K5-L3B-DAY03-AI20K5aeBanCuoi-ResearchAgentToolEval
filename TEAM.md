# Team

## Thông tin nhóm

- Tên nhóm: 5aeBanCuoi
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-AI20K5aeBanCuoi-ResearchAgentToolEval`
- URL repo, nhánh nộp, commit chốt: https://github.com/phucluo/K5-L3B-DAY03-AI20K5aeBanCuoi-ResearchAgentToolEval · nhánh `main` · commit chốt: TODO

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Lê Ngọc Khánh | 2A202603804 |  | lekhanh2k5-dotcom | Prompt & tool declaration (v0–v3), version log |
|   2 |        |      |       |        |         |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## LeNgocKhanh-2A202603804

### Phần việc phụ trách

- System prompt và tool declaration (v0–v3); ghi `starter_v0/artifacts/version_log.csv`.

### Đóng góp cụ thể

- Cấu hình môi trường, provider Groq (`openai/gpt-oss-120b`) và key các tool (Tavily, Firecrawl, RapidAPI); preflight pass.
- Chạy baseline v0, phân tích 6 case FAIL (bảng B2 trong group report).
- v1: viết lại `system_prompt.md` (bỏ 3 chỉ dẫn xấu, thêm rule clarify / xác nhận send / multi-tool) — case_accuracy 0.70 → 0.80.

### Bằng chứng

- Commit `c6c8578`
- `starter_v0/runs/v0_B_base_openrouter_20261110T180108907998.json`
- `starter_v0/runs/v1_B_base_openrouter_20261110T181455132429.json`

## HoVaTen-MSSV

### Phần việc phụ trách

-

### Đóng góp cụ thể

-

### Bằng chứng

-
