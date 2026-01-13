# E-Commerce Dashboard 📊✨

Dashboard analisis data transaksi E-Commerce (2017–2018), termasuk KPI, tren pesanan bulanan, top kategori produk, dan segmentasi pelanggan (RFM).

---

## Setup Environment - Anaconda

```bash
# Buat environment baru
conda create --name main-ds python=3.9

# Aktifkan environment
conda activate main-ds

# Install dependencies
pip install -r requirements.txt

---

## Setup Environment - Shell/Terminal

```bash
# Buat folder proyek
mkdir proyek_analisis_data
cd proyek_analisis_data

# Install pipenv dan buat virtual environment
pipenv install
pipenv shell

# Install dependencies
pip install -r requirements.txt

---

## Run steamlit app

```bash
# Jalankan dashboard
streamlit run dashboard.py
