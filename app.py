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
        "Bài 2: Công thức lượng giác": "LY-THUYET-BAI-2.jpg",
        "Bài 3: Hàm số lượng giác": "LY-THUYET-BAI-3.jpg",
        "Bài 4: Phương trình lượng giác cơ bản": "LY-THUYET-BAI-4.jpg"
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
# ================= TAB 3: AI SINH ĐỀ TỐI ƯU TỐC ĐỘ =================
with tab_luyentap:
    st.subheader("Luyện tập thông minh dựa trên ngân hàng đề kiểm tra")
    st.write("Hệ thống AI sẽ tạo bài tập phân hóa theo chuẩn cấu trúc đề kiểm tra để em rèn luyện:")

    c1, c2 = st.columns(2)
    with c1:
        topic = st.selectbox(
            "Chọn chủ đề kiến thức:",
            [
                "Giá trị lượng giác và công thức biến đổi",
                "Tập xác định, tính chẵn lẻ và đồ thị hàm số lượng giác",
                "Phương trình lượng giác cơ bản",
                "Bài toán ứng dụng thực tế lượng giác"
            ]
        )
    with c2:
        level = st.selectbox("Mức độ tư duy:", ["Nhận biết", "Thông hiểu", "Vận dụng"])

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        btn_gen = st.button("🎲 AI tạo câu hỏi mới")
    with col_btn2:
        btn_clone = st.button("🔁 Tạo câu tương tự dạng vừa làm")

    # Đọc và bốc mẫu ngẫu nhiên từ kho đề (chỉ lấy 2-3 câu để app chạy siêu nhanh)
    mau_cau_hoi = ""
    if os.path.exists("kho_de.txt"):
        try:
            with open("kho_de.txt", "r", encoding="utf-8") as f:
                noi_dung = f.read()
                # Tách thành các câu hỏi riêng biệt
                danh_sach_cau = [c.strip() for c in noi_dung.split("Câu ") if c.strip()]
                import random
                if danh_sach_cau:
                    so_luong_mau = min(3, len(danh_sach_cau))
                    mau_cau_hoi = "Câu " + "\n\nCâu ".join(random.sample(danh_sach_cau, so_luong_mau))
        except Exception:
            mau_cau_hoi = ""

    # Xử lý tạo câu hỏi
    if btn_gen or btn_clone:
        if not client:
            st.error("Chưa cấu hình API Key.")
        elif btn_clone and "last_q" not in st.session_state:
            st.warning("Em cần tạo và làm thử 1 câu trước khi chọn tạo câu tương tự!")
        else:
            with st.spinner("Đang khởi tạo câu hỏi trong giây lát..."):
                # Nếu bấm nút tạo câu tương tự: chỉ gửi đúng câu vừa làm
                if btn_clone:
                    prompt = f"""
                    Bạn là chuyên gia khảo thí Toán THPT Việt Nam (GDPT 2018).
                    Câu hỏi gốc học sinh vừa làm:
                    "{st.session_state['last_q']}"

                    Yêu cầu:
                    1. Tạo 1 câu hỏi MỚI CÙNG DẠNG (giữ nguyên mô hình bài toán, chỉ thay đổi số liệu/hàm số).
                    2. Toàn bộ công thức toán học bắt buộc viết bằng LaTeX chuẩn trong $...$ hoặc $$...$$.
                    3. Trả về định dạng JSON thuần:
                    {{
                      "question": "Nội dung câu hỏi...",
                      "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
                      "correct_answer": "A",
                      "explanation": "Lời giải ngắn gọn từng bước..."
                    }}
                    """
                # Nếu bấm nút tạo mới: gửi câu mẫu trích xuất ngắn gọn
                else:
                    prompt = f"""
                    Bạn là chuyên gia khảo thí Toán THPT Việt Nam (GDPT 2018).
                    Dưới đây là một số câu hỏi mẫu từ đề kiểm tra:
                    ---
                    {mau_cau_hoi}
                    ---
                    Yêu cầu:
                    1. Tạo 1 câu trắc nghiệm thuộc chủ đề: "{topic}", mức độ: "{level}".
                    2. Tham khảo phong cách ra đề của câu mẫu, tạo các phương án nhiễu đánh trúng bẫy sai lầm.
                    3. Toàn bộ công thức toán học bắt buộc viết bằng LaTeX chuẩn trong $...$ hoặc $$...$$.
                    4. Trả về định dạng JSON thuần:
                    {{
                      "question": "Nội dung câu hỏi...",
                      "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
                      "correct_answer": "A",
                      "explanation": "Lời giải ngắn gọn từng bước..."
                    }}
                    """

                try:
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                            temperature=0.7
                        )
                    )
                    st.session_state["quiz"] = json.loads(response.text)
                    st.session_state["submitted"] = False
                    st.session_state["last_q"] = st.session_state["quiz"]["question"]
                except Exception as e:
                    st.error(f"Hệ thống đang bận, em hãy bấm lại lần nữa nhé (Chi tiết: {e})")

    # Hiển thị câu hỏi cho học sinh làm
    if "quiz" in st.session_state:
        q = st.session_state["quiz"]
        st.markdown("---")
        st.markdown(f"**Câu hỏi:** {q['question']}")

        choice = st.radio(
            "Chọn đáp án đúng:",
            ["A", "B", "C", "D"],
            format_func=lambda x: f"{x}. {q['options'][x]}"
        )

        if st.button("Nộp bài & Kiểm tra"):
            st.session_state["submitted"] = True

        if st.session_state.get("submitted", False):
            if choice == q["correct_answer"]:
                st.success("🎉 Chính xác! Em đã làm chủ dạng toán này.")
            else:
                st.error(f"❌ Chưa chính xác. Đáp án đúng là: **{q['correct_answer']}**")
                st.info("💡 Em có thể bấm nút **'🔁 Tạo câu tương tự dạng vừa làm'** ở trên để làm một câu tương đương nhé!")

            with st.expander("📖 Xem lời giải chi tiết và phân tích sai lầm", expanded=True):
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
                    model='gemini-2.0-flash',
                    contents=tutor_prompt
                )
                st.markdown(res.text)
