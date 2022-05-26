import pandas as pd # pip install pandas, pip install openpyxl
import plotly.express as px # pip install plotly-express
import streamlit as st # pip install streamlit

# Realizamos la configuracion principal de la pagina
st.set_page_config(
    page_title="Oficina de ventas",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)

# Creamos el dataframe con pandas
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
    df["hora"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df
df = get_data_from_excel()

# Sidebar
st.sidebar.header("Ingrese el filtro:")
city = st.sidebar.multiselect(
    "Selecciona la ciudad:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Selecciona el tipo de cliente:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique()
)

gender = st.sidebar.multiselect(
    "Selecciona el genero:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)


df_selection = df.query(
    "City == @city and Customer_type == @customer_type and Gender == @gender"
)


# Cargamos el dataframe en la pagina 
# st.dataframe(df_selection)

# Pagina principal
st.title(":bar_chart: Oficina de ventas")

# kpi
total_sales = df_selection["Total"].sum()
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * round(average_rating)
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Ventas totales:")
    st.subheader(f"US $ {total_sales}")
with middle_column:
    st.subheader("Promedio de opiniones:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Valor promedio por transaccion:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("---")


# Graficos
# Ventas por linea de producto
sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x = "Total",
    y = sales_by_product_line.index,
    orientation="h",
    title="<b>Ventas por linea de producto</b>",
    color_discrete_sequence=["#C8C8C8"],
    template="plotly_white"
)
fig_product_sales.update_layout(
    plot_bgcolor = "rgba(0, 0, 0, 0)",
    xaxis = (dict(showgrid=False))
)


# Ventas por hora
sales_by_hour = (
    df_selection.groupby(by=["hora"]).sum()[["Total"]]
)
fig_hourly_sales = px.bar(
    sales_by_hour,
    x = sales_by_hour.index,
    y = "Total",
    title="<b>Ventas por hora</b>",
    color_discrete_sequence=["#C8C8C8"],
    template="plotly_white"
)
fig_hourly_sales.update_layout(
    plot_bgcolor = "rgba(0, 0, 0, 0)",
    xaxis = (dict(tickmode="linear")),
    yaxis = (dict(showgrid=False))
)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_product_sales, use_container_width=True)
right_column.plotly_chart(fig_hourly_sales, use_container_width=True)

# Personalizando la pagina (ocultando estilos de streamlite)
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)