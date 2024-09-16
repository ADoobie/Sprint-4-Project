import streamlit as st
import pandas as pd
import plotly.express as px


# spliting into manufacturer

df = pd.read_csv('vehicles_us.csv')
df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])

# dropping some outliers that seem unrealistic to me

df = df[(df['odometer'] <= 600000) & (df['price'] <= 150000)]

st.header('Vehicle Data Workspace')

# check box to show or not show smaller manufacturers in data

show_manuf_1k_ads = st.checkbox('Include manufacturers with less than 1000 ads')
if not show_manuf_1k_ads:
    df = df.groupby('manufacturer').filter(lambda x: len(x) > 1000)

# histogram
st.dataframe(df)
st.header('Vehicle types by manufacturer')
st.write(px.histogram(df, x='manufacturer', color='type'))

# histogram
st.header('Histogram of `condition` vs `model_year`')
st.write(px.histogram(df, x='model_year', color='condition'))

# histogram with select box for comparisons
st.header('Compare price distribution between manufacturers')
manufac_list = sorted(df['manufacturer'].unique())
manufacturer_1 = st.selectbox('Select manufacturer 1',
                              manufac_list, index=manufac_list.index('chevrolet'))

manufacturer_2 = st.selectbox('Select manufacturer 2',
                              manufac_list, index=manufac_list.index('ford'))
mask_filter = (df['manufacturer'] == manufacturer_1) | (df['manufacturer'] == manufacturer_2)
df_filtered = df[mask_filter]
normalize = st.checkbox('Normalize histogram', value=True)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None
st.write(px.histogram(df_filtered,
                      x='price',
                      nbins=30,
                      color='manufacturer',
                      histnorm=histnorm,
                      barmode='overlay'))

# scatterplot
st.header('Price vs. Odometer by Manufacturer')
st.write(px.scatter(df, 
                     x='odometer', 
                     y='price', 
                     color='manufacturer', 
                     color_discrete_sequence=px.colors.qualitative.Bold))

# histogram
st.header('Listings Posed by Month')
df["date_posted"] = pd.to_datetime(df['date_posted'])
df["posted_month"] = df["date_posted"].dt.month
st.write(px.histogram(df, 
                      x='posted_month', 
                      title="Listings Posted by Month", 
                      nbins=12, 
                      color_discrete_sequence=['#636EFA']))




