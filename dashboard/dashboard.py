import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# CONFIG HALAMAN
st.set_page_config(
    page_title="E-Commerce Dashboard",
    layout="wide"
)

st.title("📊 E-Commerce Dashboard (2017–2018)")
st.markdown("Analisis transaksi, tren pesanan, dan segmentasi pelanggan")

# LOAD DATA
@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(__file__)  # folder dashboard/
    file_path = os.path.join(BASE_DIR, "final_df.csv")  # path ke file CSV
    df = pd.read_csv(file_path)
    
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    df["order_year"] = df["order_purchase_timestamp"].dt.year
    df["order_month"] = df["order_purchase_timestamp"].dt.month
    return df

df = load_data()

# SIDEBAR FILTER
st.sidebar.header("🔍 Filter Data")

year_filter = st.sidebar.multiselect(
    "Pilih Tahun",
    options=sorted(df["order_year"].unique()),
    default=sorted(df["order_year"].unique())
)

filtered_df = df[df["order_year"].isin(year_filter)]

# KPI
with st.container():
    st.subheader("📌 Ringkasan Utama")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Pesanan", filtered_df["order_id"].nunique())
    col2.metric("Total Pelanggan", filtered_df["customer_unique_id"].nunique())
    col3.metric("Total Pendapatan", f"${filtered_df['price'].sum():,.0f}")

# TOP PRODUCT CATEGORY
with st.container():
    st.subheader("🛒 Top 10 Kategori Produk")
    
    category_orders = (
        filtered_df
        .groupby("product_category_name_english")["order_id"]
        .nunique()
        .sort_values(ascending=False)
        .head(10)
    )
    
    fig1, ax1 = plt.subplots(figsize=(8,5))
    category_orders.sort_values().plot(kind="barh", ax=ax1, color="#4B8BBE")
    ax1.set_xlabel("Jumlah Pesanan")
    ax1.set_ylabel("Kategori Produk")
    ax1.grid(axis='x', linestyle='--', alpha=0.7)
    st.pyplot(fig1)

# MONTHLY ORDER TREND
with st.container():
    st.subheader("📈 Tren Jumlah Pesanan Bulanan")
    
    monthly_orders = (
        filtered_df
        .groupby(["order_year", "order_month"])["order_id"]
        .nunique()
        .reset_index()
    )
    
    monthly_orders["year_month"] = monthly_orders["order_year"].astype(str) + "-" + monthly_orders["order_month"].astype(str)
    
    fig2, ax2 = plt.subplots(figsize=(10,4))
    ax2.plot(monthly_orders["year_month"], monthly_orders["order_id"], marker="o", color="#FF7F0E")
    ax2.set_xlabel("Periode")
    ax2.set_ylabel("Jumlah Pesanan")
    ax2.set_xticks(range(len(monthly_orders["year_month"])))
    ax2.set_xticklabels(monthly_orders["year_month"], rotation=45)
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig2)

# RFM ANALYSIS
with st.container():
    st.subheader("👥 Segmentasi Pelanggan (RFM)")

    snapshot_date = filtered_df["order_purchase_timestamp"].max() + pd.Timedelta(days=1)

    rfm = filtered_df.groupby("customer_unique_id").agg({
        "order_purchase_timestamp": lambda x: (snapshot_date - x.max()).days,
        "order_id": "nunique",
        "price": "sum"
    }).reset_index()

    rfm.columns = ["customer_unique_id", "Recency", "Frequency", "Monetary"]

    # RFM Scoring
    rfm["R_Score"] = pd.qcut(rfm["Recency"], 4, labels=[4,3,2,1])
    rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 4, labels=[1,2,3,4])
    rfm["M_Score"] = pd.qcut(rfm["Monetary"], 4, labels=[1,2,3,4])

    rfm["RFM_Segment"] = rfm["R_Score"].astype(str) + rfm["F_Score"].astype(str) + rfm["M_Score"].astype(str)

    rfm_segment = rfm["RFM_Segment"].value_counts().head(10)

    fig3, ax3 = plt.subplots(figsize=(8,5))
    rfm_segment.plot(kind="bar", ax=ax3, color="#2CA02C")
    ax3.set_xlabel("RFM Segment")
    ax3.set_ylabel("Jumlah Pelanggan")
    ax3.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig3)

# FOOTER
st.markdown("---")
st.caption("Dashboard oleh Shelo Rahma Sari | E-Commerce Public Dataset")
