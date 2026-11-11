---
name: summarize_paper
track: bonus
kind: local_knowledge
provider: local_analyzer
requires_env: []
inputs: [paper_text, focus_area, max_points]
outputs: [takeaways, focus_area, point_count, status]
side_effect: false
---
# summarize_paper

Trích xuất các phát hiện nghiên cứu chính, đóng góp và giới hạn từ văn bản nội dung của bài báo khoa học.
Hỗ trợ lọc theo vùng trọng tâm (all, methodology, findings, limitations).

