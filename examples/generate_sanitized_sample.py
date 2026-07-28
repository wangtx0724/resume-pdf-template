"""Build a fully fictional two-page resume that demonstrates this skill's layout."""

from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "sanitized-sample-resume.pdf"
AVATAR = ROOT / "assets/synthetic-avatar.png"
FONT_REGULAR = "/System/Library/Fonts/STHeiti Light.ttc"
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"

PAGE_W, PAGE_H = A4
MARGIN = 24
TEXT = HexColor("#252525")
MUTED = HexColor("#555555")
DIVIDER = HexColor("#D9D9D9")

pdfmetrics.registerFont(TTFont("SampleRegular", FONT_REGULAR))
pdfmetrics.registerFont(TTFont("SampleBold", FONT_BOLD))


def y(top):
    return PAGE_H - top


def draw_text(c, x, top, value, size=8.3, bold=False, color=TEXT, align="left"):
    c.setFillColor(color)
    c.setFont("SampleBold" if bold else "SampleRegular", size)
    if align == "right":
        c.drawRightString(x, y(top), value)
    elif align == "center":
        c.drawCentredString(x, y(top), value)
    else:
        c.drawString(x, y(top), value)


def wrap(value, size, width, bold=False):
    font_name = "SampleBold" if bold else "SampleRegular"
    lines, current = [], ""
    for char in value:
        candidate = current + char
        if pdfmetrics.stringWidth(candidate, font_name, size) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = char
    if current:
        lines.append(current)
    return lines


def paragraph(c, value, top, size=8.2, leading=13, color=TEXT):
    for line in wrap(value, size, PAGE_W - MARGIN * 2):
        draw_text(c, MARGIN, top, line, size=size, color=color)
        top += leading
    return top


def section(c, title, top):
    draw_text(c, MARGIN, top, title, size=13.2, bold=True, color=HexColor("#111111"))
    c.setStrokeColor(DIVIDER)
    c.setLineWidth(0.35)
    c.line(MARGIN, y(top + 11), PAGE_W - MARGIN, y(top + 11))
    return top + 28


def entry(c, name, role, date, top):
    draw_text(c, MARGIN, top, name, size=10.1, bold=True)
    name_width = pdfmetrics.stringWidth(name, "SampleBold", 10.1)
    draw_text(c, min(MARGIN + name_width + 16, 350), top + 1, role, size=8.2)
    draw_text(c, PAGE_W - MARGIN, top + 1, date, size=8.2, color=MUTED, align="right")
    return top + 22


def label(c, value, top):
    draw_text(c, MARGIN, top, value, size=8.5, bold=True)
    return top + 14


def advantage(c, title, body, top):
    draw_text(c, MARGIN, top, title, size=8.5, bold=True)
    top += 13
    top = paragraph(c, body, top)
    return top + 5


def project(c, name, role, date, background, actions, result, top):
    top = entry(c, name, role, date, top)
    top = label(c, "内容：", top)
    top = label(c, "项目背景：", top)
    top = paragraph(c, background, top)
    top = label(c, "设计行动：", top + 2)
    for action in actions:
        top = paragraph(c, action, top)
    top = label(c, "业绩：", top + 2)
    top = paragraph(c, result, top)
    return top + 16


def header(c):
    c.drawImage(str(AVATAR), 497, PAGE_H - 25 - 49, width=49, height=49, mask="auto")
    center_x = 246.7
    draw_text(c, center_x, 48, "林知夏", size=17.5, bold=True, color=HexColor("#000000"), align="center")
    draw_text(c, center_x, 75, "女 | 年龄：29岁 | 138 0000 0000", size=8.3, align="center")
    draw_text(c, center_x, 91, "6年工作经验 | 求职意向：工业软件产品设计 | 期望薪资：15-18K | 期望城市：杭州", size=8.0, align="center")


