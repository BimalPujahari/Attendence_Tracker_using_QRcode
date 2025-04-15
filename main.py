import streamlit as st
from database import init_db, mark_attendance, get_attendance, get_attendance_by_session
from generate_qr import generate_qr
import pandas as pd

# ----------------------
# 🔐 Admin Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "pass123"  # change this
# ----------------------

# 🔁 Track login state
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

st.set_page_config(page_title="QR Attendance Tracker", layout="centered")
init_db()

st.title("📸 QR Code Attendance System (Local LAN)")

# --------------------------
# 🔐 Admin Login Section (Top)
# --------------------------
if not st.session_state.admin_logged_in:
    with st.expander("🔐 Admin Login", expanded=True):
        st.subheader("Admin Login Required")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.success("Logged in as Admin ✅")
            else:
                st.error("Invalid credentials!")
else:
    st.info("✅ Logged in as Admin")

# ---------------------------------
# 🧭 Tabs: Controlled by Admin Login
# ---------------------------------
if st.session_state.admin_logged_in:
    tab1, tab2, tab3, tab4 = st.tabs([
        "Generate QR",
        "Mark Attendance",
        "Admin Panel",
        "Export CSV"
    ])
else:
    tab2, tab3, tab4 = st.tabs([
        "Mark Attendance",
        "Admin Panel",
        "Export CSV"
    ])
    tab1 = None

# --------------------------
# 🔐 Tab 1 – QR Generation
# --------------------------
if tab1:
    with tab1:
        st.header("Generate QR Code")
        session_code = st.text_input("Enter Session Code (e.g., CS101-Apr14)")
        local_ip = st.text_input("Enter your Local IP", value="192.168.1.5")
        port = st.number_input("Enter Port (default 8501)", value=8501, step=1)

        if st.button("Generate QR"):
            if session_code:
                path, url = generate_qr(session_code, local_ip, port)
                st.success(f"QR Code generated for: {url}")
                st.image(path)
            else:
                st.error("Please enter a valid session code.")

# --------------------------
# ✅ Tab 2 – Mark Attendance
# --------------------------
with tab2:
    st.header("Mark Attendance")

    query_params = st.experimental_get_query_params()
    session_code = query_params.get("session", [None])[0]

    if session_code:
        st.success(f"Session Detected: {session_code}")
        student_id = st.text_input("Enter your Student ID")
        if st.button("Mark Attendance"):
            if student_id:
                mark_attendance(student_id, session_code)
                st.success(f"Attendance marked for {student_id}")
            else:
                st.warning("Enter your Student ID")
    else:
        st.warning("No session code found in the URL. Please scan a valid QR code.")

# --------------------------
# 🔐 Tab 3 – Admin Panel
# --------------------------
with tab3:
    st.header("Admin Panel")

    if st.session_state.admin_logged_in:
        st.subheader("📋 All Attendance Records")
        data = get_attendance()
        df = pd.DataFrame(data, columns=["ID", "Student ID", "Timestamp", "Session Code"])
        st.dataframe(df)

        st.subheader("🔎 Filter by Session")
        session_input = st.text_input("Enter Session Code to Filter")
        if st.button("View Session"):
            session_data = get_attendance_by_session(session_input)
            session_df = pd.DataFrame(session_data, columns=["ID", "Student ID", "Timestamp", "Session Code"])
            st.dataframe(session_df)
    else:
        st.warning("Admin login required to view this tab.")

# --------------------------
# 📁 Tab 4 – Export CSV
# --------------------------
with tab4:
    st.header("Export Attendance to CSV")

    if st.session_state.admin_logged_in:
        all_data = get_attendance()
        df_all = pd.DataFrame(all_data, columns=["ID", "Student ID", "Timestamp", "Session Code"])

        export_option = st.radio("What do you want to export?", ["All Records", "Filter by Session"])

        if export_option == "All Records":
            csv = df_all.to_csv(index=False).encode('utf-8')
            st.download_button("Download All Attendance", csv, "attendance_all.csv", "text/csv")
        else:
            session = st.text_input("Enter session code to export")
            if st.button("Export Session Data"):
                session_data = get_attendance_by_session(session)
                df_session = pd.DataFrame(session_data, columns=["ID", "Student ID", "Timestamp", "Session Code"])
                csv = df_session.to_csv(index=False).encode('utf-8')
                st.download_button(f"Download {session} Attendance", csv, f"attendance_{session}.csv", "text/csv")
    else:
        st.warning("Admin login required to export data.")
