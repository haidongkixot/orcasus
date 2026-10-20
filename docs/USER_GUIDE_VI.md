# Hướng dẫn sử dụng Orcasus trong Claude Code

Orcasus là thư viện **skills và quy tắc làm việc** giúp Claude Code phát triển web/mobile có kỷ luật hơn. Bộ này có hai skill cốt lõi:

- **Project Discovery**: khảo sát repository, stack, tài nguyên, assets, tích hợp, quyền truy cập và môi trường trước khi chốt thiết kế hoặc triển khai.
- **Efficient Testing**: lập kế hoạch kiểm thử theo rủi ro, ưu tiên cách kiểm tra rẻ nhất nhưng đủ tin cậy, hạn chế screenshot và báo cáo bằng chứng thực tế.

> Orcasus không phải hệ thống agent độc lập, cũng không phải cơ chế permission enforcement hoàn chỉnh. Cài skill không tự bảo đảm mọi agent đều gọi skill trong mọi nhiệm vụ. Để tăng tính tuân thủ, hãy áp dụng Agent Operating Contract vào CLAUDE.md của dự án và kiểm tra hành vi thực tế.

## 1. Khi nào nên dùng?

Dùng cho khởi tạo dự án web/mobile; xây dựng feature/module; tích hợp API, database, SSO, thanh toán, email hoặc analytics; redesign UI; migration; thay đổi schema/phân quyền; sửa lỗi có rủi ro regression; hoặc khi testing đang tạo nhiều screenshot và chạy quá nhiều test.

Với thay đổi nhỏ, rõ ràng, ít rủi ro, thực hiện discovery ở quy mô phù hợp. Không bỏ qua việc kiểm tra các phụ thuộc hoặc quyền cần thiết.

## 2. Cài đặt vào dự án Claude Code

### Bước A — Copy hai skill

Copy cả thư mục skill từ repository Orcasus vào dự án đích. Cấu trúc dự án đích cần có:

- your-project/.claude/skills/project-discovery/SKILL.md
- your-project/.claude/skills/efficient-testing/SKILL.md
- your-project/docs/agent-ops/templates/READINESS_MATRIX_TEMPLATE.md
- your-project/docs/agent-ops/templates/TEST_PLAN_TEMPLATE.md

Ví dụ PowerShell, giả sử terminal đang ở root repository Orcasus và dự án đích là C:\work\my-app:

    $target = "C:\work\my-app"
    New-Item -ItemType Directory -Force "$target\.claude\skills" | Out-Null
    Copy-Item -Recurse -Force ".\skills\project-discovery" "$target\.claude\skills\"
    Copy-Item -Recurse -Force ".\skills\efficient-testing" "$target\.claude\skills\"
    New-Item -ItemType Directory -Force "$target\docs\agent-ops\templates" | Out-Null
    Copy-Item -Force ".\templates\READINESS_MATRIX_TEMPLATE.md" "$target\docs\agent-ops\templates\"
    Copy-Item -Force ".\templates\TEST_PLAN_TEMPLATE.md" "$target\docs\agent-ops\templates\"

Ví dụ macOS/Linux, chạy từ root repository Orcasus:

    TARGET="/path/to/my-app"
    mkdir -p "$TARGET/.claude/skills" "$TARGET/docs/agent-ops/templates"
    cp -R skills/project-discovery "$TARGET/.claude/skills/"
    cp -R skills/efficient-testing "$TARGET/.claude/skills/"
    cp templates/READINESS_MATRIX_TEMPLATE.md "$TARGET/docs/agent-ops/templates/"
    cp templates/TEST_PLAN_TEMPLATE.md "$TARGET/docs/agent-ops/templates/"

Thay đường dẫn ví dụ bằng đường dẫn dự án thật. Kiểm tra thao tác không ghi đè một phiên bản skill đang được sửa riêng trong dự án.

### Bước B — Áp dụng Agent Operating Contract

Mở docs/agent-operating-contract.md. Đọc và hợp nhất các phần Required workflow, Role-specific expectations và Stop conditions vào CLAUDE.md ở root dự án đích.

- Không thay thế toàn bộ CLAUDE.md hiện có.
- Giữ nguyên hướng dẫn build/test/deploy đặc thù của repository.
- Contract giúp Main Agent/orchestrator tuân thủ các cổng quy trình; nó không thay thế permission rules hoặc chính sách bảo mật ở cấp hạ tầng.

