# -*- coding: utf-8 -*-
"""Build English LG Criteria slides matching the original 780x540 deck."""
from pathlib import Path

from PIL import Image
from reportlab.lib.colors import Color, HexColor, white, black
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle, KeepInFrame

ROOT = Path(r"D:\LG Criteria")
ASSETS = ROOT / "_assets"
OUT_PDF = ROOT / "LG Criteria Update 01-10-2026 EN.pdf"
PAGES_EN = ROOT / "pages-en"
FONT_DIR = Path(r"C:\Windows\Fonts")

PAGE_W, PAGE_H = 780, 540
LG_RED = HexColor("#A50034")
LG_RED_BRIGHT = HexColor("#C00C3F")
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
pdfmetrics.registerFont(TTFont("LG-B", str(FONT_DIR / "LG_Smart_UI-Bold.ttf")))
pdfmetrics.registerFont(TTFont("LG-SB", str(FONT_DIR / "LG_Smart_UI-SemiBold.ttf")))
pdfmetrics.registerFont(TTFont("LG-L", str(FONT_DIR / "LG_Smart_UI-Light.ttf")))


def S(name, font="LG", size=8, leading=None, color=BODY, align=TA_LEFT, **kw):
    return ParagraphStyle(
        name,
        fontName=font,
        fontSize=size,
        leading=leading if leading is not None else size + 2.8,
        textColor=color,
        alignment=align,
        **kw,
    )


ST_TITLE = S("title", "LG-SB", 22, 26, TITLE)
ST_TH = S("th", "LG-SB", 9.5, 12.2, TITLE, TA_CENTER)
ST_TH_L = S("thl", "LG-SB", 9.5, 12.2, TITLE, TA_LEFT)
ST_NO = S("no", "LG", 9, 12, BODY, TA_CENTER)
ST_ITEM = S("item", "LG-SB", 9, 12, BODY)
ST_CELL = S("cell", "LG", 8.8, 11.8, BODY)
ST_CELL_SM = S("cellsm", "LG", 8.2, 11, BODY)
ST_BULLET = S("bullet", "LG", 11, 15.5, BODY, leftIndent=14, firstLineIndent=-12)
ST_H2 = S("h2", "LG-SB", 13, 16.5, TITLE)
ST_NOTE = S("note", "LG", 9, 12.2, HexColor("#8A001C"))
ST_FOOT = S("foot", "LG", 7.5, 9.5, MUTED)
ST_COVER = S("cover", "LG-SB", 30, 36, TITLE)
ST_BANNER = S("banner", "LG-B", 15, 19, white)
ST_BODY = S("body", "LG", 10.5, 14.8, BODY)
ST_BODY_SM = S("bodysm", "LG", 9.4, 13.2, BODY)
ST_EX = S("ex", "LG", 9.6, 13.4, BODY)
ST_EX_T = S("ext", "LG-SB", 10.5, 13.5, TITLE)


def P(html, style=ST_CELL):
    return Paragraph(html, style)


def draw_header(c, title):
    logo = ASSETS / "Image12_t.png"
    c.drawImage(str(logo), PAGE_W - 118, PAGE_H - 42, width=86, height=38, mask="auto", preserveAspectRatio=True, anchor="c")
    c.setFillColor(TITLE)
    c.setFont("LG-SB", 20)
    c.drawString(28, PAGE_H - 36, title)
    c.setStrokeColor(LINE)
    c.setLineWidth(1.1)
    c.line(28, PAGE_H - 50, PAGE_W - 28, PAGE_H - 50)
    c.setFillColor(MUTED)
    c.setFont("LG", 7.5)
    c.drawString(28, 12, "Internal use only  |  LGETH  |  Update 2026.10.01  |  English translation")
    c.drawRightString(PAGE_W - 28, 12, "EN")


def place_flowable(c, flowable, x, y_top, width, height):
    boxed = KeepInFrame(width, height, [flowable], mode="shrink", hAlign="LEFT", vAlign="TOP")
    w, h = boxed.wrapOn(c, width, height)
    scale = getattr(boxed, "_scale", 1) or 1
    if scale < 0.98:
        print(f"  shrink {scale:.2f} at y_top={y_top:.0f}")
    boxed.drawOn(c, x, y_top - h)
    return h


def criteria_table(rows, col_widths, font_size=8.6):
    item_style = S("item_d", "LG-SB", font_size, font_size + 2.8, BODY)
    cell_style = S("cell_d", "LG", font_size, font_size + 2.8, BODY)
    no_style = S("no_d", "LG", font_size, font_size + 2.8, BODY, TA_CENTER)
    data = [[P("No", ST_TH), P("Items", ST_TH), P("Criteria", ST_TH)]]
    for no, item, crit in rows:
        data.append([P(str(no), no_style), P(item, item_style), P(crit, cell_style)])
    tbl = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), TH_BG),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, GRID),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("BACKGROUND", (0, 0), (0, 0), TH_BG),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
    tbl.setStyle(TableStyle(style_cmds))
    return tbl


