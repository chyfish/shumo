data1=data
for col_idx = 1:size(data,2)
    %��ȡָ��������
    current_col = data(:,col_idx);
    
    %�����ֵ�ͱ�׼��
    mean_val = mean(current_col);
    std_val = std(current_col);
    
    %�����쳣ֵ�߽�
   upper_bound = mean_val + 3 * std_val;
    lower_bound = mean_val - 3 * std_val;
    
    %ȷ���쳣ֵ������������9999����
    outliers_idx = find(current_col > upper_bound | current_col < lower_bound);
    current_col(outliers_idx) = 9999;
    
    %���޸ĺ����д��ԭʼ����
    data(:,col_idx) = current_col;
end