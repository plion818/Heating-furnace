import pandas as pd

# 讀取CSV檔案
df = pd.read_csv("data/processed/sensorID_28_standardized.csv")

# 檢查temperature_scaled的絕對值是否有大於3
has_outlier = (df['temperature_scaled'].abs() > 3).any()

if has_outlier:
    print('temperature_scaled 欄位有絕對值大於 3 的資料')
else:
    print('temperature_scaled 欄位所有絕對值都小於等於 3')

# 計算四個標準化欄位的平均與標準差
cols = ['current_scaled', 'voltage_scaled', 'resistance_scaled', 'temperature_scaled']
for col in cols:
    mean = df[col].mean()
    std = df[col].std()
    # 為避免顯示 -0.0000，取絕對值後再格式化顯示
    # -0.0000 只是浮點數誤差，與 0.0000 無實質差異
    print(f"{col} 平均值: {abs(mean):.4f}, 標準差: {abs(std):.4f}")

