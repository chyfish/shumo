
data=[]
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


# 实例化ExpMovAvg类，并设置衰减因子为0.9
ema = ExpMovAvg(decay=0.9)

# 依次对每个数据进行平滑处理
for i in range(len(data)):
    smoothed_data = ema.update(data[i], t=i + 1, is_biased=False)
    print(smoothed_data)
