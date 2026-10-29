# Hướng dẫn sử dụng Orcasus trong Claude Code — v1.3.0

Orcasus là thư viện skills và quy tắc vận hành giúp Claude Code phát triển web/mobile có kỷ luật hơn. Bản 1.3.0 đặt hai cổng bắt buộc:

1. **Project Discovery** — khảo sát repository, assets, giấy phép, quyền, integrations, runtime, môi trường test và ngân sách trước khi chốt giải pháp.
2. **Efficient Testing** — chọn lớp kiểm thử rẻ nhất nhưng đủ tin cậy; ngân sách screenshot, trace và video mặc định bằng 0.

Orcasus không phải agent runtime độc lập hoặc sandbox bảo mật. Cần đưa Operating Contract vào CLAUDE.md của dự án và kiểm tra kết quả thực tế.

## 1. Cài đặt vào dự án

Copy cả hai thư mục skill vào dự án đích:

- skills/project-discovery/SKILL.md → .claude/skills/project-discovery/SKILL.md
- skills/efficient-testing/SKILL.md → .claude/skills/efficient-testing/SKILL.md

Copy hai template vào docs/agent-ops/templates/:

- templates/READINESS_MATRIX_TEMPLATE.md
- templates/TEST_PLAN_TEMPLATE.md

Hợp nhất nội dung docs/agent-operating-contract.md vào CLAUDE.md hiện có. Không ghi đè các quy tắc build/test/deploy đặc thù của dự án.

Ví dụ PowerShell (đang đứng tại root repo Orcasus):

    $target = "C:\work\my-app"
    New-Item -ItemType Directory -Force "$target\.claude\skills" | Out-Null
    Copy-Item -Recurse -Force ".\skills\project-discovery" "$target\.claude\skills\"
    Copy-Item -Recurse -Force ".\skills\efficient-testing" "$target\.claude\skills\"
    New-Item -ItemType Directory -Force "$target\docs\agent-ops\templates" | Out-Null
    Copy-Item -Force ".\templates\READINESS_MATRIX_TEMPLATE.md" "$target\docs\agent-ops\templates\"
    Copy-Item -Force ".\templates\TEST_PLAN_TEMPLATE.md" "$target\docs\agent-ops\templates/"

Ví dụ macOS/Linux:

    TARGET="/path/to/my-app"
    mkdir -p "$TARGET/.claude/skills" "$TARGET/docs/agent-ops/templates"
    cp -R skills/project-discovery "$TARGET/.claude/skills/"
    cp -R skills/efficient-testing "$TARGET/.claude/skills/"
    cp templates/READINESS_MATRIX_TEMPLATE.md "$TARGET/docs/agent-ops/templates/"
    cp templates/TEST_PLAN_TEMPLATE.md "$TARGET/docs/agent-ops/templates/"

Thay đường dẫn ví dụ bằng đường dẫn dự án thật. Trước khi copy đè, kiểm tra có thay đổi riêng trong các skills đích hay không.

Mở dự án trong VS Code, bắt đầu phiên Claude Code mới nếu cần, rồi gọi:

- /project-discovery
- /efficient-testing

Xác minh skills được nhận diện theo tài liệu hiện hành: https://code.claude.com/docs/en/skills. Đừng chỉ hỏi model “đã nạp chưa”; yêu cầu nó tạo hồ sơ và đối chiếu file thật.

## 2. Bắt buộc trước khi code: Project Discovery

Với mỗi feature đáng kể, orchestrator được phép giao các agent khảo sát độc lập theo hướng **read-only**, nhưng chưa giao code cho Architect/Developer cho đến khi tổng hợp bằng chứng.

Kiểm kê:
- Stack, package scripts, phiên bản và trạng thái git hiện tại.
- Component, design tokens, logo, fonts, icons, ảnh, nguồn và giấy phép.
- API, database, authentication, integrations, scopes và trạng thái hiện diện của biến môi trường (không tiết lộ giá trị secret).
- Tool/MCP có thực sự khả dụng trong phiên hiện tại hay không.
- Runtime, CI, staging, test accounts, browser/device/emulator.
- Acceptance criteria, security, performance, accessibility, localization và ngân sách.

Tạo docs/agent-ops/READINESS_MATRIX.md và docs/agent-ops/DISCOVERY_SUMMARY.md. AVAILABLE cần bằng chứng; UNKNOWN không phải AVAILABLE.

### Nếu thiếu resource hoặc permission

Đánh dấu task phụ thuộc là BLOCKED. Trình bày 2–3 lựa chọn khả thi, trade-off về chi phí, thời gian, chất lượng, bảo mật, dữ liệu và bảo trì; đưa ra khuyến nghị và hỏi owner. Trong lúc chờ, chỉ tiếp tục việc độc lập và có thể đảo ngược.

Không tự đổi sang fake API, mock production, placeholder asset, local-only behavior hoặc làm giảm acceptance criteria khi chưa được duyệt. Không cài dependency lớn, phát sinh chi phí, mở rộng quyền hoặc thay đổi production khi chưa được phép.

