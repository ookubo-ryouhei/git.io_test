import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# アプリのタイトル
st.title("散布図・相関関係可視化ツール")
st.write("CSVファイルをアップロードして、2つのデータの関係を調べましょう。")

# ファイルアップローダー
uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type="csv")

if uploaded_file is not None:
    # データの読み込み
    df = pd.read_csv(uploaded_file)
    
    # データのプレビュー
    st.subheader("データプレビュー")
    st.write(df.head())

    # 数値列の抽出
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    if len(numeric_cols) >= 2:
        st.subheader("散布図の作成")
        
        # 軸の選択
        col1, col2 = st.columns(2)
        with col1:
            x_axis = st.selectbox("X軸（横軸）を選択", numeric_cols)
        with col2:
            y_axis = st.selectbox("Y軸（縦軸）を選択", numeric_cols)

        # グラフ描画
        fig, ax = plt.subplots()
        sns.scatterplot(data=df, x=x_axis, y=y_axis, ax=ax)
        st.pyplot(fig)

        # 相関係数の算出
        correlation = df[x_axis].corr(df[y_axis])
        st.metric(label=f"{x_axis} と {y_axis} の相関係数 ($r$)", value=round(correlation, 3))

        # 相関の強さの判定
        if abs(correlation) >= 0.7:
            st.success("強い相関があります。")
        elif abs(correlation) >= 0.4:
            st.info("中程度の相関があります。")
        else:
            st.warning("相関は弱いです。")
            
    else:
        st.error("分析には少なくとも2つの数値列が必要です。")

else:
    st.info("左側のサイドバー、または中央からCSVファイルをアップロードしてください。")
