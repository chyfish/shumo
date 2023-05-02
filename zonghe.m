% 读取数据文件
% 计算每个变量的上下四分位数和IQR（四分位距）
q1 = prctile(data{:, 2:end}, 25);
q3 = prctile(data{:, 2:end}, 75);
iqr = q3 - q1;

% 计算上下界限
lower_limit = q1 - 1.5*iqr;
upper_limit = q3 + 1.5*iqr;

% 找到噪声数据并进行插值
for i = 2:size(data, 2)
    noise_idx = data{:, i} < lower_limit(i-1) | data{:, i} > upper_limit(i-1);
    data{noise_idx, i} = NaN;
    data{:, i} = fillmissing(data{:, i}, 'pchip', 'EndValues', 'nearest');
end

% 计算每个变量的均值和标准差
mu = mean(data{:, 2:end}, 1);
sigma = std(data{:, 2:end}, 1);

% 计算Z-score值
zscore_data = abs((data{:, 2:end} - mu) ./ sigma);

% 找到异常数据
is_outlier = any(zscore_data > 3, 2);
outliers = data(is_outlier, :);