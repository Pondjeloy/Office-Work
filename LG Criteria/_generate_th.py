# -*- coding: utf-8 -*-
"""Thai LG Criteria slides, Update 2026.10.01, same 780x540 deck as the English file."""
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle, KeepInFrame

ROOT = Path(r"D:\LG Criteria")
ASSETS = ROOT / "_assets"
OUT_PDF = ROOT / "LG Criteria Update 01-10-2026.pdf"
PAGES = ROOT / "pages-th"
FONT_DIR = Path(r"C:\Windows\Fonts")

PAGE_W, PAGE_H = 780, 540
TITLE = HexColor("#4A4A4A")
BODY = HexColor("#222222")
MUTED = HexColor("#6B6B6B")
TH_BG = HexColor("#E8E8E8")
ROW_ALT = HexColor("#F6F6F6")
LINE = HexColor("#2B2B2B")
BANNER = HexColor("#C8102E")
SOFT = HexColor("#FFF6F0")
GRID = HexColor("#BDBDBD")

pdfmetrics.registerFont(TTFont("LG", str(FONT_DIR / "LG_Smart_UI-Regular.ttf")))
pdfmetrics.registerFont(TTFont("LG-SB", str(FONT_DIR / "LG_Smart_UI-SemiBold.ttf")))
pdfmetrics.registerFont(TTFont("TH", str(FONT_DIR / "leelawad.ttf")))
pdfmetrics.registerFont(TTFont("THB", str(FONT_DIR / "leelawdb.ttf")))
pdfmetrics.registerFontFamily("TH", normal="TH", bold="THB", italic="TH", boldItalic="THB")

AR = (
    "ตรวจสอบ AR (การค้างชำระ)<br/>"
    "• ลูกค้าเดิม: ไม่มีการค้างชำระ<br/>"
    "• เคยค้าง Overdue <b>2–3</b> ครั้ง: ดูประวัติ <b>6 เดือน</b>ล่าสุด<br/>"
    "• เคยค้าง Overdue <b>4</b> ครั้ง: ดูประวัติ <b>12 เดือน</b>ล่าสุด<br/>"
    "ต้องชำระดีต่อเนื่องตลอดช่วงที่ตรวจ"
)
PHONE = (
    "ต้องเป็นของผู้เช่าซื้อเท่านั้น<br/>"
    "ห้ามใช้เบอร์คนในครอบครัวทุกกรณี<br/>"
    "(ถ้าใช้แล้วถูกร้องเรียน ปรับสูงสุด <b>100,000</b> บาท ผิด PDPA)"
)


def S(name, font="TH", size=8, leading=None, color=BODY, align=TA_LEFT, **kw):
    return ParagraphStyle(
        name, fontName=font, fontSize=size,
        leading=leading if leading is not None else size + 2.6,
        textColor=color, alignment=align, **kw,
    )


ST_TH = S("th", "THB", 9, 12, TITLE, TA_CENTER)
ST_NO = S("no", "TH", 8.4, 11, BODY, TA_CENTER)
ST_ITEM = S("item", "THB", 8.4, 11, BODY)
ST_CELL = S("cell", "TH", 8.2, 10.8, BODY)
ST_BULLET = S("bullet", "TH", 11, 15.2, BODY, leftIndent=14, firstLineIndent=-12)
ST_BODY = S("body", "TH", 10.2, 14.2, BODY)
ST_BODY_SM = S("bodysm", "TH", 9.2, 12.6, BODY)
ST_BANNER = S("banner", "THB", 14, 18, white)
ST_EX = S("ex", "TH", 9.4, 12.8, BODY)


def P(html, style=ST_CELL):
    return Paragraph(html, style)


def draw_header(c, title):
    logo = ASSETS / "Image12_t.png"
    c.drawImage(str(logo), PAGE_W - 118, PAGE_H - 42, width=86, height=38, mask="auto", preserveAspectRatio=True, anchor="c")
    c.setFillColor(TITLE)
    c.setFont("THB", 18)
    c.drawString(28, PAGE_H - 36, title)
    c.setStrokeColor(LINE)
    c.setLineWidth(1.1)
    c.line(28, PAGE_H - 50, PAGE_W - 28, PAGE_H - 50)
    c.setFillColor(MUTED)
    c.setFont("TH", 8)
    c.drawString(28, 12, "ใช้ภายในเท่านั้น  |  LGETH  |  Update 2026.10.01")
    c.drawRightString(PAGE_W - 28, 12, "TH")


def place_flowable(c, flowable, x, y_top, width, height):
    boxed = KeepInFrame(width, height, [flowable], mode="shrink", hAlign="LEFT", vAlign="TOP")
    w, h = boxed.wrapOn(c, width, height)
    scale = getattr(boxed, "_scale", 1) or 1
    if scale < 0.98:
        print(f"  shrink {scale:.2f} at y_top={y_top:.0f}")
    boxed.drawOn(c, x, y_top - h)
    return h


def criteria_table(rows, col_widths):
    data = [[P("No", ST_TH), P("รายการ", ST_TH), P("เกณฑ์", ST_TH)]]
    for no, item, crit in rows:
        data.append([P(str(no), ST_NO), P(item, ST_ITEM), P(crit, ST_CELL)])
    tbl = Table(data, colWidths=col_widths)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), TH_BG),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, GRID),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
        ("ALIGN", (0, 1), (0, -1), "CENTER"),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            cmds.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
    tbl.setStyle(TableStyle(cmds))
    return tbl


def two_col(rows, widths, header=("รายการ", "เกณฑ์")):
    data = [[P(header[0], ST_TH), P(header[1], ST_TH)]]
    for a, b in rows:
        data.append([
            a if isinstance(a, Paragraph) else P(a, ST_ITEM),
            b if isinstance(b, Paragraph) else P(b, ST_CELL),
        ])
    tbl = Table(data, colWidths=widths)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), TH_BG),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, GRID),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    tbl.setStyle(TableStyle(cmds))
    return tbl


