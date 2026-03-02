import streamlit as st
from tavily import TavilyClient
import google.generativeai as genai

# Cấu hình API (Thay key của bạn vào đây)
genai.configure(api_key="YOUR_GEMINI_KEY")
tavily = TavilyClient(api_key="YOUR_TAVILY_KEY")

def verify_info(content):
    # 1. Tìm kiếm thông tin liên quan trên mạng
    search_result = tavily.search(query=content, search_depth="advanced")
    context = "\n".join([f"Nguồn: {r['url']}\nNội dung: {r['content']}" for r in search_result['results']])
    
    # 2. Dùng AI để phân tích và đối chiếu
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Bạn là một chuyên gia kiểm chứng thông tin. 
    Nội dung cần kiểm tra: {content}
    Dữ liệu đối chiếu từ internet: {context}
    
    Hãy trả về kết quả theo cấu trúc:
    1. Đánh giá: (Đúng/Sai/Thiếu căn cứ)
    2. Giải thích chi tiết:
    3. Các nguồn link đối chiếu:
    """
    response = model.generate_content(prompt)
    return response.text

# Giao diện web
st.title("🛡️ Hệ thống Kiểm chứng Thông tin")
user_input = st.text_area("Nhập nội dung hoặc dán link cần kiểm tra tại đây:")

if st.button("Kiểm tra ngay"):
    if user_input:
        with st.spinner('Đang đối soát dữ liệu thực tế...'):
            result = verify_info(user_input)
            st.markdown(result)
    else:
        st.warning("Vui lòng nhập nội dung!")
