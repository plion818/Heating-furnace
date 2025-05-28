# 加熱爐異常檢測專案 (Heating Furnace Anomaly Detection)

## 🎯 專案目的 (Project Purpose)

本專案的目標是針對加熱爐的運作數據進行分析，實現異常狀況與潛在故障的早期預警。在加熱爐的穩定運作過程中，特別關注以下指標以判定異常：

*   **電阻 (Resistance):** 在溫度維持於特定範圍時，電阻值應呈現穩定趨勢。若短時間內電阻出現明顯的斜率上升或下降，這可能表示潛在的異常。
*   **電流與電壓 (Current & Voltage):** 電流或電電圧的瞬間劇烈變化也是重要的異常指標。
*   **電阻變化幅度 (Magnitude of Resistance Change):** 電阻值的變化幅度如果異常過大，同樣被視為潛在的異常行為。

## 📦 目前成果 (Current Features)

目前專案已初步完成基於 **電阻數據的異常偵測** 功能，並圍繞此功能設計了一個符合實際應用需求的網頁首頁介面 (`Homepage.py`)。此介面具備以下特點：

*   **🧭 操作直觀 (Intuitive Operation):** 提供易於理解與操作的使用者介面。
*   **📊 視覺一致 (Consistent Visualization):** 數據呈現清晰，圖表風格統一，提升資訊判讀效率。
*   **🧩 架構模組化 (Modular Architecture):** 程式碼結構清晰，考慮了未來的擴充性與維護性。
*   **🧠 分析功能實用 (Practical Analysis):** 提供初步的數據分析與視覺化功能，能夠即時反映潛在的異常情況。
*   **🎯 適合部署使用 (Deployment Ready):** 設計上考慮了實際場域的應用需求，可被快速導入與應用。

### 未來展望 (Future Work)

未來計畫持續擴充異常偵測的依據，例如導入更多種類的感測器指標數據（如溫度、壓力等），並結合更先進的分析與預測模型，以提升預警的準確性與覆蓋範圍。

## 🚀 快速開始 (Quick Start)

### 環境需求 (Prerequisites)

*   Python 3.7+
*   Streamlit
*   Pandas
*   Numpy
*   Plotly
*   Plotly Express

建議使用虛擬環境，並透過 `pip` 安裝相關套件：
```bash
pip install streamlit pandas numpy plotly plotly.express
```
(未來若提供 `requirements.txt`，可直接使用 `pip install -r requirements.txt`)

### 執行專案 (Running the Application)

1.  確保您已在專案的根目錄下。
2.  執行以下指令啟動 Streamlit 應用程式：

    ```bash
    streamlit run Homepage.py
    ```
3.  開啟瀏覽器並訪問應用程式顯示的本地網址 (通常是 `http://localhost:8501`)。
