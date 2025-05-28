# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to Semantic Versioning (though version numbers are illustrative for now).

## [0.2.0] - Homepage Enhancements & Refinements - YYYY-MM-DD 

This version represents the state of the project after significant UI/UX development on the `Homepage.py` Streamlit application, incorporating several rounds of feedback.

### Added
- **Intuitive Homepage Interface (`Homepage.py`):**
    - Reorganized sidebar controls into collapsible expanders ("⏱️ 時間選擇", "📊 圖表選項") for better clarity.
    - Implemented a combined scaled metrics chart, allowing users to compare multiple selected metrics on a single graph.
    - Added an anomaly statistics chart at the bottom of the page:
        - Initially a vertical bar chart showing normal/anomaly counts.
        - Refined to a single horizontal stacked bar chart representing 100% of data, segmented by 'Normal' and 'Anomaly' proportions.
        - On-bar text for the stacked chart displays only percentages (e.g., "95.3%"), styled to be larger, bold, and black.
        - Detailed hover text for stacked chart segments shows Segment Name, Count, and Percentage.
    - Added anomaly score (if available) to the hover text for normal (non-anomalous) data points in time-series charts.
- **Enhanced Styling and User Experience:**
    - Set a descriptive page title ("🔥 加熱爐數據趨勢分析儀") and icon.
    - Standardized the main application title and overall page layout (wide mode).
    - Refined Plotly chart aesthetics (standardized color schemes, improved hover information formatting, optimized legends).
    - Improved user feedback messages, including warnings for missing anomaly data.
- **Code Quality:**
    - Added comprehensive docstrings to functions in `Homepage.py`.
    - Added inline comments to explain complex logic and improve code readability.

### Changed
- **Scaled Metrics Display:** Evolved from individual charts in columns to a single, combined chart for better comparison.
- **Anomaly Statistics Chart:** Transformed from a grouped vertical bar to a proportional stacked horizontal bar with specific text/hover requirements based on feedback.
- **Hover Text:** Iteratively improved hover text for clarity and to include requested information (like scores for normal points, specific formatting for anomaly details).

## [0.1.0] - Initial Version - YYYY-MM-DD (Assumed)

This is the initial version of the `Heating-furnace` project. 

### Added
- Basic data loading capabilities for sensor data (e.g., from `data/processed/sensorID_28_standardized.csv`).
- Initial Streamlit page structure (`Homepage.py`) for displaying sensor data trends.
- Functionality for anomaly detection based on resistance spikes (as per `results/anomaly_results.csv`).
- Basic time-series plotting of sensor metrics.

*(Note: Details for this version are based on the project's state before the recent interactive development focused on UI/UX enhancements. Replace YYYY-MM-DD with actual dates if known.)*
```
