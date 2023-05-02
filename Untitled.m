
data=data1;

% 指数平滑因子 alpha 的选取
alpha = 0.3;

% 初始值的选取：取前 3 个观测值的平均值
initial_value = mean(data(1:3));

% 用指数平滑法进行预测
y(1) = initial_value;
for i = 2:length(data)
    y(i) = alpha * data(i) + (1-alpha) * y(i-1);
end

y=y'
% 输出预测结果
disp(y);