def page_one(c):
    c.setFillColor(HexColor("#FFFFFF"))
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    header(c)
    top = section(c, "个人优势", 130)
    top = advantage(c, "B端产品与业务梳理：", "具备制造业软件项目经验，能够理解生产、设备与仓储场景，梳理用户任务、功能边界、页面结构和交互路径。", top)
    top = advantage(c, "产品体验与界面设计：", "熟悉企业软件的信息层级与操作效率设计，关注原型细节、异常反馈、数据表达和多角色协同体验。", top)
    top = advantage(c, "设计规范与协作：", "使用Figma建立页面规范和组件复用方式，配合研发完成标注、评审与验收，提升多模块交付的一致性。", top)
    top = advantage(c, "AI与低代码验证：", "使用AI工具辅助需求拆解、方案表达和MVP验证，具备基础低代码配置及企业客户培训支持经验。", top)

    top = section(c, "工作经历", top + 14)
    top = entry(c, "云帆工业软件（示例）有限公司", "UI/产品设计", "2020.03-至今", top)
    for value in [
        "负责设备管理、生产协同和数据看板等B端模块的需求梳理、交互原型与界面方案设计。",
        "面向客户现场场景，整理业务流程与功能规则，输出产品原型、页面说明和交付支持材料。",
        "协同研发、测试和实施团队推进评审、联调与验收，持续根据使用反馈优化关键流程。",
    ]:
        top = paragraph(c, value, top)
    top = section(c, "项目经历", top + 17)
    top = project(
        c,
        "智能设备管理平台（示例项目）",
        "交互设计师&PM",
        "2024.04-2025.02",
        "面向制造现场的设备资产与维保管理系统，覆盖设备台账、状态监控、点检维保、请购审批和异常预警等业务。",
        [
            "梳理设备从采购、领用、点检、维保到报废的全流程，明确多角色操作路径与状态规则。",
            "完成设备监控看板、审批流程、资产评估和治工具管理等核心页面的原型与交互设计。",
        ],
        "完成核心模块的方案与界面交付，支持现场演示、研发联调及后续迭代。",
        top,
    )
    project(
        c,
        "制造执行协同系统（示例项目）",
        "产品体验设计",
        "2023.03-2024.03",
        "为生产计划、工单执行和异常反馈提供统一的任务协同与数据追溯入口。",
        [
            "围绕计划、执行、异常和复盘场景梳理信息架构，设计列表、详情、筛选和状态反馈机制。",
            "输出高保真原型与研发标注，建立常用表单、表格和反馈组件的使用规则。",
        ],
        "形成可复用的界面规范，支撑多个业务模块同步开发和交付。",
        top,
    )


def page_two(c):
    c.setFillColor(HexColor("#FFFFFF"))
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    project(
        c,
        "企业AI应用配置平台（示例项目）",
        "产品设计",
        "2022.05-2023.02",
        "面向企业内部知识问答和应用配置需求，提供内容管理、流程配置、权限设置及客户培训支持。",
        [
            "参与需求访谈和原型设计，梳理知识录入、应用发布、权限配置与使用反馈的流程。",
            "协助制作培训材料与演示Demo，配合客户完成试用、问题收集和方案优化。",
        ],
        "支持多个方案演示与内部试点，沉淀常见场景的配置说明和交付素材。",
        43,
    )
    top = section(c, "专业技能", 252)
    for value in [
        "产品设计：Figma、需求梳理、信息架构、交互原型、设计规范、组件库、数据看板",
        "工业软件：MES、EPMS、WMS、设备预防维护、生产协同、设备与治工具管理",
        "AI与低代码：AI辅助原型验证、低代码配置、企业客户培训、基础Python与MySQL",
    ]:
        top = paragraph(c, value, top)
        top += 5
    top = section(c, "教育经历", top + 22)
    top = entry(c, "示例科技大学", "本科  交互设计", "2016-2020", top)
    top = section(c, "说明", top + 30)
    paragraph(c, "本页所有姓名、联系方式、公司、项目、日期和经历均为虚构示例，仅用于展示版式与排版结构。", top)


def main():
    c = canvas.Canvas(str(OUTPUT), pagesize=A4, pageCompression=1)
    c.setTitle("Sanitized Sample Resume")
    c.setAuthor("Resume PDF Template")
    c.setSubject("Fictional sample for layout reference only")
    page_one(c)
    c.showPage()
    page_two(c)
    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    main()
