
import pandas as pd  
import plotly.express as px  
import streamlit as st  
import pydeck as pdk
import numpy as np

st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io="supermarkt_sales.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000,
    )
    
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()


st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique(),
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

branch = st.sidebar.multiselect("Select Branch:",
            options = df['Branch'].unique(),
            default = df['Branch'].unique()
            )

customer_type = st.sidebar.multiselect("Select Customer Type:",
            options = df['Customer_type'].unique(),
            default = df['Customer_type'].unique()
            )

df_selection = df.query(
    "City == @city & Customer_type ==@customer_type & Gender == @gender & Branch == @branch & Customer_type == @customer_type"
)


st.title(":bar_chart: Sales Dashboard")
st.markdown("##")


total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"GBP {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")

with st.expander("See Data In Tabular Form", expanded = False):
    st.write(df_selection)
    
sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)

fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)

fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]

fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)

fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)



df_for_comparison = df.groupby(by=["Gender"]).sum()['Total']
fig_sales_based_on_gender = px.pie(df_for_comparison, names=['Female', 'LGBTQ', 'Male'], values='Total', hole=.3)
# fig.show()
with st.expander("Sales Figures Based On Genders", expanded=True):
    st.plotly_chart(fig_sales_based_on_gender)


quantity_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Quantity"]].sort_values(by="Quantity")
)

fig_product_quantity = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Quantity by Product Line</b>",
    # color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)

fig_product_quantity.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

with st.expander("Product Quantity Sales", expanded=True):
    st.plotly_chart(fig_product_quantity)

total_by_payment_type = (
    df_selection.groupby(by=["Payment"]).sum()[["Total"]]
)


fig_payment_comparison = px.bar(
    total_by_payment_type,
    x="Total",
    y=total_by_payment_type.index,
    orientation="h",
    title="<b>Quantity by Product Line</b>",
    # color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)

with st.expander("Payments Type Comparison", expanded=True):
    st.plotly_chart(fig_payment_comparison)

gross_income_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["gross income"]].sort_values(by="gross income")
)

# print(gross_income_by_product_line)

fig_gross_income_by_product = px.bar(
    gross_income_by_product_line,
    x="gross income",
    y=gross_income_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(gross_income_by_product_line),
    template="plotly_white",
)

with st.expander("Gross Income By Product Type", expanded=True):
    st.plotly_chart(fig_gross_income_by_product)

df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [52.4, -1.89],
    columns=['lat', 'lon'])
with st.expander("Customers By Location", expanded=True):
    st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=52.4,
         longitude=-1.89,
         zoom=11,
         pitch=50,
     ),
     layers=[
         pdk.Layer(
            'HexagonLayer',
            data=df,
            get_position='[lon, lat]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
         ),
         pdk.Layer(
             'ScatterplotLayer',
             data=df,
             get_position='[lon, lat]',
             get_color='[200, 30, 0, 160]',
             get_radius=200,
         ),
     ],
 ))