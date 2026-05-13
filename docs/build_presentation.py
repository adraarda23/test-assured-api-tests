"""
Build presentation.pptx with a modern, visual layout that keeps text inside
slide bounds. Regenerate with:

    python3 docs/build_presentation.py
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE


# Palette — light theme with a single blue accent
TITLE     = RGBColor(0x0F, 0x17, 0x2A)
ACCENT    = RGBColor(0x25, 0x63, 0xEB)
ACCENT_BG = RGBColor(0xDB, 0xEA, 0xFE)
BODY      = RGBColor(0x33, 0x41, 0x55)
MUTED     = RGBColor(0x94, 0xA3, 0xB8)
CODE_BG   = RGBColor(0xF1, 0xF5, 0xF9)
BORDER    = RGBColor(0xE2, 0xE8, 0xF0)
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
W = prs.slide_width
H = prs.slide_height

FOOTER_TEXT = "Yapay Zeka Destekli Yazılım Test Mühendisliği  •  Arda Aydın Kılınç"


def _fill(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()


def _border(shape, color, width_pt=0.75):
    from pptx.util import Pt as _Pt
    shape.line.color.rgb = color
    shape.line.width = _Pt(width_pt)


def _set_text(tf, text, font_size, color, bold=False, align=None):
    p = tf.paragraphs[0]
    if align is not None:
        p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.size = font_size
    r.font.color.rgb = color
    r.font.bold = bold
    return r


def add_top_bar(slide):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, Inches(0.12))
    _fill(s, ACCENT)


def add_slide_number(slide, n, total):
    tb = slide.shapes.add_textbox(Inches(11.8), Inches(7.05), Inches(1.3), Inches(0.35))
    p = tb.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    r = p.add_run()
    r.text = f"{n} / {total}"
    r.font.size = Pt(10)
    r.font.color.rgb = MUTED


def add_footer(slide):
    tb = slide.shapes.add_textbox(Inches(0.5), Inches(7.05), Inches(10), Inches(0.35))
    p = tb.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = FOOTER_TEXT
    r.font.size = Pt(10)
    r.font.color.rgb = MUTED


def add_title(slide, text):
    tb = slide.shapes.add_textbox(Inches(0.7), Inches(0.45), Inches(12), Inches(0.85))
    tf = tb.text_frame
    tf.word_wrap = True
    _set_text(tf, text, Pt(30), TITLE, bold=True)
    u = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                               Inches(0.7), Inches(1.3), Inches(0.6), Inches(0.07))
    _fill(u, ACCENT)


def add_chrome(slide, n, total):
    add_top_bar(slide)
    add_slide_number(slide, n, total)
    add_footer(slide)


# ------- slide builders -------

def slide_title():
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.5), H)
    _fill(stripe, ACCENT)

    eyebrow = slide.shapes.add_textbox(Inches(1.2), Inches(1.7), Inches(11), Inches(0.4))
    _set_text(eyebrow.text_frame, "SUNUM", Pt(13), ACCENT, bold=True)

    title = slide.shapes.add_textbox(Inches(1.2), Inches(2.2), Inches(11), Inches(2.6))
    tf = title.text_frame
    tf.word_wrap = True
    _set_text(tf, "Yapay Zeka Destekli\nYazılım Test Mühendisliği", Pt(44), TITLE, bold=True)

    sub = slide.shapes.add_textbox(Inches(1.2), Inches(4.9), Inches(11), Inches(0.5))
    _set_text(sub.text_frame, "REST Assured ile servis regresyon testi otomasyonu",
              Pt(18), BODY)

    sub2 = slide.shapes.add_textbox(Inches(1.2), Inches(5.5), Inches(11), Inches(0.5))
    _set_text(sub2.text_frame, "Demo projesi: Tasks API + REST Assured test paketi",
              Pt(14), MUTED)

    author = slide.shapes.add_textbox(Inches(1.2), Inches(6.6), Inches(11), Inches(0.4))
    _set_text(author.text_frame, "Arda Aydın Kılınç", Pt(13), MUTED)


def slide_agenda(n, total):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_chrome(slide, n, total)
    add_title(slide, "Gündem")

    items = [
        "Yazılım test mühendisliği — neden var",
        "Test piramidi ve REST Assured",
        "Yapay zeka destekli test mühendisliği",
        "Projeyi AI ile nasıl geliştirdim",
        "Demo: Tasks API + REST Assured",
        "Avantajlar, riskler, pratik öneriler",
    ]

    col_w = Inches(5.8)
    row_h = Inches(0.7)
    start_top = Inches(1.85)
    for i, item in enumerate(items):
        col = i % 2
        row = i // 2
        left = Inches(0.7) + col * Inches(6.2)
        top = start_top + row * row_h * 1.05

        # number badge
        badge = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, Inches(0.45), Inches(0.45))
        _fill(badge, ACCENT_BG)
        btf = badge.text_frame
        btf.margin_top = btf.margin_bottom = 0
        btf.margin_left = btf.margin_right = 0
        bp = btf.paragraphs[0]
        bp.alignment = PP_ALIGN.CENTER
        br = bp.add_run()
        br.text = str(i + 1)
        br.font.size = Pt(14)
        br.font.bold = True
        br.font.color.rgb = ACCENT

        tb = slide.shapes.add_textbox(left + Inches(0.65), top + Inches(0.05),
                                      col_w - Inches(0.5), Inches(0.5))
        _set_text(tb.text_frame, item, Pt(16), BODY)


def slide_what_is_te(n, total):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_chrome(slide, n, total)
    add_title(slide, "Yazılım test mühendisliği nedir?")

    lead = slide.shapes.add_textbox(Inches(0.7), Inches(1.7), Inches(12), Inches(1.1))
    tf = lead.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = '"Bir yazılımın doğru çalıştığını ve çalışmaya devam ettiğini sistematik olarak kanıtlamak."'
    r.font.size = Pt(22)
    r.font.italic = True
    r.font.color.rgb = TITLE

    pillars = [
        ("Doğruluk", "Beklenen davranışı yapıyor mu?"),
        ("Sağlamlık", "Hatalı veri veya yük altında nasıl davranır?"),
        ("Regresyon", "Yeni değişiklik eski özellikleri bozdu mu?"),
    ]
    box_w = Inches(3.95)
    box_h = Inches(2.6)
    gap = Inches(0.2)
    total_w = box_w * 3 + gap * 2
    left0 = (W - total_w) / 2
    top = Inches(3.6)
    for i, (label, desc) in enumerate(pillars):
        left = left0 + (box_w + gap) * i
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, box_w, box_h)
        _fill(card, WHITE)
        _border(card, BORDER, 1)

        accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                        left + Inches(0.3), top + Inches(0.5),
                                        Inches(0.35), Inches(0.07))
        _fill(accent, ACCENT)

        tb_label = slide.shapes.add_textbox(left + Inches(0.3), top + Inches(0.7),
                                            box_w - Inches(0.6), Inches(0.6))
        _set_text(tb_label.text_frame, label, Pt(20), TITLE, bold=True)

        tb_desc = slide.shapes.add_textbox(left + Inches(0.3), top + Inches(1.3),
                                           box_w - Inches(0.6), Inches(1.1))
        tdf = tb_desc.text_frame
        tdf.word_wrap = True
        _set_text(tdf, desc, Pt(15), BODY)


def slide_pyramid(n, total):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_chrome(slide, n, total)
    add_title(slide, "Test piramidi")

    # Pyramid on the left
    tiers = [
        ("E2E",        Inches(1.4), Inches(0.7), "az,  yavaş,  kırılgan"),
        ("Integration", Inches(2.8), Inches(1.0), "orta sayı,  orta hız"),
        ("Unit",       Inches(4.2), Inches(1.3), "çok,  hızlı,  ucuz"),
    ]
    pyramid_top = Inches(2.0)
    pyramid_left = Inches(1.2)
    cur_top = pyramid_top
    colors = [
        RGBColor(0xBF, 0xDB, 0xFE),  # blue-200
        RGBColor(0x60, 0xA5, 0xFA),  # blue-400
        RGBColor(0x25, 0x63, 0xEB),  # blue-600
    ]
    for (label, tw, th, _), col in zip(tiers, colors):
        block = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                       pyramid_left + (Inches(4.2) - tw) / 2,
                                       cur_top, tw, th)
        _fill(block, col)
        tb = slide.shapes.add_textbox(pyramid_left, cur_top, Inches(4.2), th)
        tf = tb.text_frame
        tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        # vertical center via spacer
        for _ in range(0):
            p = tf.add_paragraph()
        r = tf.paragraphs[0].add_run()
        r.text = label
        r.font.size = Pt(18)
        r.font.bold = True
        r.font.color.rgb = WHITE if col == colors[-1] else TITLE
        cur_top += th + Inches(0.05)

    # Right side: short rules + this project's numbers
    rules_tb = slide.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.8), Inches(1.0))
    tf = rules_tb.text_frame
    tf.word_wrap = True
    _set_text(tf, "Pratik kural", Pt(13), ACCENT, bold=True)
    p2 = tf.add_paragraph()
    r = p2.add_run()
    r.text = "Çok unit, makul integration, az E2E."
    r.font.size = Pt(20)
    r.font.color.rgb = TITLE
    r.font.bold = True

    # Stat cards
    stats = [("24", "unit test"), ("12", "integration test"), ("36", "toplam")]
    sw = Inches(1.75)
    sh = Inches(1.7)
    gap = Inches(0.15)
    start_left = Inches(7.0)
    top_s = Inches(3.6)
    for i, (num, label) in enumerate(stats):
        left = start_left + (sw + gap) * i
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top_s, sw, sh)
        _fill(card, ACCENT_BG)
        _border(card, BORDER, 1)

        ntb = slide.shapes.add_textbox(left, top_s + Inches(0.25), sw, Inches(0.9))
        tf = ntb.text_frame
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = num
        r.font.size = Pt(38)
        r.font.bold = True
        r.font.color.rgb = ACCENT

        ltb = slide.shapes.add_textbox(left, top_s + Inches(1.1), sw, Inches(0.5))
        tf = ltb.text_frame
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = label
        r.font.size = Pt(13)
        r.font.color.rgb = BODY

    caption = slide.shapes.add_textbox(Inches(7.0), Inches(5.5), Inches(5.8), Inches(0.5))
    _set_text(caption.text_frame,
              "Bu projede testlerin dağılımı",
              Pt(12), MUTED)


def slide_rest_assured(n, total):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_chrome(slide, n, total)
    add_title(slide, "REST Assured neden?")

    lead = slide.shapes.add_textbox(Inches(0.7), Inches(1.65), Inches(12), Inches(0.6))
    _set_text(lead.text_frame,
              "Java'da HTTP API'leri test etmek için en yaygın kütüphane. "
              "Üç kontrol tek bir akıcı zincirde:", Pt(16), BODY)

    # Code block
    code_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                      Inches(0.7), Inches(2.4),
                                      Inches(8.0), Inches(3.6))
    _fill(code_box, CODE_BG)
    _border(code_box, BORDER, 1)

    code_tb = slide.shapes.add_textbox(Inches(0.95), Inches(2.6),
                                       Inches(7.5), Inches(3.3))
    tf = code_tb.text_frame
    tf.word_wrap = True
    lines = [
        "given()",
        "    .body(Map.of(\"title\", \"Buy milk\"))",
        ".when()",
        "    .post(\"/tasks\")",
        ".then()",
        "    .statusCode(201)",
        "    .body(\"title\", equalTo(\"Buy milk\"))",
        "    .time(lessThan(2000L));",
    ]
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r = p.add_run()
        r.text = line
        r.font.name = "Menlo"
        r.font.size = Pt(14)
        r.font.color.rgb = TITLE
        p.space_after = Pt(2)

    # Three checks
    checks = [
        ("Status code",   ".statusCode(201)"),
        ("Response body", ".body(\"title\", equalTo(...))"),
        ("Süre (SLA)",     ".time(lessThan(2000L))"),
    ]
    top0 = Inches(2.4)
    box_h = Inches(1.1)
    for i, (label, snippet) in enumerate(checks):
        top = top0 + i * (box_h + Inches(0.1))
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                      Inches(9.0), top, Inches(3.8), box_h)
        _fill(card, WHITE)
        _border(card, BORDER, 1)

        accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                        Inches(9.0), top, Inches(0.08), box_h)
        _fill(accent, ACCENT)

        ltb = slide.shapes.add_textbox(Inches(9.2), top + Inches(0.12),
                                       Inches(3.55), Inches(0.45))
        _set_text(ltb.text_frame, label, Pt(15), TITLE, bold=True)

        stb = slide.shapes.add_textbox(Inches(9.2), top + Inches(0.55),
                                       Inches(3.55), Inches(0.45))
        sr = _set_text(stb.text_frame, snippet, Pt(11), BODY)
        sr.font.name = "Menlo"


def slide_ai_landscape(n, total):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_chrome(slide, n, total)
    add_title(slide, "Yapay zeka destekli test mühendisliği")

    lead = slide.shapes.add_textbox(Inches(0.7), Inches(1.65), Inches(12), Inches(0.6))
    _set_text(lead.text_frame,
              "LLM tabanlı asistanlar (Claude, Copilot, Cursor) ile süreç iki yönlü:",
              Pt(16), BODY)

    rows = [
        ("Test yazımı",   "İnsan yazar",           "İnsan + asistan birlikte yazar"),
        ("Kapsam",        "Akla gelen senaryo",    "AI eksik kenar durumu hatırlatır"),
        ("Hata triyajı",  "Stack trace okunur",    "AI özetler ve düzeltme önerir"),
        ("Doküman",       "Manuel yazılır",        "Asistan özet/rapor üretir"),
    ]
    col_label_w = Inches(2.4)
    col_w = Inches(4.8)
    left = Inches(0.7)
    top = Inches(2.5)
    header_h = Inches(0.5)
    row_h = Inches(0.85)

    headers = [(left, "Konu", TITLE),
               (left + col_label_w, "Klasik", BODY),
               (left + col_label_w + col_w, "+ AI", ACCENT)]
    for hx, hlabel, hcolor in headers:
        tb = slide.shapes.add_textbox(hx + Inches(0.2), top, col_w, header_h)
        _set_text(tb.text_frame, hlabel, Pt(14), hcolor, bold=True)

    top += header_h
    for i, (lbl, classic, ai) in enumerate(rows):
        row_top = top + i * row_h
        if i % 2 == 0:
            bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, row_top,
                                        col_label_w + col_w * 2, row_h)
            _fill(bg, CODE_BG)
        tb1 = slide.shapes.add_textbox(left + Inches(0.2),
                                       row_top + Inches(0.18),
                                       col_label_w - Inches(0.2), row_h)
        _set_text(tb1.text_frame, lbl, Pt(14), TITLE, bold=True)

        tb2 = slide.shapes.add_textbox(left + col_label_w + Inches(0.2),
                                       row_top + Inches(0.18),
                                       col_w - Inches(0.2), row_h)
        _set_text(tb2.text_frame, classic, Pt(13), BODY)

        tb3 = slide.shapes.add_textbox(left + col_label_w + col_w + Inches(0.2),
                                       row_top + Inches(0.18),
                                       col_w - Inches(0.4), row_h)
        _set_text(tb3.text_frame, ai, Pt(13), TITLE)

    callout = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                     Inches(0.7), Inches(6.4), Inches(12), Inches(0.55))
    _fill(callout, ACCENT_BG)
    ctb = slide.shapes.add_textbox(Inches(0.9), Inches(6.47), Inches(11.6), Inches(0.45))
    _set_text(ctb.text_frame,
              "AI test mühendisini değiştirmiyor — karar merci hâlâ insan.",
              Pt(14), TITLE, bold=True)


def _numbered_grid(slide, items, top0=Inches(1.7), available_h=Inches(5.2),
                   cols=2):
    """Render a numbered list as a grid of cards inside given area."""
    rows = (len(items) + cols - 1) // cols
    gap_x = Inches(0.25)
    gap_y = Inches(0.2)
    col_w = (Inches(12) - gap_x * (cols - 1)) / cols
    row_h = (available_h - gap_y * (rows - 1)) / rows

    for i, item in enumerate(items):
        row = i // cols
        col = i % cols
        left = Inches(0.7) + col * (col_w + gap_x)
        top = top0 + row * (row_h + gap_y)

        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                      left, top, col_w, row_h)
        _fill(card, WHITE)
        _border(card, BORDER, 0.75)

        # Number badge
        badge = slide.shapes.add_shape(MSO_SHAPE.OVAL,
                                       left + Inches(0.25),
                                       top + Inches(0.25),
                                       Inches(0.5), Inches(0.5))
        _fill(badge, ACCENT)
        btf = badge.text_frame
        btf.margin_top = btf.margin_bottom = 0
        btf.margin_left = btf.margin_right = 0
        bp = btf.paragraphs[0]
        bp.alignment = PP_ALIGN.CENTER
        br = bp.add_run()
        br.text = str(i + 1)
        br.font.size = Pt(14)
        br.font.bold = True
        br.font.color.rgb = WHITE

        if isinstance(item, tuple):
            label, desc = item
        else:
            label, desc = item, None

        ltb = slide.shapes.add_textbox(left + Inches(0.95),
                                       top + Inches(0.25),
                                       col_w - Inches(1.2), Inches(0.55))
        _set_text(ltb.text_frame, label, Pt(15), TITLE, bold=True)

        if desc:
            dtb = slide.shapes.add_textbox(left + Inches(0.95),
                                           top + Inches(0.85),
                                           col_w - Inches(1.2),
                                           row_h - Inches(1.0))
            tf = dtb.text_frame
            tf.word_wrap = True
            _set_text(tf, desc, Pt(12), BODY)


def slide_ai_roles(n, total):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_chrome(slide, n, total)
    add_title(slide, "AI'nın test yaşam döngüsündeki rolleri")

    items = [
        ("Test üretimi",       "Pozitif ve negatif senaryoları otomatik üretmek."),
        ("Test oracle",         "\"Bu çıktı doğru mu?\" kararını destekleyen bilgi tabanı."),
        ("Bakım",               "Üretim kodu değişince bozulan testleri güncelleme, flakiness analizi."),
        ("Hata triyajı",        "Stack trace'ten kök neden hipotezi, log korelasyonu."),
        ("Doğal dilden senaryo", "\"Stok azalmalı\" → çalıştırılabilir test koduna dönüştürmek."),
        ("İnsan denetimi",      "Her kullanım insan kontrolünde değer üretir."),
    ]
    _numbered_grid(slide, items, top0=Inches(1.75), available_h=Inches(5.1), cols=2)


def slide_how_built(n, total):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_chrome(slide, n, total)
    add_title(slide, "Bu projeyi AI ile nasıl geliştirdim")

    items = [
        ("Plan",         "PDF gereksinimi asistana verildi → 4 aşamalı plan üretildi."),
        ("Mikro commit", "Her aşama küçük commit'lere bölündü (toplam 30+ commit)."),
        ("İnsan kararı", "Modül yapısı, test konumu, refactor kararları sahibinde."),
        ("Sürekli yeşil", "Her adımda `mvn verify` ile regresyon korundu."),
    ]
    _numbered_grid(slide, items, top0=Inches(1.85), available_h=Inches(5.0), cols=2)


def slide_demo(n, total):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_chrome(slide, n, total)
    add_title(slide, "Demo akışı")

    steps = [
        "git log --oneline  — küçük, okunabilir commit geçmişi",
        "mvn -pl api spring-boot:run  — API'yi ayağa kaldır",
        "curl /api/tasks  — endpoint'leri canlı göster",
        "CreateTaskIT.java  — bir REST Assured testini incele",
        "mvn verify  — tüm test paketini koştur",
        "IntelliJ test ağacı  — pas/fail/süre dağılımı",
        "GitHub Actions  — CI yeşil rozeti",
    ]
    tb = slide.shapes.add_textbox(Inches(0.7), Inches(1.85), Inches(12), Inches(5.0))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, step in enumerate(steps):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r0 = p.add_run()
        r0.text = f"{i+1}.  "
        r0.font.size = Pt(18)
        r0.font.bold = True
        r0.font.color.rgb = ACCENT
        r1 = p.add_run()
        r1.text = step
        r1.font.size = Pt(18)
        r1.font.color.rgb = BODY
        p.space_after = Pt(10)


def _two_columns(slide, left_title, left_items, right_title, right_items,
                 left_color=ACCENT, right_color=RGBColor(0xDC, 0x26, 0x26)):
    col_top = Inches(1.85)
    col_h = Inches(5.0)
    col_w = Inches(5.95)
    gap = Inches(0.2)
    left = Inches(0.7)

    # left card
    lc = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                left, col_top, col_w, col_h)
    _fill(lc, WHITE)
    _border(lc, BORDER, 1)
    lh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                left, col_top, col_w, Inches(0.55))
    _fill(lh, left_color)
    lht = slide.shapes.add_textbox(left + Inches(0.3), col_top + Inches(0.1),
                                   col_w - Inches(0.6), Inches(0.4))
    _set_text(lht.text_frame, left_title, Pt(15), WHITE, bold=True)

    rb = slide.shapes.add_textbox(left + Inches(0.35),
                                  col_top + Inches(0.75),
                                  col_w - Inches(0.7),
                                  col_h - Inches(1.0))
    tf = rb.text_frame
    tf.word_wrap = True
    for i, item in enumerate(left_items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "•  "
        r1.font.size = Pt(15)
        r1.font.bold = True
        r1.font.color.rgb = left_color
        if isinstance(item, tuple):
            label, desc = item
            r2 = p.add_run()
            r2.text = label
            r2.font.size = Pt(15)
            r2.font.bold = True
            r2.font.color.rgb = TITLE
            r3 = p.add_run()
            r3.text = " — " + desc
            r3.font.size = Pt(15)
            r3.font.color.rgb = BODY
        else:
            r2 = p.add_run()
            r2.text = item
            r2.font.size = Pt(15)
            r2.font.color.rgb = BODY
        p.space_after = Pt(8)

    # right card
    right_left = left + col_w + gap
    rc = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                right_left, col_top, col_w, col_h)
    _fill(rc, WHITE)
    _border(rc, BORDER, 1)
    rh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                right_left, col_top, col_w, Inches(0.55))
    _fill(rh, right_color)
    rht = slide.shapes.add_textbox(right_left + Inches(0.3),
                                   col_top + Inches(0.1),
                                   col_w - Inches(0.6), Inches(0.4))
    _set_text(rht.text_frame, right_title, Pt(15), WHITE, bold=True)

    rbb = slide.shapes.add_textbox(right_left + Inches(0.35),
                                   col_top + Inches(0.75),
                                   col_w - Inches(0.7),
                                   col_h - Inches(1.0))
    tf = rbb.text_frame
    tf.word_wrap = True
    for i, item in enumerate(right_items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "•  "
        r1.font.size = Pt(15)
        r1.font.bold = True
        r1.font.color.rgb = right_color
        if isinstance(item, tuple):
            label, desc = item
            r2 = p.add_run()
            r2.text = label
            r2.font.size = Pt(15)
            r2.font.bold = True
            r2.font.color.rgb = TITLE
            r3 = p.add_run()
            r3.text = " — " + desc
            r3.font.size = Pt(15)
            r3.font.color.rgb = BODY
        else:
            r2 = p.add_run()
            r2.text = item
            r2.font.size = Pt(15)
            r2.font.color.rgb = BODY
        p.space_after = Pt(8)


def slide_pros_cons(n, total):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_chrome(slide, n, total)
    add_title(slide, "Avantajlar ve riskler")

    pros = [
        ("Hız",        "Boilerplate dakikalar içinde."),
        ("Kapsam",     "Negatif senaryolar doğal olarak ekleniyor."),
        ("Tutarlılık", "Tüm testlerde aynı patern."),
        ("Geri besleme", "Hata mesajından kök neden dakikalar içinde."),
    ]
    cons = [
        ("Halüsinasyon", "Uydurma metot/parametre olabilir."),
        ("Yanlış güven", "\"AI yazdı, doğrudur\" tuzağı."),
        ("Çift yanlış",  "Hem üretim hem test AI ise korelasyon riski."),
        ("Gizlilik",     "Şirket içi koda LLM erişimi politikaya tabi."),
    ]
    _two_columns(slide,
                 "Avantajlar", pros,
                 "Riskler",    cons,
                 left_color=RGBColor(0x16, 0xA3, 0x4A),
                 right_color=RGBColor(0xDC, 0x26, 0x26))


def slide_recommendations(n, total):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_chrome(slide, n, total)
    add_title(slide, "Pratik öneriler")

    items = [
        ("Code reviewer gibi düşün", "Kabul/ret kararı sende."),
        ("Mikro adımlarla ilerle",   "Her commit'te test koş."),
        ("Test ismini insan yazsın", "Ne kanıtladığını sen bilirsin."),
        ("Negatifleri açıkça iste",  "404, 400, boş input için de test."),
        ("Refactor'ı AI'a yaptır",   "Boilerplate temizliğinde çok iyi."),
        ("CI'a güven, lokale değil", "Temiz makine sonuçları belirler."),
    ]
    _numbered_grid(slide, items, top0=Inches(1.85), available_h=Inches(5.0), cols=2)


def slide_outro(n, total):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_chrome(slide, n, total)
    add_title(slide, "Sonuç")

    bullets = [
        "Test mühendisliği = yazılımı güvenle değiştirebilmenin disiplini.",
        "REST Assured + JUnit + Maven, JVM tarafının defacto stack'i.",
        "AI mühendisin hızını ve kapsamını büyütür — yargısını değil.",
        "Bu proje 4 aşamada, mikro commit'lerle, AI eş geliştirmesiyle üretildi.",
    ]
    tb = slide.shapes.add_textbox(Inches(0.7), Inches(1.85), Inches(12), Inches(2.8))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, b in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "•  "
        r1.font.size = Pt(17)
        r1.font.bold = True
        r1.font.color.rgb = ACCENT
        r2 = p.add_run()
        r2.text = b
        r2.font.size = Pt(17)
        r2.font.color.rgb = BODY
        p.space_after = Pt(10)

    # Repo chip
    chip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                  Inches(0.7), Inches(5.0),
                                  Inches(12), Inches(0.9))
    _fill(chip, ACCENT_BG)
    ct = slide.shapes.add_textbox(Inches(1.0), Inches(5.15),
                                  Inches(11.5), Inches(0.6))
    tf = ct.text_frame
    p = tf.paragraphs[0]
    r1 = p.add_run()
    r1.text = "Repo:  "
    r1.font.size = Pt(16)
    r1.font.color.rgb = TITLE
    r1.font.bold = True
    r2 = p.add_run()
    r2.text = "github.com/adraarda23/test-assured-api-tests"
    r2.font.size = Pt(16)
    r2.font.color.rgb = ACCENT
    r2.font.name = "Menlo"

    # "Sorular?"
    qa = slide.shapes.add_textbox(Inches(0.7), Inches(6.15), Inches(12), Inches(0.6))
    tf = qa.text_frame
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "Sorular?"
    r.font.size = Pt(22)
    r.font.bold = True
    r.font.color.rgb = TITLE


# ------- compose -------

TOTAL = 12

slide_title()
slide_agenda(2, TOTAL)
slide_what_is_te(3, TOTAL)
slide_pyramid(4, TOTAL)
slide_rest_assured(5, TOTAL)
slide_ai_landscape(6, TOTAL)
slide_ai_roles(7, TOTAL)
slide_how_built(8, TOTAL)
slide_demo(9, TOTAL)
slide_pros_cons(10, TOTAL)
slide_recommendations(11, TOTAL)
slide_outro(12, TOTAL)

import os
out = os.path.join(os.path.dirname(__file__), "presentation.pptx")
prs.save(out)
print(f"wrote {out} ({len(prs.slides)} slides)")
