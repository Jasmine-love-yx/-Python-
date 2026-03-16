# 生成“评论数量及评分随时间变化”的可视化图，保存为score_amount_timeSeq.png
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体，避免乱码（必加！）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 模拟数据（你可以替换成自己的真实爬取数据）
# 时间：7天，评论数量，平均评分
data = {
    '日期': ['2026-02-20', '2026-02-21', '2026-02-22', '2026-02-23', '2026-02-24', '2026-02-25', '2026-02-26'],
    '评论数量': [58, 72, 65, 88, 95, 78, 82],
    '平均评分': [4.2, 4.1, 4.3, 4.0, 4.4, 4.2, 4.5]
}
df = pd.DataFrame(data)

# 创建双轴图（评论数量+平均评分）
fig, ax1 = plt.subplots(figsize=(10, 6))

# 绘制评论数量（柱状图）
ax1.bar(df['日期'], df['评论数量'], color='#409eff', alpha=0.7, label='评论数量')
ax1.set_xlabel('日期', fontsize=12)
ax1.set_ylabel('评论数量', fontsize=12, color='#409eff')
ax1.tick_params(axis='y', labelcolor='#409eff')
# 旋转x轴标签，避免重叠
plt.xticks(rotation=45)

# 绘制平均评分（折线图）
ax2 = ax1.twinx()
ax2.plot(df['日期'], df['平均评分'], color='#f56c6c', marker='o', linewidth=2, label='平均评分')
ax2.set_ylabel('平均评分', fontsize=12, color='#f56c6c')
ax2.tick_params(axis='y', labelcolor='#f56c6c')
ax2.set_ylim(3.5, 5.0)  # 评分范围固定3.5-5分

# 添加标题和图例
fig.suptitle('评论数量及评分随时间变化', fontsize=14, fontweight='bold')
fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
plt.tight_layout()

# 保存图片到指定位置（关键！）
save_path = 'E:\\毕业设计\\Comment_analysis\\Streamlit\\score_amount_timeSeq.png'
plt.savefig(save_path, dpi=150, bbox_inches='tight')
plt.close()

print(f"✅ 时间序列图已生成：{save_path}")