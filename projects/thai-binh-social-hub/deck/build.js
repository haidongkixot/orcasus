// Thai Binh Social Hub — BOD pitch deck (Vietnamese), built on the Thai Binh Corporation design system tokens.
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const lu = require("react-icons/lu");
const { applyTheme } = require(process.env.PPTX_SKILL + "/scripts/apply_theme.js");

const LOGOS = process.env.LOGO_DIR;
const OUT = process.env.OUT_FILE;

// ---- Design-system tokens (exact hex from tokens.json) ----
const T = {
  navy: "00377B", navyDeep: "002E6E", navyPanel: "033878", navyBlock: "003C7E",
  royal: "1C489C", blueMid: "2A6AB2", heading: "0C3469", ink: "002060", inkSoft: "384D81",
  sky: "6DB6D9", skyTint: "CAE1FF", cyan: "00AAF3", decadas: "19B1E7",
  ice: "E7F1FF", mist: "EFF9FE", redHeadline: "DF1F2B", redSignal: "EB2127", redBlock: "ED1D24",
  gray: "58595B", grayCaption: "6F6F6F", white: "FFFFFF",
  food: "F47920", agri: "006834", comm: "58C5C7",
};
const THEME = {
  name: "Thai Binh Corporation",
  headFontFace: "Montserrat",
  bodyFontFace: "Montserrat",
  colors: {
    dk1: T.ink, lt1: T.white, dk2: T.heading, lt2: T.mist,
    accent1: T.navy, accent2: T.redSignal, accent3: T.royal, accent4: T.decadas,
    accent5: T.blueMid, accent6: T.ice, hlink: T.blueMid, folHlink: T.inkSoft,
  },
};

const W = 13.333, H = 7.5, M = 0.75; // slide-margin 81px on the 1440 canvas = 0.75in

async function icon(name, hex, px = 256) {
  const Comp = lu[name];
  if (!Comp) throw new Error("Missing icon " + name);
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color: "#" + hex, size: px, strokeWidth: 1.75 }));
  const buf = await sharp(Buffer.from(svg)).resize(px, px).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

