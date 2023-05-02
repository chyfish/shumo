data=data1
for i = 1:8
    subplot(4,2,i);
    boxplot(data(:,i));
    title(['Boxplot of Column ' num2str(i)]);
end

for i = 1:8
    h = findobj(gca,'Tag','Outliers');
    x = h.XData;
    y = h.YData;
    outliers = [];
    for j = 1:length(x)
        if y(j) ~= max(data(:,i)) && y(j) ~= min(data(:,i))
            outliers = [outliers; x(j) y(j)];
            data(data(:,i)==y(j),i) = 999;
        end
    end
end

for i = 1:8
    subplot(4,2,i);
    boxplot(data(:,i));
    title(['Boxplot of Column ' num2str(i) ' with Outliers Replaced by 999']);
end
