"""Generate a fictional resume on the measured reference-template grid."""

import os
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "sanitized-sample-resume.pdf"
AVATAR = ROOT / "assets/synthetic-avatar.png"
FONT_DIR = Path(
    os.environ.get(
        "ALIBABA_PUHUITI_DIR",
        ROOT.parent / "assets" / "fonts" / "AlibabaPuHuiTi-3",
    )
)
FONT_REGULAR = FONT_DIR / "AlibabaPuHuiTi-3-55-Regular" / "AlibabaPuHuiTi-3-55-Regular.ttf"
FONT_BOLD = FONT_DIR / "AlibabaPuHuiTi-3-85-Bold" / "AlibabaPuHuiTi-3-85-Bold.ttf"

PAGE_W, PAGE_H = A4
GRID_SCALE = 0.75
PAGE_GRID_H = 1122.5
GRID_MARGIN = 32
GRID_RIGHT = 761.7
TEXT = HexColor("#333333")
MUTED = HexColor("#666666")
DIVIDER = HexColor("#D9D9D9")

if not FONT_REGULAR.is_file() or not FONT_BOLD.is_file():
    raise FileNotFoundError(
        "Official Alibaba PuHuiTi is required. Run: "
        "python3 scripts/install_alibaba_puhuiti.py"
    )

pdfmetrics.registerFont(TTFont("SampleRegular", str(FONT_REGULAR)))
pdfmetrics.registerFont(TTFont("SampleBold", str(FONT_BOLD)))


def point(value):
    return value * GRID_SCALE


def page_y(grid_y, page_index):
    return PAGE_H - point(grid_y - PAGE_GRID_H * page_index)


def draw(c, page, x, grid_y, value, size=13, bold=False, color=TEXT, align="left"):
    c.setFillColor(color)
    c.setFont("SampleBold" if bold else "SampleRegular", point(size))
    x = point(x)
    y = page_y(grid_y, page)
    if align == "right":
        c.drawRightString(x, y, value)
    elif align == "center":
        c.drawCentredString(x, y, value)
    else:
        c.drawString(x, y, value)


def width(value, size=13, bold=False):
    return pdfmetrics.stringWidth(value, "SampleBold" if bold else "SampleRegular", point(size))


def wrap(value, size=13, max_width=GRID_RIGHT - GRID_MARGIN, bold=False):
    lines, line = [], ""
    for char in value:
        candidate = line + char
        if width(candidate, size, bold) <= point(max_width):
            line = candidate
        else:
            if line:
                lines.append(line)
            line = char
    if line:
        lines.append(line)
    return lines


def assert_line_count(lines, expected, context):
    if len(lines) != expected:
        raise ValueError(f"{context} requires {expected} lines, got {len(lines)}: {lines}")


def paragraph(c, page, grid_y, value, size=13, leading=24, expected_lines=None, context="paragraph"):
    lines = wrap(value, size)
    if expected_lines is not None:
        assert_line_count(lines, expected_lines, context)
    for line in lines:
        draw(c, page, GRID_MARGIN, grid_y, line, size)
        grid_y += leading
    return grid_y


def inline(c, page, grid_y, label, value, expected_lines=1, context="inline"):
    label_width = width(label, 13, True)
    first_width = point(GRID_RIGHT - GRID_MARGIN) - label_width - point(6)
    first, remainder = "", value
    for index, char in enumerate(value):
        candidate = first + char
        if width(candidate, 13) <= first_width:
            first = candidate
            remainder = value[index + 1 :]
        else:
            break
    draw(c, page, GRID_MARGIN, grid_y, label, 13, bold=True)
    c.setFillColor(TEXT)
    c.setFont("SampleRegular", point(13))
    c.drawString(point(GRID_MARGIN) + label_width + point(6), page_y(grid_y, page), first)
    lines = [first] + wrap(remainder, 13) if remainder else [first]
    assert_line_count(lines, expected_lines, context)
    for index, line in enumerate(lines[1:], start=1):
        draw(c, page, GRID_MARGIN, grid_y + index * 24, line, 13)
    return grid_y + expected_lines * 24


def divider(c, page, grid_y):
    c.setStrokeColor(DIVIDER)
    c.setLineWidth(0.35)
    c.line(point(GRID_MARGIN), page_y(grid_y, page), point(GRID_RIGHT), page_y(grid_y, page))


def section(c, page, title, grid_y):
    draw(c, page, GRID_MARGIN, grid_y, title, 20, bold=True, color=HexColor("#111111"))
    divider(c, page, grid_y + 15)


def entry(c, page, grid_y, name, role, date, role_x):
    draw(c, page, GRID_MARGIN, grid_y, name, 16, bold=True)
    draw(c, page, role_x, grid_y, role, 13)
    draw(c, page, GRID_RIGHT, grid_y, date, 13, color=MUTED, align="right")


def background(c, page):
    c.setFillColor(HexColor("#FFFFFF"))
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)


def header(c):
    # Measured from the reference render: x=663, y=33, 98 x 98 grid units.
    photo_size = point(98)
    c.drawImage(
        str(AVATAR),
        point(663),
        PAGE_H - point(33) - photo_size,
        width=photo_size,
        height=photo_size,
        mask="auto",
    )
    center = 329
    draw(c, 0, center, 63, "林知夏", 30, bold=True, color=HexColor("#000000"), align="center")
    draw(c, 0, center, 99, "女 | 年龄：29岁 | 138 0000 0000", 13, align="center")
    draw(c, 0, center, 123, "6年工作经验 | 求职意向：工业软件产品设计 | 期望薪资：15-18K | 期望城市：杭州", 13, align="center")


