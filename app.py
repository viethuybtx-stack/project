import streamlit as st
from tavily import TavilyClient
import google.generativeai as genai

# Cấu hình giao diện
st.set_page_config(page_title="Fact Checker AI", page_icon="🛡️")

# NHẬP KEY CỦA BẠN VÀO ĐÂY
TAVILY_KEY = st.secrets["TAVILY_KEY"]
GEMINI_KEY = st.secrets["GEMINI_KEY"]

# Khởi tạo clients
tavily = TavilyClient(api_key=TAVILY_KEY)
genai.configure(api_key=GEMINI_KEY)

def verify_info(content):
    try:
        # 1. Tìm kiếm dữ liệu thực tế
        search_result = tavily.search(query=content, search_depth="advanced", max_results=5)
        context = "\n".join([f"Nguồn: {r['url']}\nNội dung: {r['content']}" for r in search_result['results']])
        
        # 2. Gửi cho Gemini phân tích
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""
        Bạn là một chuyên gia kiểm chứng tin tức độc lập. 
        Nhiệm vụ: Phân tích nội dung sau dựa trên dữ liệu internet được cung cấp.
        
        NỘI DUNG CẦN KIỂM TRA: "{content}"
        
        DỮ LIỆU ĐỐI CHIẾU: 
        {context}
        
        YÊU CẦU TRÌNH BÀY:
        - Đánh giá: (ĐÚNG / SAI / GÂY TRANH CÃI / THIẾU CĂN CỨ)
        - Tóm tắt lý do (ngắn gọn, súc tích).
        - Trích dẫn các nguồn link hỗ trợ.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Có lỗi xảy ra: {e}"

# GIAO DIỆN NGƯỜI DÙNG
st.title("🛡️ Máy Kiểm Chứng Thông Tin Nhanh")
st.markdown("Hệ thống sử dụng AI và Tìm kiếm thời gian thực để xác minh độ tin cậy của thông tin.")

input_text = st.text_area("Dán nội dung bài viết, tin đồn hoặc link cần check:", placeholder="Ví dụ: Ăn sầu riêng uống Coca có chết người không?")

if st.button("Bắt đầu kiểm chứng"):
    if input_text:
        with st.spinner('Đang rà soát toàn bộ internet...'):
            result = verify_info(input_text)
            st.divider()
            st.markdown(result)
    else:
        st.error("Vui lòng không để trống nội dung!")