def two_col_table(rows, col_widths, header=("Items", "Criteria")):
    data = [[P(header[0], ST_TH), P(header[1], ST_TH)]]
    for a, b in rows:
        left = a if isinstance(a, Paragraph) else P(a, ST_ITEM)
        right = b if isinstance(b, Paragraph) else P(b, ST_CELL)
        data.append([left, right])
    tbl = Table(data, colWidths=col_widths)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), TH_BG),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, GRID),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            cmds.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
    tbl.setStyle(TableStyle(cmds))
    return tbl


def cover(c):
    c.setFillColor(white)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.drawImage(str(ASSETS / "Image8_t.png"), 0, PAGE_H - 210, width=72, height=210, mask="auto", preserveAspectRatio=True, anchor="nw")
    c.drawImage(str(ASSETS / "Image10_t.png"), PAGE_W - 210, 0, width=210, height=208, mask="auto", preserveAspectRatio=True, anchor="sw")
    c.drawImage(str(ASSETS / "Image12_t.png"), PAGE_W - 168, 92, width=108, height=48, mask="auto", preserveAspectRatio=True)
    c.setFillColor(TITLE)
    c.setFont("LG-SB", 30)
    c.drawString(88, 334, "LG Electronics Thailand CCP Regulation")
    c.drawString(88, 296, "Credit Control Policy")
    c.setFillColor(LG_RED)
    c.setFont("LG-SB", 15)
    c.drawString(88, 258, "English Version")
    c.setFillColor(MUTED)
    c.setFont("LG", 12)
    c.drawString(88, 80, "LGETH  |  Update 2026. 10. 01")
    c.setFont("LG", 8.5)
    c.drawString(88, 58, "Internal use only  ·  Translation of the Thai edition dated 1 October 2026")


def page_hours(c):
    draw_header(c, "Operating Hours — Application Review")
    bullets = [
        "- Applications are reviewed and approved within <b>1 day</b> (Credit and Non-Credit).",
        "- Operating hours: <b>08:30 – 17:30</b>, every day.",
        "- If additional documents are required, submit them within <b>15 days</b> (counted from the Credit On Hold date).<br/>Document follow-up: e-mail and phone follow-up via LP / LSM / LGM.",
        "- After documents are submitted, review and approval are completed within <b>1 day</b>.<br/><b>** If there is no result after 1 day, follow up via Group Line or e-mail.</b>",
    ]
    y = PAGE_H - 76
    for html in bullets:
        p = P(html, ST_BULLET)
        w, h = p.wrap(PAGE_W - 70, 90)
        p.drawOn(c, 40, y - h)
        y -= h + 10

    y -= 6
    c.setStrokeColor(HexColor("#D0D0D0"))
    c.setDash(1, 2)
    c.line(40, y, PAGE_W - 40, y)
    c.setDash()
    y -= 22
    c.setFillColor(TITLE)
    c.setFont("LG-SB", 13.5)
    c.drawString(40, y, "Memo case review")
    y -= 8
    memo = [
        "- Cases are reviewed within <b>1 working day</b>, counted from the date Credit Control receives the case (subject to the next-level executive approver).",
        "- If documents are insufficient for review, Credit Control will <b>Request for Check to DST</b>.",
        "- Occupations not accepted: monks, nuns, clergy, students, and any occupation with no income (Credit Card, Non-Credit, and foreign nationals).",
    ]
    for html in memo:
        p = P(html, ST_BULLET)
        w, h = p.wrap(PAGE_W - 70, 80)
        p.drawOn(c, 40, y - h)
        y -= h + 8


def page_credit_card(c):
    draw_header(c, "Category: Credit Card")
    rows = [
        ("1", "Nationality", "Thai"),
        ("2", "Age", "20–70 years (completed). Age is counted to the exact day."),
        (
            "3",
            "Installation address",
            "1. Address on the national ID card<br/>2. Current residential address<br/>3. Other current address (additional supporting documents required)",
        ),
        (
            "4",
            "Mobile number / e-mail<br/>(of the buyer)",
            "Must belong to the hire-purchase customer only. Using another person’s number — including family members — is not allowed in any case.<br/>(If another person’s number is used and a complaint is filed, the company may be fined up to <b>THB 100,000</b> for a PDPA violation.)",
        ),
        (
            "5",
            "Payment method<br/>(credit card)",
            "The card must have at least <b>3 months</b> remaining validity. Physical card or online image is accepted if name, surname, card number and expiry date are clearly visible.<br/>• Credit cards issued by financial institutions in <b>Thailand only</b><br/>• Must be the <b>same card</b> used for the 1st Payment<br/>Shopee, TrueMoney and cash-advance cards are <b>not</b> accepted.",
        ),
        (
            "6",
            "National ID card",
            "• Original ID card, or a certified true copy matching OSMS<br/>• Electronic national ID cards are <b>not</b> accepted in any case<br/>• All information on the ID card must be clearly visible",
        ),
        (
            "7",
            "Name-change document<br/>(if any)",
            "Required when the first name or surname has changed and does not match the credit card name.",
        ),
        (
            "8",
            "Additional documents",
            "Additional documents are required when:<br/>• Card details are unclear (expiry date / cardholder name / card number)<br/>• No credit-card image is attached<br/>• Total monthly installment is <b>THB 6,000/month</b> or more, or more than <b>8 units</b> — request the same documents as Non-Credit customers (installment calculated after promotional discounts)<br/>• Installation at the current address that is a 3rd (or later) address — proof of ownership or relationship is required (e.g. parents, spouse, child, sibling, or same father/mother)",
        ),
        (
            "9",
            "Outstanding payment check",
            "Check AR (outstanding payments)<br/>• Existing customers: no outstanding balance<br/>• Previous overdue <b>2–3</b> times: review the latest <b>6 months</b> (payment must stay current)<br/>• Previous overdue <b>4</b> times: review the latest <b>12 months</b> (payment must stay current)<br/><b>** E-mail LGM by the 15th of every month with the list of customers who have outstanding payments.</b><br/>Unit cap in 11 designated provinces: see the Credit Limit page.",
        ),
        (
            "10",
            "Payment by a third party",
            "Not allowed. Hire-purchase in another person’s name with a promise to pay the installments is also not allowed.",
        ),
    ]
    tbl = criteria_table(rows, [36, 138, 550], font_size=8.2)
    place_flowable(c, tbl, 28, PAGE_H - 58, 724, 466)


