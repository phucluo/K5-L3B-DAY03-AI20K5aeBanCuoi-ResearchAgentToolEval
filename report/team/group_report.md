# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: 5aeBanCuoi
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: **Groq** — model `openai/gpt-oss-120b`, gọi qua provider `openrouter` của starter (API Groq tương thích OpenAI; cấu hình `OPENROUTER_BASE_URL=https://api.groq.com/openai/v1` trong `.env`). Vì vậy trong run JSON trường provider ghi là `openrouter`. Lệnh chạy:
  `python run_eval.py --provider openrouter --model openai/gpt-oss-120b --version <vX> --suite base --eval-cases data/eval_base.json`

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

Research agent: tìm tin tức/thông tin trên web, xem bài đăng gần đây của một tài khoản X (Twitter) hoặc tìm bài đăng theo từ khóa, đọc nội dung một URL, tra paper arXiv và policy nội bộ, tổng hợp thành digest — và **hỏi lại khi thiếu thông tin**, **xin xác nhận trước khi gửi** bản tin lên Telegram.

**Cách chạy UI:**

> TODO — chờ phần UI (lệnh chạy + dependency trong `starter_v0/requirements.txt`).

**Link dùng thử (deploy):**

> URL: TODO

### A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | Hỏi lại người dùng khi thiếu thông tin hoặc cần xác nhận | không |
| timeline | Lấy bài đăng gần đây của một tài khoản X theo handle (vd `sama`) | không |
| social_search | Tìm bài đăng trên X theo từ khóa (`Latest` / `Top`) | không |
| lookup | Tìm trên web (Tavily), có `topic` general/news và `timeframe` | không |
| fetch | Đọc nội dung một URL (Firecrawl) | không |
| format | Trình bày các item đã có thành markdown digest | không |
| send | Gửi text lên Telegram channel — chỉ khi `confirmed=true` | không |
| policy | Tìm trong company policy markdown nội bộ | không |
| papers | Tìm paper trên arXiv | không |
| paper_text | Tải PDF arXiv và trích text | không |
| TODO | (tool mới của nhóm) | **có** |

### A3. Câu hỏi mẫu để thử

1. Tweet mới nhất của Sam Altman là gì?
2. Tin tức AI hôm nay có gì nổi bật?
3. Đọc giúp mình bài này: https://openai.com/research/
4. Tìm tweet về GPT-5 → agent tìm theo từ khóa trên X.
5. Đăng bản tin này lên Telegram giúp mình → agent phải **hỏi xác nhận**, không gửi ngay.

## 3. Giải pháp

- **v1 — `system_prompt.md`** (commit `c6c8578`): bỏ 3 chỉ dẫn xấu cố ý của starter ("đừng hỏi lại, cứ đoán", "chọn tài khoản nổi tiếng như Sam Altman / giả định URL", "muốn gửi thì cứ gửi luôn", "luôn làm trong 1 bước, chọn 1 tool"). Thay bằng 3 rule: (1) thiếu/mơ hồ tham số bắt buộc → gọi `clarify`, không đoán handle/bịa URL; (2) trước `send` phải cho xem nội dung và `clarify` xin xác nhận, chỉ `send(confirmed=true)` sau khi user đồng ý ở lượt sau; (3) yêu cầu nhiều phần → gọi đủ các tool cần thiết.
- v2, v3: TODO.
- Tool mới: TODO.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ [`starter_v0/artifacts/version_log.csv`](../../starter_v0/artifacts/version_log.csv) và `starter_v0/runs/*.json`. Mọi run dưới đây đều có `provider_error_cases == 0` và `measured_cases == total_cases == 20`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline (starter chưa sửa) | — | — | case 0.70 · route 0.80 · args 0.70 · multi 0.83 | [`v0_B_base_openrouter_20261110T180108907998.json`](../../starter_v0/runs/v0_B_base_openrouter_20261110T180108907998.json) |
| v1 | `system_prompt.md` | Lỗi `missing_info` / `wrong_boundary` / `wrong_tool` ở R10–R13 là do prompt starter cố ý khuyến khích đoán, gửi ngay và chỉ dùng 1 tool; bỏ và thay bằng rule clarify / xác nhận send / multi-tool sẽ sửa R10–R13 | case 0.70 · route 0.80 · args 0.70 | case **0.80** · route **0.95** · args **0.80** · multi 0.83 | [`v1_B_base_openrouter_20261110T181455132429.json`](../../starter_v0/runs/v1_B_base_openrouter_20261110T181455132429.json) |
| v2 |  |  |  |  |  |
| v3 |  |  |  |  |  |

Ghi chú v0: có một lần chạy v0 trước đó khi chưa cấu hình key tool (Tavily/Firecrawl/RapidAPI) — [`v0_B_base_openrouter_20261110T174810741710.json`](../../starter_v0/runs/v0_B_base_openrouter_20261110T174810741710.json), case 0.65. Prompt/tools hash giống hệt; khác biệt 1 case (R01) do model không tất định (xem mục 5). Nhóm dùng lần chạy thứ hai làm baseline chính thức vì tool trả dữ liệu thật.

Kết quả kiểm chứng giả thuyết v1 theo từng case:

| Case | v0 | v1 | Nhận xét |
|---|---|---|---|
| R10_missing_handle | FAIL | **PASS** | Gọi `clarify` thay vì đoán `sama` |
| R11_missing_url | FAIL | **PASS** | Hỏi URL thay vì tự `lookup` |
| R12_confirm_before_send | FAIL | FAIL (tiến bộ) | Không còn tự `send`; đã gọi `clarify` nhưng `response_type="text"` (hỏi nội dung) thay vì `"yes_no"` (xin xác nhận) |
| R13_parallel_web_and_tweets | FAIL | FAIL | Vẫn chỉ 1 tool call (`lookup`, thiếu `social_search`) |

