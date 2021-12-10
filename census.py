import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

df_census = pd.read_csv("C:/Users/anupm/OneDrive/Desktop/Plot AI/Datasets/Al/Census/Census.csv")


#MULTISLECT

#Unique option in select widget
sel_region = st.sidebar.multiselect("Region:", pd.Series(np.append('All', df_census.Region.unique())), default='All')
sel_division = st.sidebar.multiselect("Division:", pd.Series(np.append('All', df_census.Division.unique())), default='All')
sel_state = st.sidebar.multiselect("State:", pd.Series(np.append('All', df_census.State.unique())), default='All')
sel_sex = st.sidebar.multiselect('Sex:', pd.Series(np.append('All', df_census.Sex.unique())), default='All')
sel_origin = st.sidebar.multiselect('Origin:', pd.Series(np.append('All', df_census.Origin.unique())), default='All')
sel_race = st.sidebar.multiselect('Race:', pd.Series(np.append('All', df_census.Race.unique())), default='All')
sel_race_origin = st.sidebar.multiselect('Race and Origin:', pd.Series(np.append('All', df_census.Race_and_Origin.unique())), default='All')
sel_age_group = st.sidebar.multiselect('Age Group:', pd.Series(np.append('All', df_census.Age_Group.unique())), default='All')



if "All" in sel_region:
    sel_region = df_census.Region.unique()
if "All" in sel_division:
    sel_division = df_census.Division.unique()
if "All" in sel_state:
    sel_state = df_census.State.unique()
if "All" in sel_sex:
    sel_sex = df_census.Sex.unique()
if "All" in sel_origin:
    sel_origin = df_census.Origin.unique()
if "All" in sel_race:
    sel_race = df_census.Race.unique()
if "All" in sel_race_origin:
    sel_race_origin = df_census.Race_and_Origin.unique()
if "All" in sel_age_group:
    sel_age_group = df_census.Age_Group.unique()



#DATA MANIPULATION

#df_census_copy = df_census.iloc[:0,:].copy()
#st.dataframe(df[df.Country_Name==option])
# for selected in sel_region:
#        df_census_copy = df_census_copy.append(df_census[df_census.Region==selected])

df_census_copy = df_census

df_census_copy = df_census_copy.loc[df_census_copy['Region'].isin(sel_region)]
df_census_copy = df_census_copy.loc[df_census_copy['Division'].isin(sel_division)]
df_census_copy = df_census_copy.loc[df_census_copy['State'].isin(sel_state)]
df_census_copy = df_census_copy.loc[df_census_copy['Sex'].isin(sel_sex)]
df_census_copy = df_census_copy.loc[df_census_copy['Origin'].isin(sel_origin)]
df_census_copy = df_census_copy.loc[df_census_copy['Race'].isin(sel_race)]
df_census_copy = df_census_copy.loc[df_census_copy['Race_and_Origin'].isin(sel_race_origin)]
df_census_copy = df_census_copy.loc[df_census_copy['Age_Group'].isin(sel_age_group)]


#CHARTS
df_bar_region_population = df_census_copy.groupby(['Region']).sum()
bar_region_population = alt.Chart(df_bar_region_population).mark_bar().encode(
    x= 'Region:O',
    y= alt.Y('sum(Population_2019)', axis = alt.Axis( title= '2019 Population'))
).properties(width=600)


stacked_bar_age_race_origin = alt.Chart(df_census_copy).mark_bar().encode(
    x='Age_Group',
    y='sum(Population_2019)',
    color='Race_and_Origin'
)


area_age_race_origin = alt.Chart(df_census_copy).mark_area().encode(
    x='Age_Group',
    y=alt.Y('sum(Population_2019)', stack="normalize"),
    color='Race_and_Origin'
)


#DISPLAY

#st.write(df_original.head(6))
#st.write(df_census_copy.head(1000))
st.altair_chart(bar_region_population)
st.altair_chart(stacked_bar_age_race_origin)
st.altair_chart(area_age_race_origin)