def cover(c):
    c.setFillColor(white)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.drawImage(str(ASSETS / "Image8_t.png"), 0, PAGE_H - 210, width=72, height=210, mask="auto", preserveAspectRatio=True, anchor="nw")
    c.drawImage(str(ASSETS / "Image10_t.png"), PAGE_W - 210, 0, width=210, height=208, mask="auto", preserveAspectRatio=True, anchor="sw")
    c.drawImage(str(ASSETS / "Image12_t.png"), PAGE_W - 168, 92, width=108, height=48, mask="auto", preserveAspectRatio=True)
    c.setFillColor(TITLE)
    c.setFont("LG-SB", 26)
    c.drawString(88, 330, "LG Electronics Thailand CCP Regulation")
    c.drawString(88, 294, "Credit Control Policy")
    c.setFillColor(MUTED)
    c.setFont("LG", 12)
    c.drawString(88, 78, "LGETH  |  Update 2026. 10. 01")


def page_hours(c):
    draw_header(c, "เวลาทำการ การตรวจสอบใบสมัคร")
    bullets = [
        "พิจารณาและอนุมัติภายใน <b>1 วัน</b> (Credit และ Non-Credit)",
        "เวลาทำการ <b>08:30 – 17:30 น.</b> ทุกวัน",
        "ถ้าต้องส่งเอกสารเพิ่ม ให้ส่งภายใน <b>15 วัน</b> นับจากวันที่ Credit On Hold<br/>ติดตามเอกสารทางอีเมล และโทรติดตาม LP / LSM / LGM",
        "หลังส่งเอกสารแล้ว พิจารณาและอนุมัติภายใน <b>1 วัน</b><br/><b>ถ้าเกิน 1 วันยังไม่ทราบผล ให้ติดตามทาง Group Line หรืออีเมล</b>",
    ]
    y = PAGE_H - 72
    for html in bullets:
        p = P("-  " + html, ST_BULLET)
        w, h = p.wrap(PAGE_W - 70, 80)
        p.drawOn(c, 36, y - h)
        y -= h + 8
    y -= 4
    c.setStrokeColor(HexColor("#D0D0D0"))
    c.setDash(1, 2)
    c.line(40, y, PAGE_W - 40, y)
    c.setDash()
    y -= 22
    c.setFillColor(TITLE)
    c.setFont("THB", 13)
    c.drawString(40, y, "การพิจารณาเคส Memo")
    y -= 8
    for html in [
        "พิจารณาภายใน <b>1 วันทำการ</b> นับจากวันที่ Credit Control ได้รับ (ขึ้นกับผู้อนุมัติลำดับถัดไป)",
        "ถ้าเอกสารไม่พอ จะ Request for Check ไป DST",
        "ไม่รับพิจารณาอาชีพ: พระ, แม่ชี, นักบวช, นักเรียน-นักศึกษา และอาชีพที่ไม่มีรายได้ (Credit Card, Non-Credit, ต่างชาติ)",
    ]:
        p = P("-  " + html, ST_BULLET)
        w, h = p.wrap(PAGE_W - 70, 70)
        p.drawOn(c, 36, y - h)
        y -= h + 6


def page_credit_card(c):
    draw_header(c, "ประเภท : Credit Card")
    rows = [
        ("1", "สัญชาติ", "ไทย"),
        ("2", "อายุ", "20–70 ปีบริบูรณ์ นับวันชนวัน"),
        ("3", "ที่อยู่ในการติดตั้ง", "1. ที่อยู่ตามบัตรประชาชน<br/>2. ที่อยู่อาศัยปัจจุบัน<br/>3. ที่อยู่ปัจจุบันอื่น (ต้องแนบเอกสารเพิ่ม)"),
        ("4", "เบอร์มือถือ / อีเมล<br/>(ของผู้ซื้อ)", PHONE),
        ("5", "วิธีชำระเงิน<br/>(บัตรเครดิต)",
         "บัตรเหลืออายุอย่างน้อย <b>3 เดือน</b><br/>บัตรจริงหรือรูปออนไลน์ที่เห็นชื่อ นามสกุล เลขบัตร และวันหมดอายุชัด<br/>• ออกโดยสถาบันการเงินในประเทศไทยเท่านั้น<br/>• ต้องเป็นใบเดียวกับที่ตัด 1st Payment<br/>ไม่รับ Shopee, TrueMoney, บัตรกดเงินสด"),
        ("6", "บัตรประชาชน",
         "• ตัวจริงหรือสำเนารับรองถูกต้อง เหมือน OSMS<br/>• ไม่รับ e-ID ทุกกรณี<br/>• ต้องเห็นข้อมูลครบ ชัด ไม่มีแสงสะท้อน"),
        ("7", "สำเนาเปลี่ยนชื่อ<br/>(ถ้ามี)", "เมื่อชื่อหรือนามสกุลบนบัตรเครดิตไม่ตรง"),
        ("8", "เอกสารเพิ่มเติม",
         "ขอเพิ่มเมื่อ:<br/>• บัตรเห็นข้อมูลไม่ชัด (วันหมดอายุ / ชื่อ / เลขบัตร)<br/>• ไม่แนบรูปบัตร<br/>• ค่างวดรวมตั้งแต่ 6,000 บาท/เดือน หรือเกิน 8 ชิ้น<br/>  ขอเอกสารแบบ Non-Credit (คิดหลังหักโปร)<br/>• ติดตั้งที่อยู่แห่งที่ 3 ขอเอกสารความเป็นเจ้าของหรือความสัมพันธ์"),
        ("9", "ตรวจการค้างชำระ", AR + "<br/>ส่งอีเมลลูกค้าค้างชำระให้ LGM ทุกวันที่ 15<br/>เพดานชิ้น 11 จังหวัด ดูหน้า Credit Limit"),
        ("10", "ชำระผ่านบุคคลที่ 3", "ไม่อนุญาต และห้ามเช่าซื้อแทนกันโดยสัญญาว่าจะผ่อนให้"),
    ]
    place_flowable(c, criteria_table(rows, [34, 128, 562]), 28, PAGE_H - 58, 724, 466)