def page_one(c):
    background(c, 0)
    header(c)

    section(c, 0, "个人优势", 175)
    draw(c, 0, GRID_MARGIN, 216, "B端产品与业务梳理能力：", 13, bold=True)
    paragraph(c, 0, 240, "面向生产、设备和仓储等场景，梳理用户任务、业务规则和操作路径，结合现场访谈与反馈持续校正，将复杂需求转化为清晰可执行的产品方案。", expected_lines=2, context="优势一")
    draw(c, 0, GRID_MARGIN, 288, "产品体验与界面设计：", 13, bold=True)
    paragraph(c, 0, 312, "关注企业软件的信息层级、异常反馈和操作效率，能够完成原型、界面方案及关键交互细节设计。", expected_lines=1, context="优势二")
    draw(c, 0, GRID_MARGIN, 336, "设计规范与协作：", 13, bold=True)
    paragraph(c, 0, 360, "使用Figma完成组件复用、标注和评审协作，推动多模块界面风格统一并提高开发还原效率。", expected_lines=1, context="优势三")
    draw(c, 0, GRID_MARGIN, 384, "AI与低代码验证：", 13, bold=True)
    paragraph(c, 0, 408, "使用AI工具辅助需求拆解、方案表达和MVP验证，具备低代码配置及企业客户培训支持经验。", expected_lines=1, context="优势四")

    section(c, 0, "工作经历", 464)
    entry(c, 0, 506, "云帆工业软件（示例）有限公司", "UI/产品设计", "2020.03-至今", 310)
    inline(c, 0, 535, "主导产品体验设计：", "负责设备管理、生产协同和数据看板等B端模块的需求梳理、交互原型与界面方案设计。", context="工作一")
    inline(c, 0, 559, "设计规范与交付：", "建立表单、表格和状态反馈等常用组件规范，配合研发完成评审、联调与验收，并输出可复用的标注与交付材料。", expected_lines=2, context="工作二")
    inline(c, 0, 607, "客户场景支持：", "整理现场业务流程和交付材料，支持方案演示、问题收集与迭代优化。", context="工作三")
    inline(c, 0, 631, "跨团队协同：", "与研发、测试和实施团队保持沟通，推动需求按计划落地并持续优化关键流程。", context="工作四")

    section(c, 0, "项目经历", 687)
    entry(c, 0, 729, "智能设备管理平台（示例项目）", "交互设计师&PM", "2024.04-2025.02", 348)
    draw(c, 0, GRID_MARGIN, 757, "内容：", 14, bold=True)
    inline(c, 0, 780, "项目背景：", "面向制造现场的设备资产与维保管理系统，覆盖台账、点检、维保、请购和异常预警业务。", context="项目一背景")
    inline(c, 0, 804, "核心要素：", "梳理设备从采购、领用、点检、维保到报废的完整闭环，完成监控看板、审批、资产评估和预警推送等模块设计，并明确异常状态、责任人和处理时效。", expected_lines=2, context="项目一行动")
    draw(c, 0, GRID_MARGIN, 857, "业绩：", 14, bold=True)
    paragraph(c, 0, 880, "完成核心模块原型与界面方案，支持客户演示、研发联调和现场验证。", expected_lines=1, context="项目一业绩")

    entry(c, 0, 927, "制造执行协同系统（示例项目）", "产品体验设计", "2023.03-2024.03", 305)
    draw(c, 0, GRID_MARGIN, 955, "内容：", 14, bold=True)
    inline(c, 0, 978, "项目背景：", "为生产计划、工单执行和异常反馈提供统一的任务协同与数据追溯入口。", context="项目二背景")
    inline(c, 0, 1002, "设计行动：", "围绕计划、执行、异常和复盘场景梳理信息架构，设计列表、详情、筛选、状态反馈和问题闭环机制，并将关键节点沉淀为可复用的页面与交互规则。", expected_lines=2, context="项目二行动")
    draw(c, 0, GRID_MARGIN, 1079, "业绩：", 14, bold=True)
    paragraph(c, 0, 1102, "形成可复用的界面规范，支撑多个业务模块同步开发和交付。", expected_lines=1, context="项目二业绩")


def page_two(c):
    background(c, 1)
    entry(c, 1, 1163, "企业AI应用配置平台（示例项目）", "产品设计", "2022.05-2023.02", 332)
    draw(c, 1, GRID_MARGIN, 1191, "内容：", 14, bold=True)
    inline(c, 1, 1214, "项目背景：", "面向企业内部知识问答和应用配置需求，提供内容管理、流程配置、权限设置及客户培训支持。", context="项目三背景")
    inline(c, 1, 1238, "设计行动：", "参与需求访谈和原型设计，梳理知识录入、应用发布、权限配置、使用反馈及运营复盘流程，并整理企业客户培训、配置说明和常见问题处理指引。", expected_lines=2, context="项目三行动")
    draw(c, 1, GRID_MARGIN, 1291, "业绩：", 14, bold=True)
    paragraph(c, 1, 1314, "支持多个方案演示与内部试点，沉淀常见场景的配置说明和交付素材。", expected_lines=1, context="项目三业绩")

    section(c, 1, "教育经历", 1370)
    entry(c, 1, 1412, "示例科技大学", "本科  交互设计", "2016-2020", 202)


def main():
    c = canvas.Canvas(str(OUTPUT), pagesize=A4, pageCompression=1)
    c.setTitle("Sanitized Sample Resume")
    c.setAuthor("Resume PDF Template")
    c.setCreator("Resume PDF Template")
    c.setSubject("Fictional sample for layout reference only")
    page_one(c)
    c.showPage()
    page_two(c)
    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    main()
