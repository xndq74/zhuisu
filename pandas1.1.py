import pandas as pd

# 读取 Excel 文件
file_path = 'data2025-02-1126.xlsx'
df = pd.read_excel(file_path)

# 打印数据框的前几行，确认数据加载是否成功
print("数据框预览：")
print(df.head())

# 统计所有不重复的生产商数量
unique_producers = df['生产商'].unique()
num_producers = len(unique_producers)

# 外层循环：遍历所有不重复的生产商
for producer in unique_producers:
    print(f"\n正在处理的生产商：{producer}")

    # 内层循环：针对当前生产商的进货记录进行迭代
    # 使用 groupby 按生产商分组，获取当前生产商的所有记录
    producer_records = df[df['生产商'] == producer]

    # 遍历当前生产商的每一行记录
    for index, row in producer_records.iterrows():
        # 获取产品名称、进货数量和生产商信息
        product_name = row['产品名称'] if not pd.isna(row['产品名称']) else "未知产品"
        quantity = row['进货数量'] if not pd.isna(row['进货数量']) else "未知数量"

        # 输出当前处理的记录详情
        print(f"处理记录：产品名称={product_name}, 进货数量={quantity}, 生产商={producer}")