import streamlit as st
import pandas as pd
import altair as alt

@st.cache_data
def load_data():
    return pd.read_csv('indexProcessed.csv', parse_dates=['Date'])

data = load_data()

data['Year'] = data['Date'].dt.year

min_year, max_year = int(data['Year'].min()), int(data['Year'].max())
years = st.slider('Select the range of years', min_year, max_year, (min_year, max_year))

filtered_data = data[(data['Year'] >= years[0]) & (data['Year'] <= years[1])]

yearly_data = filtered_data.groupby(['Index', 'Year'])['Close'].mean().reset_index()

chart = alt.Chart(yearly_data).mark_line(point=True).encode(
    x='Year:O',  
    y='Close:Q',  
    color='Index:N', 
    tooltip=['Index', 'Year', 'Close']
).properties(
    width=800,
    height=400
).interactive()

st.title('Index Performance Over the Years')
st.altair_chart(chart, use_container_width=True)

yearly_data = filtered_data.groupby(['Index', 'Year'])['Volume'].sum().reset_index()

chart = alt.Chart(yearly_data).mark_line(point=True).encode(
    x='Year:O',  
    y=alt.Y('Volume:Q', title='Total Volume Traded'),  
    color='Index:N',  
    tooltip=['Index', 'Year', 'Volume']
).properties(
    width=800,
    height=400
).interactive()

st.title('Index Trading Volume Over the Years')
st.altair_chart(chart, use_container_width=True)