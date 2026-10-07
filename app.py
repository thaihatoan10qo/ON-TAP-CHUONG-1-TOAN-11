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

st.title("NỀN TẢNG ÔN TẬP & KHẢO THÍ CÁ NHÂN HÓA TOÁN 11")
st.caption("Chương 1: Hàm số lượng giác và Phương trình lượng giác | Ứng dụng AI Hỗ trợ Giảng dạy & Tự học")

# 2. Quản lý API Key an toàn
api_key = None
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Nhập Gemini API Key:", type="password")

client = genai.Client(api_key=api_key) if api_key else None

# 3. Tạo các phân hệ chức năng
tab_mophong, tab_lythuyet, tab_luyentap = st.tabs([
    "🌀 1. MÔ PHỎNG TRỰC QUAN", 
    "📖 2. TÓM TẮT LÝ THUYẾT", 
    "✍️ 3. LUYỆN TẬP CÙNG GIA SƯ AI"
    "📝 4. KIỂM TRA THEO MA TRẬN"
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
# ================= TAB 3: LUYỆN TẬP THÍCH ỨNG & GIA SƯ AI TRỰC TIẾP =================
with tab_luyentap:
    st.subheader("Luyện tập thông minh & Gia sư AI đồng hành")
    st.write("Em hãy luyện tập các dạng bài trọng tâm. Sau khi nộp bài, em có thể đặt câu hỏi trực tiếp cho Gia sư AI về câu hỏi vừa làm:")

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

    # Đọc và bốc mẫu ngắn gọn từ file kho_de.txt
    danh_sach_tat_ca_cau = []
    mau_cau_hoi = ""
    if os.path.exists("kho_de.txt"):
        try:
            with open("kho_de.txt", "r", encoding="utf-8") as f:
                noi_dung = f.read()
                danh_sach_tat_ca_cau = [c.strip() for c in noi_dung.split("Câu ") if c.strip()]
                import random
                if danh_sach_tat_ca_cau:
                    so_luong = min(3, len(danh_sach_tat_ca_cau))
                    mau_cau_hoi = "Câu " + "\n\nCâu ".join(random.sample(danh_sach_tat_ca_cau, so_luong))
        except Exception:
            mau_cau_hoi = ""

    # Xử lý sinh câu hỏi
    if btn_gen or btn_clone:
        if not client:
            st.error("Chưa cấu hình API Key trong mục Secrets của Streamlit.")
        elif btn_clone and "last_q" not in st.session_state:
            st.warning("Em cần tạo và làm thử 1 câu trước khi chọn tạo câu tương tự!")
        else:
            with st.spinner("AI đang thiết kế bài tập..."):
                # Reset lịch sử chat khi đổi sang câu hỏi mới
                st.session_state["chat_history"] = []

                gem_instructions = """
                Bạn là Trợ lý Chuyên gia Khảo thí Toán 11 THPT (GDPT 2018).
                Nhiệm vụ:
                1. Dựa vào câu hỏi mẫu/câu hỏi gốc để tạo câu hỏi trắc nghiệm tương đương.
                2. Xây dựng các phương án gây nhiễu đánh trúng lỗi sai kinh điển: quên điều kiện tan/cot, nhầm dấu công thức cộng, nhầm chu kỳ kpi/k2pi.
                3. Bắt buộc viết công thức toán bằng ký hiệu LaTeX chuẩn trong cặp $...$ hoặc $$...$$.
                4. Explanation (lời giải) trình bày chi tiết và chỉ rõ các bẫy sai lầm.
                5. Luôn trả về đúng định dạng JSON thuần.
                """

                if btn_clone:
                    prompt = f"""
                    Câu hỏi gốc học sinh vừa làm:
                    "{st.session_state['last_q']}"

                    Hãy tạo 1 câu hỏi MỚI CÙNG DẠNG (thay đổi số liệu/hàm số, giữ nguyên mô hình tư duy).
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
                    Dưới đây là một số câu trích mẫu từ đề kiểm tra:
                    ---
                    {mau_cau_hoi}
                    ---
                    Yêu cầu:
                    Tạo 1 câu hỏi trắc nghiệm thuộc chủ đề: "{topic}", mức độ: "{level}".
                    Bám sát văn phong câu mẫu.
                    Trả về đúng định dạng JSON:
                    {{
                      "question": "Nội dung câu hỏi (chứa LaTeX)...",
                      "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
                      "correct_answer": "A",
                      "explanation": "Lời giải chi tiết từng bước và lưu ý bẫy sai lầm..."
                    }}
                    """

                success = False
                cac_model = ['gemini-3.1-flash-lite', 'gemini-3.8-flash']
                for ten_model in cac_model:
                    try:
                        response = client.models.generate_content(
                            model=ten_model,
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
                    except Exception:
                        continue

                if not success:
                    import random
                    cau_du_phong = "Tìm tập xác định của hàm số $y = \\tan\\left(x - \\frac{\\pi}{3}\\right)$."
                    if danh_sach_tat_ca_cau:
                        cau_ngau_nhien = random.choice(danh_sach_tat_ca_cau)
                        cau_du_phong = "Câu " + cau_ngau_nhien

                    st.info("💡 Đường truyền AI đang bận, hệ thống trích xuất câu chuẩn từ ngân hàng để em luyện tập ngay:")
                    st.session_state["quiz"] = {
                        "question": cau_du_phong,
                        "options": {
                            "A": "$D = \\mathbb{R} \\setminus \\left\\{\\frac{5\\pi}{6} + k\\pi, k \\in \\mathbb{Z}\\right\\}$",
                            "B": "$D = \\mathbb{R} \\setminus \\left\\{\\frac{\\pi}{3} + k\\pi, k \\in \\mathbb{Z}\\right\\}$",
                            "C": "$D = \\mathbb{R} \\setminus \\left\\{\\frac{5\\pi}{6} + k2\\pi, k \\in \\mathbb{Z}\\right\\}$",
                            "D": "$D = \\mathbb{R} \\setminus \\left\\{\\frac{\\pi}{2} + k\\pi, k \\in \\mathbb{Z}\\right\\}$"
                        },
                        "correct_answer": "A",
                        "explanation": "Hàm số xác định khi $x - \\frac{\\pi}{3} \\neq \\frac{\\pi}{2} + k\\pi \\Leftrightarrow x \\neq \\frac{5\\pi}{6} + k\\pi$ ($k \\in \\mathbb{Z}$)."
                    }
                    st.session_state["submitted"] = False
                    st.session_state["last_q"] = st.session_state["quiz"]["question"]

    # Hiển thị câu hỏi làm bài
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
            st.session_state["user_choice"] = choice

        # Khi học sinh nộp bài
        if st.session_state.get("submitted", False):
            user_c = st.session_state.get("user_choice", choice)
            if user_c == q["correct_answer"]:
                st.success("🎉 Chính xác! Em đã làm chủ phương pháp giải bài toán này.")
            else:
                st.error(f"❌ Chưa chính xác. Đáp án đúng là: **{q['correct_answer']}**")
                st.info("💡 Em đọc kỹ lời giải bên dưới rồi có thể trao đổi với Gia sư AI ngay phần bên dưới nhé!")

            with st.expander("📖 Xem lời giải chi tiết và phân tích bẫy sai lầm", expanded=True):
                st.markdown(q["explanation"])

            # ================= PHẦN GIA SƯ AI TRÒ CHUYỆN VỀ CÂU HỎI VỪA LÀM =================
            st.markdown("---")
            st.subheader("💬 Gia sư AI: Thắc mắc về câu hỏi này?")
            st.caption("Em chưa hiểu bước biến đổi nào, tại sao công thức lại như vậy hay muốn gợi ý cách nhớ? Hãy nhập câu hỏi bên dưới nhé!")

            if "chat_history" not in st.session_state:
                st.session_state["chat_history"] = []

            # Hiển thị các tin nhắn đã trao đổi
            for msg in st.session_state["chat_history"]:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

            # Khung nhập câu hỏi cho học sinh
            user_question = st.chat_input("Nhập câu hỏi của em về bài toán trên...")
            if user_question:
                # Lưu câu hỏi của học sinh
                st.session_state["chat_history"].append({"role": "user", "content": user_question})
                with st.chat_message("user"):
                    st.markdown(user_question)

                # Chuẩn bị ngữ cảnh cho Gia sư AI: Nắm rõ đề bài, đáp án học sinh chọn và lời giải
                context_prompt = f"""
                Bạn là Gia sư dạy Toán 11 THPT tận tâm, ân cần và sư phạm.
                Học sinh vừa làm câu hỏi sau:
                - Đề bài: {q['question']}
                - Các đáp án: {q['options']}
                - Đáp án đúng: {q['correct_answer']}
                - Đáp án học sinh đã chọn: {user_c}
                - Lời giải chi tiết: {q['explanation']}

                Học sinh đang thắc mắc: "{user_question}"

                Yêu cầu sư phạm:
                1. Trả lời trực tiếp vào thắc mắc của học sinh, giải thích cặn kẽ từng bước, không phán xét.
                2. Dùng lời văn động viên, gần gũi như thầy/cô hướng dẫn học sinh.
                3. Các công thức toán bắt buộc viết dạng LaTeX đặt trong $...$ hoặc $$...$$.
                4. Nhắc lại mẹo nhớ hoặc lưu ý quan trọng để học sinh không lặp lại lỗi sai.
                """

                with st.chat_message("assistant"):
                    with st.spinner("Thầy/Cô AI đang xem xét câu hỏi của em..."):
                        tutor_reply = ""
                        for ten_model in ['gemini-3.1-flash-lite', 'gemini-3.8-flash']:
                            try:
                                resp = client.models.generate_content(
                                    model=ten_model,
                                    contents=context_prompt
                                )
                                tutor_reply = resp.text
                                break
                            except Exception:
                                continue

                        if not tutor_reply:
                            tutor_reply = "Hiện hệ thống đang nghẽn mạng nhẹ. Em hãy kiểm tra lại kết nối và thử gửi lại câu hỏi nhé!"

                        st.markdown(tutor_reply)
                        st.session_state["chat_history"].append({"role": "assistant", "content": tutor_reply})
# ================= TAB 4: KIỂM TRA ĐÁNH GIÁ (TRẮC NGHIỆM + TRẢ LỜI NGẮN) =================
with tab_kiemtra:
    st.subheader("Kiểm tra đánh giá năng lực theo cấu trúc đề thi mới (GDPT 2018)")
    st.write("Đề thi kết hợp dạng **Trắc nghiệm nhiều lựa chọn** và **Câu hỏi trả lời ngắn**, sinh ngẫu nhiên từ ngân hàng 82 câu thực tế:")

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        loai_de = st.selectbox(
            "Chọn cấu trúc đề kiểm tra:",
            [
                "Đề tiêu chuẩn 10 câu (8 Trắc nghiệm A-B-C-D + 2 Trả lời ngắn)",
                "Đề tổng hợp 20 câu (16 Trắc nghiệm A-B-C-D + 4 Trả lời ngắn)"
            ]
        )
    with col_m2:
        st.info("""
        📋 **Cấu trúc tích hợp:**
        - **Phần 1 (Trắc nghiệm 4 lựa chọn):** Đo lường kiến thức Nhận biết & Thông hiểu.
        - **Phần 2 (Trả lời ngắn):** Tự điền đáp số (số thực/nguyên), đo lường năng lực Vận dụng & Vận dụng cao (bài toán thực tế, tìm số nghiệm, giá trị lớn nhất/nhỏ nhất).
        """)

    # Đọc dữ liệu kho 82 câu
    danh_sach_tat_ca_cau = []
    if os.path.exists("kho_de.txt"):
        try:
            with open("kho_de.txt", "r", encoding="utf-8") as f:
                raw_text = f.read()
                danh_sach_tat_ca_cau = [c.strip() for c in raw_text.split("Câu ") if c.strip()]
        except Exception:
            pass

    # Nút bấm tạo đề kiểm tra
    if st.button("🚀 Khởi tạo đề kiểm tra mới (Có câu hỏi trả lời ngắn)"):
        if not client:
            st.error("Chưa cấu hình API Key trong mục Secrets.")
        elif not danh_sach_tat_ca_cau:
            st.warning("Chưa tìm thấy nội dung trong file kho_de.txt.")
        else:
            tong_cau = 6 if "6 câu" in loai_de else 10
            so_mcq = 4 if tong_cau == 6 else 7
            so_sa = tong_cau - so_mcq

            import random
            so_mau = min(tong_cau, len(danh_sach_tat_ca_cau))
            cac_cau_mau = random.sample(danh_sach_tat_ca_cau, so_mau)
            mau_context = "\n---\n".join([f"Mẫu {i+1}: Câu " + c for i, c in enumerate(cac_cau_mau)])

            with st.spinner(f"AI đang biên soạn đề gồm {so_mcq} câu trắc nghiệm và {so_sa} câu trả lời ngắn..."):
                prompt_matrix = f"""
                Bạn là Trưởng ban Khảo thí môn Toán THPT Việt Nam (Chương trình GDPT 2018).
                Dưới đây là {so_mau} câu trích mẫu từ ngân hàng đề kiểm tra thực tế (có cả câu trắc nghiệm và câu tính toán trả lời ngắn):
                ---
                {mau_context}
                ---

                Nhiệm vụ:
                Hãy tạo 1 ĐỀ KIỂM TRA CHƯƠNG 1 TOÁN 11 gồm đúng {tong_cau} câu:
                - {so_mcq} câu TRẮC NGHIỆM 4 PHƯƠNG ÁN (type: "mcq"): mức độ Nhận biết, Thông hiểu.
                - {so_sa} câu TRẢ LỜI NGẮN (type: "short_answer"): mức độ Vận dụng, Vận dụng cao (yêu cầu học sinh tính ra con số cụ thể, ví dụ: số nghiệm, chiều rộng mét, thời điểm t...). Đáp án đúng bắt buộc là MỘT CON SỐ CỤ THỂ (ví dụ: "28.3", "4", "-1", "12").
                - Toàn bộ công thức toán học bắt buộc viết bằng LaTeX chuẩn trong cặp $...$ hoặc $$...$$.

                Trả về đúng định dạng JSON thuần là một mảng gồm {tong_cau} đối tượng:
                [
                  {{
                    "id": 1,
                    "type": "mcq",
                    "level": "Nhận biết",
                    "question": "Nội dung câu trắc nghiệm...",
                    "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
                    "correct_answer": "A",
                    "explanation": "Giải thích chi tiết..."
                  }},
                  {{
                    "id": {so_mcq + 1},
                    "type": "short_answer",
                    "level": "Vận dụng",
                    "question": "Nội dung bài toán tính toán ra con số...",
                    "options": null,
                    "correct_answer": "28.3",
                    "explanation": "Giải thích chi tiết các bước tính ra kết quả..."
                  }}
                ]
                """

                exam_success = False
                cac_model = ['gemini-3.1-flash-lite', 'gemini-3.8-flash']
                for ten_model in cac_model:
                    try:
                        resp = client.models.generate_content(
                            model=ten_model,
                            contents=prompt_matrix,
                            config=types.GenerateContentConfig(
                                response_mime_type="application/json",
                                temperature=0.7
                            )
                        )
                        st.session_state["exam_data"] = json.loads(resp.text)
                        st.session_state["exam_submitted"] = False
                        st.session_state["student_answers"] = {}
                        exam_success = True
                        break
                    except Exception:
                        continue

                if not exam_success:
                    st.warning("Máy chủ AI tạm thời đang bận xử lý lưu lượng cao. Em hãy thử bấm lại nút nhé!")

    # ================= GIAO DIỆN LÀM BÀI THI =================
    if "exam_data" in st.session_state and st.session_state["exam_data"]:
        exam_list = st.session_state["exam_data"]
        st.markdown("---")
        st.markdown(f"### 📋 BÀI KIỂM TRA ĐÁNH GIÁ NĂNG LỰC ({len(exam_list)} câu)")

        with st.form("hybrid_exam_form"):
            user_exam_answers = {}
            for idx, item in enumerate(exam_list):
                q_type = item.get("type", "mcq")
                level_tag = item.get("level", "Thông hiểu")
                
                # Hiển thị câu trắc nghiệm A-B-C-D
                if q_type == "mcq":
                    st.markdown(f"**Câu {idx + 1}** `[Trắc nghiệm - {level_tag}]`: {item['question']}")
                    opts = item["options"]
                    user_exam_answers[idx] = st.radio(
                        f"Chọn đáp án câu {idx + 1}:",
                        options=["A", "B", "C", "D"],
                        format_func=lambda x, opt_dict=opts: f"{x}. {opt_dict[x]}",
                        key=f"hybrid_mcq_{idx}",
                        index=None
                    )
                # Hiển thị câu hỏi trả lời ngắn (Điền số)
                else:
                    st.markdown(f"**Câu {idx + 1}** `[Trả lời ngắn - {level_tag}]`: {item['question']}")
                    user_exam_answers[idx] = st.text_input(
                        f"Nhập kết quả câu {idx + 1} (dạng số, ví dụ 28.3 hoặc 4):",
                        key=f"hybrid_sa_{idx}",
                        placeholder="Điền đáp số tại đây..."
                    )
                st.write("")

            btn_submit_exam = st.form_submit_button("🏁 Nộp Bài Kiểm Tra")
            if btn_submit_exam:
                st.session_state["exam_submitted"] = True
                st.session_state["student_answers"] = user_exam_answers

        # ================= CHẤM ĐIỂM TỰ ĐỘNG & BÁO CÁO NĂNG LỰC =================
        if st.session_state.get("exam_submitted", False):
            ans = st.session_state.get("student_answers", {})
            dung = 0
            tong_so = len(exam_list)

            # Hàm chuẩn hóa số để so sánh (chấp nhận cả dấu phẩy và dấu chấm)
            def is_same_number(s1, s2):
                if not s1 or not s2:
                    return False
                clean1 = str(s1).strip().replace(",", ".")
                clean2 = str(s2).strip().replace(",", ".")
                try:
                    return abs(float(clean1) - float(clean2)) < 0.05
                except ValueError:
                    return clean1.lower() == clean2.lower()

            for idx, item in enumerate(exam_list):
                q_type = item.get("type", "mcq")
                user_val = ans.get(idx)
                if q_type == "mcq":
                    if user_val == item["correct_answer"]:
                        dung += 1
                else:
                    if is_same_number(user_val, item["correct_answer"]):
                        dung += 1

            diem = round((dung / tong_so) * 10, 2)
            st.markdown("---")
            st.markdown("## 🎯 BÁO CÁO KẾT QUẢ ĐÁNH GIÁ NĂNG LỰC")

            c_res1, c_res2, c_res3 = st.columns(3)
            with c_res1:
                st.metric("Điểm tổng kết", f"{diem} / 10")
            with c_res2:
                st.metric("Số câu trả lời đúng", f"{dung} / {tong_so}")
            with c_res3:
                ti_le = round((dung / tong_so) * 100, 1)
                st.metric("Tỉ lệ hoàn thành", f"{ti_le}%")

            if diem >= 8.0:
                st.success("🌟 **Tuyệt vời!** Em hoàn thành xuất sắc cả phần trắc nghiệm lẫn bài toán tính toán trả lời ngắn.")
            elif diem >= 6.5:
                st.info("👍 **Khá tốt!** Hãy rèn luyện thêm kỹ năng tính toán chính xác ở các câu hỏi trả lời ngắn.")
            else:
                st.warning("⚠️ **Cần cố gắng:** Em hãy xem kỹ lại hướng dẫn giải các bài toán thực tế bên dưới nhé!")

            # Bảng chi tiết đáp án & lời giải
            with st.expander("📖 Xem bảng đối chiếu đáp án & Hướng dẫn giải chi tiết", expanded=True):
                for idx, item in enumerate(exam_list):
                    q_type = item.get("type", "mcq")
                    user_val = ans.get(idx)
                    correct_val = item["correct_answer"]
                    
                    if q_type == "mcq":
                        is_corr = (user_val == correct_val)
                    else:
                        is_corr = is_same_number(user_val, correct_val)

                    icon = "✅" if is_corr else "❌"
                    display_type = "Trắc nghiệm" if q_type == "mcq" else "Trả lời ngắn"
                    
                    st.markdown(f"**Câu {idx + 1}** `[{display_type}]`: {icon} Em trả lời: **{user_val if user_val else 'Chưa điền/chọn'}** | Đáp án đúng: **{correct_val}**")
                    st.caption(f"**Hướng dẫn giải:** {item['explanation']}")
                    st.divider()
