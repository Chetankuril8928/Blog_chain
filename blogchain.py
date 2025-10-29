import streamlit as st
import hashlib
import datetime

# ---------- PAGE SETUP ----------
st.set_page_config(page_title="Blockchain Ledger - Chetan", layout="wide")

# ---------- CUSTOM CSS ----------
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #0F2027, #203A43, #2C5364);
        color: #E0E0E0;
        font-family: 'Poppins', sans-serif;
    }
    .main {
        background-color: transparent !important;
    }
    h1 {
        color: #00B4DB;
        text-align: center;
        font-weight: 800;
        letter-spacing: 1px;
    }
    .block-card {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px 25px;
        margin-bottom: 20px;
        box-shadow: 0px 8px 25px rgba(0,0,0,0.4);
        border: 1px solid rgba(255,255,255,0.15);
        transition: all 0.3s ease-in-out;
    }
    .block-card:hover {
        transform: scale(1.01);
        background: rgba(255, 255, 255, 0.1);
    }
    .block-header {
        font-size: 22px;
        font-weight: bold;
        color: #00B4DB;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00B4DB, #0083B0);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        font-size: 15px;
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover {
        transform: scale(1.06);
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .css-1d391kg p {
        color: #E0E0E0;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #00B4DB, #0083B0);
        color: white;
    }
    .sidebar .sidebar-content h2 {
        color: white !important;
    }
    code {
        background: rgba(0,180,219,0.15);
        color: #00E5FF;
        padding: 2px 6px;
        border-radius: 6px;
        font-size: 13px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("<h1>💠 Blockchain Ledger - Chetan</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#A9CCE3;'>A sleek blockchain ledger with futuristic UI</p>", unsafe_allow_html=True)
st.write("---")

# ---------- INITIALIZE SESSION ----------
if "previous_hash" not in st.session_state:
    st.session_state.previous_hash = "0000"
if "block_number" not in st.session_state:
    st.session_state.block_number = 0
if "ledger" not in st.session_state:
    st.session_state.ledger = []

# ---------- SIDEBAR ----------
st.sidebar.title("➕ Add Transaction")
sender = st.sidebar.text_input("👤 Sender Name")
receiver = st.sidebar.text_input("💸 Receiver Name")
amount = st.sidebar.text_input("💰 Amount (₹)")

def generate_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

if st.sidebar.button("Add Block"):
    if not sender or not receiver or not amount:
        st.sidebar.error("⚠ Please fill all fields!")
    else:
        st.session_state.block_number += 1
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = f"Block:{st.session_state.block_number}|{sender}{receiver}{amount}{st.session_state.previous_hash}{timestamp}"
        block_hash = generate_hash(data)

        block = {
            "Block #": st.session_state.block_number,
            "Sender": sender,
            "Receiver": receiver,
            "Amount": amount,
            "Timestamp": timestamp,
            "Prev Hash": st.session_state.previous_hash,
            "Hash": block_hash
        }

        st.session_state.ledger.append(block)
        st.session_state.previous_hash = block_hash
        st.sidebar.success("✅ Block Added Successfully!")

# ---------- DISPLAY LEDGER ----------
st.subheader("📜 Blockchain Ledger")
if len(st.session_state.ledger) == 0:
    st.info("No blocks yet. Add one from the sidebar!")
else:
    for block in reversed(st.session_state.ledger):
        st.markdown(f"""
        <div class="block-card">
            <div class="block-header">🔷 Block #{block['Block #']}</div>
            <p><b>👤 Sender:</b> {block['Sender']}</p>
            <p><b>💸 Receiver:</b> {block['Receiver']}</p>
            <p><b>💰 Amount:</b> ₹{block['Amount']}</p>
            <p><b>🕒 Timestamp:</b> {block['Timestamp']}</p>
            <p><b>🔗 Prev Hash:</b> <code>{block['Prev Hash']}</code></p>
            <p><b>🔒 Hash:</b> <code>{block['Hash']}</code></p>
        </div>
        """, unsafe_allow_html=True)

# ---------- CLEAR BUTTON ----------
if st.sidebar.button("🧹 Clear Blockchain"):
    st.session_state.ledger = []
    st.session_state.previous_hash = "0000"
    st.session_state.block_number = 0
    st.sidebar.warning("🗑 Ledger Cleared!")