def page_non_credit(c):
    draw_header(c, "ประเภท : Non Credit")
    rows = [
        ("1", "สัญชาติ", "ไทย"),
        ("2", "อายุ", "20–70 ปีบริบูรณ์ นับวันชนวัน"),
        ("3", "ที่อยู่ในการติดตั้ง", "1. ที่อยู่ตามบัตรประชาชน<br/>2. ที่อยู่อาศัยปัจจุบัน<br/>3. ที่อยู่ปัจจุบันอื่น (ต้องแนบเอกสารเพิ่ม)"),
        ("4", "เบอร์มือถือ / อีเมล<br/>(ของผู้ซื้อ)", PHONE),
        ("5", "วิธีชำระเงิน<br/>(เดบิต / หักบัญชี)",
         "• บัตรเดบิตที่ออกโดยธนาคารในประเทศเท่านั้น (ไม่ใช่บัตรกดเงินสด)<br/>• หักบัญชีผ่าน <b>ODD Online</b>: กสิกรไทย / กรุงศรี / ไทยพาณิชย์ / กรุงไทย<br/>• <b>ไม่ต้องส่ง</b>เอกสารหักบัญชีอัตโนมัติ"),
        ("6", "บัตรประชาชน",
         "• ตัวจริงหรือสำเนารับรองถูกต้อง เหมือน OSMS<br/>• ไม่รับ e-ID ทุกกรณี<br/>• ต้องเห็นข้อมูลครบ ชัด ไม่มีแสงสะท้อน"),
        ("7", "สำเนาเปลี่ยนชื่อ<br/>(ถ้ามี)", "เมื่อชื่อไม่ตรงเอกสาร เช่น หน้าสมุดบัญชี หรือสลิปเงินเดือน"),
        ("8", "เอกสารรายได้<br/>และรายงาน NCB",
         "<b>ผู้มีรายได้ประจำ ส่งอย่างใดอย่างหนึ่ง</b><br/>• สลิปเงินเดือนเดือนล่าสุด (ไม่รับแคปหน้าจอ) <b>หรือ</b><br/>• สเตทเมนต์ย้อนหลัง <b>3 เดือน</b>ต่อเนื่อง<br/><br/><b>อาชีพอิสระ / เจ้าของกิจการ</b><br/>• สเตทเมนต์ย้อนหลัง <b>6 เดือน</b>ต่อเนื่อง<br/>• ใบจดทะเบียนพาณิชย์ หรือภาพถ่ายยืนยันอาชีพ<br/><br/>• รายได้ต่อเดือนตั้งแต่ <b>15,000</b> บาท (เฉลี่ยจากสเตทเมนต์)<br/>• ยอดคงเหลือในบัญชีต้องไม่น้อยกว่า<b>ค่างวด LG รวมทุกสัญญา</b><br/>• NCB + Credit Scoring ออกไม่เกิน 60 วัน<br/>NCB กระดาษหน้าเคาน์เตอร์ ต้องมีใบเสร็จรับเงิน"),
    ]
    place_flowable(c, criteria_table(rows, [34, 128, 562]), 28, PAGE_H - 58, 724, 466)


def product_limit_table():
    header = [P("<b>ประเภท</b>", ST_TH), P("<b>ชิ้น</b>", ST_TH), P("<b>ประเภท</b>", ST_TH), P("<b>ชิ้น</b>", ST_TH)]
    pairs = [
        ("เครื่องกรองน้ำ", "1", "เครื่องปรับอากาศ", "4"),
        ("ตู้เย็น", "2", "เครื่องฟอกอากาศ", "2"),
        ("เครื่องซักผ้า", "1", "เครื่องลดความชื้น", "1"),
        ("เครื่องอบผ้า", "1", "TV", "2"),
        ("เครื่องล้างจาน", "1", "SoundBar", "2"),
        ("Styler", "1", "Monitor", "2"),
        ("เครื่องดูดฝุ่น", "2", "Microwave", "1"),
    ]
    name = S("pn", "TH", 8, 10.4, BODY)
    qty = S("pq", "THB", 8, 10.4, BODY, TA_CENTER)
    data = [header]
    for a, n1, b, n2 in pairs:
        data.append([P(a, name), P(n1, qty), P(b, name), P(n2, qty)])
    inner = Table(data, colWidths=[150, 42, 150, 42])
    inner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TH_BG),
        ("BACKGROUND", (1, 1), (1, -1), HexColor("#F3F3F3")),
        ("BACKGROUND", (3, 1), (3, -1), HexColor("#F3F3F3")),
        ("GRID", (0, 0), (-1, -1), 0.35, GRID),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("ALIGN", (3, 0), (3, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 1.4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.4),
    ]))
    return inner


