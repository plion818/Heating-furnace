import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objs as go

# === 載入主要感測資料 ===
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/sensorID_28_standardized.csv")
    df['record Time'] = pd.to_datetime(df['record Time'])
    return df

# === 載入異常檢測結果（包含異常標記與分數） ===
@st.cache_data
def load_anomaly_results():
    try:
        return pd.read_csv("results/anomaly_results.csv")
    except:
        return None

# === 資料初始化 ===
df = load_data()
anomaly_df = load_anomaly_results()

# === 頁面標題 ===
st.markdown("""
    <h2 style='text-align: center; color: #2C3E50;'>📈 Metric Trend Comparison Viewer</h2>
""", unsafe_allow_html=True)

# === 側邊欄：選擇查詢時間區間 ===
st.sidebar.markdown("---")
st.sidebar.markdown("### ⏱ 選擇資料區間")

# 預設查詢起始時間區段
if 'time_start' not in st.session_state:
    st.session_state.time_start = datetime.strptime("2025-02-06 02:00:00", "%Y-%m-%d %H:%M:%S")
    st.session_state.time_end = datetime.strptime("2025-02-06 02:50:00", "%Y-%m-%d %H:%M:%S")

# 時間區段長度選項（分鐘）
interval_minutes = st.sidebar.selectbox("選擇時間區段長度", [15, 30, 60], index=1)

# 手動輸入查詢起訖時間
manual_start = st.sidebar.text_input("Start Time", st.session_state.time_start.strftime("%Y-%m-%d %H:%M:%S"))
manual_end = st.sidebar.text_input("End Time", st.session_state.time_end.strftime("%Y-%m-%d %H:%M:%S"))

# 時間區段左右移動按鈕
col_prev, col_next = st.sidebar.columns(2)
if col_prev.button("⬅ 上一段"):
    delta = timedelta(minutes=interval_minutes)
    st.session_state.time_end = st.session_state.time_start
    st.session_state.time_start = st.session_state.time_end - delta
if col_next.button("下一段 ➡"):
    delta = timedelta(minutes=interval_minutes)
    st.session_state.time_start = st.session_state.time_end
    st.session_state.time_end = st.session_state.time_start + delta

# 手動送出按鈕以更新查詢時間
if st.sidebar.button("🚀 生成圖表"):
    try:
        st.session_state.time_start = datetime.strptime(manual_start, "%Y-%m-%d %H:%M:%S")
        st.session_state.time_end = datetime.strptime(manual_end, "%Y-%m-%d %H:%M:%S")
    except:
        st.error("❌ 時間格式錯誤，請使用 YYYY-MM-DD HH:MM:SS")
        st.stop()

# 顯示目前查詢時間區間
st.sidebar.markdown(f"**目前查詢區間：**\n{st.session_state.time_start} ~ {st.session_state.time_end}")

# === 側邊欄：選擇要繪製的欄位 ===
st.sidebar.markdown("---")
columns = ['current', 'voltage', 'resistance', 'temperature']
scaled_columns = ['current_scaled', 'voltage_scaled', 'resistance_scaled', 'temperature_scaled']
mapping = dict(zip(columns, scaled_columns))

# 選擇要顯示標準化數據的指標
selected_metrics = st.sidebar.multiselect("Select Scaled Metrics to Compare (1~4)", columns, default=["resistance", "temperature"])

# 選擇是否顯示原始數據圖表
st.sidebar.markdown("---")
raw_option = st.sidebar.selectbox("Select Raw Metric to Plot", ["none"] + columns, index=0)

# 勾選是否要顯示異常點紅點
show_anomaly = st.sidebar.checkbox("🔍 顯示阻抗異常點")

# === 根據查詢時間區間過濾資料 ===
try:
    mask = (df['record Time'] >= st.session_state.time_start) & (df['record Time'] <= st.session_state.time_end)
    df_filtered = df.loc[mask].copy()
except:
    st.error("❌ 時間格式轉換錯誤")
    st.stop()

st.success("✅ 圖表已生成。請滑鼠移動檢視原始資料詳情")

# === 套用異常標記與分數欄位 ===
if show_anomaly and anomaly_df is not None:
    df['res_spike_anomaly'] = anomaly_df['res_spike_anomaly']
    df['res_spike_anomaly_score'] = anomaly_df['res_spike_anomaly_score']
    df_filtered['res_spike_anomaly'] = df.loc[df_filtered.index, 'res_spike_anomaly']
    df_filtered['res_spike_anomaly_score'] = df.loc[df_filtered.index, 'res_spike_anomaly_score']

    total = len(df_filtered)
    num_anomalies = df_filtered['res_spike_anomaly'].sum()
    percentage = (num_anomalies / total) * 100 if total > 0 else 0

    total_all = len(df)
    total_anomalies_all = df['res_spike_anomaly'].sum()
    percent_all = (total_anomalies_all / total_all) * 100 if total_all > 0 else 0

    st.info(f"📌 異常點數量（區間）：{int(num_anomalies)} / {total} 筆資料（{percentage:.2f}%）")

