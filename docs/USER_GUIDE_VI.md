# Hướng dẫn sử dụng Orcasus — Claude Code Agent Team System v2.2.0

Orcasus không chỉ là hai skill. Đây là **bộ vận hành Agent Teams hoàn chỉnh** dành cho Claude Code: cấu hình, agents, skills, quyền, hooks, Team Secretary, logger, quy trình debate/vote, template, validation và hướng dẫn nghiệm thu.

## 1. Bắt đầu trong VS Code

1. Mở thư mục gốc của repository Orcasus trong VS Code.
2. Chọn Claude harness và đăng nhập Claude Code theo hướng dẫn chính thức: https://code.claude.com/docs/en/setup
3. Đọc CLAUDE.md và .claude/settings.json. File settings bật Agent Teams ở chế độ experimental, thiết lập các quyền bảo vệ và hook ghi log.
4. Kiểm tra Python 3 trong terminal.
5. Chạy:
   - python scripts/test_meeting_logger.py
   - python scripts/validate_bundle.py
6. Mở một phiên Claude Code interactive mới, copy phần Initialization prompt từ INITIALIZE_AGENTS.md và gửi.
7. Chạy acceptance tests trong docs/ACCEPTANCE_TESTS.md ở workspace không production trước khi phụ thuộc vào hook/logger.

Không overlay cấu hình lên repository có sẵn một cách mù quáng. Hãy sao lưu/đối chiếu CLAUDE.md, settings, agents và skills; hợp nhất các nội dung hiện có.

## 2. Thành phần trong bộ cài đặt

- .claude/settings.json: bật Agent Teams, permission defaults và hooks.
- .claude/agents/: 15 vai trò gồm Product Manager, Product Analyst, Domain Architect, Product Designer, UX Researcher, Frontend, Backend, Mobile, Integration, Data Platform, QA, Security Reviewer, Performance Reviewer, Devil's Advocate và Team Secretary.
- .claude/skills/: 9 workflows; bao gồm Project Discovery, Efficient Testing, Team Debate, Meeting Record, Platform Discovery, Root Cause Debate, Vertical Slice Delivery, Design Quality Gate và Delivery Readiness.
- scripts/: event logger, unit tests, static validator.
- docs/ và templates/: operating model, debate/meeting protocols, reference architecture, UX quality, acceptance tests, readiness/test-plan templates.
- meetings/, evidence/, decisions/, projects/, reports/: nơi lưu các hồ sơ bền vững.

## 3. Quy trình cho một feature

### Bước 1 — Discovery trước khi thiết kế
Gọi /project-discovery. Orchestrator có thể phân công các agent khảo sát read-only song song, nhưng chưa được giao coding tasks cho đến khi đã tổng hợp bằng chứng về stack, assets/licences, integrations, permission scopes, môi trường, test runner, fixtures và ngân sách.

Tạo docs/agent-ops/READINESS_MATRIX.md và docs/agent-ops/DISCOVERY_SUMMARY.md. AVAILABLE phải có bằng chứng; UNKNOWN không phải AVAILABLE. Nếu thiếu quyền, asset, integration, runtime hay quyết định sản phẩm quan trọng, đánh dấu BLOCKED cho phần phụ thuộc và đưa ra lựa chọn cùng trade-offs để chị quyết định.

### Bước 2 — Debate nếu có nhiều phương án
Gọi /team-debate cho quyết định lớn có nhiều phương án hợp lý. Chọn nhóm nhỏ 3–5 teammates phù hợp; bắt đầu Team Secretary trước khi thảo luận. Mỗi agent đề xuất độc lập, phản biện, trả lời phản biện, chấm điểm phương án và gửi FINAL_BALLOT. Secretary ghi nhận thông tin quan sát được, không bỏ phiếu mặc định và không ghi hidden chain-of-thought.

Lưu ADR, minutes, vote register, action items và coverage report. Nếu hook chưa được thử trực tiếp, trạng thái capture là PARTIAL hoặc NOT VERIFIED.