def page_non_credit(c):
    draw_header(c, "Category: Non-Credit")
    rows = [
        ("1", "Nationality", "Thai"),
        ("2", "Age", "20–70 years (completed). Age is counted to the exact day."),
        (
            "3",
            "Installation address",
            "1. Address on the national ID card<br/>2. Current residential address<br/>3. Other current address (additional supporting documents required)",
        ),
        (
            "4",
            "Mobile number / e-mail<br/>(of the buyer)",
            "Must belong to the hire-purchase customer only. Using another person’s number — including family members — is not allowed in any case.<br/>(If another person’s number is used and a complaint is filed, the company may be fined up to <b>THB 100,000</b> for a PDPA violation.)",
        ),
        (
            "5",
            "Payment method<br/>(debit card / bank<br/>direct debit)",
            "• Debit cards issued by banks in Thailand only (not cash-advance cards)<br/>• Direct debit via <b>ODD Online</b>: Kasikorn Bank, Bank of Ayudhya (Krungsri), Siam Commercial Bank, and Krungthai Bank<br/>• An automatic direct-debit form is <b>not</b> required",
        ),
        (
            "6",
            "National ID card",
            "• Original ID card, or a certified true copy matching OSMS<br/>• Electronic national ID cards are <b>not</b> accepted in any case<br/>• All information must be clearly visible, with no glare or reflection",
        ),
        (
            "7",
            "Name-change document<br/>(if any)",
            "Required when the first name or surname does not match other documents (e.g. bank book, payslip).",
        ),
        (
            "8",
            "Income documents and<br/>NCB report",
            "Salaried income — submit <b>either</b>:<br/>• Latest monthly payslip (screen captures are not accepted), <b>or</b><br/>• Bank statements for the latest <b>3 consecutive months</b><br/><br/>Self-employed / business owner:<br/>• Bank statements for the latest <b>6 consecutive months</b><br/>• Commercial registration <b>or</b> a photo confirming the occupation<br/><br/>• Monthly income of <b>THB 15,000 or more</b> (average from bank statements)<br/>• Account balance must be at least the <b>total LG monthly installment of every contract</b><br/>• NCB report + Credit Scoring (issued within 60 days)<br/>If the NCB report is requested on paper at the counter, attach the receipt.",
        ),
    ]
    tbl = criteria_table(rows, [36, 138, 550], font_size=8.2)
    place_flowable(c, tbl, 28, PAGE_H - 58, 724, 466)


def product_limit_table():
    header = [P("<b>Product</b>", ST_TH), P("<b>Max units</b>", ST_TH), P("<b>Product</b>", ST_TH), P("<b>Max units</b>", ST_TH)]
    pairs = [
        ("Water purifier", "1", "Air conditioner", "4"),
        ("Refrigerator", "2", "Air purifier", "2"),
        ("Washing machine", "1", "Dehumidifier", "1"),
        ("Dryer", "1", "TV", "2"),
        ("Dishwasher", "1", "SoundBar", "2"),
        ("Styler", "1", "Monitor", "2"),
        ("Vacuum cleaner", "2", "Microwave", "1"),
    ]
    data = [header]
    qty = S("qty", "LG-SB", 8.2, 10.8, BODY, TA_CENTER)
    name = S("pname", "LG", 8.2, 10.8, BODY)
    for a, n1, b, n2 in pairs:
        data.append([P(a, name), P(n1, qty), P(b, name), P(n2, qty)])
    inner = Table(data, colWidths=[130, 50, 130, 50])
    inner.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), TH_BG),
                ("BACKGROUND", (1, 1), (1, -1), HexColor("#F3F3F3")),
                ("BACKGROUND", (3, 1), (3, -1), HexColor("#F3F3F3")),
                ("GRID", (0, 0), (-1, -1), 0.35, GRID),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 0), (1, -1), "CENTER"),
                ("ALIGN", (3, 0), (3, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 1.6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6),
            ]
        )
    )
    return inner


