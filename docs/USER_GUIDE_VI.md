# Hướng dẫn sử dụng Orcasus — Claude Code Agent Team System v2.3.0

Orcasus không chỉ là hai skill. Đây là **bộ vận hành Agent Teams hoàn chỉnh** dành cho Claude Code: cấu hình, agents, skills, quyền, hooks, Team Secretary, logger, quy trình debate/vote, template, validation và hướng dẫn nghiệm thu.

## 1. Bắt đầu trong VS Code

1. Mở thư mục gốc của repository Orcasus trong VS Code.
2. Chọn Claude harness và đăng nhập Claude Code theo hướng dẫn chính thức: https://code.claude.com/docs/en/setup
3. Đọc CLAUDE.md và .claude/settings.json. File settings bật Agent Teams ở chế độ experimental, thiết lập các quyền bảo vệ và hook ghi log.
4. Kiểm tra Python 3.8+ trong terminal (`python3`, `python` hoặc `py -3`). Nếu Python nằm ở chỗ khác, đặt biến môi trường `ORCASUS_PYTHON` trỏ tới file chạy Python. Trên Windows, hook cần Git Bash.
5. Chạy (Windows: thay `python3` bằng `py -3`):
   - python3 scripts/validate_bundle.py
   - python3 scripts/test_meeting_logger.py
   - python3 scripts/test_hook_launcher.py
   - python3 scripts/test_knowledge_links.py
   - python3 scripts/check_knowledge_links.py
6. Mở một phiên Claude Code interactive mới. Đầu phiên phải thấy dòng "Orcasus hook runtime: OK"; nếu thấy WARNING thì sửa Python trước khi họp. Sau đó copy phần Initialization prompt từ INITIALIZE_AGENTS.md và gửi.
7. Chạy acceptance tests trong docs/ACCEPTANCE_TESTS.md ở workspace không production trước khi phụ thuộc vào hook/logger.

Không overlay cấu hình lên repository có sẵn một cách mù quáng. Hãy sao lưu/đối chiếu CLAUDE.md, settings, agents và skills; hợp nhất các nội dung hiện có.

## 2. Thành phần trong bộ cài đặt

- .claude/settings.json: bật Agent Teams, permission defaults, kiểm tra runtime hook đầu phiên và hooks ghi log (gọi Python qua scripts/hooks/run_python.sh).
- .claude/agents/: 17 vai trò gồm Product Manager, Product Analyst, Domain Architect, Product Designer, UX Researcher, Frontend, Backend, Mobile, Integration, Data Platform, QA, Security Reviewer, Performance Reviewer, Devil's Advocate, Team Secretary, Governance Auditor và Knowledge Steward.
- .claude/skills/: 16 workflows phủ đủ S0–S10 (xem docs/AI_SDLC_STAGE_MAP.md): Change Intake, Project Discovery, Platform Discovery, Requirements Traceability, Team Debate, Meeting Record, Backlog Slicing, Efficient Testing, Vertical Slice Delivery, Root Cause Debate, Design Quality Gate, Delivery Readiness, Closeout Report, Governance Audit, Process Retro và Knowledge Curation. Mỗi skill có bộ eval trong evals/evals.json.
- scripts/: event logger, launcher Python cho hook, bộ kiểm tra link tri thức/trích dẫn, công cụ eval skill, unit tests, static validator.
- .github/workflows/validate.yml: CI chạy toàn bộ kiểm tra trên mỗi pull request.
- knowledge/: chỉ mục tri thức có nguồn được theo dõi và duyệt của curator.
- docs/ và templates/: operating model, debate/meeting protocols, reference architecture, UX quality, acceptance tests, readiness/test-plan templates.
- meetings/, evidence/, decisions/, projects/, reports/: nơi lưu các hồ sơ bền vững.

## 3. Quy trình cho một feature

### Bước 0 — Intake (S0)
Gọi /change-intake. Agent trích nguyên văn yêu cầu, phân loại từng hạng mục theo file thực sự bị ảnh hưởng, tìm bản trùng/xung đột trong knowledge/INDEX.md, projects/, decisions/, meetings/, reports/, rồi soạn mục tiêu và giá trị để chị xác nhận. Agent không tự bịa metric hay deadline. Kết quả: docs/agent-ops/INTAKE_RECORD.md với scope contract; nếu làm phát sinh ngoài scope thì phải dừng và phân loại lại.

### Bước 1 — Discovery trước khi thiết kế
Gọi /project-discovery. Orchestrator có thể phân công các agent khảo sát read-only song song, nhưng chưa được giao coding tasks cho đến khi đã tổng hợp bằng chứng về stack, assets/licences, integrations, permission scopes, môi trường, test runner, fixtures và ngân sách.

Tạo docs/agent-ops/READINESS_MATRIX.md và docs/agent-ops/DISCOVERY_SUMMARY.md. AVAILABLE phải có bằng chứng; UNKNOWN không phải AVAILABLE. Nếu thiếu quyền, asset, integration, runtime hay quyết định sản phẩm quan trọng, đánh dấu BLOCKED cho phần phụ thuộc và đưa ra lựa chọn cùng trade-offs để chị quyết định.

