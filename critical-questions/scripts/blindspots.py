#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
投资盲区识别器 - 纯代码分析，不调用 LLM
自包含脚本，不依赖外部项目代码。

通过文本分析识别资料中没有涉及但投决必知的信息。
包含技术维度的专项盲区检测。

用法: python blindspots.py <资料目录>
"""
import sys
import os
import re
import json
import argparse
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# 复用本 skill 内置的 doc_loader 加载文档
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))
from doc_loader import load_directory


def load_industry_profiles():
    """Load bundled industry profiles. Returns (metrics_dict, aliases_dict) or (None, None)."""
    try:
        profile_path = SKILL_DIR / "references" / "industry-profiles.json"
        if profile_path.exists():
            with open(profile_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            metrics = {}
            aliases = {}
            for key, profile in data.get("industries", {}).items():
                metrics[key] = [(m["metric"], m["why"]) for m in profile.get("key_metrics", [])]
                for alias in profile.get("aliases", []):
                    aliases[alias] = key
            return metrics, aliases
    except Exception:
        pass
    return None, None


# ==================== 行业关键指标 ====================

COMMON_METRICS = [
    ("TAM/SAM/SOM", "市场规模是估值基础/决定天花板"),
    ("市占率", "竞争地位和增长空间的直接指标"),
    ("增速/增长率", "增长是PE投资的核心逻辑"),
]

# Hardcoded fallback (used when JSON file is not available)
_HARDCODED_INDUSTRY_METRICS = {
    "半导体": [("制程节点", "技术代际决定竞争力"), ("良率", "制造能力核心指标"), ("产能利用率", "收入可预测性"), ("国产替代率", "政策驱动力")],
    "SaaS": [("NRR/净收入留存率", "产品粘性和扩展性"), ("CAC/LTV", "获客效率"), ("ARR", "订阅制核心指标"), ("Churn/流失率", "客户粘性")],
    "医疗": [("临床进度", "产品离商业化多远"), ("审批状态", "监管风险"), ("医保覆盖", "支付能力"), ("试验数据", "有效性验证")],
    "新能源": [("转换效率", "技术竞争力"), ("度电成本", "经济性"), ("产能/出货量", "规模化能力"), ("补贴依赖度", "政策风险")],
    "消费": [("复购率", "品牌粘性"), ("渠道结构", "销售可控性"), ("客单价", "定位和升级空间"), ("同店增长", "内生增长能力")],
    "AI": [("模型性能/精度", "技术竞争力"), ("推理成本", "商业模式可行性"), ("数据壁垒", "护城河"), ("API调用量/DAU", "产品化程度")],
    "制造": [("产能利用率", "需求饱满度"), ("良率", "工艺水平"), ("大客户占比", "依赖风险"), ("自动化率", "效率提升空间")],
    "金融科技": [("风控指标/不良率", "信用风险"), ("牌照", "合规性"), ("资金成本", "盈利能力"), ("交易规模/撮合量", "平台价值")],
}

_HARDCODED_ALIASES = {
    "芯片": "半导体", "集成电路": "半导体", "IC设计": "半导体",
    "云计算": "SaaS", "软件": "SaaS", "订阅": "SaaS",
    "医药": "医疗", "生物": "医疗", "器械": "医疗", "创新药": "医疗",
    "光伏": "新能源", "储能": "新能源", "风电": "新能源", "锂电": "新能源",
    "零售": "消费", "餐饮": "消费", "品牌": "消费",
    "大模型": "AI", "人工智能": "AI", "机器学习": "AI", "深度学习": "AI",
    "工业": "制造", "装备": "制造",
    "支付": "金融科技", "借贷": "金融科技", "保险科技": "金融科技",
}

# Try loading from JSON, fall back to hardcoded
_json_metrics, _json_aliases = load_industry_profiles()
INDUSTRY_METRICS = _json_metrics if _json_metrics else _HARDCODED_INDUSTRY_METRICS
INDUSTRY_ALIASES = _json_aliases if _json_aliases else _HARDCODED_ALIASES

SKIP_WORDS = {"资料未提供", "未知", "无", "N/A", "null", "None", "暂无", ""}


def detect_industry(text: str) -> str:
    """从文本中推测行业"""
    for keyword in INDUSTRY_METRICS:
        if keyword in text:
            return keyword
    # 模糊匹配
    for alias, industry in INDUSTRY_ALIASES.items():
        if alias in text:
            return industry
    return ""


def identify_product_blindspots(doc_text: str) -> list:
    """识别产品细节缺失的盲区"""
    blindspots = []

    # 只扫描前20000字符提取产品名称（避免匹配正文中的噪音）
    scan_limit = 20000

    product_patterns = [
        r'(?:核心产品|主打产品|主要产品|旗舰产品|产品线)[是为：:]+\s*([^，。,\.\n]{2,30})',
        r'(?:产品|平台|系统)[是为：:]+\s*"?([^"，。,\.\n]{2,30})"?',
    ]
    mentioned_products = set()
    for pat in product_patterns:
        for m in re.finditer(pat, doc_text[:scan_limit]):
            name = m.group(1).strip()
            if name and len(name) >= 2 and name not in SKIP_WORDS:
                mentioned_products.add(name)

    detail_keywords = ["功能", "参数", "性能", "指标", "规格", "客户", "订单",
                       "收入", "销量", "反馈", "对比", "优势", "壁垒", "专利"]

    for product in list(mentioned_products)[:10]:
        mentions = doc_text.count(product)
        if mentions == 0:
            continue

        has_detail = False
        for m in re.finditer(re.escape(product), doc_text):
            start = max(0, m.start() - 500)
            end = min(len(doc_text), m.end() + 500)
            context = doc_text[start:end]
            if any(kw in context for kw in detail_keywords):
                has_detail = True
                break

        if not has_detail:
            blindspots.append({
                "type": "产品细节缺失",
                "item": product,
                "detail": f"产品 {product} 被提及 {mentions} 次，但缺少功能、参数、客户反馈等深度信息",
                "why_critical": "核心产品的具体能力直接影响估值和竞争力判断",
                "needed": f"{product} 的功能详情、技术参数、客户使用反馈、与竞品对比",
            })

    return blindspots


def identify_industry_metric_blindspots(doc_text: str, industry: str) -> list:
    """识别行业关键指标缺失"""
    blindspots = []
    metrics = COMMON_METRICS[:]

    for key, vals in INDUSTRY_METRICS.items():
        if key in industry or industry in key:
            metrics.extend(vals)
            break

    if not industry:
        metrics.extend([("核心业务指标", "该行业最关键的运营指标"),
                        ("行业标杆对比", "与行业龙头/上市公司的差距")])

    for metric_name, metric_desc in metrics:
        found = metric_name in doc_text
        if not found:
            # 模糊匹配：检查指标描述中的关键词（斜杠分隔）
            for kw in metric_desc.split("/"):
                if kw in doc_text:
                    found = True
                    break

        if not found:
            industry_label = industry or "该"
            blindspots.append({
                "type": "行业关键指标缺失",
                "item": metric_name,
                "detail": f"{industry_label}行业投资决策需关注 {metric_name}，但资料中未涉及",
                "why_critical": metric_desc,
                "needed": f"{metric_name} 的具体数据和行业对标",
            })

    return blindspots


def identify_customer_blindspots(doc_text: str) -> list:
    """识别客户集中度风险"""
    blindspots = []

    # 只扫描前20000字符提取客户名称
    scan_limit = 20000

    customer_patterns = [
        r'(?:主要客户|核心客户|大客户)[是为：:]+\s*([^，。,\.\n]{2,100})',
    ]
    customers = []
    for pat in customer_patterns:
        for m in re.finditer(pat, doc_text[:scan_limit]):
            raw = m.group(1)
            for c in re.split(r'[,，、;；\s]', raw):
                c = c.strip()
                if c and len(c) >= 2 and c not in SKIP_WORDS:
                    customers.append(c)

    if customers and len(customers) <= 3:
        blindspots.append({
            "type": "客户集中度风险",
            "item": "客户结构",
            "detail": f"仅提及 {len(customers)} 个客户，可能存在严重客户集中风险",
            "why_critical": "客户集中度过高是PE投资重大红旗，需确认前5大客户占比",
            "needed": "前5大客户收入占比、客户留存率、新客获取情况",
        })
    elif not customers:
        customer_keywords = ["客户", "用户", "订单", "合同"]
        has_any = any(kw in doc_text for kw in customer_keywords)
        if not has_any:
            blindspots.append({
                "type": "客户信息完全缺失",
                "item": "客户结构",
                "detail": "资料中未提及任何客户信息",
                "why_critical": "没有客户信息就无法判断收入质量和可持续性",
                "needed": "主要客户、收入占比、客户粘性、获客成本",
            })

    return blindspots


def identify_competition_blindspots(doc_text: str) -> list:
    """识别竞争格局模糊"""
    blindspots = []

    # 只扫描前20000字符提取竞争对手名称
    scan_limit = 20000

    advantage_keywords = ["竞争优势", "核心竞争力", "壁垒", "护城河", "领先", "独特"]
    has_advantage = any(kw in doc_text for kw in advantage_keywords)

    competitor_patterns = [
        r'(?:竞品|竞争对手|对标|同行)(?:公司|企业)?[是为：:]+\s*([^，。,\.\n]{2,20})',
    ]
    competitor_names = []
    for pat in competitor_patterns:
        for m in re.finditer(pat, doc_text[:scan_limit]):
            name = m.group(1).strip()
            if name and name not in SKIP_WORDS:
                competitor_names.append(name)

    if has_advantage and not competitor_names:
        blindspots.append({
            "type": "竞争格局模糊",
            "item": "竞争对手",
            "detail": "资料提到竞争优势但未指明具体竞争对手",
            "why_critical": "不知对手是谁就无法验证竞争壁垒的真实性",
            "needed": "主要竞争对手名单、各家市占率、差异化对比",
        })

    return blindspots


def identify_exit_blindspots(doc_text: str) -> list:
    """识别退出路径盲区"""
    exit_keywords = ["退出", "IPO", "并购", "回购", "上市", "收购"]
    has_exit = any(kw in doc_text for kw in exit_keywords)

    if not has_exit:
        return [{
            "type": "退出路径未讨论",
            "item": "退出策略",
            "detail": "资料中未涉及任何退出路径信息",
            "why_critical": "PE投资必须有退出路径，无退出=无投资",
            "needed": "IPO可行性、潜在并购方、回购条款、行业退出案例",
        }]
    return []


def identify_founder_blindspots(doc_text: str) -> list:
    """识别创始人信息不足"""
    blindspots = []

    founder_keywords = ["创始人", "CEO", "创始人兼CEO", "实际控制人"]
    has_founder_mention = any(kw in doc_text for kw in founder_keywords)

    detail_keywords = ["履历", "经历", "背景", "创业", "学历", "毕业", "曾任", "之前"]
    has_founder_detail = any(kw in doc_text for kw in detail_keywords)

    if has_founder_mention and not has_founder_detail:
        blindspots.append({
            "type": "创始人信息不足",
            "item": "创始人背景",
            "detail": "资料中提到创始人但缺乏详细背景信息",
            "why_critical": "一级市场投资核心是投人，创始人背景是关键决策依据",
            "needed": "创始人履历、过往创业经历、行业资源、团队稳定性",
        })
    elif not has_founder_mention:
        blindspots.append({
            "type": "创始人信息不足",
            "item": "创始人背景",
            "detail": "资料中未提及任何创始人/核心团队信息",
            "why_critical": "一级市场投资核心是投人，创始人背景是关键决策依据",
            "needed": "创始人履历、过往创业经历、行业资源、团队稳定性",
        })

    return blindspots


def identify_technology_blindspots(doc_text: str) -> list:
    """识别技术维度盲区 — 科技公司投研的核心关注点"""
    blindspots = []

    # 检查是否有技术相关表述
    tech_claim_keywords = ["技术领先", "技术优势", "核心技术", "自研", "自主研发",
                           "技术壁垒", "技术护城河", "技术架构", "算法", "模型",
                           "引擎", "平台", "系统", "技术路线"]
    has_tech_claim = any(kw in doc_text for kw in tech_claim_keywords)

    # 1. 技术架构描述缺失
    arch_keywords = ["架构", "技术栈", "技术方案", "实现方式", "设计", "组件", "模块", "框架"]
    has_arch = any(kw in doc_text for kw in arch_keywords)

    if has_tech_claim and not has_arch:
        blindspots.append({
            "type": "技术架构缺失",
            "item": "技术架构",
            "detail": "资料中提到技术优势/核心技术，但缺少技术架构、技术栈、实现方式的描述",
            "why_critical": "没有架构描述就无法判断技术方案的工程可行性和扩展性",
            "needed": "技术架构图、核心技术栈、关键组件说明、技术选型理由",
        })

    # 2. 技术性能指标缺失
    perf_keywords = ["性能", "指标", "benchmark", "延迟", "吞吐", "速度", "精度",
                     "效率", "推理成本", "参数量", "推理速度", "QPS", "TPS", "FPS",
                     "响应时间", "并发", "吞吐量"]
    has_perf = any(kw in doc_text for kw in perf_keywords)

    if has_tech_claim and not has_perf:
        blindspots.append({
            "type": "技术性能指标缺失",
            "item": "技术性能",
            "detail": "资料中声称技术领先，但缺少可量化的性能指标或 benchmark 数据",
            "why_critical": "没有量化指标就无法验证技术领先的真实性，也无法与竞品做客观对比",
            "needed": "具体性能指标（延迟、吞吐、精度等）、第三方 benchmark 对比、实测数据",
        })

    # 3. 技术壁垒证据缺失
    barrier_evidence_keywords = ["专利", "知识产权", "自研核心", "数据壁垒", "算法壁垒"]
    has_barrier_claim = any(kw in doc_text for kw in ["壁垒", "护城河", "领先", "独家", "独有", "独创"])
    has_barrier_evidence = any(kw in doc_text for kw in barrier_evidence_keywords)

    if has_barrier_claim and not has_barrier_evidence:
        blindspots.append({
            "type": "技术壁垒证据缺失",
            "item": "技术壁垒验证",
            "detail": "资料中声称有技术壁垒/护城河，但缺少专利、独有数据、自研核心等具体证据",
            "why_critical": "技术壁垒是科技公司估值的核心支撑，没有证据的壁垒声明不可信",
            "needed": "专利数量与覆盖范围、自研vs开源比例、数据壁垒具体形式、壁垒可持续性分析",
        })

    # 4. 研发投入信息缺失
    rd_keywords = ["研发", "R&D", "研发团队", "研发投入", "研发支出", "研发占比",
                   "技术团队", "工程师", "CTO", "技术负责人"]
    has_rd = any(kw in doc_text for kw in rd_keywords)

    if not has_rd:
        blindspots.append({
            "type": "研发投入信息缺失",
            "item": "研发能力",
            "detail": "资料中未提及任何研发团队规模、研发投入、技术负责人信息",
            "why_critical": "科技公司研发能力是核心竞争力来源，研发投入直接决定技术迭代速度",
            "needed": "研发团队规模与背景、研发支出占比、核心技术人才密度、CTO/技术负责人履历",
        })

    # 5. 技术路线风险未讨论
    risk_keywords = ["替代", "风险", "变更", "演进", "路线", "颠覆", "开源替代",
                     "技术迭代", "技术方向", "技术趋势"]
    has_risk = any(kw in doc_text for kw in risk_keywords)

    if not has_risk and has_tech_claim:
        blindspots.append({
            "type": "技术路线风险未讨论",
            "item": "技术路线风险",
            "detail": "资料中涉及技术内容但未讨论技术路线变更风险、开源替代威胁",
            "why_critical": "科技公司最大的风险是技术路线被颠覆，不讨论风险=不理解风险",
            "needed": "当前技术路线的替代方案、开源替代成熟度、大厂跟进可能性、技术演进方向",
        })

    return blindspots


def identify_all_blindspots(documents: list) -> list:
    """识别所有投资盲区"""
    full_text = "\n".join(d["content"] for d in documents)

    industry = detect_industry(full_text)

    blindspots = []
    blindspots.extend(identify_product_blindspots(full_text))
    blindspots.extend(identify_industry_metric_blindspots(full_text, industry))
    blindspots.extend(identify_customer_blindspots(full_text))
    blindspots.extend(identify_competition_blindspots(full_text))
    blindspots.extend(identify_exit_blindspots(full_text))
    blindspots.extend(identify_founder_blindspots(full_text))
    blindspots.extend(identify_technology_blindspots(full_text))

    return blindspots, industry


def main():
    parser = argparse.ArgumentParser(description="投资盲区识别器 - 纯代码分析，不调用 LLM")
    parser.add_argument("directory", help="资料目录路径")
    args = parser.parse_args()

    # 创建缓存目录
    source_dir = Path(args.directory).resolve()
    cache_dir = source_dir.parent / "_doc_cache" / source_dir.name
    cache_dir.mkdir(parents=True, exist_ok=True)

    # 加载文档
    documents = load_directory(args.directory, cache_dir)
    if not documents:
        print(json.dumps({"error": "未找到可加载的文档", "directory": args.directory}, ensure_ascii=False, indent=2))
        sys.exit(1)

    # 识别盲区
    blindspots, industry = identify_all_blindspots(documents)

    output = {
        "directory": args.directory,
        "detected_industry": industry or "未识别",
        "total_documents": len(documents),
        "total_blindspots": len(blindspots),
        "blindspots": blindspots,
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()