def page_non_credit_2(c):
    draw_header(c, "Category: Non-Credit (continued)")
    ncb_html = (
        "<b>NCB score</b><br/>"
        "• <b>AA – CC</b>: income documents not required (normal account status and no late-payment history)<br/>"
        "• <b>DD – EE</b>: income documents required<br/>"
        "• <b>FF</b>: not accepted<br/><br/>"
        "<b>Not accepted</b><br/>"
        "1. History of debt restructuring<br/>"
        "2. History of NPL sold/transferred and the account is still open<br/>"
        "3. History of written-off debt<br/>"
        "4. History of joining a government relief program that prohibits new debt<br/><br/>"
        "<b>Late-payment watch period</b><br/>"
        "• Overdue <b>31–90 days</b>: review 6 consecutive months of new payment history<br/>"
        "• Overdue <b>more than 90 days</b> (from day 91): review 12 consecutive months<br/><br/>"
        "<b>Accepted under normal review</b><br/>"
        "1. Account closed more than 1 year ago<br/>"
        "2. Late payment on the current billing cycle (must pay first and attach the receipt). Payment slips are not accepted."
    )
    rows = [
        ("9", "NCB credit-grade review", ncb_html),
        (
            "10",
            "Outstanding payment check",
            "Check AR (outstanding payments)<br/>• Existing customers: no outstanding balance<br/>• Previous overdue <b>2–3</b> times: review the latest <b>6 months</b><br/>• Previous overdue <b>4</b> times: review the latest <b>12 months</b><br/>Payment must stay current throughout the review period.",
        ),
        (
            "11",
            "Payment by a third party",
            "Not allowed. Hire-purchase in another person’s name with a promise to pay the installments is also not allowed.",
        ),
        ("12", "Product quantity limit by category", ""),
    ]
    item_style = S("item5", "LG-SB", 8.0, 10.6, BODY)
    cell_style = S("cell5", "LG", 7.9, 10.5, BODY)
    no_style = S("no5", "LG", 8.0, 10.6, BODY, TA_CENTER)
    data = [[P("No", ST_TH), P("Items", ST_TH), P("Criteria", ST_TH)]]
    for no, item, crit in rows:
        if no == "12":
            data.append([P(no, no_style), P(item, item_style), product_limit_table()])
        else:
            data.append([P(no, no_style), P(item, item_style), P(crit, cell_style)])
    tbl = Table(data, colWidths=[36, 138, 550])
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), TH_BG),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, GRID),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("BACKGROUND", (0, 2), (-1, 2), ROW_ALT),
        ("BACKGROUND", (0, 4), (-1, 4), ROW_ALT),
    ]
    tbl.setStyle(TableStyle(cmds))
    place_flowable(c, tbl, 28, PAGE_H - 56, 724, 468)


def page_income(c):
    draw_header(c, "Income Calculation and Installation Address")
    c.setFillColor(TITLE)
    c.setFont("LG-SB", 13.5)
    c.drawString(32, PAGE_H - 72, "How income is calculated")
    rules = [
        "1. Applicant income is based on bank-statement history for the past <b>3 or 6 months</b>.",
        "2. Total debt burden (including LG debt) must not exceed <b>80%</b> of income (DTI not more than 80%).",
        "3. Actual debt burden is calculated from the figures shown in the NCB report.",
        "4. For credit cards on the NCB report, use the <b>minimum payment</b> shown in the NCB report.",
        "5. If there is a co-borrower, divide the debt burden by the number of co-borrowers.",
        "6. For Non-Credit, the account balance must be at least the <b>total LG monthly installment of every contract</b>.",
    ]
    y = PAGE_H - 78
    for html in rules:
        p = P(html, ST_BODY)
        w, h = p.wrap(PAGE_W - 64, 40)
        p.drawOn(c, 32, y - h)
        y -= h + 3

    y -= 10
    tbl = two_col_table(
        [
            (
                P("Installation address<br/>and supporting<br/>documents", ST_ITEM),
                P(
                    "1. Same address as the national ID card<br/>"
                    "2. Current address<br/>"
                    "**************************************************<br/>"
                    "3. 3rd current address (supporting documents required)<br/><br/>"
                    "<b>Documents for installation address #3</b><br/>"
                    "1. Rental contract with rent-payment receipts<br/>"
                    "2. House registration of the applicant or a family member<br/>"
                    "3. Proof of relationship<br/>"
                    "4. Water, electricity or utility bills (mobile-phone bills, credit-card statements and parcel-delivery addresses are <b>not</b> accepted)<br/>"
                    "5. Other documents proving ownership of the residence or a family relationship",
                    ST_CELL,
                ),
            )
        ],
        [160, 560],
    )
    place_flowable(c, tbl, 28, y, 724, y - 28)


