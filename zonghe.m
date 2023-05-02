% ��ȡ�����ļ�
% ����ÿ�������������ķ�λ����IQR���ķ�λ�ࣩ
q1 = prctile(data{:, 2:end}, 25);
q3 = prctile(data{:, 2:end}, 75);
iqr = q3 - q1;

% �������½���
lower_limit = q1 - 1.5*iqr;
upper_limit = q3 + 1.5*iqr;

% �ҵ��������ݲ����в�ֵ
for i = 2:size(data, 2)
    noise_idx = data{:, i} < lower_limit(i-1) | data{:, i} > upper_limit(i-1);
    data{noise_idx, i} = NaN;
    data{:, i} = fillmissing(data{:, i}, 'pchip', 'EndValues', 'nearest');
end

% ����ÿ�������ľ�ֵ�ͱ�׼��
mu = mean(data{:, 2:end}, 1);
sigma = std(data{:, 2:end}, 1);

% ����Z-scoreֵ
zscore_data = abs((data{:, 2:end} - mu) ./ sigma);

% �ҵ��쳣����
is_outlier = any(zscore_data > 3, 2);
outliers = data(is_outlier, :);