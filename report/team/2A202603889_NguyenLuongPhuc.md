# Báo cáo cá nhân — Nguyễn Lương Phúc-2A202603889

## 1. Thông tin thành viên

- Họ tên: Nguyễn Lương Phúc
- MSSV: 2A202603889
- Email: 26ai.phucnl@vinuni.edu.vn
- Nhóm: AI20K5aeBanCuoi
- Lớp: L3B
- Nhánh nộp bài: `main`

## 2. Phần việc phụ trách

- Team lead, điều phối và tổng hợp kết quả của các thành viên.
- Review và merge PR để tích hợp bài làm lên `main`.
- Quản lý, rà soát `starter_v0/artifacts/version_log.csv`, đối chiếu version, hash, giả thuyết, metric trước/sau và đường dẫn run.
- Tổng hợp nhận xét cho mục B6 Reflection trong báo cáo nhóm.
- Rà soát checklist theo `README.md`, `RUBRIC.md` và `SUBMISSION.md` trước khi chốt bài.

## 3. Đóng góp cụ thể

### Tích hợp bài làm và tổng hợp đóng góp

- Mở và merge PR #2 từ `AnhQuanHanuDay03` vào `main` bằng merge commit `18b7b30`, đưa code của Quân cùng 7 commit trong PR vào lịch sử nhánh nộp.
- Cập nhật tên, MSSV và vai trò của mình tại mục 6 trong `group_report.md` qua commit `012c2a9`.
- Cập nhật thông tin thành viên, phân công trong `TEAM.md` và hoàn thiện báo cáo cá nhân theo mẫu 5 mục của lab.

### Rà soát version log và kết quả thực nghiệm

Với sự hỗ trợ của Codex, đối chiếu bốn dòng v0–v3 trong [version log](../../starter_v0/artifacts/version_log.csv) với các run JSON được liên kết bên dưới. Cả bốn run dùng Groq `openai/gpt-oss-120b`, có `provider_error_cases == 0` và `measured_cases == total_cases == 20`. Các trường `artifact_version`, tiền tố `prompt_hash`/`tools_hash`, `metric_after` và `run_file` trong CSV khớp với run tương ứng.

| Version | Artifact thay đổi | Case accuracy trước → sau | Nhận xét từ run |
|---|---|---|---|
| v0 | Baseline | — → 0.70 (14/20) | Làm mốc so sánh cho các vòng tối ưu |
| v1 | `system_prompt.md` | 0.70 → 0.90 (18/20) | Tăng 20 điểm phần trăm so với baseline |
| v2 | `tools.yaml` | 0.90 → 0.90 (18/20) | Metric này giữ ở mức của v1 |
| v3 | `system_prompt.md` | 0.90 → 0.90 (18/20) | Còn FAIL ở `R12_confirm_before_send` và `R13_parallel_web_and_tweets` |

### Nhận xét phục vụ B6 Reflection

- System prompt phù hợp để quy định hành vi chung như hỏi lại khi thiếu thông tin, xin xác nhận trước khi gửi và dùng nhiều tool khi yêu cầu cần nhiều nguồn. Kết quả v1 cho thấy việc sửa prompt đi kèm mức tăng case accuracy từ 0.70 lên 0.90.
- Tool declaration giúp mô tả công dụng, điều kiện sử dụng và quy ước tham số như `screenname`, `topic`, `timeframe`. Trong chuỗi run base đã ghi, v2 và v3 đều đạt 0.90. Cần giữ kết luận này khi tổng hợp Reflection theo tiêu chí C3 về phân tích trung thực.
- Trong run base v3, `R12` gọi `clarify` với `response_type="text"` thay vì `"yes_no"`; `R13` thiếu `social_search`. Hướng cải thiện là tập trung từng giả thuyết vào hai lỗi này rồi chạy lại cùng bộ base.
- Run group đạt 10/10 với `provider_error_cases == 0`, `measured_cases == total_cases == 10`. Run này dùng hash prompt `78914f1c4e10` và tools `6a18d5b42487`, khớp với artifacts hiện tại và transcript live. Run base v3 trong CSV dùng hash `f0065401bee1` và `6c871965929f`. Cần ghi thêm phiên bản cho lần đổi artifacts và chạy base trên cùng cấu hình để so sánh với group.
- Transcript live ghi nhận luồng hỏi xác nhận rồi gọi `send(confirmed=true)` ở lượt sau. Kết quả tool `send` trả `RuntimeError`; việc đánh giá gửi Telegram thành công cần bằng chứng `status: sent` theo rubric bonus.

### Rà soát checklist trước khi chốt bài

