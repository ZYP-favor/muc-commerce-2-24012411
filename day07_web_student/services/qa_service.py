from pathlib import Path

import pandas as pd


def answer_question(base_dir: Path, question: str) -> str:
    data_dir = base_dir / "data"
    metrics_df = pd.read_csv(data_dir / "overall_metrics.csv", encoding="utf-8-sig")
    metrics = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    category_df = pd.read_csv(data_dir / "category_analysis.csv", encoding="utf-8-sig")
    segment_df = pd.read_csv(data_dir / "segment_analysis.csv", encoding="utf-8-sig")
    normalized = question.replace(" ", "").lower()

    if any(word in normalized for word in ["多少用户", "用户数", "总用户"]):
        return f"数据集中共有{int(metrics['用户数']):,}名用户。"
    # 每个回答都必须引用data目录中已经计算的指标，不得编造数值。
    if any(word in normalized for word in ["流失率", "流失比例", "多少流失"]):
        loss_num = int(metrics["流失人数"])
        loss_rate = metrics["流失率"]
        return f"平台流失用户共{loss_num:,}人，整体用户流失率为{loss_rate:.1%}。"

    # 订单相关提问（平均订单数）
    if any(word in normalized for word in ["订单", "平均订单", "下单次数"]):
        avg_order = metrics["平均订单数"]
        median_order = metrics["订单数中位数"]
        return f"平台用户平均订单数为{avg_order:.2f}次，订单数中位数为{median_order:.2f}次。"

    # 生命周期风险：流失最高阶段
    if any(word in normalized for word in ["生命周期", "流失最高", "风险最高", "哪个阶段流失"]):
        max_loss_line = segment_df.loc[segment_df["流失率"].idxmax()]
        stage = max_loss_line["TenureGroup"]
        rate = max_loss_line["流失率"]
        return f"流失风险最高的用户生命周期阶段是{stage}，该群体流失率达到{rate:.1%}。"

    # 偏好品类相关
    if any(word in normalized for word in ["偏好品类", "最受欢迎", "品类用户最多"]):
        max_cat_line = category_df.loc[category_df["用户数"].idxmax()]
        cat_name = max_cat_line["PreferedOrderCat"]
        cat_user = int(max_cat_line["用户数"])
        cat_rate = max_cat_line["流失率"]
        return f"用户偏好度最高的品类是{cat_name}，该品类用户{cat_user:,}人，品类流失率{cat_rate:.1%}。"

    return (
        "基础问答尚未完成。目前可查询：总用户数、流失率、平均订单/订单中位数、流失最高生命周期阶段、热门偏好品类。"
        "请换一种更具体的问法。"
    )
