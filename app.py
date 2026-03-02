import streamlit as st
from tavily import TavilyClient
import google.generativeai as genai

# Cấu hình giao diện
st.set_page_config(page_title="Fact Checker AI", page_icon="🛡️")

# Lấy Key từ Secrets
try:
    TAVILY_KEY = st.secrets["TAVILY_KEY"]
    GEMINI_KEY = st.secrets["GEMINI_KEY"]
except:
    st.error("Chưa cấu hình API Key trong phần Secrets!")
    st.stop()

# Khởi tạo
tavily = TavilyClient(api_key=TAVILY_KEY)
genai.configure(api_key=GEMINI_KEY)

def verify_info(content):
    try:
        # 1. Tìm kiếm
        search_result = tavily.search(query=content, search_depth="advanced", max_results=5)
        context = "\n".join([f"Nguồn: {r['url']}\nNội dung: {r['content']}" for r in search_result['results']])
        
        # 2. Gọi Model với tên đầy đủ (Fix lỗi 404)
        # Thử với gemini-1.5-flash, nếu không được sẽ tự động dùng gemini-pro
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"Dựa trên dữ liệu sau:\n{context}\n\nHãy kiểm chứng xem thông tin này đúng hay sai: {content}"
            response = model.generate_content(prompt)
        except:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(f"Kiểm chứng: {content}\nBối cảnh: {context}")
            
        return response.text
    except Exception as e:
        return f"Lỗi kết nối: {str(e)}"

# Giao diện
st.title("🛡️ Máy Kiểm Chứng Thông Tin")
input_text = st.text_area("Nhập nội dung cần check:")

if st.button("Kiểm tra ngay"):
    if input_text:
        with st.spinner('Đang rà soát dữ liệu...'):
            result = verify_info(input_text)
            st.markdown(result)
