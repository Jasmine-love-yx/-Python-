import os

# 1. 获取当前脚本的绝对路径（关键！）
current_file = os.path.abspath(__file__)
print("✅ 当前脚本(check_path.py)的绝对路径：", current_file)

# 2. 获取当前脚本所在目录
current_dir = os.path.dirname(current_file)
print("✅ 当前脚本所在目录：", current_dir)

# 3. 测试拼接目标图片路径（按你的目录结构）
# 从Streamlit目录 → 上一级(Comment_analysis) → resources → LDA_related → pictures → 项目周期表.png
target_image = os.path.join(
    current_dir,          # Streamlit目录
    "..",                 # 上一级：Comment_analysis
    "resources",          # 资源目录
    "LDA_related",        # LDA相关目录
    "pictures",           # 图片目录
    "项目周期表.png"      # 目标图片
)

# 4. 转换为绝对路径（消除..的影响，看得更清楚）
target_image_abs = os.path.abspath(target_image)
print("✅ 目标图片的绝对路径：", target_image_abs)

# 5. 检查文件是否存在
if os.path.exists(target_image_abs):
    print("✅ 恭喜！图片文件存在！")
else:
    print("❌ 图片文件不存在！")
    # 检查父目录是否存在，以及目录里有什么文件
    parent_dir = os.path.dirname(target_image_abs)
    if os.path.exists(parent_dir):
        print(f"📂 父目录({parent_dir})下的文件列表：")
        for file in os.listdir(parent_dir):
            print(f"  - {file}")
    else:
        print(f"📂 父目录({parent_dir})不存在！")