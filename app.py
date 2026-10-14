
import streamlit as st

# ==========================================
# CẤU HÌNH GIAO DIỆN
# ==========================================
st.set_page_config(
    page_title="Ứng dụng tính chỉ số DTI",
    page_icon="🏦",
    layout="centered"
)

st.title("🏦 ỨNG DỤNG TÍNH CHỈ SỐ DTI")
st.write(
    "Nhập thông tin khoản vay và thu nhập của khách hàng "
    "để tính chỉ số DTI."
)

st.divider()

# ==========================================
# NHẬP THÔNG TIN KHÁCH HÀNG
# ==========================================
st.subheader("📋 Thông tin khoản vay")

col1, col2 = st.columns(2)

with col1:
    STV = st.number_input(
        "Số tiền vay (VNĐ)",
        min_value=0,
        value=800_000_000,
        step=10_000_000
    )

    THV = st.number_input(
        "Thời hạn vay (năm)",
        min_value=1,
        value=5,
        step=1
    )

    LS = st.number_input(
        "Lãi suất vay (%/năm)",
        min_value=0.0,
        value=12.0,
        step=0.5,
        format="%.2f"
    )

    TN = st.number_input(
        "Thu nhập hàng tháng (VNĐ)",
        min_value=0,
        value=45_000_000,
        step=1_000_000
    )

with col2:
    NC = st.number_input(
        "Nợ cũ phải trả hàng tháng (VNĐ)",
        min_value=0,
        value=10_000_000,
        step=1_000_000
    )

    CPSH = st.number_input(
        "Chi phí sinh hoạt mỗi người/tháng (VNĐ)",
        min_value=0,
        value=4_000_000,
        step=500_000
    )

    SN = st.number_input(
        "Số người trong gia đình",
        min_value=1,
        value=3,
        step=1
    )

st.divider()

# ==========================================
# TÍNH TOÁN DTI
# ==========================================
if st.button("🧮 TÍNH CHỈ SỐ DTI", type="primary",
             use_container_width=True):

    # Kiểm tra dữ liệu đầu vào
    if TN <= CPSH * SN:
        st.error(
            "Thu nhập phải lớn hơn tổng chi phí sinh hoạt "
            "của cả gia đình."
        )

    elif THV <= 0:
        st.error("Thời hạn vay phải lớn hơn 0.")

    else:
        # Lãi suất nhập theo %/năm, chuyển sang số thập phân
        lai_suat_thang = (LS / 100) / 12

        # Tiền gốc phải trả trung bình mỗi tháng
        tien_goc_thang = STV / (THV * 12)

        # Tiền lãi tháng theo công thức ban đầu
        tien_lai_thang = STV * lai_suat_thang

        # Tổng nghĩa vụ trả nợ hàng tháng
        tong_tra_no = (
            tien_goc_thang
            + tien_lai_thang
            + NC
        )

        # Thu nhập còn lại sau chi phí sinh hoạt
        thu_nhap_con_lai = TN - CPSH * SN

        # Chỉ số DTI
        DTI = tong_tra_no / thu_nhap_con_lai

        # ======================================
        # HIỂN THỊ KẾT QUẢ
        # ======================================
        st.subheader("📊 Kết quả tính toán")

        col3, col4 = st.columns(2)

        with col3:
            st.metric(
                label="Chỉ số DTI",
                value=f"{DTI * 100:.2f}%"
            )

        with col4:
            st.metric(
                label="Ngưỡng DTI",
                value="70%"
            )

        st.progress(min(max(DTI, 0.0), 1.0))

        st.write(
            f"**Tiền gốc trả hàng tháng:** "
            f"{tien_goc_thang:,.0f} VNĐ"
        )

        st.write(
            f"**Tiền lãi hàng tháng:** "
            f"{tien_lai_thang:,.0f} VNĐ"
        )

        st.write(
            f"**Tổng nghĩa vụ trả nợ hàng tháng:** "
            f"{tong_tra_no:,.0f} VNĐ"
        )

        st.write(
            f"**Thu nhập sau chi phí sinh hoạt:** "
            f"{thu_nhap_con_lai:,.0f} VNĐ"
        )

        st.divider()

        # ======================================
        # KẾT LUẬN THEO YÊU CẦU
        # DTI < 70%: KHÔNG ĐƯỢC VAY
        # DTI >= 70%: ĐƯỢC VAY
        # ======================================
        if DTI < 0.7:
            st.error(
                "❌ KẾT LUẬN: KHÔNG ĐƯỢC VAY"
            )
            st.write(
                "Lý do: Chỉ số DTI nhỏ hơn 70% "
                "theo quy tắc bạn yêu cầu."
            )
        else:
            st.success(
                "✅ KẾT LUẬN: ĐƯỢC VAY"
            )
            st.write(
                "Lý do: Chỉ số DTI lớn hơn hoặc bằng 70% "
                "theo quy tắc bạn yêu cầu."
            )

st.caption(
    "Lưu ý: Kết quả là đánh giá theo công thức và "
    "quy tắc được cài đặt, không thay thế quyết định "
    "phê duyệt tín dụng thực tế của ngân hàng."
)