def page_non_credit_2(c):
    draw_header(c, "ประเภท : Non Credit (ต่อ)")
    ncb = (
        "<b>เกรด NCB</b><br/>"
        "• <b>AA–CC</b> ไม่ต้องใช้เอกสารรายได้ (บัญชีปกติ และไม่เคยชำระล่าช้า)<br/>"
        "• <b>DD–EE</b> ต้องใช้เอกสารรายได้<br/>"
        "• <b>FF</b> ไม่รับพิจารณา<br/><br/>"
        "<b>ไม่พิจารณา</b><br/>"
        "1. ประวัติปรับปรุงโครงสร้างหนี้<br/>"
        "2. โอนขายหนี้เสีย และยังไม่ปิดบัญชี<br/>"
        "3. ตัดหนี้สูญ<br/>"
        "4. เข้าโครงการรัฐที่ห้ามก่อหนี้เพิ่ม<br/><br/>"
        "<b>รอดูประวัติค้างชำระ</b><br/>"
        "• ค้าง <b>31–90 วัน</b> ดูประวัติชำระใหม่ 6 เดือนต่อเนื่อง<br/>"
        "• ค้าง <b>มากกว่า 90 วัน</b> (ตั้งแต่วันที่ 91) ดู 12 เดือนต่อเนื่อง<br/><br/>"
        "<b>พิจารณาปกติ</b><br/>"
        "1. ปิดบัญชีแล้วเกิน 1 ปี<br/>"
        "2. ชำระล่าช้ารอบบิลปัจจุบัน ต้องชำระก่อนและแนบใบเสร็จ (ไม่รับสลิปจ่ายเงิน)"
    )
    item = S("i5", "THB", 8, 10.4, BODY)
    cell = S("c5", "TH", 7.7, 10.1, BODY)
    no = S("n5", "TH", 8, 10.4, BODY, TA_CENTER)
    rows = [
        ("9", "พิจารณาเกรด NCB", ncb),
        ("10", "ตรวจการค้างชำระ", AR),
        ("11", "ชำระผ่านบุคคลที่ 3", "ไม่อนุญาต และห้ามเช่าซื้อแทนกันโดยสัญญาว่าจะผ่อนให้"),
        ("12", "จำกัดจำนวนต่อประเภท", ""),
    ]
    data = [[P("No", ST_TH), P("รายการ", ST_TH), P("เกณฑ์", ST_TH)]]
    for n, label, crit in rows:
        if n == "12":
            data.append([P(n, no), P(label, item), product_limit_table()])
        else:
            data.append([P(n, no), P(label, item), P(crit, cell)])
    tbl = Table(data, colWidths=[34, 128, 562])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TH_BG),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, GRID),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2.4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.4),
        ("BACKGROUND", (0, 2), (-1, 2), ROW_ALT),
        ("BACKGROUND", (0, 4), (-1, 4), ROW_ALT),
    ]))
    place_flowable(c, tbl, 28, PAGE_H - 56, 724, 468)


def page_income(c):
    draw_header(c, "วิธีคำนวณรายได้ และที่อยู่ติดตั้ง")
    c.setFillColor(TITLE)
    c.setFont("THB", 13)
    c.drawString(32, PAGE_H - 70, "วิธีคำนวณรายได้")
    rules = [
        "1. คำนวณรายได้จากสเตทเมนต์ย้อนหลัง <b>3 หรือ 6 เดือน</b>",
        "2. ภาระหนี้รวม (รวมหนี้ LG) ต้องไม่เกิน <b>80%</b> ของรายได้ (DTI ไม่เกิน 80%)",
        "3. ใช้ภาระหนี้ตามตัวเลขที่ปรากฏในรายงาน NCB",
        "4. บัตรเครดิตใน NCB คิดจาก<b>ยอดขั้นต่ำ</b>ที่แสดงในรายงาน",
        "5. มีผู้กู้ร่วม ให้หารภาระหนี้ตามจำนวนผู้กู้ร่วม",
        "6. Non-Credit: ยอดเงินคงเหลือในบัญชีต้องไม่น้อยกว่า<b>ค่างวด LG รวมทุกสัญญา</b>",
    ]
    y = PAGE_H - 78
    for html in rules:
        p = P(html, ST_BODY)
        w, h = p.wrap(PAGE_W - 64, 36)
        p.drawOn(c, 32, y - h)
        y -= h + 2
    y -= 8
    tbl = two_col([
        (P("ที่อยู่ติดตั้ง<br/>และเอกสาร", ST_ITEM), P(
            "1. ที่อยู่เดียวกับบัตรประชาชน<br/>2. ที่อยู่ปัจจุบัน<br/>"
            "3. ที่อยู่แห่งที่ 3 ต้องมีเอกสารประกอบ<br/><br/>"
            "<b>เอกสารติดตั้ง #3</b><br/>"
            "1. สัญญาเช่าพร้อมใบเสร็จค่าเช่า<br/>"
            "2. ทะเบียนบ้านตนเองหรือบุคคลในครอบครัว<br/>"
            "3. เอกสารแสดงความสัมพันธ์<br/>"
            "4. บิลค่าน้ำ ค่าไฟ ค่าสาธารณูปโภค<br/>"
            "ไม่รับบิลมือถือ ใบแจ้งหนี้บัตรเครดิต และที่อยู่จัดส่งพัสดุ<br/>"
            "5. เอกสารอื่นที่แสดงความเป็นเจ้าของหรือความสัมพันธ์<br/>"
            "ทุกเอกสารไม่รับภาพแคปหน้าจอ",
            ST_CELL)),
    ], [150, 574])
    place_flowable(c, tbl, 28, y, 724, y - 24)


