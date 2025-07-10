import streamlit as st
import pandas as pd
import os

# --- Setup ---
st.set_page_config(page_title="🧾 Shop Payment Tracker", layout="centered")

# --- Constants ---
EXCEL_FILE = "shop_data.xlsx"
COLUMNS = ["Shop Name", "Total Amount (₹)", "Paid Amount (₹)", "Remaining Amount (₹)"]

# --- Load or Create Excel File ---
if os.path.exists(EXCEL_FILE):
    try:
        df = pd.read_excel(EXCEL_FILE, engine="openpyxl")
        df = df[COLUMNS]  # Ensure column order
    except Exception as e:
        st.error("⚠️ Error reading Excel file. Creating new.")
        df = pd.DataFrame(columns=COLUMNS)
else:
    df = pd.DataFrame(columns=COLUMNS)

# --- UI ---
st.title("🧾 Shop Payment Tracker")

with st.form("payment_form"):
    shop_name = st.text_input("🛍️ Shop Name").strip()
    total_amount = st.number_input("💰 Total Amount (₹)", min_value=0)
    paid_amount = st.number_input("✅ Paid Amount (₹)", min_value=0)
    submitted = st.form_submit_button("💾 Save Payment")

if submitted:
    if not shop_name:
        st.warning("❗ Shop name is required.")
    elif paid_amount > total_amount:
        st.error("❌ Paid amount cannot be more than total amount.")
    else:
        remaining = total_amount - paid_amount
        new_row = pd.DataFrame([{
            "Shop Name": shop_name,
            "Total Amount (₹)": total_amount,
            "Paid Amount (₹)": paid_amount,
            "Remaining Amount (₹)": remaining
        }])
        df = pd.concat([df, new_row], ignore_index=True)
        try:
            df.to_excel(EXCEL_FILE, index=False, engine="openpyxl")
            st.success(f"✅ Saved for '{shop_name}' – Remaining ₹{remaining}")
        except Exception as e:
            st.error(f"❌ Error saving to Excel: {e}")

# --- Display Data ---
st.divider()
st.subheader("📊 All Payments")
st.dataframe(df, use_container_width=True)

