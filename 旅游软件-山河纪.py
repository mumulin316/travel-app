import streamlit as st
import spider
import time
from guangdong import dongguan,guangzhou
#
# st.set_page_config(page_title="山河纪 - 广东旅游攻略", layout="wide")
# st.title("🌏 山河纪 - 广东旅游攻略")
# 手机适配配置
st.set_page_config(
    page_title="山河纪",
    page_icon="🌍",
    layout="centered",  # 居中布局，更适合手机
    initial_sidebar_state="collapsed"  # 隐藏侧边栏
)

# 禁止缩放，模拟原生App效果
st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
""", unsafe_allow_html=True)

# 城市路由映射（以后加城市只在这里加一行）
city_data_map = {
    "东莞": dongguan,
    "广州": guangzhou
}

# 1. 选择城市
selected_city = st.selectbox("请选择城市", list(city_data_map.keys()))
city_data = city_data_map[selected_city]

# 2. 加载该城市的景点列表
selected_spot = st.selectbox("请选择景点", city_data.spots)

# 3. 页面展示（带加载条，体验拉满）
if selected_spot:
    # 3.1 历史文化（图片+简介，带加载条）
    st.subheader("🏛️ 历史文化")
    with st.spinner("正在加载景点信息..."):
        # 从数据文件里取图片URL，传给工具
        image_url = city_data.spot_images.get(selected_spot, "")
        intro_text = spider.get_spot_intro(selected_spot, selected_city, image_url)
    st.write(intro_text)

    # ... existing code ...

    # 3.2 特色小吃（带加载条）
    st.subheader("🍜 特色小吃")
    with st.spinner("正在查询特色美食..."):
        # 传入景点名称，获取该景点周边美食
        food_text = spider.get_city_food(selected_city, selected_spot)
    st.write(food_text)

    # ... existing code ...

    # 3.3 交通指南（固定在最下方，带加载条）
    st.subheader("🚗 交通指南")
    with st.spinner("正在获取交通路线..."):
        # 从数据文件里直接取交通信息
        traffic_text = city_data.traffic_guide.get(selected_spot, "暂无交通信息")
    st.write(traffic_text)
