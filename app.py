import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# PAGE CONFIG
st.set_page_config(
    page_title="Sales Forecast Dashboard",
    layout="wide"
)

st.title("📈 Sales Forecast Dashboard")


# LOAD DATA
forecast = pd.read_csv("final_forecasting.csv")

forecast['Date'] = pd.to_datetime(forecast['Date'])

forecast['Period'] = forecast['Date'].dt.strftime('%Y-%m')


# FILTER
st.sidebar.header("Forecast Filter")

period_list = forecast['Period'].tolist()

start_period = st.sidebar.selectbox(
    "Periode Awal",
    period_list,
    index=0
)

end_period = st.sidebar.selectbox(
    "Periode Akhir",
    period_list,
    index=min(2, len(period_list)-1)
)

submit = st.sidebar.button("🔍 Submit")


# DISPLAY
if submit:

    start_date = pd.to_datetime(start_period)
    end_date = pd.to_datetime(end_period)

    if start_date > end_date:
        st.error("Periode Awal tidak boleh lebih besar dari Periode Akhir")

    else:

        selected_data = forecast[
            (forecast['Date'] >= start_date) &
            (forecast['Date'] <= end_date)
        ]

        # HEADER
        st.success(
            f"Forecast Periode: {start_period} sampai {end_period}"
        )

        # KPI
        total_qty = selected_data['Forecast_Qty'].sum()
        total_revenue = selected_data['Forecast_Revenue'].sum()
        col1, col2 = st.columns(2)
        col1.metric(
            "Total Forecast Qty",
            f"{total_qty:,.0f}"
        )

        col2.metric(
            "Total Forecast Revenue",
            f"Rp {total_revenue:,.0f}"
        )

        # TABLE
        st.subheader("Forecast Detail")

        st.dataframe(
            selected_data[
                [
                    'Date',
                    'Forecast_Qty',
                    'Forecast_Revenue'
                ]
            ],
            use_container_width=True
        )

        # CHART QTY
        st.subheader("Forecast Qty Trend")

        fig1, ax1 = plt.subplots(figsize=(10,4))

        ax1.plot(
            selected_data['Date'],
            selected_data['Forecast_Qty'],
            marker='o',
            linewidth=2
        )

        ax1.set_xlabel("Date")
        ax1.set_ylabel("Qty")
        ax1.grid(True)

        st.pyplot(fig1)

        # CHART REVENUE
        st.subheader("Forecast Revenue Trend")

        fig2, ax2 = plt.subplots(figsize=(10,4))
        ax2.plot(
            selected_data['Date'],
            selected_data['Forecast_Revenue'],
            marker='o',
            linewidth=2
        )

        ax2.set_xlabel("Date")
        ax2.set_ylabel("Revenue")
        ax2.grid(True)

        st.pyplot(fig2)

        # BUSINESS RECOMMENDATION
        st.subheader("Business Recommendation")

        highest_rev = selected_data.loc[
            selected_data['Forecast_Revenue'].idxmax()
        ]

        st.info(
            f"""
            Forecast periode *{start_period} sampai {end_period}*

            • Revenue tertinggi diperkirakan terjadi pada
              *{highest_rev['Date'].strftime('%B %Y')}*

            • Siapkan stok dan distribusi menjelang periode tersebut.

            • Gunakan forecast ini sebagai dasar target penjualan dan inventory planning.
            """
        )

else:

    st.info(
        "Pilih rentang periode kemudian klik Submit."
    )