### Bước C — Khởi động và xác minh

Mở thư mục dự án đích trong VS Code, tạo phiên Claude Code mới nếu cần, rồi gọi trực tiếp hai skill:

- /project-discovery
- /efficient-testing

Nếu slash command không xuất hiện, kiểm tra đường dẫn .claude/skills/<skill-name>/SKILL.md, frontmatter, phiên làm việc và tài liệu hiện hành: https://code.claude.com/docs/en/skills.

Đừng chỉ hỏi model “đã nạp skill chưa”. Yêu cầu nó thực hiện workflow trên feature thử nghiệm và kiểm tra các đầu ra đã tạo.

## 3. Quy trình chuẩn cho một feature

### Giai đoạn 1 — Discovery

Gọi /project-discovery và khảo sát:
- Kiến trúc/stack, package scripts và phiên bản.
- Component, design tokens, fonts, logos, icons, ảnh, nguồn và giấy phép assets.
- API, database, authentication, integration, tên biến môi trường và quyền/scope.
- Test runner, fixtures, CI, browser/device, preview hoặc staging.
- Yêu cầu chức năng, acceptance criteria, bảo mật, hiệu năng và ngân sách.

Tạo hồ sơ ở docs/agent-ops/:
- READINESS_MATRIX.md
- DISCOVERY_SUMMARY.md

Chỉ đánh dấu AVAILABLE khi có bằng chứng. Không đưa giá trị secret vào báo cáo; chỉ ghi tên biến và trạng thái có/thiếu.

### Giai đoạn 2 — Xử lý blocker và lựa chọn phương án

Phân loại:
- **BLOCKER**: chưa thể đáp ứng yêu cầu nếu thiếu tài nguyên/quyền/quyết định.
- **HIGH RISK**: có thể triển khai nhưng đánh đổi đáng kể về chất lượng, bảo mật, chi phí hoặc bảo trì.
- **NON-BLOCKING**: có thể tiếp tục mà không làm giảm chất lượng yêu cầu.
- **UNKNOWN**: chưa đủ bằng chứng; không được coi là sẵn sàng.

Với blocker/trade-off quan trọng, trình bày 2–3 lựa chọn khả thi (nếu có), chi phí/thời gian, hệ quả chất lượng/bảo mật, tính đảo ngược, khuyến nghị và quyết định cần từ owner.

Không âm thầm dùng mock, placeholder, ảnh sinh bởi AI, local-only implementation hoặc integration giả làm giải pháp production. Mock được phép cho unit test cô lập nếu ghi rõ phạm vi và không che giấu rủi ro tích hợp thật.

### Giai đoạn 3 — Chốt thiết kế và test plan

Trước khi code:
1. So sánh phương án dựa trên yêu cầu và Readiness Matrix.
2. Ghi quyết định quan trọng vào ADR, gồm cả phương án bị loại và lý do.
3. Xác định acceptance criteria, task owner, dependencies và phạm vi.
4. Dùng docs/agent-ops/templates/TEST_PLAN_TEMPLATE.md để tạo docs/agent-ops/TEST_PLAN.md.
5. Xin phê duyệt trước khi cài dependency lớn, phát sinh chi phí, mở rộng quyền hoặc thay đổi production.

### Giai đoạn 4 — Implement và test theo lớp

| Lớp kiểm thử | Dùng để kiểm tra | Ví dụ |
|---|---|---|
| Static | Cấu hình/chất lượng mã | lint, typecheck, format, schema check |
| Unit | Logic, validation, quyền, phép tính | hàm thuần, service nhỏ |
| API/Integration | Contract, persistence, auth, tích hợp | route, query, migration |
| Component | Tương tác và accessibility | form, keyboard, role/name |
| E2E | Hành trình người dùng quan trọng | đăng nhập, tạo bản ghi, luồng chính |
| Visual regression | Yêu cầu hiển thị cụ thể | clipping, responsive, spacing, theme |

Chọn lớp rẻ nhất nhưng đủ tin cậy để chứng minh acceptance criterion. Không chạy toàn bộ E2E sau mỗi lần sửa nếu test ở lớp thấp hơn đã đủ. Chạy targeted tests khi phát triển, mở rộng phạm vi ở các mốc nghiệm thu.

### Giai đoạn 5 — Quy tắc screenshot

