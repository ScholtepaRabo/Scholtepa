import pandas as pd
import streamlit as st

st.title('Marine Fish Data')

# Read the CSV file into a DataFrame
df = pd.read_csv('./Marine_Fish_Data.csv')

#markdown a text with streamlit
st.markdown('This is a dataset of marine fish. The data includes the following columns:')
#use streamlit to plot a histogram of the column 'Species'


#use streamlit to plot a dynamic table df
st.write(df)
#make a header with streamlit
st.header('Fish Data Analysis')
#use streamlit to plot a dynamic table df.describe()
st.write(df.describe())
#use streamlit to plot a dynamic table df.info()
st.write(df.info())
#use streamlit to plot a dynamic table df.columns
st.write(df.columns)
#use streamlit to plot a dynamic table df.head()
st.write(df.head())
#use streamlit to plot a dynamic table df.tail()
st.write(df.tail())
#use streamlit to plot a dynamic table df.shape
st.write(df.shape)
#use streamlit to plot a dynamic table df.dtypes
st.write(df.dtypes)