→ Giả thuyết v1 đúng một phần (R10, R11, nửa R12).

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run v0 chính thức và run v1.

| Case ID | Failure Type | Actual Tool Calls (v0) | What Failed | Fix |
|---|---|---|---|---|
| R03_web_news_routing | wrong_arg_value (case label `wrong_tool`) | `lookup(query="AI news today", topic="news", timeframe="day")` | `query` expected `AI`; model nhồi "news today" vào query dù đã có `topic`/`timeframe`. v1 vẫn FAIL (`"AI news"`) | v2: mô tả convention arg của `lookup` trong `tools.yaml` |
| M02_carryover_timeframe | wrong_arg_value | `lookup(query="robotics news today", topic="news", timeframe="day")` | `query` expected `robotics`; cùng nguyên nhân R03. v1 vẫn FAIL | v2: như R03 |
| R10_missing_handle | missing_info | `timeline(screenname="sama", limit=5)` | Không hỏi tài khoản nào mà tự đoán Sam Altman — đúng như prompt starter chỉ dẫn | v1 ✅ |
| R11_missing_url | missing_info | `lookup(query="OpenAI GPT-4 Turbo announcement", ...)` | Không hỏi URL mà tự tìm — prompt starter bảo "assume a likely URL" | v1 ✅ |
| R12_confirm_before_send | wrong_boundary | `send(confirmed=true, text="🚀 New breakthrough in AI…")` | Tự soạn nội dung và gửi ngay không xin xác nhận (chỉ không gửi được vì chưa có token Telegram). v1: đã `clarify` nhưng sai `response_type` | v1 một phần; v3: mô tả `clarify`/`send` boundary trong `tools.yaml` |
| R13_parallel_web_and_tweets | wrong_tool | `social_search(query="AI", search_type="Latest")` | Thiếu `lookup` — prompt starter ép "pick one tool". v1: chỉ gọi `lookup`, thiếu `social_search` | v1 chưa đủ; xem mục 7 |

### B3. Team Eval Cases

> TODO — chờ `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn) và run `--suite group`.

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
|  |  |  |  |

### B4. Live Chat Evidence

> TODO — chờ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) |  |  |  |
| Unit test tool mới (≥ 3 test/tool) | `pytest` output (0 failed) |  |  |
| UI (lệnh chạy + link dùng thử) |  |  |  |

Tool unit tests: số test đã viết, và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

- **Chọn provider miễn phí:** nhóm dùng Groq (free tier) thay vì OpenRouter trả phí. Starter không có provider Groq riêng, nhưng API Groq tương thích OpenAI nên dùng lại provider `openrouter` bằng cách đổi `OPENROUTER_BASE_URL`. Hệ quả: run JSON ghi provider `openrouter`; phải luôn truyền `--model openai/gpt-oss-120b` vì model mặc định `openai/gpt-4o-mini` không có trên Groq. Preflight pass.
- **Rate limit Groq:** header phản hồi cho thấy free tier của `openai/gpt-oss-120b` giới hạn 1.000 request/ngày và **8.000 token/phút**. Mỗi request mang system prompt + 10 tool schema (~2–3k token), nên nguy cơ HTTP 429 → `provider_error` → run không hợp lệ, nhất là khi `tools.yaml` dài ra ở v2/v3 hoặc nhiều thành viên dùng chung key. Cách xử lý: kiểm tra `provider_error_cases == 0` sau mỗi run; mỗi thành viên dùng key riêng. Đến v1 chưa run nào bị lỗi provider.
- **Run v0 đầu tiên thiếu key tool:** lần chạy đầu ([`v0_..._174810741710.json`](../../starter_v0/runs/v0_B_base_openrouter_20261110T174810741710.json)) các tool trả `Missing TAVILY_API_KEY env var`. Điểm vẫn hợp lệ (eval chấm routing + args), nhưng nhóm chạy lại sau khi cấu hình đủ key để log có kết quả tool thật.
- **Model không tất định:** cùng prompt/tools hash, R01 lần 1 FAIL (`screenname="SamAltman"`), lần 2 PASS (`"sama"`) dù `temperature=0`. Vì vậy chênh lệch ±1 case (±0.05) có thể chỉ là nhiễu; nhóm so sánh theo từng case chứ không chỉ tổng điểm.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- **Fix nào thuộc `system_prompt.md`?** Hành vi chung: khi nào phải hỏi lại (R10, R11), boundary xác nhận trước hành động có side effect (R12), được gọi nhiều tool (R13). v1 cho thấy chỉ bỏ chỉ dẫn xấu + thêm rule đã sửa được R10, R11.
- **Fix nào thuộc `tools.yaml`?** Convention của từng argument (R03, M02: `query` chỉ là chủ đề, "tin tức"/"hôm nay" thuộc `topic`/`timeframe`) và chi tiết tham số như `clarify.response_type="yes_no"` khi xin xác nhận (R12). Kế hoạch v2/v3.
- **Failure nào cần review thủ công?** R12 ở v1: agent đã không gửi và đã hỏi lại (hành vi an toàn) nhưng vẫn FAIL vì `response_type`; hỏi nội dung trước khi hỏi xác nhận cũng là hành vi hợp lý khi user chưa đưa nội dung. R13: agent starter chỉ gọi model một lần, nên model phải trả 2 tool call song song trong một response — có thể là giới hạn của model hơn là của prompt.
- **Nếu có thêm một vòng:** TODO (sau v3).

## 8. Tài liệu tham khảo

- [README.md](../../README.md), [RUBRIC.md](../../RUBRIC.md), [docs/TOOL-SETUP.md](../../docs/TOOL-SETUP.md)
- Groq API (OpenAI-compatible): https://console.groq.com/docs