def page_limits(c):
    draw_header(c, "เกณฑ์ Credit Limit และ Unit Limit")
    top = Table([
        [P("No", ST_TH), P("รายการ", ST_TH), P("เกณฑ์", ST_TH)],
        [P("1.", ST_NO), P("Credit Limit", ST_ITEM), P("<b>6,000 บาทต่อเดือน</b>", ST_CELL)],
        [P("2.", ST_NO), P("Unit Limit (Memo)", ST_ITEM), P("<b>ตั้งแต่ 8 ชิ้นขึ้นไป</b>", ST_CELL)],
    ], colWidths=[50, 180, 494])
    top.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TH_BG),
        ("BACKGROUND", (0, 2), (-1, 2), ROW_ALT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, GRID),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
    ]))
    place_flowable(c, top, 28, PAGE_H - 62, 724, 78)
    body = (
        "<b>ก. เกิน 6,000 บาทต่อเดือน และไม่เกิน 8 ชิ้น</b> (คิดหลังหักโปร) เครดิตเป็นผู้พิจารณา<br/><br/>"
        "เอกสารเพิ่ม: 1. NCB + Credit Scoring "
        "2. เอกสารรายได้ตามอาชีพ (พนักงานประจำหรืออาชีพอิสระ)<br/><br/>"
        "<b>ข. ตั้งแต่ 8 ชิ้นขึ้นไป</b> ผู้บริหารพิจารณาผ่าน Consult<br/><br/>"
        "เอกสารเพิ่ม: 1. NCB + Credit Scoring "
        "2. เอกสารรายได้ตามอาชีพ "
        "3. จัดทำ Memo ขออนุมัติผู้บริหาร"
    )
    place_flowable(c, two_col([(P("Credit Card<br/>และ Non-Credit", ST_ITEM), P(body, ST_CELL))], [150, 574]), 28, PAGE_H - 150, 724, 175)
    province = (
        "<b>ใช้กับลูกค้าบุคคลเท่านั้น ไม่ใช้กับลูกค้าองค์กร</b><br/>"
        "ไม่เกิน <b>2 ชิ้น/คน</b> ใน 11 จังหวัด: สระแก้ว, จันทบุรี, ชัยภูมิ, หนองคาย, บึงกาฬ, "
        "หนองบัวลำภู, กาญจนบุรี, พัทลุง, พะเยา, น่าน, สุโขทัย<br/>"
        "ประวัติชำระดีกับบริษัทมากกว่า <b>6 เดือน</b> เพิ่มได้อีก 1 ชิ้น (รวมไม่เกิน 3)<br/>"
        "มากกว่า <b>12 เดือน</b> เพิ่มได้อีก 2 ชิ้น (รวมไม่เกิน 4)<br/>"
        "พื้นที่อื่นยังใช้เพดาน 6,000 บาท/เดือน และ 8 ชิ้น/คน"
    )
    place_flowable(c, two_col([(P("จังหวัดที่กำหนด", ST_ITEM), P(province, ST_CELL))], [150, 574]), 28, PAGE_H - 336, 724, 155)


def page_foreigner(c):
    draw_header(c, "ประเภท : ต่างชาติ")
    rows = [
        ("1", "สัญชาติ", "ชาวต่างชาติทุกประเทศ"),
        ("2", "อายุ", "20–60 ปีบริบูรณ์"),
        ("3", "ที่อยู่จัดส่ง / ติดตั้ง", "ที่พักอาศัยตามสัญญาเช่า"),
        ("4", "เบอร์มือถือ / อีเมล<br/>(ของผู้ซื้อ)", PHONE),
        ("5", "วิธีชำระเงิน", "บัตรเครดิตสถาบันการเงิน<b>ในไทยเท่านั้น</b><br/>เหลืออายุอย่างน้อย <b>3 ปี</b>"),
        ("6", "Work Permit<br/>และ Passport", "ต้องมี Work Permit และ Passport"),
        ("7", "เอกสารติดตั้ง", "สัญญาเช่า / เอกสารความเป็นเจ้าของ / เอกสารความสัมพันธ์<br/><b>ไม่รับ</b>เอกสารที่อยู่ ต.ม."),
        ("8", "เดบิต / เงินสด / โอน", "จ่ายไม่ได้"),
        ("9", "ชำระผ่านบุคคลที่ 3", "ไม่อนุญาต และห้ามเช่าซื้อแทนกันโดยสัญญาว่าจะผ่อนให้"),
    ]
    place_flowable(c, criteria_table(rows, [36, 150, 538]), 28, PAGE_H - 58, 724, 466)


def page_juristic(c):
    draw_header(c, "ประเภท : นิติบุคคลไทย")
    no = S("jn", "TH", 8, 10.6, BODY, TA_CENTER)
    item = S("ji", "THB", 8, 10.6, BODY)
    cell = S("jc", "TH", 8, 10.6, BODY)
    data = [
        [P("ลำดับ", ST_TH), P("รายการ", ST_TH), P("เงื่อนไข", ST_TH)],
        [P("1.1<br/>1.2", no),
         P("สำเนาหนังสือรับรองบริษัท อายุไม่เกิน 6 เดือน ทุกแผ่นลงนามผู้มีอำนาจและประทับตรา<br/><br/>ภ.พ.20", item),
         P("ดำเนินกิจการไม่น้อยกว่า <b>2 ปี</b> และมีกำไร<br/>ห้ามองค์กรไม่แสวงหาผลกำไร", cell)],
        [P("2", no), P("สำเนาบัตรประชาชนเจ้าของหรือผู้มีอำนาจ หรือพาสปอร์ต", item), P("ต้องมี", cell)],
        [P("3", no), P("รูปสถานประกอบการและแผนที่", item), P("สถานประกอบการ", cell)],
        [P("4", no), P("เบอร์มือถือ / อีเมลของผู้ซื้อ", item),
         P("ของผู้เช่าซื้อหรือผู้รับมอบอำนาจแทนบริษัท ห้ามใช้เบอร์บุคคลอื่น", cell)],
        [P("5", no), P("สั่งซื้อโดยผู้รับมอบอำนาจ", item),
         P("ต้องมีหนังสือมอบอำนาจและสำเนาบัตรผู้รับมอบอำนาจ", cell)],
        [P("6.1<br/>6.2", no),
         P("วางบิล / โอน / บัตรเครดิต<br/><br/>บัตรกรรมการตามหนังสือรับรอง หรือบัตรนามบริษัท", item),
         P("ขอรายละเอียดวางบิล: ชื่อ เบอร์ อีเมล วันที่วางบิล และที่อยู่วางบิล<br/>ห้ามใช้บัตรบุคคลที่ 3 ทุกกรณี", cell)],
        [P("7", no), P("ที่อยู่จัดส่ง / ติดตั้ง", item),
         P("1. ตามหนังสือรับรองบริษัท<br/>2. สาขาต้องมีเอกสารจัดตั้งสาขาหรือ ภ.พ.20<br/>"
           "ติดตั้งที่สถานประกอบการเท่านั้น ไม่รับบ้านพักกรรมการ<br/><br/>" + AR +
           "<br/>สั่งซื้อตั้งแต่ <b>9 เครื่อง</b>ใน 1 คำสั่งซื้อ เป็นลูกค้าองค์กร (หน้าถัดไป)", cell)],
    ]
    tbl = Table(data, colWidths=[48, 250, 426])
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), TH_BG),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, GRID),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
    ]
    for i in range(2, len(data), 2):
        cmds.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
    tbl.setStyle(TableStyle(cmds))
    place_flowable(c, tbl, 28, PAGE_H - 56, 724, 468)


