import os
import streamlit as st
import pandas as pd
import joblib

st.title("Du doan churn")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model_xgb.pkl")

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    st.error(f"Khong tim thay hoac khong doc duoc model_xgb.pkl: {e}")
    st.stop()

file = st.file_uploader("Chon file", type=["csv", "xlsx"])

if file is not None:
    try:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        st.write("Du lieu:")
        st.dataframe(df.head())

        df["Du_Doan"] = model.predict(df)

        st.write("Ket qua:")
        st.dataframe(df.head())

        output_path = os.path.join(BASE_DIR, "ket_qua.xlsx")
        df.to_excel(output_path, index=False)

        with open(output_path, "rb") as f:
            st.download_button(
                "Tai file",
                data=f,
                file_name="ket_qua.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

    except Exception as e:
        st.error(f"Loi: {e}")