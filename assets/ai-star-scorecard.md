# AI 之星鉴定卡

> Judge the claim, not the person. 评价文本，不评价人。

**AI 之星指数：{{score}} / 100**  
**文本标签：{{label}}**  
范围：{{scope}} · 有效主张：{{n}} · 判断信心：{{confidence_and_reason}}

| 维度 | 原始均分 / 4 | 加权贡献 / 100 |
|---|---:|---:|
| 黑话浓度 J | {{J}} | {{J_contribution}} |
| 比喻替代原理 M | {{M}} | {{M_contribution}} |
| 焦虑贩卖 A | {{A}} | {{A_contribution}} |
| 权威借力 R | {{R}} | {{R_contribution}} |
| 时代宣言 T | {{T}} | {{T_contribution}} |
| 可验证信息 V（越高越具体） | {{V}} | {{information_gap_contribution}} |

**原文证据**  
{{short_quotes_with_reasons}}

**完整主张表**  
{{unit_scores_and_calibration}}

**翻成人话**：{{plain_statement}}  
**最值得追问**：{{question}}

{{context_and_calibration_notes}}

AI Hero Detector v0.1 · 分数表示文本话术特征，不代表事实真伪或作者能力。引用材料未进行外部核验。

<!-- 制卡时替换全部占位符。无有效主张时将分数改为“无法评分”，删除数值表，写明原因；不要填 0。公开截图脱敏，保留范围与边界。 -->
