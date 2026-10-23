from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Customer Orders & Retention Dashboard", page_icon="📊", layout="wide")

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

@st.cache_data
def load_data():
    orders = pd.read_csv(DATA_DIR / "orders.csv")
    customers = pd.read_csv(DATA_DIR / "customers.csv")
    products = pd.read_csv(DATA_DIR / "products.csv")
    orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")
    orders["order_status"] = orders["order_status"].astype(str).str.strip().str.title()
    orders["sales_channel"] = orders["sales_channel"].astype(str).str.strip().str.title()
    orders["calculated_order_value"] = (
        orders["quantity"] * orders["unit_price"] * (1 - orders["discount_pct"])
    ).round(2)
    data = orders.merge(customers, on="customer_id", how="left").merge(
        products[["product_id", "product_name", "category"]], on="product_id", how="left"
    )
    return data, customers, products

try:
    df, customers, products = load_data()
except Exception as exc:
    st.error("Could not load the project CSV files. Make sure app.py and the data/ folder are in the same project directory.")
    st.exception(exc)
    st.stop()

st.title("📊 Customer Orders & Retention Dashboard")
st.caption("Portfolio project · Python · pandas · Streamlit · Plotly · SQL analysis")
st.warning("Practice project: these are synthetic records and sample currency units, not verified real-business results. Profit cannot be calculated accurately because product costs, shipping, marketing, and operating costs are not included.")

with st.sidebar:
    st.header("Dashboard filters")
    min_date = df["order_date"].min().date()
    max_date = df["order_date"].max().date()
    date_range = st.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    channels = sorted(df["sales_channel"].dropna().unique().tolist())
    selected_channels = st.multiselect("Sales channel", channels, default=channels)
    cities = sorted(df["city"].dropna().unique().tolist())
    selected_cities = st.multiselect("City", cities, default=cities)
    categories = sorted(df["category"].dropna().unique().tolist())
    selected_categories = st.multiselect("Product category", categories, default=categories)
    st.divider()
    st.caption("All visuals update with the selected filters.")

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]) + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)
else:
    start_date, end_date = pd.Timestamp(min_date), pd.Timestamp(max_date) + pd.Timedelta(days=1)

filtered = df[
    df["order_date"].between(start_date, end_date)
    & df["sales_channel"].isin(selected_channels)
    & df["city"].isin(selected_cities)
    & df["category"].isin(selected_categories)
].copy()

if filtered.empty:
    st.info("No orders match these filters. Choose a wider date range or more filter options.")
    st.stop()

delivered = filtered[filtered["order_status"] == "Delivered"].copy()
returned = filtered[filtered["order_status"] == "Returned"]
cancelled = filtered[filtered["order_status"] == "Cancelled"]
all_orders = len(filtered)
delivered_orders = len(delivered)
delivery_rate = delivered_orders / all_orders * 100 if all_orders else 0
return_rate = len(returned) / all_orders * 100 if all_orders else 0
cancel_rate = len(cancelled) / all_orders * 100 if all_orders else 0
delivered_sales = delivered["calculated_order_value"].sum()

# Repeat purchase is based on delivered orders inside the selected filtered period.
customer_order_counts = delivered.groupby("customer_id")["order_id"].nunique()
active_customers = int((customer_order_counts >= 1).sum())
repeat_customers = int((customer_order_counts >= 2).sum())
repeat_share = repeat_customers / active_customers * 100 if active_customers else 0

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Orders", f"{all_orders:,}")
k2.metric("Delivered sales", f"{delivered_sales:,.0f}", help="Delivered order values only; sample currency units.")
k3.metric("Delivery rate", f"{delivery_rate:.1f}%")
k4.metric("Return rate", f"{return_rate:.1f}%")
k5.metric("Repeat-customer share", f"{repeat_share:.1f}%", help="Share of customers with a delivered order in the selected period who had at least two delivered orders in that same period.")

