from flask import Flask
import requests
import datetime
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/", methods=['GET'])
def GetPredictProfit():
    info_url = "http://hq.sinajs.cn/list="

    rebar_code = "RB2001"

    iron_code = "I2001"
    coke_code = "J2001"

    # 获取铁矿最新价
    url = info_url + iron_code
    result = requests.get(url)
    result_str = result.text.split("\"")[1]

    iron_lastest_price = float(result_str.split(",")[8])

    # 获取焦炭最新价
    url = info_url + coke_code
    result = requests.get(url)
    result_str = result.text.split("\"")[1]

    coke_lastest_price = float(result_str.split(",")[8])

    # 获取螺纹钢最新价
    url = info_url + rebar_code
    result = requests.get(url)
    result_str = result.text.split("\"")[1]

    rebar_lastest_price = float(result_str.split(",")[8])

    # 获取废钢价格
    result = requests.get("http://www.96369.net/indices/78").text

    soup = BeautifulSoup(result, "html.parser")
    scrap_steel_price = float(soup.find("table", attrs={"class", "mod_tab"}).tr.next_sibling.next_sibling.td.next_sibling.get_text())

    # 计算
    b = 0.5

    cal_result = 1.6 * float(iron_lastest_price) + b * float(coke_lastest_price)

    final_price = round((0.95 * cal_result + 0.15 * scrap_steel_price) / 0.8 + 200, 2)

    predict_profit = rebar_lastest_price - final_price
    return "钢厂预期收益："+str(round(predict_profit,2))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)