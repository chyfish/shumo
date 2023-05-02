for i=1:8
% 创建一个服从正态分布的数据集
data =datao(:,i);

% 进行 Jarque-Bera 正态性检验
[h,p] = jbtest(data, 0.05);

% 显示检验结果
if h == 0
    fprintf('数据集符合正态分布 with p-value:%.4f\n', p);
else
    fprintf('数据集不符合正态分布 with p-value:%.4f\n', p);
end
end