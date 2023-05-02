# 导入NumPy库
import numpy as np
import pandas as pd
import math
# 读取 Excel 表格中的数据
df = pd.read_excel('datas.xls', sheet_name='Sheet1', header=None)

# 取出需要处理的列向量
column_index = 0  # 假设我们要获取第一列的数据
data = df.iloc[:, column_index]

# 设定移动窗口大小
window = 7

# 计算实际值的平均值
mean_values = []
for i in range(window, len(data) - window):
    mean = np.mean(data[i-window:i+window+1])
    mean_values.append(mean)

# 计算每个时刻的实际值和平均值之间的差
differences = np.array(data[window:-window]) - np.array(mean_values)

# 计算差的平方
squared_differences = differences ** 2

# 计算每个时刻的移动方差
moving_variances = []
for i in range(window, len(squared_differences) - window):
    variance = np.mean(squared_differences[i-window:i+window+1])
    moving_variances.append(math.sqrt(variance))

# 输出结果
print(moving_variances)
new_df = pd.DataFrame(moving_variances)
new_df.to_excel('fangcha.xlsx', index=False)