def page_limits(c):
    draw_header(c, "Credit Limit and Unit Limit Criteria")
    top = Table(
        [
            [P("No", ST_TH), P("Items", ST_TH), P("Criteria", ST_TH)],
            [P("1.", ST_NO), P("Credit Limit", ST_ITEM), P("<b>THB 6,000 per month</b>", ST_CELL)],
            [P("2.", ST_NO), P("Unit Limit (Memo)", ST_ITEM), P("<b>8 units or more</b>", ST_CELL)],
        ],
        colWidths=[50, 180, 494],
    )
    top.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), TH_BG),
                ("BACKGROUND", (0, 2), (-1, 2), ROW_ALT),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 0.4, GRID),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("ALIGN", (0, 0), (0, -1), "CENTER"),
            ]
        )
    )
    place_flowable(c, top, 28, PAGE_H - 62, 724, 90)

    body = (
        "<b>A. Over THB 6,000 per month and not more than 8 units</b> "
        "(installment calculated after promotional discounts) — reviewed by Credit<br/><br/>"
        "Attach the following additional documents:<br/>"
        "1. NCB report + Credit Scoring<br/>"
        "2. Income documents according to the customer’s occupation (salaried employee or self-employed)<br/><br/>"
        "<b>B. 8 units or more</b> — reviewed by management via Consult<br/><br/>"
        "Attach the following additional documents:<br/>"
        "1. NCB report + Credit Scoring<br/>"
        "2. Income documents according to the customer’s occupation (salaried employee or self-employed)<br/>"
        "3. Prepare a Memo requesting approval from management"
    )
    bottom = two_col_table(
        [(P("Credit Card and<br/>Non-Credit", ST_ITEM), P(body, ST_CELL))],
        [160, 564],
    )
    place_flowable(c, bottom, 28, PAGE_H - 158, 724, 168)
    province = (
        "<b>11 designated provinces — individual customers only, not Corporate Customers.</b> "
        "Maximum <b>2 units per person</b>: Sa Kaeo, Chanthaburi, Chaiyaphum, Nong Khai, Bueng Kan, "
        "Nong Bua Lam Phu, Kanchanaburi, Phatthalung, Phayao, Nan, and Sukhothai.<br/>"
        "Good payment history with the company for more than <b>6 months</b>: 1 extra unit (3 in total). "
        "More than <b>12 months</b>: 2 extra units (4 in total).<br/>"
        "Everywhere else stays at THB 6,000 per month and 8 units per person."
    )
    box = two_col_table(
        [(P("Designated provinces", ST_ITEM), P(province, ST_CELL))],
        [160, 564],
    )
    place_flowable(c, box, 28, PAGE_H - 336, 724, 150)


def page_foreigner(c):
    draw_header(c, "Category: Foreign Nationals")
    rows = [
        ("1", "Nationality", "Foreign national — all countries"),
        ("2", "Age", "20–60 years (completed)"),
        ("3", "Delivery / installation address", "Residential address (as stated in the rental contract)"),
        (
            "4",
            "Mobile number / e-mail<br/>(of the buyer)",
            "Must belong to the hire-purchase customer only. Using another person’s number — including family members — is not allowed in any case.<br/>(If another person’s number is used and a complaint is filed, the company may be fined up to <b>THB 100,000</b> for a PDPA violation.)",
        ),
        (
            "5",
            "Payment method",
            "The card must have at least <b>3 years</b> remaining validity (foreign nationals). Credit cards issued by financial institutions in <b>Thailand only</b>.",
        ),
        ("6", "Work Permit and passport", "• Work Permit / Passport"),
        (
            "7",
            "Installation documents",
            "• Proof of installation address, e.g. rental contract, proof of ownership, proof of relationship<br/>• Immigration (TM) address documents are <b>not</b> accepted",
        ),
        ("8", "Debit card / cash / bank transfer", "Cannot be used for payment"),
        (
            "9",
            "Payment by a third party",
            "Not allowed. Hire-purchase in another person’s name with a promise to pay the installments is also not allowed.",
        ),
    ]
    tbl = criteria_table(rows, [36, 168, 520], font_size=8.6)
    place_flowable(c, tbl, 28, PAGE_H - 58, 724, 466)


def page_juristic(c):
    draw_header(c, "Category: Thai Juristic Person")
    th = S("jth", "LG-SB", 9.2, 12, TITLE, TA_CENTER)
    item = S("jitem", "LG-SB", 8.2, 11, BODY)
    cell = S("jcell", "LG", 8.2, 11, BODY)
    no = S("jno", "LG", 8.2, 11, BODY, TA_CENTER)
    data = [
        [P("No", th), P("Items", th), P("Conditions", th)],
        [
            P("1.1<br/>1.2", no),
            P(
                "Copy of company affidavit (not older than 6 months)<br/>"
                "Every page signed by the authorized director(s) of the juristic person, with company seal<br/><br/>"
                "VAT certificate (Por Por 20)",
                item,
            ),
            P(
                "The business must have been operating for at least <b>2 years</b><br/>"
                "• Operating at a profit<br/>"
                "Sales contracts with non-profit organizations are <b>not</b> allowed",
                cell,
            ),
        ],
        [
            P("2", no),
            P("Copy of national ID (owner or authorized person)<br/>or passport (if a foreign national)", item),
            P("Required", cell),
        ],
        [P("3", no), P("Photos of the place of business and a map", item), P("Place of business", cell)],
        [
            P("4", no),
            P("Mobile number / e-mail<br/>(of the buyer)", item),
            P(
                "Must belong to the hire-purchase customer, or a person authorized to act for the company. Using another person’s number is not allowed in any case.",
                cell,
            ),
        ],
        [
            P("5", no),
            P("Order placed by an authorized representative", item),
            P(
                "1. Must be approved by the company’s authorized person<br/>(attach a power of attorney and a copy of the representative’s national ID)",
                cell,
            ),
        ],
        [
            P("6.<br/>6.1<br/>6.2", no),
            P(
                "Payment method<br/>Billing / bank transfer / credit card<br/><br/>"
                "Credit card of an authorized director per the company affidavit, or a company-name credit card",
                item,
            ),
            P(
                "• Request the company’s billing details: name, phone, e-mail, billing date, and billing address<br/>"
                "• Credit card of an authorized director per the company affidavit / company-name credit card",
                cell,
            ),
        ],
        [
            P("7.", no),
            P("Delivery / installation address", item),
            P(
                "1. Address on the company affidavit<br/>"
                "2. Company (branch) address — additional proof of branch registration or VAT certificate (Por Por 20) is required<br/>"
                "Installation remains at the place of business. A director’s private home is not accepted.<br/><br/>"
                "<b>Outstanding AR:</b> no current overdue. Overdue 2–3 times: review the latest 6 months. Overdue 4 times: review the latest 12 months. Payment must stay current.<br/>"
                "An order of <b>9 units or more in one order</b> is a Corporate Customer (next page).<br/><br/>"
                "<b>A third party’s credit card cannot be used for payment in any case.</b>",
                cell,
            ),
        ],
    ]
    tbl = Table(data, colWidths=[50, 250, 424])
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), TH_BG),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, GRID),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            cmds.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
    tbl.setStyle(TableStyle(cmds))
    place_flowable(c, tbl, 28, PAGE_H - 56, 724, 468)