### Bước 3 — Test plan trước code/test
Gọi /efficient-testing và lập docs/agent-ops/TEST_PLAN.md. Mỗi acceptance criterion cần một lớp test có lý do. Ưu tiên static, unit, API/integration và component tests trước E2E. Chỉ bổ sung framework/dependency nếu đã xác minh có khoảng trống thực sự.

### Bước 4 — Xây một vertical slice
Gọi /vertical-slice-delivery. Chốt API/data/UI contracts, dependencies và file ownership. Implement một luồng end-to-end hoàn chỉnh thay vì nhiều màn hình mock rời rạc. Không tạo workaround làm giảm chất lượng hoặc thay đổi behavior mà chưa được duyệt.

### Bước 5 — Review và bàn giao
QA, Security, Design, Performance hoặc Mobile Reviewer kiểm tra phần liên quan. Gọi /delivery-readiness trước mốc bàn giao. Báo cáo lệnh/test thực sự chạy, findings, artifact counts và phạm vi chưa kiểm tra.

## 4. Chính sách screenshot/trace/video

Ba ngân sách mặc định đều bằng **0**.

- Không generate hình để chứng minh ứng dụng hoạt động.
- Không chụp tất cả route, state, viewport, theme hoặc mọi vòng lặp.
- Trước khi capture, cần ghi câu hỏi cụ thể, trang/state đại diện, viewport/device, số artifact tối đa, nơi lưu, retention/cleanup và owner approval hoặc CI policy đã được duyệt.
- Ưu tiên assertion, DOM/API state, accessibility queries, console/network logs và kiểm tra geometry.
- Trace có thể chứa screenshot và DOM snapshots; trace archive cũng tính vào ngân sách.
- Không chấp nhận snapshot mới chỉ để làm test xanh; phải kiểm tra diff và lý do.
- Khi test fail, giữ lỗi đầu tiên, chẩn đoán nguyên nhân rồi chạy targeted test. Không retry mù toàn bộ suite.

## 5. Quyền và an toàn

Các quy tắc permissions/deny/ask trong settings là lớp bảo vệ giảm rủi ro, không phải sandbox hoàn chỉnh. Xem lại trước khi dùng. Không sử dụng cấu hình bỏ qua mọi quyền trên workstation có secrets/production. Không deploy, publish, xóa dữ liệu quan trọng, migrate production, mở rộng scope, gọi dịch vụ trả phí hay cam kết bên ngoài khi chưa được phép.

## 6. Kiểm tra Team Secretary

1. Tạo meeting ID duy nhất và đặt meetings/CURRENT_MEETING.json active.
2. Bắt đầu Secretary và tối thiểu hai teammate thực sự gửi tin nhắn qua công cụ nhắn tin của Agent Teams.
3. Kiểm tra events JSON có sender, recipient và stated message content đủ dùng.
4. Đối chiếu event log với tin nhắn thực tế, balloting, minutes và coverage report.
5. Chỉ ghi CAPTURE VERIFIED nếu có bằng chứng runtime không có khoảng trống quan trọng; nếu không, dùng PARTIAL hoặc NOT VERIFIED.

Logger ghi những thông điệp được quan sát qua hook. Nó không ghi mọi trạng thái nội tâm hay đảm bảo mọi session teammate đều phát ra event.

## 7. Các trạng thái báo cáo

- PASS: đã xác minh bằng thực thi/bằng chứng.
- FAIL: tiêu chí không đạt.
- BLOCKED: thiếu resource hoặc quyết định.
- NOT RUN: chưa chạy kiểm tra.
- SKIPPED: không chạy theo policy có ghi nhận.

Không báo test đã pass khi chỉ mới tạo file test hoặc xem screenshot. Không gọi feature “đã kiểm thử” nếu chưa có kết quả chạy thực tế.

## Tài liệu chính thức
- Agent Teams: https://code.claude.com/docs/en/agent-teams
- Skills: https://code.claude.com/docs/en/skills
- Hooks: https://code.claude.com/docs/en/hooks
- Permissions: https://code.claude.com/docs/en/permissions
- Playwright capture options: https://playwright.dev/docs/api/class-testoptions
