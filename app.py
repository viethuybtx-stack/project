import streamlit as st
from tavily import TavilyClient
import google.generativeai as genai

# Lấy Key từ hệ thống Secrets của Streamlit (Không dán trực tiếp vào code)
TAVILY_KEY = st.secrets["TAVILY_KEY"]
GEMINI_KEY = st.secrets["GEMINI_KEY"]

# Cấu hình
tavily = TavilyClient(api_key=TAVILY_KEY)
genai.configure(api_key=GEMINI_KEY)

def verify_info(content):
    try:
        # Bước 1: Tìm kiếm thông tin
        search_result = tavily.search(query=content, search_depth="advanced")
        context = "\n".join([f"Nguồn: {r['url']}\nNội dung: {r['content']}" for r in search_result['results']])
        
        # Bước 2: Gọi Model (Dùng 'gemini-1.5-flash' là ổn định nhất hiện nay)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"Kiểm chứng nội dung: {content}\n\nDựa trên dữ liệu: {context}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Lỗi hệ thống: {str(e)}"

# Giao diện Streamlit (Giữ nguyên phần dưới của bạn)
# ...