def banner(c, x, y, w, h, text):
    c.setFillColor(BANNER)
    c.roundRect(x, y, w, h, 3, fill=1, stroke=0)
    p = P(text, ST_BANNER)
    pw, ph = p.wrap(w - 24, h)
    p.drawOn(c, x + 14, y + (h - ph) / 2)


def page_corporate_def(c):
    draw_header(c, "Category: Thai Juristic Person (Corporate Customer)")
    banner(c, 80, PAGE_H - 112, 620, 40, 'Clause 3  —  Definition of "Corporate Customer"')
    y = PAGE_H - 134
    p = P(
        "<font color='#C8102E'><b>①</b></font>  A customer qualifies as a <b>Corporate Customer</b> only if <b>both</b> of the following are met:",
        ST_BODY,
    )
    w, h = p.wrap(620, 40)
    p.drawOn(c, 88, y - h)
    y -= h + 4
    for line in [
        '1. The organization can submit the corporate-customer qualification documents required under the Credit Control policy.',
        "2. The customer enters into a membership hire-purchase contract for <b>9 units or more (Contract)</b> in a single order.",
    ]:
        p = P(line, ST_BODY)
        w, h = p.wrap(600, 36)
        p.drawOn(c, 100, y - h)
        y -= h + 2
    y -= 4
    p = P(
        "<font color='#C8102E'><b>②</b></font>  Unit count includes <b>all product categories combined</b>. Products do not need to be the same type.",
        ST_BODY,
    )
    w, h = p.wrap(620, 40)
    p.drawOn(c, 88, y - h)
    y -= h + 8

    c.setFillColor(SOFT)
    c.roundRect(88, y - 72, 604, 72, 4, fill=1, stroke=0)
    p = P("<b>Example</b>", ST_EX_T)
    pw, ph = p.wrap(580, 18)
    p.drawOn(c, 100, y - 20)
    p = P(
        "6 water purifiers + 3 air purifiers = <b>9 units in total</b><br/>"
        "(Different product types are still counted together, so this meets the Corporate Customer threshold.)",
        ST_EX,
    )
    pw, ph = p.wrap(580, 44)
    p.drawOn(c, 100, y - 20 - ph - 4)
    y -= 88

    banner(c, 80, y - 40, 620, 40, "Clause 5  —  Installation-site conditions")
    y -= 54
    clauses = [
        (
            "①",
            "The installation site is limited to the place of business, building, or area that the contracting Corporate Customer owns or leases directly. "
            "Installation at a location registered in another person’s name is not allowed — e.g. an employee’s private residence or the office of an affiliated company.",
        ),
        (
            "②",
            "If paragraph 1 is met, the customer may split installation across multiple sites (see permitted-site examples in <b>[Appendix Table 1]</b>).",
        ),
        (
            "③",
            "If after signing it turns out that some sites cannot be installed, and the number of units actually installed falls below 9, request approval under Clause 10 (exception approval). "
            "The company reserves the right to inspect readiness and feasibility of the installation area.",
        ),
        (
            "④",
            "The contract term follows the membership service terms and conditions.",
        ),
    ]
    for num, text in clauses:
        p = P(f"<font color='#C8102E'><b>{num}</b></font>  {text}", ST_BODY_SM)
        w, h = p.wrap(620, 70)
        p.drawOn(c, 88, y - h)
        y -= h + 5