### Bước 1b — Yêu cầu có trích dẫn đã kiểm chứng (S3)
Gọi /requirements-traceability. Mỗi yêu cầu phải ghi nguồn (tin nhắn của chị kèm ngày, ticket, file#dòng, meeting ID, ADR, URL) và agent phải mở nguồn để ghi VERIFIED, PARAPHRASE-OK, MISMATCH, UNVERIFIABLE hoặc NO SOURCE. Yêu cầu MISMATCH/UNVERIFIABLE/NO SOURCE thành câu hỏi cho chị, không được APPROVED. Kết quả: TRACE_MATRIX.md; script check_knowledge_links.py kiểm tra link và trạng thái.

### Bước 2 — Debate nếu có nhiều phương án
Gọi /team-debate cho quyết định lớn có nhiều phương án hợp lý. Chọn nhóm nhỏ 3–5 teammates phù hợp; bắt đầu Team Secretary trước khi thảo luận. Mỗi agent đề xuất độc lập, phản biện, trả lời phản biện, chấm điểm phương án và gửi FINAL_BALLOT. Secretary ghi nhận thông tin quan sát được, không bỏ phiếu mặc định và không ghi hidden chain-of-thought.

Lưu ADR, minutes, vote register, action items và coverage report. Nếu hook chưa được thử trực tiếp, trạng thái capture là PARTIAL hoặc NOT VERIFIED.

### Bước 2b — Chia backlog và ưu tiên (S5)
Gọi /backlog-slicing khi phạm vi cần nhiều thay đổi. Mỗi slice có một mục đích, acceptance criterion quan sát được, bằng chứng chứng minh, lớp test và kết luận testability (TESTABLE, NEEDS SPLIT, BLOCKED, UNTESTABLE). Agent đề xuất thứ tự theo một framework (RICE, WSJF, MoSCoW...) và đánh dấu số liệu ước đoán; chị quyết định thứ tự cuối cùng. Kết quả: projects/<slug>/BACKLOG.md.

### Bước 3 — Test plan trước code/test
Gọi /efficient-testing và lập docs/agent-ops/TEST_PLAN.md. Mỗi acceptance criterion cần một lớp test có lý do. Ưu tiên static, unit, API/integration và component tests trước E2E. Chỉ bổ sung framework/dependency nếu đã xác minh có khoảng trống thực sự.

### Bước 4 — Xây một vertical slice
Gọi /vertical-slice-delivery. Chốt API/data/UI contracts, dependencies và file ownership. Implement một luồng end-to-end hoàn chỉnh thay vì nhiều màn hình mock rời rạc. Không tạo workaround làm giảm chất lượng hoặc thay đổi behavior mà chưa được duyệt.

### Bước 5 — Review và bàn giao
QA, Security, Design, Performance hoặc Mobile Reviewer kiểm tra phần liên quan. Gọi /delivery-readiness trước mốc bàn giao. Báo cáo lệnh/test thực sự chạy, findings, artifact counts và phạm vi chưa kiểm tra. Việc merge do người quyết định.

### Bước 6 — Đóng việc, kiểm toán và cải tiến (S9)
- /closeout-report cho mọi task/slice: 8 mục, bắt buộc có mục "Intentionally not done" (ghi "None." nếu trống), file thay đổi lấy từ git, lệnh và kết quả thật, bảng truy vết yêu cầu → file → kiểm tra → bằng chứng.
- /governance-audit do agent governance-auditor (read-only, không phải người làm) kiểm tra thay đổi đã đi đúng quy trình chưa: PASS, FAIL hoặc UNVERIFIABLE; thiếu bằng chứng không bao giờ là PASS.
- /process-retro cuối mỗi milestone: gom nguyên nhân lặp lại và đề xuất thay đổi quy trình ở trạng thái PROPOSED; chỉ áp dụng sau khi chị duyệt.

### Bước 7 — Tri thức (S10)
Gọi /knowledge-curation. Agent knowledge-steward thêm mục PROPOSED vào knowledge/INDEX.md: mỗi mục một sự thật, có nguồn được theo dõi, ngày tuyệt đối, không chứa secret. Chỉ curator là người (chị hoặc người được giao) mới ghi tên và ngày để chuyển sang APPROVED. Mục bị thay thế phải trỏ tới mục mới.

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
6. Kiểm tra meetings/HOOK_ERRORS.log. Nếu có dòng lỗi trong thời gian họp, nghĩa là logger không chạy được (thường do thiếu Python) và trạng thái tối đa là PARTIAL.

Logger ghi những thông điệp được quan sát qua hook. Nó không ghi mọi trạng thái nội tâm hay đảm bảo mọi session teammate đều phát ra event.

## 7. Hook và Python

Trước v2.3.0, hook gọi thẳng `python`; máy chỉ có `python3` (macOS, nhiều bản Linux) hoặc Windows có alias Store giả sẽ làm logger lỗi âm thầm. Từ v2.3.0:
- Mọi hook gọi Python qua scripts/hooks/run_python.sh. Script thử lần lượt `ORCASUS_PYTHON`, `python3`, `python`, `py -3` bằng cách chạy thật, nên bỏ qua alias giả.
- Hook SessionStart in một dòng đầu phiên: OK (kèm phiên bản Python) hoặc WARNING kèm cách sửa.
- Nếu không có Python, hook ghi vào meetings/HOOK_ERRORS.log và báo lỗi ra stderr, nhưng vẫn không chặn tin nhắn của team.
- Cách sửa: cài Python 3.8+ hoặc đặt `ORCASUS_PYTHON`, rồi mở phiên mới. Có thể tự kiểm tra bằng `sh scripts/hooks/run_python.sh --check`.

## 8. Kiểm tra tự động (CI) và eval skill

- .github/workflows/validate.yml chạy trên Ubuntu và macOS cho mỗi pull request: validator, eval skill, test logger/launcher/link checker và kiểm tra link tri thức/trích dẫn.
- CI không chạy model. Để đo hành vi thật của skill: `python3 scripts/skill_evals.py sheet --out reports/skill-eval-sheet.md`, chạy từng prompt trong phiên Claude Code mới và chấm PASS/FAIL kèm bằng chứng.

## 9. Các trạng thái báo cáo

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
