import streamlit as st
import pandas as pd
import os

file_name = "shop_data.xlsx"

# Ensure correct structure
expected_columns = ["Shop Name", "Total Amount", "Paid Amount", "Remaining Amount"]

if os.path.exists(file_name):
    try:
        df = pd.read_excel(file_name)
        if not all(col in df.columns for col in expected_columns):
            df = pd.DataFrame(columns=expected_columns)
    except:
        df = pd.DataFrame(columns=expected_columns)
else:
    df = pd.DataFrame(columns=expected_columns)

st.title("🧾 Shop Payment Tracker v2")

shop_name = st.text_input("🛍️ Shop Name")
total_amount = st.number_input("💰 Total Amount (₹)", min_value=0)
paid_amount = st.number_input("✅ Paid Amount (₹)", min_value=0)

if st.button("Add / Update"):
    if shop_name:
        if shop_name in df["Shop Name"].values:
            idx = df[df["Shop Name"] == shop_name].index[0]
            df.at[idx, "Paid Amount"] += paid_amount
            df.at[idx, "Remaining Amount"] = df.at[idx, "Total Amount"] - df.at[idx, "Paid Amount"]
        else:
            remaining = total_amount - paid_amount
            new_data = {
                "Shop Name": shop_name,
                "Total Amount": total_amount,
                "Paid Amount": paid_amount,
                "Remaining Amount": remaining
            }
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_excel(file_name, index=False)
        st.success("Data saved successfully!")
    else:
        st.error("Please enter a shop name.")

st.subheader("📊 All Payments")
st.dataframe(df)
