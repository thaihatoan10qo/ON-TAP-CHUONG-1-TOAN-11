import streamlit as st
import json
import os
import streamlit.components.v1 as components
from google import genai
from google.genai import types

# 1. Cấu hình giao diện
st.set_page_config(
    page_title="Ôn Tập & Luyện Thi Toán 11 - Chương 1",
    page_icon="📐",
    layout="wide"
)

st.title("📐 Nền Tảng Ôn Tập & Khảo Thí Cá Nhân Hóa Toán 11")
st.caption("Chương 1: Hàm số lượng giác và Phương trình lượng giác | Ứng dụng AI Hỗ trợ Giảng dạy & Tự học")

# 2. Quản lý API Key an toàn
api_key = None
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Nhập Gemini API Key:", type="password")

client = genai.Client(api_key=api_key) if api_key else None

# 3. Tạo các phân hệ chức năng
tab_mophong, tab_lythuyet, tab_luyentap, tab_giasu = st.tabs([
    "🌀 1. Mô Phỏng Trực Quan", 
    "📖 2. Tóm Tắt Lý Thuyết",
    "📝 3. Luyện Tập Thích Ứng (AI Sinh Đề)", 
    "🤖 4. Gia Sư AI Hỏi Đáp"
])

# ================= TAB 1: MÔ PHỎNG TRỰC QUAN =================
with tab_mophong:
    st.subheader("Mô phỏng tương tác trực quan Chương 1")
    st.write("Học sinh chọn chuyên đề để thao tác với mô hình trực quan:")
    
    # Danh mục liên kết trực tiếp tới 3 file HTML bạn đã tải lên
    danh_sach_mo_phong = {
        "1. Giá trị lượng giác & Vòng tròn đơn vị": "GIÁ TRỊ LƯỢNG GIÁC.html",
        "2. Đồ thị & Tính chất Hàm số lượng giác": "HÀM SỐ LƯỢNG GIÁC.html",
        "3. Phương trình lượng giác cơ bản": "PT LƯỢNG GIÁC.html"
    }
    
    # Hộp lựa chọn chuyên đề
    lua_chon = st.selectbox("Chọn mô hình muốn tương tác:", list(danh_sach_mo_phong.keys()))
    file_html_can_chieu = danh_sach_mo_phong[lua_chon]
    
    # Đọc và hiển thị file HTML tương ứng
    if os.path.exists(file_html_can_chieu):
        with open(file_html_can_chieu, "r", encoding="utf-8") as f:
            html_content = f.read()
        components.html(html_content, height=680, scrolling=True)
    else:
        st.warning(f"Chưa tìm thấy file '{file_html_can_chieu}' trên hệ thống.")


 # ================= TAB 2: TÓM TẮT LÝ THUYẾT =================
with tab_lythuyet:
    st.subheader("Hệ thống hóa kiến thức trọng tâm bằng Infographic")
    st.write("Học sinh chọn bài học để xem sơ đồ tóm tắt lý thuyết:")

    # Khai báo đúng tên file thực tế bạn đã tải lên GitHub
    danh_sach_anh = {
        "Bài 1: Giá trị lượng giác của góc lượng giác": "LY-THUYET-BAI-1.jpg",
        "Bài 2: Công thức lượng giác": "LY-THUYET-BAI-2.pdf",
        "Bài 3: Hàm số lượng giác": "LY-THUYET-BAI-3.PDF",
        "Bài 4: Phương trình lượng giác cơ bản": "LY-THUYET-BAI-4.PDF"
    }

    bai_chon = st.selectbox("Chọn bài học cần ôn tập:", list(danh_sach_anh.keys()))
    file_anh = danh_sach_anh[bai_chon]

    if os.path.exists(file_anh):
        try:
            from PIL import Image
            img = Image.open(file_anh)
            st.image(img, caption=bai_chon, use_container_width=True)
        except Exception as e:
            st.error(f"Không thể đọc file ảnh '{file_anh}'. Vui lòng kiểm tra lại định dạng file (lỗi: {e}).")
    else:
        st.warning(f"Chưa tìm thấy file '{file_anh}' trên hệ thống. Hãy kiểm tra lại tên file trên GitHub.")

