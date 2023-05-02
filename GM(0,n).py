import numpy as np
from scipy.optimize import curve_fit

def grey_predict(data, n=2, steps=1):
    # 灰色生成
    F, R = differential_generation(data)
    # 权重修正
    W = weight_coefficient(R)
    # n阶累加预测方程
    B = np.zeros((n, len(F)-n))
    for i in range(n):
        B[i] = F[i:i-n-1:-1]
    Y = F[n:]
    X = np.dot(np.linalg.inv(np.dot(B, B.T)), np.dot(B, Y))
    a = np.concatenate(([1], -X))
    # 预测发展趋势
    F_pred = np.zeros(len(F) + steps)
    F_pred[:n] = F[:n]
    for i in range(n, len(F_pred)):
        F_pred[i] = sum(a * F_pred[i-n:i][::-1])
    # 权重修正并计算预测值
    W_pred = weight_coefficient(F_pred[:-steps] / data)
    return (F_pred[-steps:] * W_pred[-steps:] * data[-1], F_pred[-steps:])