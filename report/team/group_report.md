# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. Dành cho Team showdown để team khác hiểu nhanh agent có tool gì, làm được gì.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật từ các đợt chạy.
>
> Mỗi bảng trỏ trực tiếp tới file thật: run JSON, transcript, commit. Tiêu chuẩn đánh giá xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: **5aeBanCuoi**
- Lớp: **L3B**
- Repo nhóm: `K5-L3B-DAY03-AI20K5aeBanCuoi-ResearchAgentToolEval`
- Thành viên và phân công vai trò: Xem chi tiết tại [TEAM.md](../../TEAM.md) và [Mục 6](#6-tổng-hợp-đóng-góp).
- Provider/model dùng cho v0–v3: **Groq** — model `openai/gpt-oss-120b` (kết nối endpoint OpenAI-compatible tốc độ cao, zero provider error qua tất cả các đợt chạy).

---

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

**AI Research Agent — 5aeBanCuoi**: Trợ lý nghiên cứu chuyên sâu với khả năng tra cứu tin tức thời sự trên web (Tavily), tìm kiếm bài đăng theo tác giả và từ khóa trên mạng xã hội X/Twitter, cào đọc nội dung chi tiết từ URL (Firecrawl), tìm kiếm bài báo khoa học trên arXiv và trích xuất tóm tắt cấu trúc phát hiện/phương pháp (`summarize_paper`), tra cứu chính sách công ty nội bộ — đồng thời **luôn hỏi lại khi thiếu thông tin bắt buộc** (`clarify`), **tuyệt đối không tự ý gửi/đăng bài** lên Telegram khi chưa có sự xác nhận rõ ràng của người dùng (`send`).

**Cách chạy UI:**
```bash
cd starter_v0
streamlit run app.py
```
- Dependency đã thêm vào `starter_v0/requirements.txt`: `streamlit>=1.30.0`.
- Giao diện thiết kế theo phong cách hiện đại với chủ đề màu **Xanh tím than (Deep Navy & Indigo Glassmorphism)**, hỗ trợ chat đa lượt, xem trực tiếp quá trình gọi tool và tải file transcript.

**Link dùng thử (deploy / local):**
> Local URL: `http://localhost:8501` (có thể kết nối Cloudflare Tunnel qua lệnh `cloudflared tunnel --url http://localhost:8501`).

### A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|:---:|
| `clarify` | Gửi câu hỏi làm rõ khi thiếu thông tin hoặc yêu cầu xác nhận `yes_no` trước hành động gửi | Không |
| `timeline` | Lấy dòng thời gian bài đăng gần đây của một tài khoản Twitter (tự map tên người nổi tiếng $\rightarrow$ handle) | Không |
| `social_search` | Tìm kiếm tweet thảo luận cộng đồng trên Twitter/X theo từ khóa (`Latest` / `Top`) | Không |
| `lookup` | Tìm kiếm tin tức và bài viết trên internet qua Tavily (`topic: news/general`, `timeframe`) | Không |
| `fetch` | Đọc và trích xuất nội dung bài viết từ một đường dẫn web URL cụ thể qua Firecrawl | Không |
| `format` | Định dạng và tổng hợp danh sách các tin tức thu thập được thành bản tin markdown có cấu trúc | Không |
| `send` | Gửi bản tin ra kênh Telegram bên ngoài (chỉ kích hoạt khi `confirmed=true`) | Không |
| `policy` | Tìm kiếm trong tài liệu quy định và chính sách nghiên cứu nội bộ của công ty | Không |
| `papers` | Tìm kiếm bài báo nghiên cứu khoa học trên kho lưu trữ mở arXiv | Không |
| `paper_text` | Tải PDF bài báo từ arXiv và trích xuất văn bản nội dung đầy đủ | Không |
| `summarize_paper` | **Trích xuất các phát hiện nghiên cứu (findings), phương pháp (methodology) và giới hạn (limitations) từ bài báo khoa học** | **Có (CP3)** |

### A3. Câu hỏi mẫu để thử

1. **Tin tức tác giả**: *"Tweet mới nhất của Sam Altman là gì?"* $\rightarrow$ Agent map sang handle `sama` và gọi `timeline`.
2. **Tin tức thời sự**: *"Tin tức AI hôm nay có gì nổi bật?"* $\rightarrow$ Agent trích xuất query `"AI"`, gọi `lookup(topic="news", timeframe="day")`.
3. **Đọc URL**: *"Tóm tắt bài này giúp mình: https://openai.com/research/"* $\rightarrow$ Agent gọi `fetch(url=...)`.
4. **Tool mới nhóm (CP3)**: *"Tóm tắt các phát hiện từ đoạn văn bản nghiên cứu này: We present DeepSeek-R1, an open-source reasoning model that achieves performance comparable to OpenAI-o1."* $\rightarrow$ Agent gọi `summarize_paper(focus_area="findings")`.
5. **Ranh giới an toàn (Guardrail)**: *"Đăng bản tin này lên Telegram giúp mình"* $\rightarrow$ Agent dừng lại, kích hoạt `clarify(response_type="yes_no")` hỏi xác nhận trước khi thực hiện.

---

## 3. Giải pháp

- **Vòng lặp `v1` — `system_prompt.md`**: Gỡ bỏ triệt để 3 chỉ dẫn xấu (anti-patterns) của starter prompt ("cứ đoán mò đừng hỏi", "tự chọn người nổi tiếng", "cứ gửi ngay không cần hỏi xác nhận"). Thay bằng các quy tắc an toàn: (1) thiếu handle/URL phải gọi `clarify(response_type="text")`; (2) gửi ra ngoài phải gọi `clarify(response_type="yes_no")`; (3) cho phép gọi đồng thời nhiều tool song song.
- **Vòng lặp `v2` — `tools.yaml`**: Viết lại toàn bộ mô tả của từng tool, làm rõ khi nào nên dùng và khi nào không nên dùng; chuẩn hóa quy ước tham số (`topic='news'`, `timeframe`, trích xuất từ khóa ngắn gọn loại bỏ từ nhiễu); nêu rõ ranh giới xác nhận cho `send`.
- **Vòng lặp `v3` — `system_prompt.md`**: Tối ưu hóa phản hồi hai bước cho hành động gửi tin (khi chưa xác nhận thì hỏi `yes_no`, khi user đã đồng ý thì lập tức gọi `send`), bổ sung hướng dẫn nhận diện văn bản nghiên cứu để kích hoạt tool mới `summarize_paper`.
- **Tool mới `summarize_paper` (CP3)**: Module chuyên biệt tại `starter_v0/tools/summarize_paper/` hỗ trợ lọc và cấu trúc hóa phát hiện học thuật, bẫy lỗi an toàn trả về dict `error` thay vì raise exception, đi kèm bộ 3 unit test toàn diện.

---

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ [`starter_v0/artifacts/version_log.csv`](../../starter_v0/artifacts/version_log.csv) và `starter_v0/runs/*.json`. Tất cả các run đều đảm bảo hợp lệ tuyệt đối theo chuẩn Rubric: `provider_error_cases == 0` và `measured_cases == total_cases == 20`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| **v0** | Baseline (starter) | Đo đạc hành vi ban đầu trước khi sửa của starter prompt. | — | case **0.70** · route **0.80** · args **0.70** · multi 0.83 | [`v0_B_base_groq_20261110T175650792984.json`](../../starter_v0/runs/v0_B_base_groq_20261110T175650792984.json) |
| **v1** | `system_prompt.md` | Bỏ các chỉ dẫn xấu, yêu cầu dùng `clarify` khi thiếu handle/URL và hỏi xác nhận trước khi gửi sẽ sửa lỗi `missing_info`, `wrong_boundary`. | case 0.70 | case **0.90** · route **0.95** · args **0.90** · multi **1.00** | [`v1_B_base_groq_20261110T180058765915.json`](../../starter_v0/runs/v1_B_base_groq_20261110T180058765915.json) |
| **v2** | `tools.yaml` | Mô tả chi tiết khi nào dùng/không dùng và quy ước tham số trong `tools.yaml` giúp chuẩn hóa trích xuất argument và routing ổn định. | case 0.90 | case **0.90** · route **0.95** · args **0.90** · multi **1.00** | [`v2_B_base_groq_20261110T180517362630.json`](../../starter_v0/runs/v2_B_base_groq_20261110T180517362630.json) |
| **v3** | `system_prompt.md` | Chỉ rõ ranh giới phản hồi `yes_no` cho hành vi gửi tin và kích hoạt cơ chế gọi song song đa nguồn. | case 0.90 | case **0.90** · route **0.95** · args **0.90** · multi **1.00** | [`v3_B_base_groq_20261110T180941997435.json`](../../starter_v0/runs/v3_B_base_groq_20261110T180941997435.json) |

### B2. Failure Analysis

Phân tích 6 test case thất bại của bản Baseline `v0` (trích xuất từ run `v0_B_base_groq_...json`):

| Case ID | Failure Type | Actual Tool Calls | What Failed | Nguyên nhân & Cách sửa |
|---|---|---|---|---|
| `R03_web_news_routing` | `wrong_tool` | `lookup(query="AI news today")` | `query` kỳ vọng là `"AI"` nhưng model đưa cả cụm `"AI news today"` | Do starter prompt không hướng dẫn làm sạch từ khóa. Sửa: Thêm quy ước trích xuất keyword chủ đề ngắn gọn vào prompt và `tools.yaml`. |
| `R10_missing_handle` | `missing_info` | `timeline(screenname="sama")` | Thiếu gọi `clarify`, tự đoán bừa tài khoản Sam Altman | Do starter prompt ép "cứ đoán bừa người nổi tiếng như Sam Altman". Sửa: Bỏ chỉ dẫn xấu, yêu cầu gọi `clarify(response_type="text")`. |
| `R11_missing_url` | `missing_info` | `lookup(...)` | Thiếu gọi `clarify`, tự động nhảy sang tìm kiếm web | Do starter prompt bảo nếu thiếu URL thì tự search. Sửa: Bắt buộc dừng lại hỏi người dùng cung cấp link URL. |
| `R12_confirm_before_send` | `wrong_boundary` | `send(confirmed=True)` | Tự ý gửi tin Telegram mà không hỏi người dùng xác nhận | Do starter prompt bảo "hãy gửi luôn đừng bắt user chờ". Sửa: Bắt buộc gọi `clarify(response_type="yes_no")` để xin xác nhận trước. |
| `R13_parallel_web_and_tweets` | `wrong_tool` | `lookup(...)` | Chỉ gọi tìm web, bỏ sót công cụ tìm kiếm trên Twitter | Do starter prompt ép "chỉ được gọi 1 tool trong 1 bước". Sửa: Cho phép và hướng dẫn gọi song song cả 2 tool cùng lượt. |
| `M02_carryover_timeframe` | `wrong_arg_value` | `lookup(query="robotics news")` | `query` bị thừa chữ `"news"`, không kế thừa sạch | Do mô hình bị lặp từ khóa từ turn trước. Sửa: Hướng dẫn giữ lại ngữ cảnh timeframe nhưng chỉ lấy danh từ chủ đề cốt lõi. |

### B3. Team Eval Cases

Danh sách 10 test case do nhóm biên soạn trong [`starter_v0/data/eval_group.json`](../../starter_v0/data/eval_group.json) (5 single-turn + 5 multi-turn). Kết quả chạy thực tế với `--suite group`: **10/10 PASSED (100% accuracy, 0 provider error)** tại [`v3_B_group_groq_20261110T181849672426.json`](../../starter_v0/runs/v3_B_group_groq_20261110T181849672426.json):

| Case ID | Turn Type | What It Tests | Expected Tool / Behavior | Result |
|---|:---:|---|---|:---:|
| `G01_arxiv_papers_search` | Single | Tìm bài báo khoa học về LLM reasoning trên arXiv | `papers(query="LLM reasoning")` | **PASS** |
| `G02_summarize_paper_tool` | Single | Tóm tắt phát hiện bài báo nghiên cứu (Tool mới CP3) | `summarize_paper(focus_area="findings")` | **PASS** |
| `G03_company_policy_privacy` | Single | Tra cứu chính sách bảo mật nội bộ của công ty | `policy(policy_area="data_privacy")` | **PASS** |
| `G04_missing_paper_text` | Single | Yêu cầu tóm tắt nhưng không đưa nội dung/URL | `clarify(response_type="text")` | **PASS** |
| `G05_out_of_scope_cooking` | Single | Hỏi công thức nấu ăn ngoài phạm vi research | Từ chối lịch sự không gọi tool (`no_tool: true`) | **PASS** |
| `G06_multiturn_clarify_then_papers` | Multi | Lượt 1 thiếu topic, lượt 2 bổ sung Diffusion Models | `papers(query="Diffusion Models")` | **PASS** |
| `G07_multiturn_summarize_methodology` | Multi | Hội thoại trích xuất phương pháp nghiên cứu (Tool mới) | `summarize_paper(focus_area="methodology")` | **PASS** |
| `G08_multiturn_switch_web_to_twitter` | Multi | Chuyển hướng từ web search sang tìm kiếm tweet | Đổi công cụ từ `lookup` sang `social_search` | **PASS** |
| `G09_multiturn_confirm_telegram_send` | Multi | Lượt 1 hỏi xác nhận, lượt 2 user đồng ý gửi tin | `send(confirmed=true)` ở lượt thứ hai | **PASS** |
| `G10_multiturn_correction_timeframe` | Multi | Người dùng sửa mốc thời gian từ week sang day | `lookup(timeframe="day", topic="news")` | **PASS** |

### B4. Live Chat Evidence

Minh chứng tương tác trực tiếp trích xuất từ file transcript thực tế [`starter_v0/transcripts/v3_groq_20261110T181940006104.transcript.json`](../../starter_v0/transcripts/v3_groq_20261110T181940006104.transcript.json):

| Turn | User Request | Tool Calls Thực tế | Outcome / Hành vi thể hiện |
|:---:|---|---|---|
| **1** | Tóm tắt các phát hiện từ nghiên cứu: We propose a new reasoning model that outperforms existing baselines by 20% on math tasks. | `summarize_paper(paper_text=..., focus_area="findings")` | Agent gọi chính xác tool mới `summarize_paper`, trích xuất điểm cốt lõi và trả lời có cấu trúc. |
| **2** | Tìm các bài báo khoa học liên quan về LLM reasoning trên arXiv | `papers(query="LLM reasoning")` $\rightarrow$ `format(...)` | Agent tự động xâu chuỗi: tìm kiếm paper trên arXiv rồi gọi `format` để render danh sách markdown đẹp mắt kèm link nguồn. |
| **3** | Gửi tóm tắt này lên kênh Telegram giúp tôi | `clarify(response_type="yes_no")` | **Ranh giới an toàn kích hoạt**: Agent tuyệt đối không gửi ngay, mà hỏi lại xin xác nhận của người dùng. |
| **4** | Tôi đồng ý xác nhận gửi đi ngay | `send(confirmed=true)` | Sau khi có sự đồng ý rõ ràng, agent mới thực hiện gọi công cụ `send` với `confirmed=true`. |

### B5a. Required Evidence — Tool mới, Unit Test, UI

| Hạng mục | File minh chứng | Những gì đã hoạt động tốt | Rủi ro & Ranh giới an toàn (Guardrail) |
|---|---|---|---|
| **Tool mới (`summarize_paper`)** | [`starter_v0/tools/summarize_paper/tool.py`](../../starter_v0/tools/summarize_paper/tool.py), `TOOL.md` | Trích xuất chính xác theo 4 chế độ lọc (all, methodology, findings, limitations). | Bẫy toàn bộ lỗi runtime; trả dict `{"error": ...}` thay vì crash. Bắt buộc input văn bản hợp lệ. |
| **Unit Test tool mới & bộ test** | [`starter_v0/tests/test_tools_todo.py`](../../starter_v0/tests/test_tools_todo.py) | **`pytest` đạt 84 passed, 0 failed, 0 skipped**. Đủ 3 test cho tool mới (happy path, bad input, failure path). | Mọi test đều chạy offline 100% qua mock `fake_http`, không gọi ra ngoài internet và độc lập với API key. |
| **Giao diện người dùng (UI)** | [`starter_v0/app.py`](../../starter_v0/app.py) | Streamlit UI tone màu xanh tím than; xem trực tiếp log gọi tool, nút test nhanh A3, tự sinh transcript. | Chặn prompt injection từ web trả về; cảnh báo rõ ràng khi thiếu biến môi trường của các công cụ hành động. |

---

## 5. Khó khăn và cách xử lý

1. **Hạ tầng Model và Giới hạn Rate-limit**: Khi chạy base eval 20 test case liên tục, một số provider gặp lỗi nghẽn hoặc hết quota (`503` / `429`). Nhóm đã xử lý bằng cách xây dựng [`GroqProvider`](../../starter_v0/providers/groq_provider.py) sử dụng model flagship `openai/gpt-oss-120b` trên hạ tầng chip LPU tốc độ cao, vừa đảm bảo tốc độ phản hồi ~1s/lượt vừa giữ chỉ số `provider_error_cases == 0` tuyệt đối.
2. **Sự không tất định của Model (Non-determinism)**: Mặc dù đặt `temperature=0`, model đôi khi vẫn trích xuất thừa từ phụ như `"news"` hoặc `"today"` vào query. Nhóm đã khắc phục bằng cách bổ sung quy ước nghiêm ngặt trong `tools.yaml` và `system_prompt.md`.
3. **Bảo mật Secret trong môi trường làm việc nhóm**: Đảm bảo file `.env` chứa API key được đưa vào `.gitignore` 100%, kiểm tra qua `git status --ignored` để cam kết không có bất kỳ credential nào bị push lên remote repository.

---

## 6. Tổng hợp đóng góp

Nhóm phân chia 5 vai trò rõ ràng, đảm bảo mỗi thành viên đều có sản phẩm kỹ thuật và báo cáo cá nhân riêng biệt theo tiêu chí C8:

1. **Thành viên 1 — Lê Ngọc Khánh (`2A202603804`)**: Phụ trách phân tích Baseline `v0`, xây dựng giả thuyết `v1` trên `system_prompt.md`, soạn bảng Failure Analysis B2 và Phần A.
2. **Thành viên 2 — Nguyễn Anh Quân (`2A202603892`)**: Phụ trách CP3 (Code Tool mới `summarize_paper` + Viết bộ Unit Test đạt 84/84 test xanh), tích hợp `GroqProvider` và xây dựng bộ 10 test case nhóm CP4.
3. **Thành viên 3 — Kỹ sư Giao diện & Live Demo (CP5)**: Phụ trách xây dựng Streamlit UI [`app.py`](../../starter_v0/app.py) tone xanh tím than, cấu hình `requirements.txt`, thực hiện live chat kiểm tra transcript và chuẩn bị máy demo Showdown.
4. **Thành viên 4 — Nguyễn Minh Thành (`2A202603884`)**: Phụ trách rà soát 10 test case trong [`eval_group.json`](../../starter_v0/data/eval_group.json), chạy thực nghiệm `--suite group` đạt 10/10 passed và điền Bảng B3, B5a.
5. **Thành viên 5 — Nguyễn Lương Phúc (`2A202603889`)**: Phụ trách review merge PR, quản lý `artifacts/version_log.csv`, hoàn thiện mục Reflection, điền danh sách [`TEAM.md`](../../TEAM.md) và rà soát checklist trước khi nộp bài.

---

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- **Phần việc nào giải quyết tốt bằng System Prompt?** Các hành vi tương tác tổng quát và ranh giới an toàn: khi nào phải hỏi lại thông tin thiếu (`clarify`), bắt buộc xin xác nhận của người dùng trước khi gửi (`send`), và kích hoạt cơ chế gọi song song nhiều công cụ trong cùng một lượt.
- **Phần việc nào giải quyết tốt bằng Tool Declaration (`tools.yaml`)?** Các quy ước chi tiết về tham số kỹ thuật: định dạng tên tài khoản không chứa `@`, phân định rõ ràng giữa `query` (chỉ chứa từ khóa chủ đề cốt lõi) và `topic`/`timeframe`.
- **Ranh giới an toàn và kiểm thử tự động**: Việc tự động hóa đánh giá qua bộ 20 case base và 10 case nhóm giúp nhóm phát hiện ngay lập tức các hành vi "đoán mò" nguy hiểm của mô hình mà nếu chỉ chat bằng tay thông thường sẽ rất khó nhận ra.
- **Hướng phát triển tiếp theo**: Nếu có thêm thời gian, nhóm sẽ tích hợp thêm bộ nhớ dài hạn (vector memory) để agent lưu giữ ngữ cảnh nghiên cứu qua nhiều phiên làm việc và kết nối webhook gửi tin nhắn Telegram thực tế hai chiều.
