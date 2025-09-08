import streamlit as st
import os
from blockchain import Blockchain, Block
from storage_utils import save_file

st.set_page_config("Blockchain File Sharing - User", layout="wide")

# Load blockchain
bc = Blockchain(difficulty=2)

st.title("📂 Blockchain Cloud File Sharing (User)")

# Upload file
uploaded_file = st.file_uploader("Upload a file")
if uploaded_file:
    file_bytes = uploaded_file.read()
    meta = save_file(file_bytes, uploaded_file.name)
    block = Block(len(bc.chain), bc.get_latest_block().hash, bc.get_latest_block().timestamp, meta)
    bc.add_block(block)
    st.success(f"File '{uploaded_file.name}' uploaded and added to blockchain ✅")

# Search file
st.subheader("🔍 Search Files")
search_term = st.text_input("Enter filename keyword")
if search_term:
    results = bc.find_by_filename(search_term)
    if results:
        for b in results:
            d = b.data
            st.write(f"📄 {d['filename']} | Hash: `{d['hash']}` | Block #{b.index}")
            storage_path = d.get("storage_path")
            if storage_path and os.path.exists(storage_path):
                 with open(storage_path, "rb") as f:
                  st.download_button(
                    f"Download {d['filename']}",
                    f,
                    file_name=d["filename"],
                  key=f"download_{b.index}"  # unique key per block
        )

    else:
        st.warning("No files found.")

# Verify blockchain
st.subheader("🔐 Verify Blockchain")
if st.button("Check validity"):
    if bc.is_chain_valid():
        st.success("Blockchain is valid ✅")
    else:
        st.error("Blockchain is corrupted ❌")
