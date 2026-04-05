import streamlit as st
import pandas as pd
import io

# 🔐 パスワード認証
password = st.text_input("パスワードを入力してください", type="password")
if password != "1234":
    st.stop()

st.set_page_config(page_title="商品データ変換ツール(PUMA)", layout="centered")

st.title("📦 商品データ 自動変換(PUMA用)")
st.write("発注書（Excel）をアップロードすると、スマレジ登録用CSVに自動変換します。")

uploaded_file = st.file_uploader("発注書（Excel）をアップロード", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    out = pd.DataFrame()

    out["商品ID"] = None
    out["部門ID"] = None
    out["商品コード"] = df["EAN"]
    out["商品名"] = df["商品名"]
    out["品番"] = df["スタイル"]

    # カラー整形：01PUMA BLACK → 01 _ PUMA BLACK
    out["カラー"] = (
        df["カラー名称"].str[:2]
        + " _ "
        + df["カラー名称"].str[2:].str.strip()
    )

    out["サイズ"] = df["サイズ"]
    out["商品単価"] = df["上代"]
    out["原価"] = (df["上代"] * 0.52).round()

    out["税区分"] = 1
    out["免税区分"] = 1
    out["グループコード"] = "p26fa"
    out["属性1: メーカー"] = 3
    out["属性2: 季節"] = None
    out["属性3: シルエット"] = None
    out["部門名"] = None
    out["在庫"] = None

    out = out[
        [
            "商品ID",
            "部門ID",
            "商品コード",
            "商品名",
            "品番",
            "カラー",
            "サイズ",
            "商品単価",
            "原価",
            "税区分",
            "免税区分",
            "グループコード",
            "属性1: メーカー",
            "属性2: 季節",
            "属性3: シルエット",
            "部門名",
            "在庫",
        ]
    ]

    # CSV をメモリに書き込む
    csv_buffer = io.BytesIO()
    out.to_csv(csv_buffer, index=False, encoding="cp932")
    csv_buffer.seek(0)

    st.success("変換が完了しました！")
    st.download_button(
        label="📥 スマレジ用CSVをダウンロード",
        data=csv_buffer,
        file_name="smaregi_output.csv",
        mime="text/csv"
    )
