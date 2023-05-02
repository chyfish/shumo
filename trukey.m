%计算Q1、Q3和IQR的函数
calc_stats = @(column_data) [prctile(column_data, 25), prctile(column_data, 75), iqr(column_data)];

%计算每列中的异常值
for col_idx = 1:size(data1,2)
    %读取指定列向量
    current_col = data1(:,col_idx);
    
    %计算Q1、Q3和IQR
    stats = calc_stats(current_col);
    
    %计算内限上限和下限
    upper_fence = stats(2) + 2 * stats(3);
    lower_fence = stats(1) - 2 * stats(3);
    
    %确定异常值的索引
    outliers_idx = find(current_col > upper_fence | current_col < lower_fence);
    
    %用999代替异常值
    current_col(outliers_idx) = 999;

    %将修改后的列写回原始数据
    data(:,col_idx) = current_col;
end