import streamlit as st
from blockchain import Blockchain

st.set_page_config("Blockchain File Sharing - Admin", layout="wide")

st.title("🛠 Admin Dashboard")

# --- Authentication ---
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"  # change this!

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.subheader("🔑 Login Required")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.authenticated = True
            st.success("✅ Login successful")
        else:
            st.error("❌ Invalid credentials")
    st.stop()  # stop rendering the rest until logged in

# --- Load Blockchain ---
bc = Blockchain(difficulty=2)

st.subheader("📑 Uploaded Files")
for block in bc.chain:
    d = block.data
    if d.get("filename") != "Genesis Block":
        st.write(
            f"📄 **{d['filename']}** | Hash: `{d['hash']}` | Stored at: `{d['storage_path']}` | Block #{block.index}"
        )

st.subheader("🔐 Blockchain Status")
if bc.is_chain_valid():
    st.success("Blockchain is valid ✅")
else:
    st.error("Blockchain is corrupted ❌")