st.divider()
left, right = st.columns(2)
with left:
    st.subheader("Order outcomes")
    status_summary = filtered.groupby("order_status", as_index=False).agg(orders=("order_id", "nunique"), order_value=("calculated_order_value", "sum"))
    fig = px.pie(status_summary, names="order_status", values="orders", hole=0.52,
                 title="Orders by status", color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(legend_title_text="Status", margin=dict(t=55, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Monthly delivered sales")
    if delivered.empty:
        st.info("No delivered orders in this filter selection.")
    else:
        monthly = delivered.assign(month=delivered["order_date"].dt.to_period("M").dt.to_timestamp()).groupby("month", as_index=False)["calculated_order_value"].sum()
        fig = px.line(monthly, x="month", y="calculated_order_value", markers=True,
                      labels={"month": "Month", "calculated_order_value": "Delivered sales (sample units)"})
        fig.update_layout(margin=dict(t=20, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Delivered sales by category")
    cat = delivered.groupby("category", as_index=False).agg(delivered_sales=("calculated_order_value", "sum"), delivered_orders=("order_id", "nunique"))
    cat = cat.sort_values("delivered_sales", ascending=True)
    fig = px.bar(cat, x="delivered_sales", y="category", orientation="h", text_auto=".2s",
                 labels={"delivered_sales": "Delivered sales (sample units)", "category": "Category"})
    fig.update_layout(margin=dict(t=15, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Delivered sales by city")
    city_sales = delivered.groupby("city", as_index=False).agg(delivered_sales=("calculated_order_value", "sum"), delivered_orders=("order_id", "nunique"))
    city_sales = city_sales.sort_values("delivered_sales", ascending=False)
    fig = px.bar(city_sales, x="city", y="delivered_sales", labels={"city": "City", "delivered_sales": "Delivered sales (sample units)"}, text_auto=".2s")
    fig.update_layout(xaxis_tickangle=-25, margin=dict(t=15, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Channel performance")
    channel_summary = filtered.groupby("sales_channel", as_index=False).agg(
        orders=("order_id", "nunique"), delivered_orders=("order_status", lambda s: (s == "Delivered").sum()),
        delivered_sales=("calculated_order_value", lambda s: s[filtered.loc[s.index, "order_status"].eq("Delivered")].sum())
    )
    channel_summary["delivery_rate_pct"] = (channel_summary["delivered_orders"] / channel_summary["orders"] * 100).round(1)
    st.dataframe(channel_summary.sort_values("orders", ascending=False), hide_index=True, use_container_width=True)
with right:
    st.subheader("Category and channel risk")
    risk = filtered.pivot_table(index="category", columns="order_status", values="order_id", aggfunc="nunique", fill_value=0).reset_index()
    for col in ["Delivered", "Returned", "Cancelled"]:
        if col not in risk.columns:
            risk[col] = 0
    risk["orders"] = risk[["Delivered", "Returned", "Cancelled"]].sum(axis=1)
    risk["return_rate_pct"] = (risk["Returned"] / risk["orders"] * 100).round(1)
    risk["cancel_rate_pct"] = (risk["Cancelled"] / risk["orders"] * 100).round(1)
    st.dataframe(risk[["category", "orders", "return_rate_pct", "cancel_rate_pct"]].sort_values("return_rate_pct", ascending=False), hide_index=True, use_container_width=True)

st.divider()
st.header("💡 Profitability improvement lab")
st.write("Use this scenario tool to estimate the value of reducing returns and cancellations. It is a planning scenario, not a forecast: recovered orders may not convert one-for-one, and actual costs are not available in this practice dataset.")
sc1, sc2, sc3 = st.columns(3)
with sc1:
    target_return_reduction = st.slider("Reduce return rate by (percentage points)", min_value=0, max_value=10, value=3)
with sc2:
    target_cancel_reduction = st.slider("Reduce cancellation rate by (percentage points)", min_value=0, max_value=10, value=2)
with sc3:
    assumed_margin = st.slider("Assumed gross margin (%)", min_value=0, max_value=80, value=25, help="Replace this assumption with a real margin when cost data is available.")

avg_order_value = delivered["calculated_order_value"].mean() if not delivered.empty else 0
potential_return_orders = min(len(returned), all_orders * target_return_reduction / 100)
potential_cancel_orders = min(len(cancelled), all_orders * target_cancel_reduction / 100)
potential_recovered_sales = (potential_return_orders + potential_cancel_orders) * avg_order_value
potential_gross_profit = potential_recovered_sales * assumed_margin / 100
p1, p2, p3 = st.columns(3)
p1.metric("Illustrative recovered orders", f"{potential_return_orders + potential_cancel_orders:.1f}")
p2.metric("Illustrative recovered sales", f"{potential_recovered_sales:,.0f}", help="Uses average delivered order value as a proxy.")
p3.metric("Illustrative gross profit", f"{potential_gross_profit:,.0f}", help="Scenario only: recovered sales multiplied by the user-selected assumed gross margin; not actual profit.")
st.caption("This simulator applies the selected percentage-point reductions to the filtered order count and values the scenario using average delivered order value. Validate assumptions with real operational and cost data before using for business decisions.")

st.subheader("Actionable recommendations")
recommendations = []
if return_rate > 0:
    recommendations.append(f"Investigate the {return_rate:.1f}% return rate: review product descriptions, quality issues, packaging, and return reasons by category.")
if cancel_rate > 0:
    recommendations.append(f"Investigate the {cancel_rate:.1f}% cancellation rate: review stock availability, delivery promises, payment failures, and checkout friction.")
if not cat.empty:
    top_category = cat.sort_values("delivered_sales", ascending=False).iloc[-1]
    recommendations.append(f"Prioritize analysis of {top_category['category']} for delivered sales; compare its gross margin and return rate before increasing promotion.")
if not city_sales.empty:
    top_city = city_sales.iloc[0]
    recommendations.append(f"Use {top_city['city']} as a candidate market to study, because it leads this filtered sample in delivered sales. Validate customer acquisition cost and delivery costs first.")
recommendations.append("Build a real profit model by adding unit cost, shipping/fulfilment cost, payment fees, advertising spend, and return handling cost for each order.")
for rec in recommendations:
    st.markdown(f"- {rec}")

with st.expander("View filtered order data"):
    display_cols = ["order_id", "order_date", "customer_id", "product_name", "category", "quantity", "discount_pct", "order_status", "sales_channel", "city", "calculated_order_value"]
    st.dataframe(filtered[display_cols].sort_values("order_date", ascending=False), hide_index=True, use_container_width=True)
    csv = filtered[display_cols].to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered data as CSV", data=csv, file_name="filtered_customer_orders.csv", mime="text/csv")

st.caption("Built for learning and portfolio demonstration. Customer names are synthetic placeholders; no real customer information is included.")