# === 標準化數據趨勢圖繪製 ===
if selected_metrics:
    fig_scaled = go.Figure()
    for metric in selected_metrics:
        fig_scaled.add_trace(go.Scatter(
            x=df_filtered['record Time'],
            y=df_filtered[mapping[metric]],
            mode='lines+markers',
            name=f'{metric.capitalize()} (scaled)',
            marker=dict(size=4),
            hoverinfo='text',
            text=[
                f"Time: {t}<br>Current: {cur:.2f}<br>Voltage: {vol:.2f}<br>Resistance: {res:.4f}<br>Temperature: {temp:.2f}"
                for t, cur, vol, res, temp in zip(
                    df_filtered['record Time'],
                    df_filtered['current'],
                    df_filtered['voltage'],
                    df_filtered['resistance'],
                    df_filtered['temperature']
                )
            ]
        ))
    # 異常紅點標記
    if show_anomaly and 'resistance' in selected_metrics and 'res_spike_anomaly' in df_filtered:
        anomaly_points = df_filtered[df_filtered['res_spike_anomaly'] == 1]
        fig_scaled.add_trace(go.Scatter(
            x=anomaly_points['record Time'],
            y=anomaly_points['resistance_scaled'],
            mode='markers',
            name='Resistance Anomaly (scaled)',
            marker=dict(color='red', size=8, symbol='circle'),
            showlegend=True,
            hoverinfo='text',
            text=[
                f"<span style='color:red'>Time: {t}<br>Current: {cur:.2f}<br>Voltage: {vol:.2f}<br>Resistance: {res:.4f}<br>Temperature: {temp:.2f}<br>Score: {score:.4f}</span>"
                for t, cur, vol, res, temp, score in zip(
                    anomaly_points['record Time'],
                    anomaly_points['current'],
                    anomaly_points['voltage'],
                    anomaly_points['resistance'],
                    anomaly_points['temperature'],
                    anomaly_points['res_spike_anomaly_score']
                )
            ]
        ))
    fig_scaled.update_layout(
        title='📊 Scaled Metrics Trend',
        xaxis_title='Time',
        yaxis_title='Scaled Value',
        hovermode='closest',
        height=500,
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_scaled, use_container_width=True)

# === 原始數據圖表繪製 ===
if raw_option != "none":
    fig_raw = go.Figure()
    fig_raw.add_trace(go.Scatter(
        x=df_filtered['record Time'],
        y=df_filtered[raw_option],
        mode='lines+markers',
        name=f'{raw_option.capitalize()} (raw)',
        marker=dict(size=4),
        hoverinfo='text',
        text=[
            f"Time: {t}<br>Current: {cur:.2f}<br>Voltage: {vol:.2f}<br>Resistance: {res:.4f}<br>Temperature: {temp:.2f}"
            for t, cur, vol, res, temp in zip(
                df_filtered['record Time'],
                df_filtered['current'],
                df_filtered['voltage'],
                df_filtered['resistance'],
                df_filtered['temperature']
            )
        ]
    ))
    # 原始紅點標記
    if show_anomaly and raw_option == 'resistance' and 'res_spike_anomaly' in df_filtered:
        anomaly_points = df_filtered[df_filtered['res_spike_anomaly'] == 1]
        fig_raw.add_trace(go.Scatter(
            x=anomaly_points['record Time'],
            y=anomaly_points['resistance'],
            mode='markers',
            name='Resistance Anomaly (raw)',
            marker=dict(color='red', size=8, symbol='circle'),
            showlegend=True,
            hoverinfo='text',
            text=[
                f"<span style='color:red'>Time: {t}<br>Current: {cur:.2f}<br>Voltage: {vol:.2f}<br>Resistance: {res:.4f}<br>Temperature: {temp:.2f}<br>Score: {score:.4f}</span>"
                for t, cur, vol, res, temp, score in zip(
                    anomaly_points['record Time'],
                    anomaly_points['current'],
                    anomaly_points['voltage'],
                    anomaly_points['resistance'],
                    anomaly_points['temperature'],
                    anomaly_points['res_spike_anomaly_score']
                )
            ]
        ))
    fig_raw.update_layout(
        title=f'📈 Raw Metric Trend: {raw_option.capitalize()}',
        xaxis_title='Time',
        yaxis_title='Raw Value',
        hovermode='closest',
        height=500,
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_raw, use_container_width=True)


# ✅ 條件判斷：使用者有選擇要顯示的圖（標準化或原始）且有勾選「🔍 顯示阻抗異常點」→ 才執行下面的匯出按鈕
if (selected_metrics or raw_option != "none") and show_anomaly:
    st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
    st.download_button(
        label="📤 匯出目前區間異常點資料",
        data=df_filtered[df_filtered['res_spike_anomaly'] == 1].to_csv(index=False).encode('utf-8-sig'),
        file_name="filtered_anomalies.csv",
        mime='text/csv',
        key="download-below-plot"
    )
    st.markdown("</div>", unsafe_allow_html=True)


# === 整體異常統計（放在頁面最下方） ===
if show_anomaly and anomaly_df is not None:
    st.markdown("---")
    st.info(f"📊 異常點數量（全部）：{int(total_anomalies_all)} / {total_all} 筆資料（{percent_all:.2f}%）")
