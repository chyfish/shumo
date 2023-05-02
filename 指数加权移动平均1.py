import numpy as np
import pandas as pd
import math
import scipy.interpolate as interp1d
import xlrd


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

    # 对始端进行修正
    # 方案一：计算简单移动平均
    # ma = np.mean(data[:5])
    # 使用循环将前5个值设为简单平均
    # for i in range(5):
    #     res[i] = ma
    # 方案二：前五个使用初始值代替
    for k in range(10):
        res[k] = data[k]

    print(res)
    ewma_corr = ewma_bias_corr(res, 0.8)
    for j in range(10):
        res[j] = ewma_corr[j]

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

    outcome = [data, upperlimit, downlimit]
    new_df = pd.DataFrame(outcome)
    new_df.to_excel('output1{}.xlsx'.format(i), index=False)
    print(f"数据已经成功保存到 outcome.xlsx 中")


# res 是输入数据
# alpha 是指数加权平均的衰减因子。
# 通过循环计算得到了未经过修正的指数加权平均 ewma，然后计算了一个偏差修正系数 corr_factor，最后将这两个值相乘得到了修正后的指数加权平均 ewma_corr。
def ewma_bias_corr(res, alpha):
    # 计算指数加权平均
    ewma = np.zeros(len(res))
    ewma[0] = res[0]
    for index in range(1, len(res)):
        ewma[index] = alpha * res[index] + (1 - alpha) * ewma[index - 1]

    zeros = np.zeros_like(np.arange(0, len(res)))
    zeros[np.power(1 - alpha, np.arange(0, len(res))) == 0] = 1e-8
    eps = 1e-6
    # 该函数使用的是动态偏差修正算法，其思想是将时间序列中每个时间点之前的所有数据都视为初始状态，然后逐步将当前的数据融入进去，这样就能够消除初始状态带来的影响
    denominator = 1 - np.power(1 - alpha, np.arange(0, len(res)) + zeros)
    denominator[denominator < eps] = eps
    corr_factor = 1 / denominator

    # 对指数加权平均进行偏差修正
    ewma_corr = ewma * corr_factor

    return ewma_corr