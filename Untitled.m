
data=data1;

% ָ��ƽ������ alpha ��ѡȡ
alpha = 0.3;

% ��ʼֵ��ѡȡ��ȡǰ 3 ���۲�ֵ��ƽ��ֵ
initial_value = mean(data(1:3));

% ��ָ��ƽ��������Ԥ��
y(1) = initial_value;
for i = 2:length(data)
    y(i) = alpha * data(i) + (1-alpha) * y(i-1);
end

y=y'
% ���Ԥ����
disp(y);