def page_appendix(c):
    draw_header(c, "Category: Thai Juristic Person (Corporate Customer)")
    c.setFillColor(BANNER)
    c.roundRect(70, PAGE_H - 132, 640, 60, 3, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("LG-B", 14)
    c.drawString(88, PAGE_H - 98, "[Appendix Table 1]  Examples of permitted installation sites")
    c.setFont("LG", 11.5)
    c.drawString(88, PAGE_H - 118, "(for Thailand)")

    head = S("ah", "LG-SB", 8.6, 11.4, white, TA_LEFT)
    cell = S("ac", "LG", 8.4, 11.4, BODY)
    cell_no = S("an", "LG", 8.4, 11.4, HexColor("#7A0018"))
    rows = [
        [
            P("<b>Organization type</b>", head),
            P("<b>Examples of permitted sites</b>", head),
            P("<b>Examples of sites not permitted</b>", head),
        ],
        [
            P("Juristic person /<br/>private company", cell),
            P("HQ, branch, factory, distribution center (warehouse), registered shopfront", cell),
            P("Private home of an employee / executive / company director", cell_no),
        ],
        [
            P("Educational institution", cell),
            P("Main campus, satellite campus, academic building, dormitory operated by the institution", cell),
            P("Private home of a teacher / lecturer / education staff member", cell_no),
        ],
        [
            P("Government agency /<br/>state enterprise", cell),
            P("Department/division (central), regional office, public service center, district office", cell),
            P("Private home of a civil servant / state-enterprise employee", cell_no),
        ],
        [
            P("Healthcare facility", cell),
            P("Main hospital, branch hospital, health-check center, clinic in the network", cell),
            P("Private home of a doctor / nurse / medical staff member", cell_no),
        ],
        [
            P("Other organizations<br/>(foundation, association, etc.)", cell),
            P("Place of business, building, or area that the organization owns or leases and operates legally", cell),
            P("Office of a partner company; site of an affiliated company (registered as a different juristic person)", cell_no),
        ],
    ]
    tbl = Table(rows, colWidths=[150, 255, 235])
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), BANNER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#E0B8C0")),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("BACKGROUND", (0, 2), (-1, 2), HexColor("#FFF8F8")),
        ("BACKGROUND", (0, 4), (-1, 4), HexColor("#FFF8F8")),
    ]
    tbl.setStyle(TableStyle(cmds))
    place_flowable(c, tbl, 70, PAGE_H - 140, 640, 270)

    notes = [
        '1. Examples in this table are a starting guideline only. Actual site approval follows Clause 5 paragraph 1: the site must be owned or legally leased by the contracting organization.',
        "2. Even if the department or on-site unit name differs from this table, installation is allowed if it can be proven that Clause 5 paragraph 1 is met.",
    ]
    y = 118
    for t in notes:
        p = P(t, ST_BODY_SM)
        w, h = p.wrap(640, 40)
        p.drawOn(c, 70, y - h)
        y -= h + 4


