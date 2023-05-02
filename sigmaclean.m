data1=data
for col_idx = 1:size(data,2)
    %读取指定列向量
    current_col = data(:,col_idx);
    
    %计算均值和标准差
    mean_val = mean(current_col);
    std_val = std(current_col);
    
    %计算异常值边界
   upper_bound = mean_val + 3 * std_val;
    lower_bound = mean_val - 3 * std_val;
    
    %确定异常值的索引并且用9999代替
    outliers_idx = find(current_col > upper_bound | current_col < lower_bound);
    current_col(outliers_idx) = 9999;
    
    %将修改后的列写回原始数据
    data(:,col_idx) = current_col;
end