- Ngân sách mặc định: **0 screenshot**.
- Không dùng image generation để tạo hình giả làm bằng chứng app chạy.
- Chỉ chụp screenshot thật khi trả lời một câu hỏi thị giác cụ thể hoặc kiểm tra visual baseline đã duyệt.
- Trước visual test, ghi rõ câu hỏi, trang/trạng thái đại diện, viewport/device/theme, số ảnh tối đa, nơi lưu và dọn dẹp.
- Nếu Playwright đã được cấu hình, cân nhắc chụp khi test thất bại và trace ở lần retry đầu tiên, nếu phiên bản hiện tại hỗ trợ. Không cài Playwright chỉ vì có hướng dẫn này.
- Không chụp mọi trang × mọi trạng thái × mọi viewport mặc định.
- Không chấp nhận snapshot mới chỉ để làm test xanh; phải xem diff và ghi lý do.

### Giai đoạn 6 — Khi test thất bại

1. Lưu lỗi đầu tiên và bằng chứng tối thiểu hữu ích.
2. Chẩn đoán nguyên nhân trước khi retry.
3. Xác định lỗi do code, môi trường, quyền, fixture, service hay test không ổn định.
4. Nếu resource/access chưa sẵn sàng, đánh dấu BLOCKED hoặc NOT RUN và cập nhật Readiness Matrix.
5. Nếu cần giảm chất lượng/coverage hoặc đổi phương án, quay lại owner xin quyết định.
6. Không retry mù liên tục, xóa assertion hoặc bỏ qua lỗi chỉ để đạt màu xanh.

### Giai đoạn 7 — Báo cáo nghiệm thu

Báo cáo cuối phải liệt kê:
- Lệnh đã chạy, exit code và thời lượng nếu có.
- Số PASS, FAIL, SKIPPED, BLOCKED và NOT RUN.
- Số screenshot/trace/video được giữ lại và lý do.
- Phạm vi chưa kiểm tra; integrations/permissions chưa xác minh.
- Dependencies/cấu hình mới và lý do.
- Sai lệch so với test plan và phê duyệt tương ứng.
- Quyết định hoặc blocker còn chờ owner.

Không gọi feature là “đã test” nếu mới tạo test mà chưa chạy test thật.

## 4. Prompt khởi động gợi ý

> Trước khi thiết kế hoặc code, hãy gọi skill /project-discovery và khảo sát repository, assets, quyền truy cập, integrations, test infrastructure và môi trường. Tạo docs/agent-ops/READINESS_MATRIX.md và DISCOVERY_SUMMARY.md với bằng chứng. Sau đó gọi /efficient-testing và lập docs/agent-ops/TEST_PLAN.md, screenshot budget mặc định bằng 0. Nếu thiếu tài nguyên/quyền hoặc có trade-off ảnh hưởng chất lượng, hãy đưa ra lựa chọn và hỏi tôi; không tự dựng workaround. Chỉ bắt đầu phần triển khai có thể thực hiện an toàn sau khi các cổng này được xử lý. Báo cáo chính xác các lệnh và test thực tế đã chạy.

## 5. Checklist nghiệm thu

- [ ] Hai skills có trong .claude/skills/ và gọi được.
- [ ] Main Agent thực hiện discovery trước khi chọn kiến trúc.
- [ ] Readiness Matrix phân biệt AVAILABLE/MISSING/UNKNOWN/BLOCKED.
- [ ] Assets, integrations, permissions, environment và test resources được kiểm tra.
- [ ] Blockers có lựa chọn, trade-off và quyết định owner khi cần.
- [ ] Test plan gắn với acceptance criteria, rủi ro và lớp test.
- [ ] Screenshot budget mặc định bằng 0; mọi ảnh có câu hỏi cụ thể.
- [ ] Test evidence đến từ app/runtime thật, không phải ảnh AI.
- [ ] Báo cáo phân biệt PASS/FAIL/BLOCKED/NOT RUN và ghi coverage gaps.
- [ ] Không có workaround giảm chất lượng hoặc đổi hành vi mà chưa được duyệt.

## 6. Tài liệu tham khảo

- Claude Code Skills: https://code.claude.com/docs/en/skills
- Claude Code Permissions: https://code.claude.com/docs/en/permissions
- Claude Code Hooks: https://code.claude.com/docs/en/hooks
- Playwright test options: https://playwright.dev/docs/api/class-testoptions
- Testing Library query priority: https://testing-library.com/docs/queries/about/
