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

# ================= TAB 1: MÔ PHỎNG TRỰC QUAN TỪ FILE HTML =================
with tab_mophong:
    st.subheader("Mô phỏng tương tác: Góc lượng giác")
    st.write("Học sinh tương tác trực tiếp với mô hình trực quan để củng cố khái niệm:")
    
    html_filename = "GIÁ TRỊ LƯỢNG GIÁC.html"
    if os.path.exists(html_filename):
        with open(html_filename, "r", encoding="utf-8") as f:
            html_content = f.read()
        # Hiển thị trực tiếp file HTML
        components.html(html_content, height=650, scrolling=True)
    else:
        st.warning(f"Chưa tìm thấy file '{html_filename}' trong thư mục kho lưu trữ.")

# ================= TAB 2: TÓM TẮT LÝ THUYẾT =================
with tab_lythuyet:
    st.subheader("Hệ thống công thức trọng tâm")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 1. Công thức cộng lượng giác")
        st.latex(r"\sin(a \pm b) = \sin a \cos b \pm \cos a \sin b")
        st.latex(r"\cos(a \pm b) = \cos a \cos b \mp \sin a \sin b")
        
        st.markdown("#### 2. Công thức nhân đôi")
        st.latex(r"\sin 2a = 2\sin a \cos a")
        st.latex(r"\cos 2a = \cos^2 a - \sin^2 a = 2\cos^2 a - 1 = 1 - 2\sin^2 a")
    
    with col2:
        st.markdown("#### 3. Tập xác định & Chu kỳ")
        st.write(r"- $y = \sin x, y = \cos x$: $D = \mathbb{R}$, tuần hoàn chu kỳ $T = 2\pi$")
        st.write(r"- $y = \tan x$: $D = \mathbb{R} \setminus \left\{\frac{\pi}{2} + k\pi, k \in \mathbb{Z}\right\}$, chu kỳ $T = \pi$")
        st.write(r"- $y = \cot x$: $D = \mathbb{R} \setminus \{k\pi, k \in \mathbb{Z}\}$, chu kỳ $T = \pi$")

        st.markdown("#### 4. Phương trình cơ bản")
        st.latex(r"\sin x = \sin \alpha \iff x = \alpha + k2\pi \text{ hoặc } x = \pi - \alpha + k2\pi")
        st.latex(r"\cos x = \cos \alpha \iff x = \pm \alpha + k2\pi")

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