| Hạng mục | Kết quả đối chiếu và phần cần hoàn tất |
|---|---|
| Run base v0–v3 và CSV | Có đủ bốn run được tham chiếu, đủ measured cases, 0 provider error; hash và metric khớp CSV |
| Eval nhóm | Có đúng 10 case, gồm 5 single turn và 5 multi turn; G02/G07 kiểm tra tool mới `summarize_paper`; run group đạt 10/10 |
| Tính nhất quán của phiên bản | Cần ghi nhận cấu hình group/live khác base v3 và bổ sung run base tương ứng |
| Báo cáo cá nhân | Có file đúng tên cho cả 5 thành viên trên `main`; cần đối chiếu commit kỹ thuật của từng người theo C8 |
| Unit test và UI | Báo cáo nhóm ghi 84 passed, 0 failed, 0 skipped và có lệnh chạy Streamlit; cần kiểm tra output `pytest` và chạy UI ở môi trường nộp bài |
| Live chat | Transcript chính có 4 lượt; cần bổ sung tình huống thiếu thông tin rồi người dùng cung cấp thêm theo C6 |
| Chốt bài | Cần điền SHA commit chốt vào `TEAM.md` sau các cập nhật cuối và xác nhận mỗi người đã nộp cùng link repo lên LMS |

## 4. Bằng chứng

### File, commit và PR

- PR tích hợp code Quân và commit merge do `phucluo` thực hiện. [PR #2](https://github.com/phucluo/K5-L3B-DAY03-AI20K5aeBanCuoi-ResearchAgentToolEval/pull/2), [commit 18b7b30](https://github.com/phucluo/K5-L3B-DAY03-AI20K5aeBanCuoi-ResearchAgentToolEval/commit/18b7b305f2c7ffc9d97383e0f18f110bbd0855bf).
- Cập nhật vai trò nhóm trưởng trong tổng hợp đóng góp. [Commit 012c2a9](https://github.com/phucluo/K5-L3B-DAY03-AI20K5aeBanCuoi-ResearchAgentToolEval/commit/012c2a99a7a4ad9754eddb18a49e3511e3a7ff7f).
- Cập nhật phân công thành viên. [Commit 96810d7](https://github.com/phucluo/K5-L3B-DAY03-AI20K5aeBanCuoi-ResearchAgentToolEval/commit/96810d777b6193f95bc547aab2115bd0d8936499), [TEAM.md](../../TEAM.md).
- Dữ liệu nhóm dùng để đối chiếu version và tổng hợp nhận xét Reflection. [Version log](../../starter_v0/artifacts/version_log.csv), [báo cáo nhóm](group_report.md).
- Run base đã đối chiếu. [v0](../../starter_v0/runs/v0_B_base_groq_20261110T175650792984.json), [v1](../../starter_v0/runs/v1_B_base_groq_20261110T180058765915.json), [v2](../../starter_v0/runs/v2_B_base_groq_20261110T180517362630.json), [v3](../../starter_v0/runs/v3_B_base_groq_20261110T180941997435.json).
- Eval nhóm và live chat. [10 case nhóm](../../starter_v0/data/eval_group.json), [run group](../../starter_v0/runs/v3_B_group_groq_20261110T181849672426.json), [transcript 4 lượt](../../starter_v0/transcripts/v3_groq_20261110T181940006104.transcript.json).
- Hướng dẫn dùng để rà soát bài. [README.md](../../README.md), [RULES.md](../../RULES.md), [RUBRIC.md](../../RUBRIC.md), [SUBMISSION.md](../../SUBMISSION.md).

### AI/công cụ đã dùng và cách kiểm tra kết quả

- Dùng Codex để hỗ trợ hiểu quy trình PR/merge, đọc hướng dẫn lab, đối chiếu bằng chứng trong repo và biên tập báo cáo cá nhân cùng phần đóng góp trong `TEAM.md`.
- Dùng GitHub để xem lịch sử commit, PR và nội dung trên `main`. Trong quá trình hỗ trợ rà soát, Codex dùng Python để kiểm tra CSV, hash SHA-256 của artifacts và số liệu JSON tải trực tiếp từ GitHub.
- Cách kiểm tra là đối chiếu từng nhận xét với đường dẫn file/commit/PR, kiểm tra số case, điều kiện run hợp lệ, metric và hash. Các nhận xét về unit test/UI được ghi kèm việc cần xác nhận bằng output hoặc chạy thử.
- Các run được dẫn là kết quả nhóm đã lưu trên GitHub. Phần rà soát này đối chiếu dữ liệu của nhánh `main` tại commit [`ba823d8`](https://github.com/phucluo/K5-L3B-DAY03-AI20K5aeBanCuoi-ResearchAgentToolEval/tree/ba823d8f8a00d721165eec3dc361e64835c39d22).

## 5. Tự đánh giá
- Kiểm soát đầu ra ở mức tạm chấp nhận cho dự án.
- Bản thân còn nhiều điều chưa làm tốt trong việc chủ động phân công và thúc đẩy các thành viên hoàn thiện tiến độ sớm.