Nếu phát hiện giả định sai lúc chạy, dừng phần công việc phụ thuộc, cập nhật readiness matrix và quay lại owner khi phương án hoặc chất lượng bị ảnh hưởng.

## 3. Trước khi test: lập Test Plan

Gọi /efficient-testing và tạo docs/agent-ops/TEST_PLAN.md theo template.

| Lớp kiểm thử | Dùng để kiểm tra | Ví dụ |
|---|---|---|
| Static | Cấu hình/chất lượng mã | lint, typecheck, format, schema check |
| Unit | Logic, validation, quyền, phép tính | hàm thuần, service nhỏ |
| API/Integration | Contract, persistence, auth, tích hợp | route, query, migration |
| Component | Tương tác và accessibility | form, keyboard, role/name |
| E2E | Hành trình người dùng quan trọng | các luồng chính |
| Visual regression | Yêu cầu hiển thị cụ thể | clipping, responsive, spacing, theme |

Chọn lớp rẻ nhất nhưng đủ tin cậy để chứng minh acceptance criterion. Không chạy toàn bộ E2E sau mỗi lần sửa nếu test ở lớp thấp hơn đã đủ. Không thêm runner mới trước khi xác minh test stack hiện tại.

## 4. Chính sách screenshot/trace/video

Ngân sách mặc định của cả ba loại artifact đều là **0**.

- Không dùng image generation để tạo screenshot giả hoặc bằng chứng rằng ứng dụng thật hoạt động.
- Không chụp mọi route, component, state, test, viewport hoặc mỗi vòng lặp.
- Trước khi bật capture, phải ghi câu hỏi cần trả lời, trang/trạng thái đại diện, viewport/device/theme, hạn mức artifact, thư mục lưu, retention/cleanup và phê duyệt hoặc policy CI đã được duyệt.
- Ưu tiên assertion, API/DOM state, semantic/accessibility queries, console/network logs và kiểm tra geometry.
- Trace có thể chứa screenshot/screencast và DOM snapshots; trace archive cũng tính vào artifact budget.
- Với Playwright đã có sẵn, giữ screenshot, trace và video ở chế độ off trong vòng lặp thường ngày. Chỉ bật capture có chọn lọc cho test chẩn đoán/visual cụ thể đã được lập kế hoạch. Không cài Playwright chỉ vì tài liệu gợi ý.
- Không chấp nhận snapshot mới chỉ để làm test xanh; phải xem diff và ghi lý do.

Tài liệu Playwright: https://playwright.dev/docs/api/class-testoptions và https://playwright.dev/docs/test-use-options.

## 5. Khi test thất bại

1. Giữ assertion/log lỗi đầu tiên và bằng chứng tối thiểu.
2. Phân loại nguyên nhân: code, giả định test, fixture/data, quyền, service, môi trường, browser/device hoặc flaky timing.
3. Sửa nguyên nhân và chạy targeted test; không retry mù toàn bộ suite.
4. Nếu thiếu resource, đánh dấu BLOCKED hoặc NOT RUN và trở lại discovery/owner gate.
5. Không bỏ qua test, hạ assertion hoặc thay requirement để đạt màu xanh.
6. Dừng vòng lặp sửa lỗi khi cùng lỗi tái diễn mà chưa có nguyên nhân mới; báo blocker.

## 6. Báo cáo cuối

Báo cáo phải có:
- Acceptance criteria nào đã được xác minh và ở test layer nào.
- Lệnh đã chạy, exit code và thời lượng nếu có.
- Số PASS, FAIL, SKIPPED, BLOCKED, NOT RUN.
- Số screenshot/trace/video, lý do, thư mục lưu và phê duyệt.
- Lỗi đầu tiên, root cause, các retry có mục tiêu.
- Integrations, permissions, devices hoặc phạm vi chưa được xác minh.
- Workaround/dependency/cấu hình thay đổi và phê duyệt liên quan.

Không gọi feature là “đã test” nếu test chưa thực sự chạy.

## 7. Checklist

- [ ] Discovery được tổng hợp trước khi giao code.
- [ ] Assets, licences, integrations, credential/scopes và environments có bằng chứng.
- [ ] Blocker và trade-off quan trọng đã được đưa ra owner.
- [ ] Không có workaround làm giảm chất lượng chưa được duyệt.
- [ ] Test plan map từng acceptance criterion sang lớp test.
- [ ] Screenshot, trace, video budget mặc định bằng 0.
- [ ] Mỗi artifact khác 0 có câu hỏi, hạn mức và phê duyệt/policy.
- [ ] Report phản ánh lệnh/test thực tế và coverage gaps.

## Tài liệu

- Claude Code Skills: https://code.claude.com/docs/en/skills
- Claude Code Permissions: https://code.claude.com/docs/en/permissions
- Claude Code Hooks: https://code.claude.com/docs/en/hooks
- Playwright test options: https://playwright.dev/docs/api/class-testoptions
- Testing Library query priority: https://testing-library.com/docs/queries/about/
