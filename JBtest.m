for i=1:8
% ����һ��������̬�ֲ������ݼ�
data =datao(:,i);

% ���� Jarque-Bera ��̬�Լ���
[h,p] = jbtest(data, 0.05);

% ��ʾ������
if h == 0
    fprintf('���ݼ�������̬�ֲ� with p-value:%.4f\n', p);
else
    fprintf('���ݼ���������̬�ֲ� with p-value:%.4f\n', p);
end
end