(async () => {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  pres.title = "Thai Binh Social Hub — Đề xuất dự án";
  pres.author = "Giám đốc Marcom, Thai Binh Corporation";
  pres.company = "Thai Binh Corporation";
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  const C = pres.SchemeColor;

  const lockupColor = path.join(LOGOS, "thaibinh-lockup-color.png");
  const lockupWhite = path.join(LOGOS, "thaibinh-lockup-white.png");
  const logoH = 0.52, logoW = logoH * 656 / 188;

  // ---- Layouts ----
  const titlePh = (color) => ({
    placeholder: {
      options: { name: "title", type: "title", x: M, y: 0.42, w: 9.4, h: 1.0, fontSize: 24, bold: true,
        color, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 0.95 },
      text: "",
    },
  });
  pres.defineSlideMaster({
    title: "TB_CONTENT",
    background: { color: T.white },
    objects: [
      { image: { path: lockupColor, x: W - M - logoW, y: 0.42, w: logoW, h: logoH, altText: "Thai Binh Corporation logo" } },
      titlePh(T.heading),
    ],
    slideNumber: { x: W - M - 0.6, y: H - 0.45, w: 0.6, h: 0.3, fontSize: 10, color: T.grayCaption, align: "right" },
  });
  pres.defineSlideMaster({
    title: "TB_COVER",
    background: { color: T.mist },
    objects: [
      { image: { path: lockupColor, x: W - M - logoW, y: 0.42, w: logoW, h: logoH, altText: "Thai Binh Corporation logo" } },
    ],
  });
  pres.defineSlideMaster({
    title: "TB_DIVIDER",
    background: { color: T.royal },
    objects: [
      { image: { path: lockupWhite, x: W - M - logoW, y: 0.42, w: logoW, h: logoH, altText: "Thai Binh Corporation logo" } },
      { placeholder: { options: { name: "body", type: "body", x: 6.6, y: 2.45, w: 6.0, h: 1.0, fontSize: 54, bold: true, color: T.cyan, align: "left", margin: 0, valign: "bottom" }, text: "" } },
      { placeholder: { options: { name: "title", type: "title", x: 6.6, y: 3.5, w: 6.0, h: 1.3, fontSize: 36, bold: true, color: T.white, align: "left", margin: 0, valign: "top" }, text: "" } },
    ],
  });

  const addTitle = (slide, l1, l2) =>
    slide.addText([
      { text: l1, options: { color: T.heading, breakLine: true } },
      { text: l2, options: { color: T.sky } },
    ], { placeholder: "title" });

  const shadow = () => ({ type: "outer", color: T.navy, opacity: 0.14, blur: 12, offset: 4, angle: 90 });
  const card = (slide, x, y, w, h, name, fill = T.white) =>
    slide.addShape(pres.ShapeType.roundRect, { x, y, w, h, fill: { color: fill }, line: { color: fill, width: 0 },
      rectRadius: 0.2, shadow: shadow(), objectName: name });
  const disc = async (slide, x, y, d, iconName, discColor, iconColor, name) => {
    slide.addShape(pres.ShapeType.ellipse, { x, y, w: d, h: d, fill: { color: discColor }, line: { color: discColor, width: 0 }, objectName: name + " disc" });
    const s = d * 0.56;
    slide.addImage({ data: await icon(iconName, iconColor), x: x + (d - s) / 2, y: y + (d - s) / 2, w: s, h: s, altText: name, objectName: name + " icon" });
  };
  const tag = (slide, text, x, y, w, h = 0.36, fill = T.redSignal) =>
    slide.addText(text, { x, y, w, h, fill: { color: fill }, color: T.white, fontSize: 13, bold: true, align: "center", valign: "middle",
      margin: 0, isTextBox: true, objectName: "Tag " + text });
  // Level Ring (derived from the brand's cyan→red circle frame; our app's progress ring)
  const levelRing = (slide, cx, cy, r, thick = 0.09, gapDeg = 40) => {
    const box = { x: cx - r, y: cy - r, w: 2 * r, h: 2 * r };
    slide.addShape(pres.ShapeType.blockArc, { ...box, fill: { color: T.decadas }, line: { color: T.decadas, width: 0 },
      angleRange: [150, 300], arcThicknessRatio: thick, objectName: "Level ring cyan" });
    slide.addShape(pres.ShapeType.blockArc, { ...box, fill: { color: T.redSignal }, line: { color: T.redSignal, width: 0 },
      angleRange: [300, 150 - gapDeg + 360 > 360 ? 150 - gapDeg : 150 - gapDeg], arcThicknessRatio: thick, objectName: "Level ring red" });
  };

  // ===== 1. COVER =====
  pres.addSection({ title: "Mở đầu" });
  let s = pres.addSlide({ masterName: "TB_COVER", sectionTitle: "Mở đầu" });
  tag(s, "ĐỀ XUẤT DỰ ÁN", M, 1.55, 2.2);
  s.addText([
    { text: "THAI BINH", options: { fontSize: 60, bold: true, color: T.navy, breakLine: true } },
    { text: "SOCIAL HUB", options: { fontSize: 44, bold: true, color: T.navyDeep } },
  ], { x: M, y: 2.1, w: 6.6, h: 1.9, margin: 0, valign: "top", isTextBox: true, lineSpacingMultiple: 0.9, objectName: "Cover title" });
  s.addText("Nền tảng kết nối 1.000+ nhân viên với các kênh truyền thông của Tập đoàn — vui hơn, gắn kết hơn, đo lường được.",
    { x: M, y: 4.1, w: 6.2, h: 1.0, fontSize: 18, color: T.inkSoft, bold: true, margin: 0, valign: "top", isTextBox: true, objectName: "Cover subtitle" });
  s.addText("Trình bày: Giám đốc Marcom  ·  Kính gửi: Hội đồng Quản trị  ·  Tháng 11/2026",
    { x: M, y: 6.45, w: 7.5, h: 0.4, fontSize: 12, color: T.gray, margin: 0, isTextBox: true, objectName: "Cover byline" });
  // circle motif: level ring + white disc + trophy + points pop
  levelRing(s, 9.75, 4.25, 2.25, 0.07);
  s.addShape(pres.ShapeType.ellipse, { x: 9.75 - 1.9, y: 4.25 - 1.9, w: 3.8, h: 3.8, fill: { color: T.white }, line: { color: T.white, width: 0 }, shadow: shadow(), objectName: "Cover disc" });
  s.addImage({ data: await icon("LuTrophy", T.navy), x: 9.75 - 0.95, y: 4.25 - 1.15, w: 1.9, h: 1.9, altText: "Cúp", objectName: "Cover trophy" });
  s.addText("Cùng nhau lan toả", { x: 9.75 - 1.6, y: 4.95, w: 3.2, h: 0.45, fontSize: 15, bold: true, color: T.heading, align: "center", margin: 0, isTextBox: true, objectName: "Cover disc caption" });
  tag(s, "+10 ĐIỂM", 11.25, 5.75, 1.45, 0.42);
  s.addNotes("Kính thưa Hội đồng Quản trị. Hôm nay Marcom xin trình bày đề xuất Thai Binh Social Hub: một nền tảng nội bộ giúp hơn 1.000 nhân viên đồng hành cùng các kênh mạng xã hội của Tập đoàn, kèm cơ chế ghi nhận và thi đua vui vẻ. Mục tiêu của buổi hôm nay là xin phê duyệt giai đoạn khảo sát, thiết kế và thí điểm.");

  // ===== 2. CONTEXT & OPPORTUNITY =====
  s = pres.addSlide({ masterName: "TB_CONTENT", sectionTitle: "Mở đầu" });
  addTitle(s, "BỐI CẢNH & CƠ HỘI", "1.000+ ĐẠI SỨ THƯƠNG HIỆU");
  const stats = [
    { big: "1.000+", color: T.redHeadline, label: "nhân viên Thái Bình — mỗi người là một kênh lan toả thương hiệu", cap: "" },
    { big: "[ ? ]", color: T.navy, label: "người theo dõi trên các fanpage và Instagram của Tập đoàn", cap: "Số liệu cần bổ sung từ Meta Business Suite" },
    { big: "[ ? ]", color: T.navy, label: "tương tác trung bình trên mỗi bài đăng hiện nay", cap: "Số liệu cần bổ sung từ Meta Business Suite" },
  ];
  const sw = 3.75, sg = 0.33;
  stats.forEach((st, i) => {
    const x = M + i * (sw + sg);
    card(s, x, 1.75, sw, 1.95, "Stat card " + (i + 1));
    s.addText(st.big, { x: x + 0.3, y: 1.9, w: sw - 0.6, h: 0.8, fontSize: 40, bold: true, color: st.color, margin: 0, isTextBox: true, objectName: "Stat value " + (i + 1) });
    s.addText(st.label, { x: x + 0.3, y: 2.7, w: sw - 0.6, h: 0.6, fontSize: 14, color: T.ink, margin: 0, valign: "top", isTextBox: true, objectName: "Stat label " + (i + 1) });
    if (st.cap) s.addText(st.cap, { x: x + 0.3, y: 3.3, w: sw - 0.6, h: 0.3, fontSize: 10, italic: true, color: T.grayCaption, margin: 0, isTextBox: true, objectName: "Stat caption " + (i + 1) });
  });
  const cols = [
    { head: "THÁCH THỨC HIỆN NAY", iconName: "LuAlertTriangle", items: [
      "Lượt tiếp cận tự nhiên của fanpage phụ thuộc thuật toán",
      "Nhân viên chưa có kênh tập trung để biết và đồng hành cùng các chiến dịch",
      "Chưa đo lường và ghi nhận được đóng góp của từng người, từng phòng ban",
    ] },
    { head: "CƠ HỘI CHO THÁI BÌNH", iconName: "LuSparkles", items: [
      "Biến niềm tự hào của 1.000+ nhân viên thành tương tác thật",
      "Lan toả văn hoá Tận tâm, Sáng tạo qua thi đua vui vẻ",
      "Dữ liệu đo lường theo chiến dịch, phòng ban, chi nhánh",
    ] },
  ];
  for (let i = 0; i < cols.length; i++) {
    const x = M + i * 6.0;
    await disc(s, x, 4.1, 0.55, cols[i].iconName, i === 0 ? T.ice : T.redSignal, i === 0 ? T.navy : T.white, cols[i].head);
    s.addText(cols[i].head, { x: x + 0.7, y: 4.1, w: 5.0, h: 0.55, fontSize: 16, bold: true, color: T.heading, valign: "middle", margin: 0, isTextBox: true, objectName: "Col head " + i });
    s.addText(cols[i].items.map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < cols[i].items.length - 1 } })),
      { x: x + 0.7, y: 4.8, w: 5.1, h: 1.9, fontSize: 14, color: T.ink, valign: "top", margin: 0, paraSpaceAfter: 8, isTextBox: true, objectName: "Col items " + i });
  }
  s.addNotes("Thái Bình có hơn 1.000 nhân viên — đây là lực lượng lan toả lớn nhất mà chúng ta đang có nhưng chưa khai thác. Hai ô số liệu còn trống sẽ được Marcom bổ sung từ Meta Business Suite trước buổi họp: tổng người theo dõi và mức tương tác trung bình mỗi bài. Ghi chú: các nghiên cứu ngành thường trích dẫn rằng nội dung do nhân viên chia sẻ đạt lượt tiếp cận cao hơn nhiều so với kênh thương hiệu; con số phổ biến 561% chưa xác minh được nguồn gốc nên không đưa lên slide.");

  // ===== 3. DIVIDER 01 =====
  pres.addSection({ title: "Giải pháp" });
  const divider = async (num, title, sub, iconName, section, notes) => {
    const d = pres.addSlide({ masterName: "TB_DIVIDER", sectionTitle: section });
    d.addText(num, { placeholder: "body" });
    d.addText(title, { placeholder: "title" });
    d.addText(sub, { x: 6.6, y: 4.85, w: 5.8, h: 0.8, fontSize: 16, color: T.skyTint, margin: 0, valign: "top", isTextBox: true, objectName: "Divider subtitle" });
    levelRing(d, 3.4, 3.9, 2.2, 0.07);
    d.addShape(pres.ShapeType.ellipse, { x: 3.4 - 1.85, y: 3.9 - 1.85, w: 3.7, h: 3.7, fill: { color: T.white }, line: { color: T.white, width: 0 }, objectName: "Divider disc" });
    d.addImage({ data: await icon(iconName, T.navy), x: 3.4 - 0.9, y: 3.9 - 0.9, w: 1.8, h: 1.8, altText: title, objectName: "Divider icon" });
    d.addNotes(notes);
  };
  await divider("01.", "GIẢI PHÁP", "Thai Binh Social Hub — kết nối, gắn kết và ghi nhận", "LuSmartphone", "Giải pháp",
    "Phần 1: giải pháp — nền tảng là gì, nhân viên dùng như thế nào và cơ chế gamification.");

  // ===== 4. WHAT IS IT =====
  s = pres.addSlide({ masterName: "TB_CONTENT", sectionTitle: "Giải pháp" });
  addTitle(s, "THAI BINH SOCIAL HUB", "NỀN TẢNG GẮN KẾT NỘI BỘ");
  const pillars = [
    { t: "KẾT NỐI", i: "LuLink", d: "Đăng nhập bằng Facebook, xem tất cả fanpage và Instagram của Tập đoàn tại một nơi." },
    { t: "GẮN KẾT", i: "LuMessageCircle", d: "Nhiệm vụ mỗi ngày: bình luận, bày tỏ cảm xúc, chia sẻ — một chạm để mở bài viết trên ứng dụng Facebook/Instagram." },
    { t: "GHI NHẬN", i: "LuAward", d: "Điểm, huy hiệu, bảng xếp hạng phòng ban và giải thưởng định kỳ cho tinh thần đồng hành." },
  ];
  for (let i = 0; i < 3; i++) {
    const x = M + i * (sw + sg);
    card(s, x, 1.75, sw, 4.15, "Pillar card " + (i + 1));
    await disc(s, x + sw / 2 - 0.5, 2.05, 1.0, pillars[i].i, i === 1 ? T.redSignal : T.ice, i === 1 ? T.white : T.navy, pillars[i].t);
    s.addText(pillars[i].t, { x: x + 0.3, y: 3.25, w: sw - 0.6, h: 0.5, fontSize: 20, bold: true, color: T.heading, align: "center", margin: 0, isTextBox: true, objectName: "Pillar title " + (i + 1) });
    // brand InfoCard device: short red-signal underline with a centre dot
    s.addShape(pres.ShapeType.line, { x: x + sw / 2 - 0.38, y: 3.85, w: 0.76, h: 0, line: { color: T.redSignal, width: 1.75 }, objectName: "Pillar underline " + (i + 1) });
    s.addShape(pres.ShapeType.ellipse, { x: x + sw / 2 - 0.04, y: 3.81, w: 0.08, h: 0.08, fill: { color: T.redSignal }, line: { color: T.redSignal, width: 0 }, objectName: "Pillar dot " + (i + 1) });
    s.addText(pillars[i].d, { x: x + 0.35, y: 4.05, w: sw - 0.7, h: 1.65, fontSize: 15, bold: true, color: T.inkSoft, align: "center", valign: "top", margin: 0, isTextBox: true, objectName: "Pillar text " + (i + 1) });
  }
  s.addText("Ứng dụng web tối ưu cho điện thoại — truy cập bằng một đường link, không cần cài đặt.",
    { x: M, y: 6.2, w: W - 2 * M, h: 0.5, fill: { color: T.ice }, fontSize: 15, bold: true, color: T.navy, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "Banner bar" });
  s.addNotes("Ba giá trị cốt lõi của nền tảng: Kết nối — mọi kênh của Tập đoàn ở một nơi; Gắn kết — nhiệm vụ rõ ràng, một chạm là tương tác; Ghi nhận — điểm, huy hiệu, bảng xếp hạng và giải thưởng. Nhân viên chỉ cần mở một đường link trên điện thoại, không phải cài ứng dụng.");

  // ===== 5. EMPLOYEE JOURNEY =====
  s = pres.addSlide({ masterName: "TB_CONTENT", sectionTitle: "Giải pháp" });
  addTitle(s, "HÀNH TRÌNH NHÂN VIÊN", "6 BƯỚC ĐƠN GIẢN");
  const steps = [
    { n: "01", t: "Đăng nhập", d: "Bằng tài khoản Facebook cá nhân", i: "LuLogIn" },
    { n: "02", t: "Hồ sơ", d: "Khai báo mã nhân viên, phòng ban, chi nhánh", i: "LuContact" },
    { n: "03", t: "Phê duyệt", d: "Quản trị viên xác nhận đúng là nhân viên", i: "LuUserCheck" },
    { n: "04", t: "Xác thực", d: "Bình luận mã một lần để liên kết FB/IG", i: "LuKeyRound" },
    { n: "05", t: "Tương tác", d: "Làm nhiệm vụ trên bài đăng của Tập đoàn", i: "LuMousePointerClick" },
    { n: "06", t: "Nhận điểm", d: "Tự động cộng điểm, huy hiệu, lên cấp", i: "LuTrophy" },
  ];
  const lineY = 3.55, stepW = (W - 2 * M) / 6;
  s.addShape(pres.ShapeType.line, { x: M, y: lineY, w: W - 2 * M, h: 0, line: { color: T.navy, width: 2 }, objectName: "Timeline line" });
  for (let i = 0; i < steps.length; i++) {
    const x = M + i * stepW;
    await disc(s, x + 0.1, 1.9, 0.9, steps[i].i, i === 5 ? T.redSignal : T.ice, i === 5 ? T.white : T.navy, steps[i].t);
    s.addShape(pres.ShapeType.ellipse, { x: x + 0.4, y: lineY - 0.15, w: 0.3, h: 0.3, fill: { color: T.white }, line: { color: T.redSignal, width: 3 }, objectName: "Timeline dot " + steps[i].n });
    s.addText(steps[i].n, { x: x + 0.1, y: 3.85, w: stepW - 0.2, h: 0.45, fontSize: 20, bold: true, color: T.heading, margin: 0, isTextBox: true, objectName: "Step number " + steps[i].n });
    s.addText(steps[i].t, { x: x + 0.1, y: 4.3, w: stepW - 0.2, h: 0.4, fontSize: 16, bold: true, color: T.navy, margin: 0, isTextBox: true, objectName: "Step title " + steps[i].n });
    s.addText(steps[i].d, { x: x + 0.1, y: 4.72, w: stepW - 0.3, h: 0.9, fontSize: 14, color: T.ink, valign: "top", margin: 0, isTextBox: true, objectName: "Step text " + steps[i].n });
  }
  s.addText([
    { text: "Lưu ý: ", options: { bold: true, color: T.redHeadline } },
    { text: "Theo chính sách của Meta, bình luận và cảm xúc được thực hiện trên ứng dụng Facebook/Instagram. Social Hub ghi nhận tự động qua kết nối chính thức (webhook) với fanpage của Tập đoàn.", options: { color: T.navy } },
  ], { x: M, y: 5.95, w: W - 2 * M, h: 0.75, fill: { color: T.ice }, fontSize: 14, valign: "middle", margin: [6, 14, 6, 14], isTextBox: true, objectName: "Meta note" });
  s.addNotes("Hành trình của một nhân viên gồm 6 bước. Điểm quan trọng: Meta không cho phép ứng dụng bên ngoài bình luận thay người dùng, nên khi bấm 'Bình luận', bài viết mở ngay trong ứng dụng Facebook hoặc Instagram. Ngay khi nhân viên bình luận, fanpage của Tập đoàn gửi tín hiệu về hệ thống và điểm được cộng tự động. Bước 'Xác thực' — bình luận một mã ngắn — giúp liên kết đúng tài khoản với đúng nhân viên.");

  // ===== 6. GAMIFICATION =====
  s = pres.addSlide({ masterName: "TB_CONTENT", sectionTitle: "Giải pháp" });
  addTitle(s, "GAMIFICATION", "VUI — CÔNG BẰNG — TÔN VINH");
  s.addText("HUY HIỆU THEO 5 GIÁ TRỊ CỐT LÕI", { x: M, y: 1.7, w: W - 2 * M, h: 0.45, fill: { color: T.ice }, fontSize: 14, bold: true, color: T.navy, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "Badges banner" });
  const badges = [
    { t: "Chính trực", i: "LuShieldCheck" }, { t: "Tận tâm", i: "LuHeart" }, { t: "Sáng tạo", i: "LuLightbulb" },
    { t: "Kiên trì", i: "LuMountain" }, { t: "Vững mạnh", i: "LuZap" },
  ];
  const bw = (W - 2 * M) / 5;
  for (let i = 0; i < 5; i++) {
    const cx = M + i * bw + bw / 2;
    levelRing(s, cx, 2.95, 0.55, 0.12);
    await disc(s, cx - 0.42, 2.95 - 0.42, 0.84, badges[i].i, T.navy, T.white, badges[i].t);
    s.addText(badges[i].t, { x: cx - 1.0, y: 3.58, w: 2.0, h: 0.4, fontSize: 15, bold: true, color: T.heading, align: "center", margin: 0, isTextBox: true, objectName: "Badge label " + i });
  }
  const mech = [
    { t: "Điểm & cấp độ", d: "Vòng cấp độ quanh ảnh đại diện đầy dần khi tích điểm", i: "LuStar" },
    { t: "Nhiệm vụ & chiến dịch", d: "Nhiệm vụ hằng ngày, chiến dịch theo sự kiện có đếm ngược", i: "LuTarget" },
    { t: "Bảng vàng", d: "Xếp hạng cá nhân, phòng ban, chi nhánh; chuỗi ngày hoạt động", i: "LuCrown" },
    { t: "Giải thưởng định kỳ", d: "Thưởng cho sự tham gia đều đặn — không “mua” lượt thích", i: "LuGift" },
  ];
  const mw = (W - 2 * M - 0.33) / 2;
  for (let i = 0; i < 4; i++) {
    const x = M + (i % 2) * (mw + 0.33), y = 4.25 + Math.floor(i / 2) * 1.25;
    card(s, x, y, mw, 1.05, "Mechanic card " + i);
    await disc(s, x + 0.25, y + 0.2, 0.65, mech[i].i, i === 3 ? T.redSignal : T.ice, i === 3 ? T.white : T.navy, mech[i].t);
    s.addText(mech[i].t, { x: x + 1.1, y: y + 0.12, w: mw - 1.3, h: 0.4, fontSize: 16, bold: true, color: T.heading, margin: 0, isTextBox: true, objectName: "Mechanic title " + i });
    s.addText(mech[i].d, { x: x + 1.1, y: y + 0.52, w: mw - 1.3, h: 0.45, fontSize: 14, color: T.ink, margin: 0, valign: "top", isTextBox: true, objectName: "Mechanic text " + i });
  }
  s.addNotes("Cơ chế thi đua gắn trực tiếp với 5 giá trị cốt lõi của Thái Bình: Chính trực, Tận tâm, Sáng tạo, Kiên trì, Vững mạnh — mỗi giá trị là một bộ huy hiệu. Bốn cơ chế chính: điểm và cấp độ, nhiệm vụ và chiến dịch, bảng vàng theo cá nhân và phòng ban, và giải thưởng định kỳ. Nguyên tắc: thưởng cho sự tham gia đều đặn, đa dạng — không trả thưởng theo từng lượt thích, để tuân thủ chính sách Meta.");

  // ===== 7. EXPERIENCE (mockups) =====
  s = pres.addSlide({ masterName: "TB_CONTENT", sectionTitle: "Giải pháp" });
  addTitle(s, "TRẢI NGHIỆM", "VUI TƯƠI TRÊN NỀN THƯƠNG HIỆU");
  const pw = 2.75, ph = 4.55, pgap = 1.05, px0 = (W - (3 * pw + 2 * pgap)) / 2, py = 1.65;
  const phone = (x, screenColor, name) => {
    s.addShape(pres.ShapeType.roundRect, { x, y: py, w: pw, h: ph, fill: { color: T.navyDeep }, line: { color: T.navyDeep, width: 0 }, rectRadius: 0.3, shadow: shadow(), objectName: name + " frame" });
    s.addShape(pres.ShapeType.roundRect, { x: x + 0.1, y: py + 0.1, w: pw - 0.2, h: ph - 0.2, fill: { color: screenColor }, line: { color: screenColor, width: 0 }, rectRadius: 0.22, objectName: name + " screen" });
  };
  const t = (text, x, y, w, h, o = {}) => s.addText(text, { x, y, w, h, margin: 0, isTextBox: true, fontSize: 10, color: T.ink, ...o });
  // Phone 1 — Today
  let x = px0;
  phone(x, T.mist, "Today");
  t("HÔM NAY", x + 0.3, py + 0.25, 2.1, 0.3, { fontSize: 11, bold: true, color: T.heading });
  levelRing(s, x + pw / 2, py + 1.25, 0.6, 0.12);
  s.addShape(pres.ShapeType.ellipse, { x: x + pw / 2 - 0.46, y: py + 1.25 - 0.46, w: 0.92, h: 0.92, fill: { color: T.ice }, line: { color: T.white, width: 2 }, objectName: "Avatar" });
  s.addImage({ data: await icon("LuUsers", T.navy), x: x + pw / 2 - 0.25, y: py + 1.0, w: 0.5, h: 0.5, altText: "Ảnh đại diện", objectName: "Avatar icon" });
  t("Cấp 4 · Tận tâm", x + 0.2, py + 1.95, pw - 0.4, 0.25, { fontSize: 10, bold: true, color: T.heading, align: "center" });
  t("1.250 điểm", x + 0.2, py + 2.2, pw - 0.4, 0.35, { fontSize: 16, bold: true, color: T.redHeadline, align: "center" });
  const mission = (y, title, pts, prog) => {
    s.addShape(pres.ShapeType.roundRect, { x: x + 0.25, y, w: pw - 0.5, h: 0.62, fill: { color: T.white }, line: { color: T.white, width: 0 }, rectRadius: 0.1, objectName: "Mission " + title });
    t(title, x + 0.35, y + 0.06, pw - 1.35, 0.3, { fontSize: 9, bold: true, color: T.heading });
    t(pts, x + pw - 0.95, y + 0.08, 0.6, 0.24, { fontSize: 9, bold: true, color: T.white, fill: { color: T.redSignal }, align: "center", valign: "middle" });
    s.addShape(pres.ShapeType.rect, { x: x + 0.35, y: y + 0.44, w: pw - 0.7, h: 0.07, fill: { color: T.ice }, line: { color: T.ice, width: 0 }, objectName: "Progress track" });
    s.addShape(pres.ShapeType.rect, { x: x + 0.35, y: y + 0.44, w: (pw - 0.7) * prog, h: 0.07, fill: { color: T.decadas }, line: { color: T.decadas, width: 0 }, objectName: "Progress fill" });
  };
  t("NHIỆM VỤ HÔM NAY", x + 0.25, py + 2.65, 2.2, 0.25, { fontSize: 9, bold: true, color: T.navy });
  mission(py + 2.92, "Bình luận bài mới TBFood", "+10", 0.0);
  mission(py + 3.62, "Chuỗi 5 ngày liên tiếp", "+20", 0.8);
  // Phone 2 — Leaderboard
  x = px0 + pw + pgap;
  phone(x, T.white, "Leaderboard");
  t("BẢNG VÀNG", x + 0.3, py + 0.25, 2.1, 0.3, { fontSize: 11, bold: true, color: T.heading });
  t("Phòng ban  ·  Tháng này", x + 0.3, py + 0.55, 2.1, 0.25, { fontSize: 9, color: T.gray });
  const podium = [
    { r: "2", h: 0.95, c: T.navyBlock, n: "Phòng B" }, { r: "1", h: 1.35, c: T.redBlock, n: "Phòng A" }, { r: "3", h: 0.7, c: T.navyPanel, n: "Phòng C" },
  ];
  const pdw = (pw - 0.6) / 3, base = py + 2.75;
  podium.forEach((p, i) => {
    const xx = x + 0.3 + i * pdw;
    s.addShape(pres.ShapeType.rect, { x: xx, y: base - p.h, w: pdw, h: p.h, fill: { color: p.c }, line: { color: p.c, width: 0 }, objectName: "Podium " + p.r });
    t(p.r, xx, base - p.h + 0.08, pdw, 0.4, { fontSize: 18, bold: true, color: T.white, align: "center" });
    t(p.n, xx - 0.05, base - p.h - 0.3, pdw + 0.1, 0.25, { fontSize: 8, bold: true, color: T.heading, align: "center" });
  });
  [["12", "Bạn", "↑3"], ["13", "Đồng nghiệp", ""], ["14", "Đồng nghiệp", ""]].forEach((r, i) => {
    const yy = base + 0.2 + i * 0.45;
    s.addShape(pres.ShapeType.roundRect, { x: x + 0.25, y: yy, w: pw - 0.5, h: 0.38, fill: { color: i === 0 ? T.ice : T.mist }, line: { color: i === 0 ? T.ice : T.mist, width: 0 }, rectRadius: 0.08, objectName: "Rank row " + r[0] });
    t(r[0], x + 0.35, yy + 0.06, 0.35, 0.26, { fontSize: 10, bold: true, color: T.heading });
    t(r[1], x + 0.75, yy + 0.06, 1.2, 0.26, { fontSize: 10, bold: i === 0, color: T.ink });
    if (r[2]) t(r[2], x + pw - 0.75, yy + 0.06, 0.4, 0.26, { fontSize: 10, bold: true, color: T.agri, align: "right" });
  });
  // Phone 3 — Celebration
  x = px0 + 2 * (pw + pgap);
  phone(x, T.royal, "Celebration");
  [[0.35, 0.45, T.redSignal], [2.1, 0.7, T.decadas], [0.6, 1.25, T.white], [2.2, 1.6, T.redSignal], [0.4, 2.0, T.decadas], [1.95, 0.35, T.white], [1.25, 0.55, T.redBlock]].forEach(([dx, dy, c], i) =>
    s.addShape(pres.ShapeType.rect, { x: x + dx, y: py + dy, w: 0.1, h: 0.1, fill: { color: c }, line: { color: c, width: 0 }, rotate: i * 25, objectName: "Confetti " + i }));
  t("05", x + 0.2, py + 1.05, pw - 0.4, 0.9, { fontSize: 48, bold: true, color: T.cyan, align: "center" });
  t("LÊN CẤP!", x + 0.2, py + 1.95, pw - 0.4, 0.45, { fontSize: 20, bold: true, color: T.white, align: "center" });
  t("Tuyệt vời! Bạn đã đạt cấp Kiên trì. Cả phòng đang cổ vũ bạn!", x + 0.3, py + 2.45, pw - 0.6, 0.65, { fontSize: 10, color: T.skyTint, align: "center", valign: "top" });
  t("CHIA SẺ VỚI ĐỘI", x + 0.35, py + 3.5, pw - 0.7, 0.45, { fontSize: 11, bold: true, color: T.white, fill: { color: T.redSignal }, align: "center", valign: "middle" });
  // captions
  ["Vòng cấp độ, điểm và nhiệm vụ trong ngày", "Thi đua theo phòng ban, luôn thấy mình tiến bộ", "Khoảnh khắc chúc mừng khi lên cấp"].forEach((c, i) =>
    t(c, px0 + i * (pw + pgap) - 0.3, py + ph + 0.12, pw + 0.6, 0.35, { fontSize: 12, bold: true, color: T.heading, align: "center" }));
  t("Thiết kế minh hoạ dựa trên hệ thống nhận diện Thái Bình; tên và số liệu trong hình là ví dụ.", M, 6.85, 9.5, 0.3, { fontSize: 10, italic: true, color: T.grayCaption });
  s.addNotes("Đây là hình minh hoạ trải nghiệm — chưa phải sản phẩm thật. Giao diện giữ nguyên màu xanh navy, đỏ và font Montserrat của Thái Bình, nhưng vui tươi hơn: vòng cấp độ quanh ảnh đại diện lấy cảm hứng từ vòng tròn xanh–đỏ trong bộ nhận diện, bục vinh danh dùng họa tiết khối vuông bậc thang, và màn hình chúc mừng dùng nền xanh royal như slide chương. Chúng tôi sẽ thử nghiệm với 5–8 nhân viên trước khi hoàn thiện.");

  // ===== 8. DIVIDER 02 =====
  pres.addSection({ title: "Triển khai" });
  await divider("02.", "TRIỂN KHAI", "Lộ trình, tuân thủ, ngân sách và đề xuất phê duyệt", "LuRocket", "Triển khai",
    "Phần 2: triển khai — lộ trình, tuân thủ và quản trị rủi ro, ngân sách, KPI và đề xuất.");

  // ===== 9. ROADMAP =====
  s = pres.addSlide({ masterName: "TB_CONTENT", sectionTitle: "Triển khai" });
  addTitle(s, "LỘ TRÌNH TRIỂN KHAI", "5 GIAI ĐOẠN · KHOẢNG 4–5 THÁNG");
  const phases = [
    { n: "GĐ 0", t: "Khảo sát & thiết kế", w: "3–4 tuần", d: "Yêu cầu chi tiết, kiến trúc, thiết kế giao diện, luật chơi" },
    { n: "GĐ 1", t: "Thử nghiệm kỹ thuật", w: "1–2 tuần", d: "Xác minh kết nối Meta trên fanpage thử; dừng nếu không đạt" },
    { n: "GĐ 2", t: "Lát cắt đầu tiên", w: "~4 tuần", d: "Đăng nhập → duyệt → nhiệm vụ → cộng điểm → bảng xếp hạng" },
    { n: "GĐ 3", t: "Hoàn thiện", w: "6–8 tuần", d: "Instagram, chiến dịch, huy hiệu, quản trị, thông báo" },
    { n: "GĐ 4", t: "Thí điểm & mở rộng", w: "4 tuần +", d: "50–100 nhân viên, tinh chỉnh, triển khai toàn Tập đoàn" },
  ];
  const fw = (W - 2 * M - 4 * 0.25) / 5;
  const phaseFill = [T.navyPanel, T.navyBlock, T.blueMid, T.royal, T.redBlock];
  phases.forEach((p, i) => {
    const xx = M + i * (fw + 0.25);
    s.addText(p.n, { x: xx, y: 1.75, w: fw, h: 0.6, fill: { color: phaseFill[i] }, fontSize: 18, bold: true, color: T.white, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "Phase head " + i });
    card(s, xx, 2.5, fw, 3.0, "Phase card " + i);
    s.addText(p.t, { x: xx + 0.2, y: 2.65, w: fw - 0.4, h: 0.75, fontSize: 16, bold: true, color: T.heading, valign: "top", margin: 0, isTextBox: true, objectName: "Phase title " + i });
    s.addText(p.w, { x: xx + 0.2, y: 3.4, w: fw - 0.4, h: 0.4, fontSize: 14, bold: true, color: T.redHeadline, margin: 0, isTextBox: true, objectName: "Phase weeks " + i });
    s.addText(p.d, { x: xx + 0.2, y: 3.85, w: fw - 0.4, h: 1.5, fontSize: 14, color: T.ink, valign: "top", margin: 0, isTextBox: true, objectName: "Phase text " + i });
  });
  tag(s, "ĐƯỜNG GĂNG", M, 5.85, 1.9, 0.42);
  s.addText("Meta xét duyệt ứng dụng và xác minh doanh nghiệp — chạy song song từ GĐ 0, thường mất vài tuần.",
    { x: M + 2.1, y: 5.85, w: W - 2 * M - 2.1, h: 0.42, fontSize: 14, bold: true, color: T.navy, valign: "middle", margin: 0, isTextBox: true, objectName: "Critical path" });
  s.addText("(Thời gian là ước tính, sẽ chốt sau Giai đoạn 0)", { x: M, y: 6.5, w: 6, h: 0.3, fontSize: 10, italic: true, color: T.grayCaption, margin: 0, isTextBox: true, objectName: "Roadmap source" });
  s.addNotes("Lộ trình 5 giai đoạn, tổng cộng khoảng 4–5 tháng. Giai đoạn 1 là điểm kiểm soát: nếu kết nối Meta không ghi nhận được tương tác như kỳ vọng, chúng ta dừng lại và báo cáo trước khi tốn thêm chi phí. Đường găng là thủ tục xét duyệt ứng dụng của Meta, vì vậy cần bắt đầu ngay khi được phê duyệt.");

  // ===== 10. COMPLIANCE & RISK =====
  s = pres.addSlide({ masterName: "TB_CONTENT", sectionTitle: "Triển khai" });
  addTitle(s, "TUÂN THỦ & QUẢN TRỊ RỦI RO", "MINH BẠCH NGAY TỪ ĐẦU");
  const risks = [
    { t: "Chính sách Meta", i: "LuScale", d: "Không mua bán, trao đổi lượt thích hay chia sẻ. Thưởng cho sự tham gia đa dạng, không trả theo từng lượt; không bình luận theo kịch bản." },
    { t: "Dữ liệu cá nhân", i: "LuLock", d: "Tuân thủ Luật Bảo vệ dữ liệu cá nhân (hiệu lực 01/01/2026) và Nghị định 13/2023: xin đồng ý, lưu tối thiểu, cho phép ẩn khỏi bảng xếp hạng." },
    { t: "Tương tác thật", i: "LuShieldCheck", d: "Giới hạn điểm theo ngày, phát hiện bình luận trùng lặp, thu hồi điểm khi xoá bình luận, hàng chờ kiểm duyệt." },
    { t: "Giới hạn kỹ thuật", i: "LuAlertTriangle", d: "Meta không cho ứng dụng bên ngoài tương tác thay người dùng: nhân viên tương tác trên app Facebook/Instagram; lượt chia sẻ chưa xác minh tự động được." },
  ];
  for (let i = 0; i < 4; i++) {
    const xx = M + (i % 2) * (mw + 0.33), yy = 1.75 + Math.floor(i / 2) * 2.2;
    card(s, xx, yy, mw, 2.0, "Risk card " + i);
    await disc(s, xx + 0.3, yy + 0.3, 0.75, risks[i].i, i === 3 ? T.redSignal : T.ice, i === 3 ? T.white : T.navy, risks[i].t);
    s.addText(risks[i].t, { x: xx + 1.3, y: yy + 0.3, w: mw - 1.55, h: 0.45, fontSize: 18, bold: true, color: T.heading, margin: 0, isTextBox: true, objectName: "Risk title " + i });
    s.addText(risks[i].d, { x: xx + 1.3, y: yy + 0.8, w: mw - 1.55, h: 1.1, fontSize: 14, color: T.ink, valign: "top", margin: 0, isTextBox: true, objectName: "Risk text " + i });
  }
  s.addText("Pháp chế rà soát luật chơi, giải thưởng và nội dung đồng ý dữ liệu trước khi ra mắt.", { x: M, y: 6.3, w: 9, h: 0.35, fontSize: 12, italic: true, color: T.grayCaption, margin: 0, isTextBox: true, objectName: "Compliance note" });
  s.addNotes("Chúng tôi chủ động nêu rủi ro ngay từ đầu. Thứ nhất, chính sách Meta cấm mua bán lượt thích — nên giải thưởng dựa trên sự tham gia đều đặn, không trả theo lượt. Thứ hai, dữ liệu nhân viên tuân thủ Luật Bảo vệ dữ liệu cá nhân có hiệu lực từ 01/01/2026 và Nghị định 13. Thứ ba, có cơ chế chống tương tác ảo. Thứ tư, giới hạn kỹ thuật: nhân viên vẫn tương tác trong app Facebook/Instagram, và lượt chia sẻ hiện chưa thể xác minh tự động.");

  // ===== 11. BUDGET =====
  s = pres.addSlide({ masterName: "TB_CONTENT", sectionTitle: "Triển khai" });
  addTitle(s, "NGÂN SÁCH & NGUỒN LỰC", "CHI PHÍ VẬN HÀNH TINH GỌN");
  const hdr = (txt) => ({ text: txt, options: { bold: true, color: T.white, fill: { color: T.navy }, fontSize: 14, valign: "middle" } });
  const cell = (txt, o = {}) => ({ text: txt, options: { fontSize: 14, color: T.ink, valign: "middle", ...o } });
  const rows = [
    [hdr("HẠNG MỤC"), hdr("NỘI DUNG"), hdr("CHI PHÍ")],
    [cell("Hạ tầng", { bold: true, color: T.heading }), cell("Vercel (lưu trữ ứng dụng) + Neon (cơ sở dữ liệu), gói trả phí"), cell("Cần báo giá theo tháng", { italic: true, color: T.gray })],
    [cell("Kết nối Meta", { bold: true, color: T.heading }), cell("Graph API, webhook, xét duyệt ứng dụng"), cell("Không thu phí API")],
    [cell("Phát triển", { bold: true, color: T.heading }), cell("Đội AI agent (Claude Code + Orcasus), ước tính 115–130 triệu token"), cell("Quy đổi theo bảng giá khi phê duyệt", { italic: true, color: T.gray })],
    [cell("Quỹ giải thưởng", { bold: true, color: T.heading }), cell("Giải định kỳ theo quý cho cá nhân và phòng ban"), cell("Marcom đề xuất", { italic: true, color: T.gray })],
    [cell("Nhân sự nội bộ", { bold: true, color: T.heading }), cell("Marcom vận hành, HR duyệt tài khoản, Pháp chế rà soát"), cell("Thời gian nội bộ")],
  ];
  s.addTable(rows, { x: M, y: 1.75, w: W - 2 * M, colW: [2.4, 6.6, 2.833], rowH: 0.62, border: { type: "solid", pt: 0.75, color: T.ice },
    fill: { color: T.white }, margin: [4, 10, 4, 10], objectName: "Budget table" });
  s.addText("Chi phí cụ thể sẽ được Marcom bổ sung sau khi có báo giá và chốt quy mô thí điểm.",
    { x: M, y: 6.0, w: W - 2 * M, h: 0.5, fill: { color: T.ice }, fontSize: 14, bold: true, color: T.navy, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "Budget note" });
  s.addNotes("Cấu trúc chi phí gồm 5 hạng mục. Kết nối Meta không thu phí API. Hạ tầng Vercel và Neon cần báo giá gói trả phí. Phần phát triển do đội AI agent thực hiện theo quy trình Orcasus, ước tính 115–130 triệu token, sẽ quy đổi ra chi phí theo bảng giá tại thời điểm phê duyệt. Quỹ giải thưởng do Marcom đề xuất. Các con số cụ thể sẽ được bổ sung trước khi chốt.");

  // ===== 12. KPI & ASK =====
  s = pres.addSlide({ masterName: "TB_CONTENT", sectionTitle: "Triển khai" });
  addTitle(s, "KPI & ĐỀ XUẤT", "KÍNH TRÌNH HĐQT PHÊ DUYỆT");
  s.addText("KPI ĐO LƯỜNG THÍ ĐIỂM", { x: M, y: 1.75, w: 5.6, h: 0.45, fontSize: 16, bold: true, color: T.heading, margin: 0, isTextBox: true, objectName: "KPI head" });
  const kpis = [
    { t: "Tỉ lệ nhân viên hoạt động hằng tuần", i: "LuUsers" },
    { t: "Số tương tác đã xác minh mỗi tháng", i: "LuBadgeCheck" },
    { t: "Mức tăng lượt tiếp cận của fanpage", i: "LuTrendingUp" },
    { t: "Tỉ lệ tham gia các chiến dịch", i: "LuFlag" },
  ];
  for (let i = 0; i < 4; i++) {
    const yy = 2.35 + i * 0.85;
    await disc(s, M, yy, 0.6, kpis[i].i, T.ice, T.navy, kpis[i].t);
    s.addText(kpis[i].t, { x: M + 0.8, y: yy, w: 4.9, h: 0.6, fontSize: 15, bold: true, color: T.ink, valign: "middle", margin: 0, isTextBox: true, objectName: "KPI " + i });
  }
  s.addText("Chỉ tiêu cụ thể chốt sau GĐ 0, dựa trên số liệu nền hiện tại.", { x: M, y: 5.8, w: 5.6, h: 0.35, fontSize: 12, italic: true, color: T.grayCaption, margin: 0, isTextBox: true, objectName: "KPI note" });
  const ax = 6.9, aw = W - M - ax;
  s.addShape(pres.ShapeType.rect, { x: ax, y: 1.75, w: aw, h: 4.75, fill: { color: T.navyPanel }, line: { color: T.navyPanel, width: 0 }, objectName: "Ask panel" });
  s.addText("ĐỀ XUẤT PHÊ DUYỆT", { x: ax + 0.4, y: 1.95, w: aw - 0.8, h: 0.5, fontSize: 20, bold: true, color: T.white, margin: 0, isTextBox: true, objectName: "Ask head" });
  const asks = [
    "Thí điểm với 50–100 nhân viên tại 2 phòng ban",
    "Ngân sách hạ tầng, phát triển và quỹ giải thưởng",
    "Quyền quản trị Meta Business cho fanpage và Instagram",
    "Pháp chế và HR tham gia rà soát luật chơi, dữ liệu",
  ];
  asks.forEach((a, i) => {
    const yy = 2.65 + i * 0.92;
    s.addText(String(i + 1), { x: ax + 0.4, y: yy, w: 0.55, h: 0.55, fill: { color: T.redSignal }, fontSize: 18, bold: true, color: T.white, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "Ask num " + (i + 1) });
    s.addText(a, { x: ax + 1.15, y: yy - 0.05, w: aw - 1.5, h: 0.65, fontSize: 15, bold: true, color: T.white, valign: "middle", margin: 0, isTextBox: true, objectName: "Ask " + (i + 1) });
  });
  s.addNotes("Bốn KPI chính để đánh giá thí điểm: tỉ lệ nhân viên hoạt động hằng tuần, số tương tác đã xác minh, mức tăng tiếp cận của fanpage và tỉ lệ tham gia chiến dịch. Chỉ tiêu cụ thể sẽ chốt sau khi có số liệu nền. Marcom kính trình Hội đồng phê duyệt bốn nội dung: thí điểm, ngân sách, quyền quản trị Meta Business, và sự tham gia của Pháp chế cùng HR.");

  // ===== 13. THANK YOU =====
  s = pres.addSlide({ masterName: "TB_DIVIDER", sectionTitle: "Triển khai" });
  s.addText("CẢM ƠN!", { x: 6.6, y: 2.7, w: 6.0, h: 1.3, fontSize: 60, bold: true, color: T.white, align: "left", valign: "bottom", margin: 0, isTextBox: true, objectName: "Thank you" });
  s.addText("Cùng nhau, chúng ta tạo nên những giá trị bền vững.", { x: 6.6, y: 4.2, w: 5.8, h: 0.8, fontSize: 18, color: T.skyTint, margin: 0, valign: "top", isTextBox: true, objectName: "Closing line" });
  levelRing(s, 3.4, 3.9, 2.2, 0.07);
  s.addShape(pres.ShapeType.ellipse, { x: 3.4 - 1.85, y: 3.9 - 1.85, w: 3.7, h: 3.7, fill: { color: T.white }, line: { color: T.white, width: 0 }, objectName: "Closing disc" });
  s.addImage({ data: await icon("LuHeartHandshake", T.navy), x: 3.4 - 0.9, y: 3.9 - 0.9, w: 1.8, h: 1.8, altText: "Đồng hành", objectName: "Closing icon" });
  s.addNotes("Xin cảm ơn Hội đồng. Marcom sẵn sàng trả lời các câu hỏi và mong nhận được phê duyệt để bắt đầu Giai đoạn 0 ngay trong tháng này.");

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("wrote", OUT);
})().catch((e) => { console.error(e); process.exit(1); });
