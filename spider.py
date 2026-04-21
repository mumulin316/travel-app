# spider.py 【纯工具版】
import requests
import os
import time

API_KEY = os.getenv("DEEPSEEK_API_KEY")

# ==============================
# 流式输出工具（给景点介绍用）
# ==============================
def stream_output(text, delay=0.03):
    result = ""
    for char in text:
        result += char
        time.sleep(delay)
    return result

# ==============================
# 景点介绍（工具方法，外部传入图片）
# ==============================
def get_spot_intro(spot_name, city_name, spot_image_url):
    if not API_KEY:
        return "⚠️ 未配置环境变量 DEEPSEEK_API_KEY"

    try:
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"  # 确保这里是英文引号 ""
        }

        prompt = f"""
你是专业旅游解说，请用优美简洁的语言介绍：
城市：{city_name}
景点：{spot_name}
内容包括：历史背景、文化价值、看点亮点。200字内，文风雅致。
""".strip()

        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 600
        }

        res = requests.post(url, headers=headers, json=data, timeout=15)
        res_json = res.json()

        text = res_json["choices"][0]["message"]["content"].strip() if "choices" in res_json else "暂无介绍"

        # 图片由外部传入，不再在工具里存
        img_markdown = f"![{spot_name}]({spot_image_url})" if spot_image_url else ""
        final_text = f"{img_markdown}\n\n【景点简介】\n{text}"
        return stream_output(final_text)

    except Exception as e:
        return f"加载失败：{str(e)}"

# ==============================
# 城市特色小吃（通用工具）
# ==============================
# ... existing code ...

# ... existing code ...

def get_city_food(city_name, spot_name=""):
    if not API_KEY:
        return "未配置API Key"

    try:
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        if spot_name:
            prompt = f"""你是{city_name}本地美食专家，请推荐【{spot_name}】景点周边的地道特色美食。

严格要求：
1. 必须是{spot_name}附近3公里内能吃到的本地特色
2. 绝对不能列其他城市或其他景点的美食
3. 只写菜品名字，用顿号分隔
4. 列出6-10种即可
5. 不要任何解释、序号、多余文字

示例格式：烧鹅濑粉、厚街腊肠、道滘肉丸粥""".strip()
        else:
            prompt = f"""你是{city_name}本地美食专家，请列出【{city_name}市】最具代表性的地道特色美食。

严格要求：
1. 必须是{city_name}独有的或最有名的本地特色
2. 绝对不能列其他城市的美食
3. 只写菜品名字，用顿号分隔
4. 列出8-12种即可
5. 不要任何解释、序号、多余文字

示例格式：虾饺、干蒸烧卖、叉烧包、蛋挞""".strip()

        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": f"你是{city_name}本地人，非常了解当地美食"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.8,
            "max_tokens": 200,
            "top_p": 0.9
        }

        res = requests.post(url, headers=headers, json=data, timeout=15)
        res_json = res.json()

        if "choices" in res_json:
            result = res_json["choices"][0]["message"]["content"].strip()
            # 添加调试信息
            location = f"{spot_name}周边" if spot_name else city_name
            print(f"✅ [{location}] AI返回: {result}")
            return result
        else:
            print(f"❌ [{city_name}] API错误: {res_json}")
            return "暂无美食"
    except Exception as e:
        print(f"❌ [{city_name}] 请求失败: {str(e)}")
        return "获取失败"
