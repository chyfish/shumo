import np as np
import pandas as pd
import math
from scipy.interpolate import interp1d


# 导入ExpMovAvg类
class ExpMovAvg(object):
    def __init__(self, decay=0.9):
        self.shadow = 0
        self.decay = decay
        self.first_time = True

    def update(self, data, t, is_biased=False):
        if self.first_time:
            self.shadow = data
            self.first_time = False
            return data
        else:
            self.shadow = self.decay * self.shadow + (1 - self.decay) * data
            if is_biased:
                return self.shadow / (1 - self.decay ** t)
            else:
                return self.shadow


# 要获取的列column_index，decay衰减系数，
def nvd(column_index=0, extent=1.2, decay=0.8):
    # 读取 Excel 表格中的数据
    df = pd.read_excel('datas.xls', sheet_name='Sheet1', header=None)
    # 取出需要处理的列向量
    data = df.iloc[:, column_index]
    # 实例化ExpMovAvg类，并设置衰减因子为
    ema = ExpMovAvg(decay=decay)
    res = []
    # 依次对每个数据进行平滑处理
    for i in range(len(data)):
        smoothed_data = ema.update(data[i], t=i + 1, is_biased=True)
        res.append(smoothed_data)
        print(smoothed_data)

    # 对于前window和后window个数所产生的移动方差归一化处理，然后使用插值技术将它们扩展到与原始数据序列一样的长度。具体地说，我们可以先计算正常区域（即窗口可以滑动的区域）的移动方差，然后计算前window和后window个数的移动方差均值，并与正常区域的移动方差序列一起进行插值，将结果扩展到原始数据序列的长度。
    # 设定移动窗口大小
    window = 7

    # 计算实际值的平均值
    mean_values = []
    for i in range(window, len(data) - window):
        mean = np.mean(data[i - window:i + window + 1])
        mean_values.append(mean)

    # 计算每个时刻的实际值和平均值之间的差
    differences = np.array(data[window:-window]) - np.array(mean_values)

    # 计算差的平方
    squared_differences = differences ** 2

    # 计算正常区域的移动方差
    moving_variances = []
    for i in range(window, len(squared_differences) - window):
        variance = np.mean(squared_differences[i - window:i + window + 1])
        moving_variances.append(variance)

    # 计算前window个数和后window个数的移动方差均值
    front_mean = np.mean(squared_differences[:window])
    end_mean = np.mean(squared_differences[-window:])

    # 对于前window个数和后window个数所产生的移动方差，归一化处理
    normalized_front_variances = np.ones(window) * front_mean
    normalized_end_variances = np.ones(window) * end_mean

    # 将正常区域的移动方差序列插值拼接，并将前window个数和后window个数部分去除
    f = interp1d(range(len(moving_variances)), moving_variances, kind='linear')
    extended_variances = f(np.linspace(0, len(moving_variances) - 1, len(data) - 2 * window))

    # 拼接所有部分得到最终结果
    normalized_variances = np.concatenate((normalized_front_variances, extended_variances, normalized_end_variances))

    sqrt_variances = [extent * math.sqrt(num) for num in normalized_variances]

    #  计算数据的上下限
    upperlimit = np.add(res, sqrt_variances)
    downlimit = np.subtract(res, sqrt_variances)


    # 判断当前值是否超出范围
    flag_arr=np.zeros(100)
    for j in range(100):
            if (data[j] > upperlimit[j]) or (data[j] < downlimit[j]):
                flag_arr[j] = 1
            else:
                # 未超出范围，将标注为 0
                flag_arr[j] = 0

    outcome = [data, upperlimit, downlimit,flag_arr]
    new_df = pd.DataFrame(outcome)
    new_df=new_df.transpose()
    new_df.columns = ['data', 'max', 'min', 'isout']
    new_df.to_excel('output{}.xlsx'.format(column_index), index=False)
    print(f"数据已经成功保存到 outcome.xlsx 中")


for i in range(8):
    nvd(i,1.5)