# ================= TAB 3: AI SINH ĐỀ LUYỆN TẬP =================
with tab_luyentap:
    st.subheader("Luyện tập trắc nghiệm phân hóa theo mảng kiến thức")
    
    c1, c2 = st.columns(2)
    with c1:
        topic = st.selectbox(
            "Mảng kiến thức cần luyện:",
            [
                "Khái niệm góc lượng giác và giá trị lượng giác",
                "Công thức lượng giác (cộng, nhân đôi, biến đổi)",
                "Tập xác định, tính chẵn lẻ và đồ thị hàm số lượng giác",
                "Giải phương trình lượng giác cơ bản"
            ]
        )
    with c2:
        level = st.selectbox("Mức độ yêu cầu:", ["Nhận biết", "Thông hiểu", "Vận dụng"])

    if st.button("🎲 AI Tạo Câu Hỏi Ngẫu Nhiên"):
        if not client:
            st.error("Chưa cấu hình API Key. Vui lòng cung cấp khóa ở cột bên trái.")
        else:
            with st.spinner("AI đang tạo câu hỏi chuẩn hóa chương trình GDPT 2018..."):
                prompt = f"""
                Bạn là chuyên gia khảo thí Toán THPT Việt Nam (Chương trình GDPT 2018).
                Tạo 1 câu hỏi trắc nghiệm Toán 11 Chương 1:
                - Chủ đề: {topic}
                - Mức độ: {level}
                - Toàn bộ ký hiệu toán học phải viết chuẩn LaTeX đặt trong cặp dấu $...$ (nếu inline) hoặc $$...$$ (nếu display).
                
                Trả về kết quả dưới dạng JSON thuần theo mẫu sau (không chứa markdown khác ngoài json):
                {{
                  "question": "Nội dung câu hỏi...",
                  "options": {{
                     "A": "Đáp án A",
                     "B": "Đáp án B",
                     "C": "Đáp án C",
                     "D": "Đáp án D"
                  }},
                  "correct_answer": "A",
                  "explanation": "Lời giải chi tiết từng bước..."
                }}
                """
                try:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                        config=types.GenerateContentConfig(response_mime_type="application/json")
                    )
                    st.session_state["quiz"] = json.loads(response.text)
                    st.session_state["submitted"] = False
                except Exception as e:
                    st.error(f"Lỗi tạo câu hỏi: {e}")

    # Hiển thị bài tập nếu đã sinh thành công
    if "quiz" in st.session_state:
        q = st.session_state["quiz"]
        st.markdown("---")
        st.markdown(f"**Câu hỏi:** {q['question']}")
        
        choice = st.radio(
            "Chọn phương án trả lời:",
            ["A", "B", "C", "D"],
            format_func=lambda x: f"{x}. {q['options'][x]}"
        )
        
        if st.button("Xác nhận nộp bài"):
            st.session_state["submitted"] = True
            
        if st.session_state.get("submitted", False):
            if choice == q["correct_answer"]:
                st.success("🎉 Chính xác! Bạn đã hiểu đúng bản chất vấn đề.")
            else:
                st.error(f"❌ Đáp án chưa đúng. Phương án chính xác là: **{q['correct_answer']}**")
            
            with st.expander("📖 Xem lời giải chi tiết và phân tích", expanded=True):
                st.markdown(q["explanation"])

# ================= TAB 4: GIA SƯ AI =================
with tab_giasu:
    st.subheader("Hỏi đáp trực tiếp cùng Trợ lý Gia sư AI")
    user_q = st.text_input("Nhập câu hỏi hoặc phần kiến thức em chưa hiểu rõ:")
    
    if st.button("Gửi câu hỏi cho Gia sư"):
        if not client:
            st.error("Chưa cấu hình API Key.")
        elif user_q.strip():
            with st.spinner("Gia sư AI đang soạn phản hồi..."):
                tutor_prompt = f"""
                Bạn là một thầy/cô giáo dạy Toán THPT nhiệt tình, chuẩn mực sư phạm. 
                Hãy giải đáp ngắn gọn, dễ hiểu, trực quan cho học sinh câu hỏi sau:
                "{user_q}"
                Yêu cầu: Công thức toán viết bằng LaTeX đặt trong dấu $ hoặc $$.
                """
                res = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=tutor_prompt
                )
                st.markdown(res.text)