FAQ_EN = [
    ("Credit card / card image", "A damaged card hides some details. Can an in-app image be sent instead?", "Yes, if the name, expiry year, and card number are clearly visible."),
    ("Credit card / card image", "Can an online credit card be used to order?", "Yes, if the name, expiry date, and card number are clearly visible."),
    ("Credit card / card image", "Are Shopee Pay and TrueMoney Wallet accepted?", "No. TrueMoney Mastercard is a prepaid card, and Shopee Pay Unlimited is prepaid wallet credit, not a credit card."),
    ("Credit card / card image", "Can an individual use a corporate card or someone else’s card?", "No. The customer must use their own credit card."),
    ("Credit card / card image", "Can a foreign national use a card issued by a foreign bank?", "No. The card must be issued by a financial institution in Thailand, with at least 3 years of validity remaining."),
    ("Credit card / card image", "The customer already has 8 credit-card contracts. Can they order more?", "Yes, in two ways: close some accounts so the total does not exceed 8, or submit additional income documents under the criteria."),
    ("Documents / income", "3rd installation address: the husband buys and installs at the wife’s house. They are not legally married. What is required?", "A copy of the child’s birth certificate. If there is no child, another document must show they are spouses, such as a house registration that includes the wife’s name."),
    ("Documents / income", "Can a foreign national buy without renewing the Work Permit?", "No. The Work Permit must be renewed, and the renewal date must be clear."),
    ("Documents / income", "Non-Credit income is below the threshold. Can other income be attached?", "Yes, if there is a side occupation or extra income. Use a statement that shows incoming transfers from that source."),
    ("Documents / income", "Additional documents are needed, but more than 15 days have passed. What should be done?", "E-mail Credit with the reason for requesting On Hold beyond 15 days."),
    ("Documents / income", "Can an existing customer change the payment method?", "No. The payment method cannot be changed."),
    ("Documents / income", "The product is not installed yet. Can the installation site be moved?", "Yes, if the new site meets the company’s criteria."),
    ("Documents / income", "The customer is self-employed and has no tax documents. What can replace them?", "Commercial registration or proof of occupation, such as photos of the business, income documents from Shopee, LINE MAN, or Grab, or a statement with regular incoming transfers."),
    ("Documents / income", "Can income from a spouse or child be used?", "No. It is not income backed by an employment contract or a definite legal guarantee."),
    ("Documents / income", "The signature on the ID copy does not match the system, and the customer does not want to resend it. Can it be approved?", "No. The ID copy is the document that confirms the customer placed the order in person."),
    ("Documents / income", "A refund was e-mailed to Credit but was not recorded in the DST file. Can Credit refund it?", "No. Recording the file is the step that collects the refund evidence."),
    ("Documents / income", "The installation document is a rented house, dormitory, or flat, but there is no rent receipt.", "Credit reviews the rental contract. If it is not credible, extra documents are requested, such as a rent-transfer slip, or the customer is asked to obtain a receipt."),
    ("Documents / income", "How is the age range of 20–70 years counted?", "Age is completed to the exact day, based on the order date."),
    ("Documents / income", "The Work Permit expires in one month. Does that affect approval?", "The customer should renew the Work Permit."),
    ("Documents / income", "Why are extra documents required above THB 6,000 or above 8 units?", "To assess ability to pay, comparing income with existing debt plus the new LG installment, and to confirm that the income is real."),
    ("Ordering", "Can more than one Wash Tower be ordered?", "Yes, under normal review of ability to pay. The customer must use it themselves. Resale or transfer is not allowed."),
    ("Ordering", "Can one person order in another person’s name?", "Not approved in any case. The hire-purchase customer remains responsible until the contract is fully paid."),
    ("Ordering", "The site belongs to a relative who lets the customer stay for free. There is no rental contract and the surnames differ. Can they order?", "No. A document that clearly links the relationship is required."),
    ("Ordering", "Can a spouse’s or child’s phone number be used?", "No. The number must belong to the hire-purchase customer. Another number may be added as an extra contact."),
    ("Ordering", "Can an order exceed the Credit Limit or Unit Limit?", "Yes, but additional income documents under the criteria must be attached, and the company reviews the case again."),
    ("NCB / payment history", "The customer joined a government debt-holiday program that prohibits new debt. Can they order?", "No, under the measure that prohibits new debt."),
    ("NCB / payment history", "Credit score is AA, BB, or CC. What documents are required?", "Income documents are not required. Credit still reviews the case."),
    ("NCB / payment history", "The current NCB account is overdue and a default has started. What should be done?", "The case can be sent to Credit. Extra documents, such as a payment receipt, may be requested."),
    ("NCB / payment history", "An existing customer still has an outstanding balance. Can they order?", "The account must be brought current first. Credit then reviews the new order."),
    ("NCB / payment history", "NCB shows late payment of more than 300 days, and the account was closed less than 1 year ago. Can they buy?", "No. The account must have been closed for at least 1 year."),
    ("Juristic person", "What counts as a non-profit organization?", "Examples: a social-welfare foundation, a charity hospital, and a religious institution."),
    ("Juristic person", "The juristic person has operated for more than 2 years but does not submit financial statements. Is that accepted?", "No. Annual financial statements are required, and tax must be filed as required by law."),
    ("Juristic person", "Can a company order for installation at a director’s home?", "No. Installation must be at the company’s established premises."),
    ("Juristic person", "The company authorizes a buyer to order. What documents are required?", "1) The normal juristic-person documents. 2) One power of attorney that states the authority clearly. 3) ID copies of the person granting authority and the person receiving it."),
]


def page_faq(c, chunk, page_no, page_count):
    draw_header(c, f"FAQ  01/10/2026   ({page_no}/{page_count})")
    qstyle = S(f"faq-q-{page_no}", "LG", 7.6, 9.8, BODY)
    astyle = S(f"faq-a-{page_no}", "LG", 7.6, 9.8, BODY)
    hstyle = S(f"faq-h-{page_no}", "LG-SB", 8.2, 10.6, TITLE, TA_CENTER)
    data = [[P("Topic", hstyle), P("Question", hstyle), P("Answer", hstyle)]]
    for topic, question, answer in chunk:
        data.append([P(topic, qstyle), P(question, qstyle), P(answer, astyle)])
    tbl = Table(data, colWidths=[118, 300, 306])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TH_BG),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.35, GRID),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("BACKGROUND", (0, 2), (-1, 2), ROW_ALT),
        ("BACKGROUND", (0, 4), (-1, 4), ROW_ALT),
        ("BACKGROUND", (0, 6), (-1, 6), ROW_ALT),
    ]))
    place_flowable(c, tbl, 22, PAGE_H - 56, 736, 460)


def main():
    PAGES_EN.mkdir(exist_ok=True)
    c = canvas.Canvas(str(OUT_PDF), pagesize=(PAGE_W, PAGE_H))
    pages = [
        cover,
        page_hours,
        page_credit_card,
        page_non_credit,
        page_non_credit_2,
        page_income,
        page_limits,
        page_foreigner,
        page_juristic,
        page_corporate_def,
        page_appendix,
    ]
    faq_size = 7
    faq_chunks = [FAQ_EN[i:i + faq_size] for i in range(0, len(FAQ_EN), faq_size)]
    for i, fn in enumerate(pages):
        fn(c)
        c.showPage()
    for n, chunk in enumerate(faq_chunks, 1):
        page_faq(c, chunk, n, len(faq_chunks))
        if n < len(faq_chunks):
            c.showPage()
    c.save()
    print("wrote", OUT_PDF)

    from pypdf import PdfReader, PdfWriter

    reader = PdfReader(str(OUT_PDF))
    for i, page in enumerate(reader.pages, 1):
        w = PdfWriter()
        w.add_page(page)
        dest = PAGES_EN / f"page-{i:02d}.pdf"
        with dest.open("wb") as f:
            w.write(f)
        print("split", dest.name)


if __name__ == "__main__":
    main()
