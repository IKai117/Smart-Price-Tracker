# 🛒 Smart Price Tracker: 全端電商比價與趨勢分析系統

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Framework-Flask-lightgrey.svg)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-green.svg)
![Chart.js](https://img.shields.io/badge/Frontend-Chart.js-orange.svg)

## 📖 專案簡介
本專案是一個整合多電商平台的即時比價系統，使用者只需輸入關鍵字，系統即可自動從 **PChome、MOMO、蝦皮** 等平台擷取最新的商品價格，並透過 **MongoDB** 追蹤歷史價格波動，提供直觀的數據視覺化分析。

## 🚀 核心技術亮點

### 1. 異質 API 逆向工程 (API Reverse Engineering)
* 不同於傳統易出錯的 HTML Parsing，本專案分析並串接各電商平台的底層 RESTful API。
* 實作資料清洗 (Data Cleaning) 邏輯，自動剔除「二手」、「配件」、「保護殼」等非目標商品資訊。

### 2. 歷史價格追蹤 (NoSQL Data Persistence)
* 使用 **MongoDB** 紀錄每一次搜尋的最低價數據，構建時序型數據庫。
* 利用 Flask 後端處理數據聚合，提供前端精確的歷史趨勢分析。

### 3. 前端動態視覺化 (Data Visualization)
* 透過 **Chart.js** 實作動態折線圖，即時呈現商品價格走勢。
* 採用響應式設計 (Responsive Design)，並內建搜尋載入動畫 (Spinner)，優化使用者體驗。

## 🏗️ 系統架構
1. **Scraper Layer**: 負責對各電商平台發送模擬請求，處理資料擷取 (Data Extraction) 與分頁邏輯 (Pagination)。
2. **Backend Layer**: 使用 Flask 處理路由、邏輯運算與 MongoDB 數據存取。
3. **Frontend Layer**: 基於 Jinja2 模板引擎與 CSS 網格系統 (Grid) 建構現代化 UI。

## 🛠️ 技術細節與挑戰
在開發過程中，針對各大電商的反爬蟲機制進行了深入研究：
* **PChome**: 實作動態 `totalPage` 偵測，達成全分頁自動抓取。
* **MOMO**: 透過封包分析擷取 JSON Payload，並繞過基礎 WAF 限制。
* **Shopee (Experimental)**: 針對高強度反爬蟲（403 Forbidden）進行標頭模擬與 Cookie 處理研究。

## 📦 快速開始
1. 安裝環境依賴：
   ```bash
   pip install flask pymongo requests
   ```
2. 啟動本地 MongoDB 伺服器。

3. 執行主程式：
```bash
    python app.py