def banner(c, x, y, w, h, text):
    c.setFillColor(BANNER)
    c.roundRect(x, y, w, h, 3, fill=1, stroke=0)
    p = P(text, ST_BANNER)
    pw, ph = p.wrap(w - 24, h)
    p.drawOn(c, x + 14, y + (h - ph) / 2)


def page_corporate(c):
    draw_header(c, "ประเภท : นิติบุคคลไทย (ลูกค้าองค์กร)")
    banner(c, 70, PAGE_H - 108, 640, 36, "ข้อ 3  นิยามลูกค้าองค์กร")
    y = PAGE_H - 122
    lines = [
        "<font color='#C8102E'><b>1.</b></font>  เป็นลูกค้าองค์กรเมื่อ<b>ครบทั้ง 2 ข้อ</b>",
        "1. ส่งเอกสารคุณสมบัติลูกค้าองค์กรตามระเบียบ Credit Control ได้",
        "2. สัญญาเช่าซื้อแบบสมาชิก <b>ตั้งแต่ 9 เครื่องขึ้นไปใน 1 คำสั่งซื้อ</b>",
        "<font color='#C8102E'><b>2.</b></font>  นับรวมทุกประเภทสินค้า เช่น กรองน้ำ 6 + ฟอกอากาศ 3 = 9 เครื่อง",
    ]
    for html in lines:
        p = P(html, ST_BODY)
        w, h = p.wrap(620, 36)
        p.drawOn(c, 86, y - h)
        y -= h + 3
    y -= 6
    c.setFillColor(SOFT)
    c.roundRect(86, y - 48, 608, 48, 4, fill=1, stroke=0)
    p = P("ตัวอย่าง: กรองน้ำ 6 เครื่อง + ฟอกอากาศ 3 เครื่อง = <b>9 เครื่อง</b> แม้คนละประเภท ก็นับรวมกัน", ST_EX)
    pw, ph = p.wrap(584, 36)
    p.drawOn(c, 98, y - 16 - ph)
    y -= 64
    banner(c, 70, y - 36, 640, 36, "ข้อ 5  เงื่อนไขสถานที่ติดตั้ง")
    y -= 48
    clauses = [
        "<font color='#C8102E'><b>1.</b></font> สถานที่ติดตั้งได้เฉพาะสถานประกอบการ อาคาร หรือพื้นที่ที่องค์กรคู่สัญญาเป็นเจ้าของหรือผู้เช่าโดยตรง ห้ามบ้านพักพนักงาน ผู้บริหาร กรรมการ และสำนักงานบริษัทในเครือที่เป็นนิติบุคคลคนละราย",
        "<font color='#C8102E'><b>2.</b></font> ถ้าเข้าข้อ 1 ติดตั้งแยกหลายแห่งได้ ดูตัวอย่างในตารางแนบ 1",
        "<font color='#C8102E'><b>3.</b></font> หลังทำสัญญา ถ้าติดตั้งจริงต่ำกว่า 9 เครื่อง ให้ขออนุมัติข้อ 10 (ยกเว้น) บริษัทสงวนสิทธิ์ตรวจความพร้อมของพื้นที่",
        "<font color='#C8102E'><b>4.</b></font> ระยะเวลาสัญญาเป็นไปตามเงื่อนไขบริการแบบสมาชิก",
    ]
    for text in clauses:
        p = P(text, ST_BODY_SM)
        w, h = p.wrap(620, 60)
        p.drawOn(c, 86, y - h)
        y -= h + 4


def page_appendix(c):
    draw_header(c, "ประเภท : นิติบุคคลไทย (ลูกค้าองค์กร)")
    c.setFillColor(BANNER)
    c.roundRect(48, PAGE_H - 118, 684, 48, 3, fill=1, stroke=0)
    p = P("[ตารางแนบ 1] ตัวอย่างสถานที่ติดตั้งที่อนุญาต (ประเทศไทย)", S("apph", "THB", 13, 16, white))
    pw, ph = p.wrap(650, 30)
    p.drawOn(c, 64, PAGE_H - 100)
    head = S("ah", "THB", 8, 10.6, white)
    cell = S("ac", "TH", 7.8, 10.4, BODY)
    no = S("ano", "TH", 7.8, 10.4, HexColor("#7A0018"))
    rows = [
        [P("ประเภทองค์กร", head), P("ตัวอย่างที่อนุญาต", head), P("ตัวอย่างที่ไม่อนุญาต", head)],
        [P("นิติบุคคล / บริษัทเอกชน", cell), P("สำนักงานใหญ่ สาขา โรงงาน คลังสินค้า หน้าร้านที่จดทะเบียน", cell), P("บ้านพักพนักงาน ผู้บริหาร หรือกรรมการ", no)],
        [P("สถานศึกษา", cell), P("วิทยาเขตหลัก วิทยาเขตย่อย อาคารเรียน หอพักของสถาบัน", cell), P("บ้านพักครู อาจารย์ หรือบุคลากร", no)],
        [P("หน่วยงานรัฐ / รัฐวิสาหกิจ", cell), P("ส่วนกลาง สำนักงานภูมิภาค ศูนย์บริการ หน่วยงานระดับอำเภอ", cell), P("บ้านพักข้าราชการหรือพนักงานรัฐวิสาหกิจ", no)],
        [P("สถานพยาบาล", cell), P("โรงพยาบาลหลัก สาขา ศูนย์ตรวจสุขภาพ คลินิกในเครือ", cell), P("บ้านพักแพทย์ พยาบาล หรือบุคลากร", no)],
        [P("องค์กรอื่น เช่น มูลนิธิ สมาคม", cell), P("สถานประกอบการหรือพื้นที่ที่องค์กรเป็นเจ้าของหรือเช่าและดำเนินกิจการถูกต้อง", cell), P("สำนักงานคู่ค้า หรือบริษัทในเครือที่จดทะเบียนเป็นนิติบุคคลคนละราย", no)],
    ]
    tbl = Table(rows, colWidths=[150, 270, 250])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BANNER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#E0B8C0")),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("BACKGROUND", (0, 2), (-1, 2), HexColor("#FFF8F8")),
        ("BACKGROUND", (0, 4), (-1, 4), HexColor("#FFF8F8")),
    ]))
    place_flowable(c, tbl, 48, PAGE_H - 132, 684, 280)
    y = 100
    for text in [
        "1. ตารางนี้เป็นแนวทางเริ่มต้น การอนุมัติจริงยึดข้อ 5 ว่าองค์กรคู่สัญญาเป็นเจ้าของหรือผู้เช่าโดยถูกต้อง",
        "2. แม้ชื่อหน่วยงานไม่ตรงตาราง ติดตั้งได้ถ้าพิสูจน์ได้ว่าเข้าข้อ 5",
    ]:
        p = P(text, ST_BODY_SM)
        w, h = p.wrap(684, 36)
        p.drawOn(c, 48, y - h)
        y -= h + 3


