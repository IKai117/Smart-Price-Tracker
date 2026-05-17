from flask import Flask, render_template, request
from crawler import search_pchome, search_momo, search_shopee
from pymongo import MongoClient
import datetime

app = Flask(__name__)

# 1. 連線到本地 MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["Smart_Price_Tracker"]  # 資料庫名稱
collection = db["price_history"] # 集合名稱

@app.route('/')
def index():
    # 首頁進去時，給予空的 list，避免 JavaScript 讀取不到變數而出現 TypeError
    return render_template('index.html', results=[], labels=[], prices=[], stats=None)

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form.get('keyword')
    
    # 同時呼叫兩個爬蟲
    pchome_results = search_pchome(keyword)
    momo_results = search_momo(keyword)
    shopee_results = search_shopee(keyword)
    
    # 合併所有結果
    all_results = pchome_results + momo_results + shopee_results
    all_results.sort(key=lambda x: x['price']) # 全網最低價排序
    
    # 存入 MongoDB 
    if all_results:
        search_record = {
            "keyword": keyword,
            "timestamp": datetime.datetime.now(),
            "data": all_results
        }
        collection.insert_one(search_record)
    
    # 2. 從 MongoDB 抓出該關鍵字的「所有」歷史紀錄並按時間排序
    history_cursor = collection.find({"keyword": keyword}).sort("timestamp", 1)

    labels = []  # 用於前端圖表的 X 軸 (日期)
    prices = []  # 用於前端圖表的 Y 軸 (最低價)

    for record in history_cursor:
        # 格式化日期：2025-12-19
        date_str = record["timestamp"].strftime("%Y-%m-%d %H:%M")
        labels.append(date_str)
        
        # 找出該次搜尋紀錄中所有商品的最低價
        if record["data"]:
            current_min = min([p['price'] for p in record["data"]])
            prices.append(current_min)
        else:
            prices.append(0)


    # 3. 準備當次搜尋的統計資訊
    if all_results:
        current_prices = [p['price'] for p in all_results]
        stats = {
            "min": min(current_prices),
            "max": max(current_prices),
            "avg": sum(current_prices) // len(current_prices),
            "history_count": len(prices) # 告訴使用者總共有多少筆歷史紀錄
        }
    else:
        stats = None

    # 4. 最後將 results, labels, prices 全部傳給 index.html
    return render_template(
        'index.html', 
        results=all_results, # 傳送合併後的結果
        keyword=keyword, 
        stats=stats, 
        labels=labels, 
        prices=prices
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)