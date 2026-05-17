import requests
import re # 1. 引入正規表示式模組
from urllib.parse import quote # 處理編碼問題
import requests
import time # 加入延遲，避免爬太快被封鎖

def search_pchome(keyword, max_pages=3):
    all_products = []
    current_page = 1
    total_page = 1 # 初始預設為 1

    while current_page <= total_page and current_page <= max_pages:
        # 將 page={current_page} 帶入網址
        url = f"https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={keyword}&page={current_page}&sort=rnk/dc"
        
        try:
            print(f"正在爬取 PChome 第 {current_page} 頁...")
            response = requests.get(url, timeout=10)
            data = response.json()
            
            # 1. 第一次爬取時，更新總頁數
            if current_page == 1:
                total_page = data.get("totalPage", 1)
                print(f"該關鍵字總共有 {total_page} 頁")

            # 2. 解析商品資料
            if "prods" in data and data["prods"]:
                for item in data["prods"]:
                    # (這裡保留你原本的過濾邏輯與資料格式)
                    all_products.append({
                        "name": item["name"],
                        "price": item["price"],
                        "platform": "PChome",
                        "url": f"https://24h.pchome.com.tw/prod/{item['Id']}",
                        "image": f"https://cs-a.ecimg.tw{item['picS']}"
                    })
            else:
                # 如果該頁沒資料了，提早跳出
                break
            
            current_page += 1
            time.sleep(1) # 暫停 1 秒，這在爬蟲開發中是「禮貌」的表現
            
        except Exception as e:
            print(f"PChome 爬取第 {current_page} 頁出錯: {e}")
            break

    return all_products

def search_momo(keyword):
    # MOMO 搜尋 API
    url = "https://apisearch.momoshop.com.tw/momoSearchCloud/moec/textSearch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    # MOMO 需要的參數
    payload = {
        "host": "momoshop",
        "flag": "searchEngine",
        "data": {
            "searchValue": keyword,
            "curPage": "1",
            "pageSize": "20",
            "searchType": "1"
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        data = response.json()
        products = []
        # 這裡定義排除清單 (黑名單)
        exclude_keywords = ['殼', '貼', '套', '線', '架', '二手', '保護']

        if "rtnSearchData" in data and "goodsInfoList" in data["rtnSearchData"]:
            for item in data["rtnSearchData"]["goodsInfoList"]:
                name = item["goodsName"]
                
                # 處理價格字串轉為整數
                price_numbers = "".join(re.findall(r'\d+', item["goodsPrice"]))
                price = int(price_numbers) if price_numbers else 0

                
                # 1. 檢查標題是否包含任何排除字
                # any() 會檢查 name 裡面有沒有出現 exclude_keywords 的任一個詞
                is_accessory = any(word in name for word in exclude_keywords)
                
                # 2. 判斷是否要保留這個商品
                # 如果你要搜尋手機，建議價格門檻設高一點 (例如 5000)
                # 如果你要搜尋一般商品，可以把門檻拿掉或調低
                if not is_accessory and price > 1000: 
                    products.append({
                        "name": name,
                        "price": price,
                        "platform": "MOMO",
                        "url": f"https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code={item['goodsCode']}",
                        "image": item["imgUrl"]
                    })
                
            
        return products
    except Exception as e:
        print(f"MOMO 爬蟲解析出錯: {e}")
        return []
    
def search_shopee(keyword):
    # 對關鍵字進行 URL 編碼，避免 latin-1 錯誤
    encoded_keyword = quote(keyword)
    url = f"https://shopee.tw/api/v4/search/search_items?by=relevancy&keyword={encoded_keyword}&limit=20&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": f"https://shopee.tw/search?keyword={encoded_keyword}",
        "x-api-source": "pc",
        "af-ac-enc-dat": "null", # 有些 API 需要這個欄位
    }

    try:
        # 蝦皮有時需要先訪問主頁獲取 Cookie，這裡我們先嘗試簡單請求
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 403:
            print("蝦皮 403：蝦皮的高強度反爬蟲機制。")
            return []

        data = response.json()
        products = []

        if "items" in data and data["items"]:
            for item in data["items"]:
                info = item["item_basic"]
                # 蝦皮價格需要除以 100,000 (它們內部的儲存格式)
                price = info["price"] // 100000 
                
                products.append({
                    "name": info["name"],
                    "price": price,
                    "platform": "蝦皮",
                    "url": f"https://shopee.tw/product/{info['shopid']}/{info['itemid']}",
                    "image": f"https://cf.shopee.tw/file/{info['image']}"
                })
            print(f"蝦皮成功抓取 {len(products)} 筆資料！")
        return products
    except Exception as e:
        print(f"蝦皮爬蟲出錯: {e}")
        return []