FAQ = [
    ("บัตรเครดิต", "บัตรชำรุด ไม่เห็นข้อมูลบางส่วน ส่งภาพจากแอปแทนได้ไหม", "ได้ แต่ต้องเห็นชื่อ ปีหมดอายุ และเลขบัตรชัด"),
    ("บัตรเครดิต", "บัตรเครดิตออนไลน์สั่งซื้อได้ไหม", "ได้ ต้องเห็นชื่อ วันหมดอายุ และเลขบัตรชัด"),
    ("บัตรเครดิต", "Shopee Pay และ TrueMoney Wallet ใช้ได้ไหม", "ไม่ได้ ทั้งคู่เป็นบัตรเติมเงินหรือพรีเพด ไม่ใช่บัตรเครดิต"),
    ("บัตรเครดิต", "บุคคลใช้ Corporate Card หรือบัตรคนอื่นได้ไหม", "ไม่ได้ ต้องใช้บัตรเครดิตของตนเอง"),
    ("บัตรเครดิต", "ต่างชาติใช้บัตรธนาคารต่างประเทศได้ไหม", "ไม่ได้ ต้องออกในประเทศไทย และเหลืออายุไม่น้อยกว่า 3 ปี"),
    ("บัตรเครดิต", "มีครบ 8 สัญญาแล้ว สั่งเพิ่มได้ไหม", "ได้ 2 ทาง: ปิดบางบัญชีให้ไม่เกิน 8 หรือส่งเอกสารรายได้เพิ่ม"),
    ("เอกสาร / รายได้", "ที่อยู่ที่ 3 สามีซื้อ ติดตั้งบ้านภรรยา ไม่ได้จดทะเบียนสมรส", "ใช้สำเนาสูติบัตรบุตร ถ้าไม่มีบุตรต้องมีเอกสารยืนยันว่าเป็นสามีภรรยา เช่น ทะเบียนบ้านที่มีชื่อภรรยา"),
    ("เอกสาร / รายได้", "ต่างชาติไม่ได้ต่อ Work Permit ซื้อได้ไหม", "ไม่ได้ ต้องต่อ Work Permit และมีวันที่ต่อชัดเจน"),
    ("เอกสาร / รายได้", "Non-Credit รายได้ไม่ผ่าน แนบรายได้อื่นได้ไหม", "ได้ ถ้ามีอาชีพเสริม ใช้สเตทเมนต์ที่แสดงเงินเข้าจากแหล่งนั้น"),
    ("เอกสาร / รายได้", "จะส่งเอกสารเพิ่ม แต่เกิน 15 วันแล้ว", "อีเมลแจ้งเครดิตพร้อมเหตุผลที่ขอ On Hold เกิน 15 วัน"),
    ("เอกสาร / รายได้", "ลูกค้าปัจจุบันเปลี่ยนวิธีชำระได้ไหม", "เปลี่ยนไม่ได้"),
    ("เอกสาร / รายได้", "ยังไม่ติดตั้ง ขอย้ายสถานที่ติดตั้งได้ไหม", "ได้ ถ้าสถานที่ใหม่เป็นไปตามเกณฑ์"),
    ("เอกสาร / รายได้", "อาชีพอิสระไม่มีเอกสารภาษี ใช้อะไรแทน", "ทะเบียนพาณิชย์ หรือหลักฐานอาชีพ เช่น รูปกิจการ เอกสารรายได้จาก Shopee, LINE MAN, Grab หรือสเตทเมนต์ที่มีเงินเข้าสม่ำเสมอ"),
    ("เอกสาร / รายได้", "ใช้รายได้ของสามี ภรรยา หรือลูกได้ไหม", "ไม่ได้ ไม่นับเป็นรายได้ที่มีสัญญาจ้างหรือหลักประกันทางกฎหมาย"),
    ("เอกสาร / รายได้", "ลายเซ็นสำเนาบัตรไม่ตรงระบบ ลูกค้าไม่ส่งใหม่", "อนุมัติไม่ได้ เพราะเป็นเอกสารยืนยันว่าลูกค้าสั่งซื้อเอง"),
    ("เอกสาร / รายได้", "แจ้งคืนเงินทางอีเมลแต่ไม่ได้ลงไฟล์ DST", "เครดิตคืนเงินให้ไม่ได้ เพราะต้องมีหลักฐานในไฟล์ DST"),
    ("เอกสาร / รายได้", "บ้าน หอ หรือแฟลตเช่า แต่ไม่มีใบเสร็จค่าเช่า", "เครดิตพิจารณาสัญญาเช่า ถ้าไม่น่าเชื่อถือจะขอสลิปโอนหรือใบเสร็จเพิ่ม"),
    ("เอกสาร / รายได้", "นับอายุ 20–70 ปีอย่างไร", "นับวันชนวันบริบูรณ์ โดยยึดวันที่ส่งคำสั่งซื้อ"),
    ("เอกสาร / รายได้", "Work Permit เหลือ 1 เดือน มีผลไหม", "แนะนำให้ต่อ Work Permit ใหม่"),
    ("เอกสาร / รายได้", "ทำไมเกิน 6,000 บาทหรือเกิน 8 เครื่องต้องส่งเอกสารเพิ่ม", "เพื่อเทียบรายได้กับหนี้เดิมบวกค่างวดใหม่ของ LG และยืนยันว่ามีรายได้จริง"),
    ("การสั่งซื้อ", "สั่ง Wash Tower มากกว่า 1 เครื่องได้ไหม", "ได้ตามปกติ ต้องใช้งานเอง ห้ามจำหน่ายหรือโอนต่อ"),
    ("การสั่งซื้อ", "สั่งซื้อแทนกันได้ไหม", "ไม่อนุมัติทุกกรณี ผู้เช่าซื้อต้องรับผิดชอบจนผ่อนครบ"),
    ("การสั่งซื้อ", "อยู่บ้านญาติฟรี ไม่มีสัญญาเช่า คนละนามสกุล", "ไม่ได้ ต้องมีเอกสารเชื่อมความสัมพันธ์ที่ชัด"),
    ("การสั่งซื้อ", "ใช้เบอร์สามี ภรรยา หรือบุตรได้ไหม", "ไม่ได้ ต้องเป็นเบอร์ผู้เช่าซื้อ เพิ่มเบอร์ติดต่ออื่นได้"),
    ("การสั่งซื้อ", "สั่งเกิน Credit Limit หรือ Unit Limit ได้ไหม", "ได้ แต่ต้องแนบเอกสารรายได้เพิ่ม และบริษัทพิจารณาอีกครั้ง"),
    ("NCB", "เคยเข้าโครงการพักหนี้รัฐแบบไม่ก่อหนี้เพิ่ม", "สั่งซื้อไม่ได้"),
    ("NCB", "เกรด AA–CC ต้องส่งเอกสารอะไร", "ไม่ต้องส่งเอกสารรายได้ แต่เครดิตพิจารณากรณีอีกครั้ง"),
    ("NCB", "บัญชีปัจจุบันค้างชำระและเริ่มผิดนัด", "ส่งให้เครดิตได้ อาจขอใบเสร็จการชำระเพิ่ม"),
    ("NCB", "ลูกค้าเดิมยังมียอดค้าง สั่งซื้อได้ไหม", "ต้องชำระให้เป็นปกติก่อน แล้วเครดิตพิจารณาอีกครั้ง"),
    ("NCB", "ช้าเกิน 300 วัน แต่ปิดบัญชีไม่ถึง 1 ปี", "ซื้อไม่ได้ ต้องปิดบัญชีมาแล้วไม่น้อยกว่า 1 ปี"),
    ("นิติบุคคล", "องค์กรไม่แสวงหากำไรมีอะไรบ้าง", "เช่น มูลนิธิช่วยเหลือสังคม โรงพยาบาลการกุศล และสถาบันศาสนา"),
    ("นิติบุคคล", "เปิดเกิน 2 ปีแต่ไม่ส่งงบการเงินได้ไหม", "ไม่ได้ ต้องส่งงบการเงินประจำปีและเสียภาษีถูกต้อง"),
    ("นิติบุคคล", "ติดตั้งที่บ้านกรรมการ แต่สั่งในนามบริษัท", "ไม่ได้ ต้องติดตั้งในพื้นที่จัดตั้งบริษัท"),
    ("นิติบุคคล", "มอบอำนาจให้จัดซื้อ ใช้เอกสารอะไร", "เอกสารนิติบุคคลตามปกติ หนังสือมอบอำนาจ 1 ฉบับ และสำเนาบัตรผู้มอบกับผู้รับมอบ"),
]


