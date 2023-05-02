%����Q1��Q3��IQR�ĺ���
calc_stats = @(column_data) [prctile(column_data, 25), prctile(column_data, 75), iqr(column_data)];

%����ÿ���е��쳣ֵ
for col_idx = 1:size(data1,2)
    %��ȡָ��������
    current_col = data1(:,col_idx);
    
    %����Q1��Q3��IQR
    stats = calc_stats(current_col);
    
    %�����������޺�����
    upper_fence = stats(2) + 2 * stats(3);
    lower_fence = stats(1) - 2 * stats(3);
    
    %ȷ���쳣ֵ������
    outliers_idx = find(current_col > upper_fence | current_col < lower_fence);
    
    %��999�����쳣ֵ
    current_col(outliers_idx) = 999;

    %���޸ĺ����д��ԭʼ����
    data(:,col_idx) = current_col;
end