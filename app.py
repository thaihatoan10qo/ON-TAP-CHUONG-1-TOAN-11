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
# ================= TAB 3: LUYỆN TẬP THÍCH ỨNG (AI SINH ĐỀ TÍCH HỢP GEM) =================
with tab_luyentap:
    st.subheader("Luyện tập thông minh dựa trên ngân hàng đề kiểm tra")
    st.write("Hệ thống tích hợp trợ lý AI chuyên biệt, phân tích ngân hàng 82 câu kiểm tra thực tế để thiết kế bài tập bám sát chuẩn kiến thức:")

    c1, c2 = st.columns(2)
    with c1:
        topic = st.selectbox(
            "Chọn chủ đề kiến thức:",
            [
                "1. Giá trị lượng giác của góc lượng giác & Công thức lượng giác",
                "2. Hàm số lượng giác (Tập xác định, tính chẵn lẻ, chu kỳ, đồ thị)",
                "3. Phương trình lượng giác cơ bản & Điều kiện nghiệm",
                "4. Ứng dụng thực tế của hàm số và phương trình lượng giác"
            ]
        )
    with c2:
        level = st.selectbox("Mức độ tư duy:", ["Nhận biết", "Thông hiểu", "Vận dụng"])

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        btn_gen = st.button("🎲 AI tạo câu hỏi từ ngân hàng đề")
    with col_btn2:
        btn_clone = st.button("🔁 Tạo câu tương tự dạng vừa làm")

    # Đọc và bốc mẫu ngắn gọn từ file kho_de.txt (giúp gửi request nhanh, không bị timeout)
    mau_cau_hoi = ""
    if os.path.exists("kho_de.txt"):
        try:
            with open("kho_de.txt", "r", encoding="utf-8") as f:
                noi_dung = f.read()
                danh_sach_cau = [c.strip() for c in noi_dung.split("Câu ") if c.strip()]
                import random
                if danh_sach_cau:
                    so_luong = min(3, len(danh_sach_cau))
                    mau_cau_hoi = "Câu " + "\n\nCâu ".join(random.sample(danh_sach_cau, so_luong))
        except Exception:
            mau_cau_hoi = ""

    # Xử lý khi bấm nút tạo câu hỏi mới hoặc tạo câu tương tự
    if btn_gen or btn_clone:
        if not client:
            st.error("Chưa cấu hình API Key trong mục Secrets của Streamlit.")
        elif btn_clone and "last_q" not in st.session_state:
            st.warning("Em cần tạo và làm thử 1 câu trước khi chọn tạo câu tương tự!")
        else:
            with st.spinner("AI Chuyên gia đang thiết kế bài tập và phân tích bẫy sai lầm..."):
                # Thiết lập "Bộ não của Gem" qua system_instruction
                gem_instructions = """
                Bạn là Trợ lý Chuyên gia Khảo thí & Luyện thi Toán 11 THPT (Chương trình GDPT 2018).
                Nhiệm vụ sư phạm cốt lõi:
                1. Dựa vào ngân hàng câu hỏi thực tế hoặc câu hỏi mẫu để tạo câu hỏi trắc nghiệm tương đương.
                2. Xây dựng các phương án gây nhiễu (distractors) đánh trúng các lỗi sai kinh điển của học sinh: quên điều kiện xác định của tan/cot, nhầm dấu công thức cộng lượng giác, nhầm chu kỳ tuần hoàn (kpi hoặc k2pi).
                3. Bắt buộc viết tất cả công thức toán học bằng ký hiệu LaTeX chuẩn mực trong cặp dấu $...$ (nếu nằm cùng dòng chữ) hoặc $$...$$ (nếu hiển thị dòng riêng).
                4. Phần explanation (lời giải) phải trình bày chi tiết từng bước và chỉ rõ vì sao các phương án sai dễ gây nhầm lẫn để học sinh rút kinh nghiệm.
                5. Luôn trả về dữ liệu đúng định dạng JSON thuần.
                """

                if btn_clone:
                    prompt = f"""
                    Dưới đây là câu hỏi học sinh vừa làm:
                    "{st.session_state['last_q']}"

                    Yêu cầu:
                    Tạo 1 câu hỏi MỚI CÙNG DẠNG (giữ nguyên mô hình bài toán và mức độ tư duy, chỉ thay đổi số liệu/hàm số).
                    Trả về đúng định dạng JSON:
                    {{
                      "question": "Nội dung câu hỏi (chứa LaTeX)...",
                      "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
                      "correct_answer": "A",
                      "explanation": "Lời giải chi tiết từng bước và lưu ý bẫy sai lầm..."
                    }}
                    """
                else:
                    prompt = f"""
                    Dưới đây là một số câu hỏi trích mẫu từ đề kiểm tra thực tế:
                    ---
                    {mau_cau_hoi}
                    ---
                    Yêu cầu:
                    Tạo 1 câu hỏi trắc nghiệm thuộc chủ đề: "{topic}", mức độ: "{level}".
                    Bám sát văn phong và cấu trúc của câu hỏi mẫu.
                    Trả về đúng định dạng JSON:
                    {{
                      "question": "Nội dung câu hỏi (chứa LaTeX)...",
                      "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
                      "correct_answer": "A",
                      "explanation": "Lời giải chi tiết từng bước và lưu ý bẫy sai lầm..."
                    }}
                    """

                # Gọi API với cơ chế tự động thử lại nếu máy chủ bận (xử lý lỗi 503)
                success = False
                for attempt in range(3):
                    try:
                        response = client.models.generate_content(
                            model='gemini-3.8-flash',
                            contents=prompt,
                            config=types.GenerateContentConfig(
                                system_instruction=gem_instructions,
                                response_mime_type="application/json",
                                temperature=0.7
                            )
                        )
                        st.session_state["quiz"] = json.loads(response.text)
                        st.session_state["submitted"] = False
                        st.session_state["last_q"] = st.session_state["quiz"]["question"]
                        success = True
                        break
                    except Exception as err:
                        if "503" in str(err) and attempt < 2:
                            import time
                            time.sleep(2)
                            continue
                        elif attempt == 2:
                            pass

                # Dự phòng câu hỏi chuẩn nếu máy chủ Google quá tải kéo dài
                if not success:
                    st.info("💡 Máy chủ AI đang có lưu lượng truy cập lớn. Hệ thống đã tự động kích hoạt câu hỏi rèn luyện chuẩn từ ngân hàng để em không bị gián đoạn:")
                    st.session_state["quiz"] = {
                        "question": "Tìm tập xác định của hàm số $y = \\tan\\left(x - \\frac{\\pi}{3}\\right)$.",
                        "options": {
                            "A": "$D = \\mathbb{R} \\setminus \\left\\{\\frac{5\\pi}{6} + k\\pi, k \\in \\mathbb{Z}\\right\\}$",
                            "B": "$D = \\mathbb{R} \\setminus \\left\\{\\frac{\\pi}{3} + k\\pi, k \\in \\mathbb{Z}\\right\\}$",
                            "C": "$D = \\mathbb{R} \\setminus \\left\\{\\frac{5\\pi}{6} + k2\\pi, k \\in \\mathbb{Z}\\right\\}$",
                            "D": "$D = \\mathbb{R} \\setminus \\left\\{\\frac{\\pi}{2} + k\\pi, k \\in \\mathbb{Z}\\right\\}$"
                        },
                        "correct_answer": "A",
                        "explanation": "Hàm số xác định khi $x - \\frac{\\pi}{3} \\neq \\frac{\\pi}{2} + k\\pi \\Leftrightarrow x \\neq \\frac{5\\pi}{6} + k\\pi$ ($k \\in \\mathbb{Z}$). Sai lầm thường gặp: Quên chu kỳ của tan là $k\\pi$ mà chọn nhầm sang $k2\\pi$ (đáp án C) hoặc quên cộng góc $\\frac{\\pi}{3}$."
                    }
                    st.session_state["submitted"] = False
                    st.session_state["last_q"] = st.session_state["quiz"]["question"]

    # Hiển thị giao diện làm bài
    if "quiz" in st.session_state:
        q = st.session_state["quiz"]
        st.markdown("---")
        st.markdown(f"**Câu hỏi:** {q['question']}")

        choice = st.radio(
            "Chọn đáp án của em:",
            ["A", "B", "C", "D"],
            format_func=lambda x: f"{x}. {q['options'][x]}"
        )

        if st.button("Nộp bài & Kiểm tra đáp án"):
            st.session_state["submitted"] = True

        if st.session_state.get("submitted", False):
            if choice == q["correct_answer"]:
                st.success("🎉 Chính xác! Em đã nắm vững phương pháp giải và không bị mắc bẫy.")
            else:
                st.error(f"❌ Chưa chính xác. Đáp án đúng là: **{q['correct_answer']}**")
                st.info("💡 Em hãy đọc kỹ phân tích bẫy sai lầm bên dưới, sau đó bấm nút **'🔁 Tạo câu tương tự dạng vừa làm'** ở trên để làm lại câu tương đương nhé!")

            with st.expander("📖 Xem lời giải chi tiết và phân tích bẫy sai lầm", expanded=True):
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