def page_faq(c, chunk, page_no, page_count):
    draw_header(c, f"FAQ  01/10/2026   ({page_no}/{page_count})")
    q = S(f"fq{page_no}", "TH", 7.5, 9.8, BODY)
    h = S(f"fh{page_no}", "THB", 8, 10.4, TITLE, TA_CENTER)
    data = [[P("หมวด", h), P("คำถาม", h), P("คำตอบ", h)]]
    for topic, question, answer in chunk:
        data.append([P(topic, q), P(question, q), P(answer, q)])
    tbl = Table(data, colWidths=[88, 310, 324])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TH_BG),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.35, GRID),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
        ("BACKGROUND", (0, 2), (-1, 2), ROW_ALT),
        ("BACKGROUND", (0, 4), (-1, 4), ROW_ALT),
        ("BACKGROUND", (0, 6), (-1, 6), ROW_ALT),
    ]))
    place_flowable(c, tbl, 24, PAGE_H - 56, 732, 460)


def main():
    PAGES.mkdir(exist_ok=True)
    c = canvas.Canvas(str(OUT_PDF), pagesize=(PAGE_W, PAGE_H))
    pages = [
        cover, page_hours, page_credit_card, page_non_credit, page_non_credit_2,
        page_income, page_limits, page_foreigner, page_juristic, page_corporate, page_appendix,
    ]
    chunks = [FAQ[i:i + 7] for i in range(0, len(FAQ), 7)]
    for fn in pages:
        fn(c)
        c.showPage()
    for n, chunk in enumerate(chunks, 1):
        page_faq(c, chunk, n, len(chunks))
        if n < len(chunks):
            c.showPage()
    c.save()
    print("wrote", OUT_PDF, "pages", 11 + len(chunks))

    from pypdf import PdfReader, PdfWriter
    reader = PdfReader(str(OUT_PDF))
    for i, page in enumerate(reader.pages, 1):
        w = PdfWriter()
        w.add_page(page)
        dest = PAGES / f"page-{i:02d}.pdf"
        with dest.open("wb") as f:
            w.write(f)


if __name__ == "__main__":
    main()
