import pandas as pd
import plotly.express as px
import streamlit as st

# dashboard page and title creation
st.set_page_config(page_title="Agricaltural Exports", page_icon=":seedling:", 
                   layout="wide")
st.title(":seedling: US Agricaltural Exports in 2011 in USD")

link = "https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv"

# data import and prep
df = pd.read_csv(link)
df.drop("category", axis=1, inplace=True)
df.rename(columns={'total fruits':'fruits', 'total veggies':'veggies'}, inplace=True)
categories = ['beef', 'pork', 'poultry', 'dairy', 'fruits', 'veggies', 
              'corn', 'wheat', 'cotton']
df['misc.'] = df['total exports'] - df[categories].sum(axis=1)
df.sort_values('code', inplace=True)
categories.append('misc.')
df_cat = pd.melt(frame=df, id_vars=['code', 'state'], 
                 value_vars=categories, var_name='category', value_name='export')

# figure 1: total exports by state in a choropleth
st.subheader("US Total Exports by State in Million USD")
fig = px.choropleth(data_frame=df,
                    locationmode='USA-states',
                    locations='code',
                    scope="usa",
                    color="total exports",
                    hover_name="state",
                    hover_data= "total exports",
                    color_continuous_scale=px.colors.sequential.Magenta)

fig.update_layout(coloraxis_colorbar={'title':'Total Exports'})
st.plotly_chart(fig, use_container_width=True, height=400)


# sidebar and state filter creation
st.sidebar.header("Filter Data by State(s): ")
state = st.sidebar.multiselect("Choose the state(s)", df['state'])

# logic for the state selection
if not state:
    df_states=df.copy()
    df_cat_states = df_cat.copy()
else:
    df_states=df.loc[df["state"].isin(state)]
    df_cat_states = df_cat.loc[df_cat['state'].isin(state)]

df_states.sort_values('total exports', ascending=False, inplace=True)
formatted_states = ", ".join(state)

# dasboard columns creation
col1, col2 = st.columns((2))

# Figure 2: total exports by state in a bar chart for chosen states
with col1:
    st.subheader("Total Exports - "+formatted_states)
    fig=px.bar(data_frame=df_states, x='code', y="total exports", hover_name="state",
               color_continuous_scale=px.colors.sequential.Magenta,
               color="total exports",
               labels={'code': 'State', 'total exports':'Total Exports'})
    
    st.plotly_chart(fig, use_container_width=True, height=200)


# Figure 3: categories breakdown for chosen states
with col2:
    st.subheader("Categories Breakdown - "+formatted_states)
    cat_states_agg = df_cat_states.groupby("category")[['export']].sum().reset_index()
    fig = px.pie(data_frame=cat_states_agg, names='category', values='export', 
             color='category', color_discrete_sequence=px.colors.qualitative.Safe, 
             hole=0.4)
    
    fig.layout.legend.title.text = "Export Categories"
    st.plotly_chart(fig, use_container_width=True, height=200)

