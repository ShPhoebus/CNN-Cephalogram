ground_truth_file = 'dataset_ground_truth_labels_Combined_Aug.csv';
predictions_file = 'dataset_prediction_labels_Combined_Aug.csv';
AB_points_file = 'AB_Combined_Aug.csv';

ground_truth_data = readcell(ground_truth_file);
predictions_data = readcell(predictions_file);

parsed_ground_truth_data = cell(size(ground_truth_data, 1), 50);
parsed_predictions_data = cell(size(predictions_data, 1), 50);

for i = 1:size(ground_truth_data, 1)
    gt_cells = strsplit(ground_truth_data{i, 1}, ',');
    gt_nums = cellfun(@str2num, gt_cells, 'UniformOutput', false);
    parsed_ground_truth_data(i, 1:length(gt_nums)) = gt_nums;
end

for i = 1:size(predictions_data, 1)
    pt_cells = strsplit(predictions_data{i, 1}, ',');
    pt_nums = cellfun(@str2num, pt_cells, 'UniformOutput', false);
    parsed_predictions_data(i, 1:length(pt_nums)) = pt_nums;
end

ground_truth_numeric = cell2mat(parsed_ground_truth_data);
predictions_numeric = cell2mat(parsed_predictions_data);

AB_points_data_raw = readcell(AB_points_file);

AB_points_numeric = zeros(size(AB_points_data_raw, 1), 4);

known_distance_mm = 152.3;

for i = 1:size(AB_points_data_raw, 1)
    A_point_str = erase(AB_points_data_raw{i, 1}, {'(', ')'});
    A_point = str2double(strsplit(A_point_str, ','));
    B_point_str = erase(AB_points_data_raw{i, 2}, {'(', ')'});
    B_point = str2double(strsplit(B_point_str, ','));
    AB_points_numeric(i, 1:2) = A_point;
    AB_points_numeric(i, 3:4) = B_point;
    pixel_distance_A_B = sqrt((A_point(1) - B_point(1))^2 + (A_point(2) - B_point(2))^2);
    AB_points_numeric(i, 5) = known_distance_mm / pixel_distance_A_B;
end

scaling_factors = AB_points_numeric(:, 5);
distances_mm = zeros(size(ground_truth_numeric, 1), size(ground_truth_numeric, 2) / 2);
thresholds_mm = [2, 2.5, 3, 4];
individual_MSE = zeros(1, size(ground_truth_numeric, 2) / 2);
individual_SDR = zeros(length(thresholds_mm), size(ground_truth_numeric, 2) / 2);

for i = 1:size(ground_truth_numeric, 1)
    for j = 1:(size(ground_truth_numeric, 2) / 2)
        dist_pixels = sqrt((predictions_numeric(i, j) - ground_truth_numeric(i, j))^2 + ...
                           (predictions_numeric(i, j + 24) - ground_truth_numeric(i, j + 24))^2);
        distances_mm(i, j) = dist_pixels * scaling_factors(i);
    end
end

for j = 1:(size(ground_truth_numeric, 2) / 2)
    valid_distances = distances_mm(:, j) > 0;
    squared_errors = (distances_mm(valid_distances, j)).^2;
    if ~isempty(squared_errors)
        individual_MSE(j) = mean(squared_errors);
    else
        individual_MSE(j) = NaN;
    end
    for t = 1:length(thresholds_mm)
        if any(valid_distances)
            individual_SDR(t, j) = mean(distances_mm(valid_distances, j) < thresholds_mm(t));
        else
            individual_SDR(t, j) = NaN;
        end
    end
end

disp('Distances in millimeters:');
disp(distances_mm);

aggregate_MSE = mean(distances_mm(:).^2);
aggregate_SDR = zeros(1, length(thresholds_mm));
for t = 1:length(thresholds_mm)
    aggregate_SDR(t) = mean(distances_mm(:) < thresholds_mm(t));
end

fprintf('Aggregate MSE in mm^2: %f\n', aggregate_MSE);
fprintf('Aggregate SDR for thresholds:\n');
for t = 1:length(thresholds_mm)
    fprintf('< %.1fmm: %f%%\n', thresholds_mm(t), aggregate_SDR(t) * 100);
end

disp('Individual MSE for each landmark in mm^2:');
for j = 1:length(individual_MSE)
    if isnan(individual_MSE(j))
        fprintf('Landmark %d: MSE = NaN\n', j);
    else
        fprintf('Landmark %d: MSE = %f\n', j, individual_MSE(j));
    end
end

for t = 1:length(thresholds_mm)
    fprintf('SDR for threshold < %.1fmm:\n', thresholds_mm(t));
    for j = 1:size(individual_SDR, 2)
        if isnan(individual_SDR(t, j))
            fprintf('Landmark %d: SDR = NaN\n', j);
        else
            fprintf('Landmark %d: SDR = %f%%\n', j, individual_SDR(t, j) * 100);
        end
    end
end

MSE_table = array2table(individual_MSE', 'RowNames', cellstr("Landmark_" + (1:length(individual_MSE))), 'VariableNames', {'MSE_mm2'});
disp(MSE_table);

for t = 1:length(thresholds_mm)
    SDR_table = array2table(individual_SDR(t, :)' * 100, 'RowNames', cellstr("Landmark_" + (1:size(individual_SDR, 2))), 'VariableNames', {sprintf('SDR_%.1fmm', thresholds_mm(t))});
    disp(SDR_table);
end

ground_truth_vector = ground_truth_numeric(:);
predictions_vector = predictions_numeric(:);

mean_ground_truth = mean(ground_truth_vector);
TSS = sum((ground_truth_vector - mean_ground_truth).^2);

RSS = sum((ground_truth_vector - predictions_vector).^2);

% Calculate R^2
R_squared = 1 - (RSS / TSS);

fprintf('R^2: %f\n', R_squared);