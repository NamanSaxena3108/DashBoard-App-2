import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Pokemon App",
    page_icon="🐉",
    layout="wide",
)

@st.cache_data
def load_data():
    df=pd.read_csv("Pokemon.csv",index_col='#')
    df=df.set_index('Name')
    return df

with st.spinner("Loading Data...."):
    df = load_data()

st.title("Pokemon Data Analytics")
st.subheader("A simple app to analyze Pokemon Data")

st.sidebar.title("Menu")
choice=st.sidebar.radio("Options",["View Data","Visualize Data","Column Analysis"])

if choice == "View Data":
    st.header("View Dataset")
    st.dataframe(df)
elif choice=='Visualize Data':
    st.header("Visualization")
    cat_col=df.select_dtypes(include='object').columns.tolist()
    num_col=df.select_dtypes(exclude='object').columns.tolist()
    num_col.remove("Generation")
    num_col.remove('Legendary')
    cat_col.append("Generation")
    cat_col.append('Legendary')

    snum_col=st.sidebar.selectbox("Select a numeric column", num_col)
    scat_col=st.sidebar.selectbox("Select a Categorical column", num_col)

    c1,c2=st.columns(2)
    fig1=px.histogram(df,x=snum_col,title=f"Distribution of {snum_col}")

    fig2=px.pie(df,names=scat_col,title=f"Distribution of {scat_col}",hole=0.3)

    c1.plotly_chart(fig1)
    c2.plotly_chart(fig2)

    fig3=px.box(df,x=scat_col,y=snum_col,title=f"{snum_col} by {scat_col}")
    st.plotly_chart(fig3)
    
    fig4=px.treemap(df,path=['Generation','Type 1'],title="Pokemon Type Distribution")
    st.plotly_chart(fig4)
elif choice=='Column Analysis':
    columns=df.columns.tolist()
    scol=st.sidebar.selectbox("Select a column",columns)
    if df[scol].dtype == 'object':
        vc=df[scol].value_counts()
        most_common=vc.idxmax()
        c1,c2=st.columns([3,1])

        fig=px.histogram(df,x=scol,title=f"Distribution of {scol}")
        c1.plotly_chart(fig)

        c2.subheader("Total Data")
        c2.dataframe(vc,use_container_width=True)
        c2.metric("Moast Common",most_common,int(vc[most_common]))
        c1,c2=st.columns(2)
        fig2=px.pie(df,names=scol,title=f"Percentage wise of {scol}",hole=0.3)
        c1.plotly_chart(fig2)
        fig3=px.box(df,x=scol,title=f"{scol} by {scol}")
        c2.plotly_chart(fig3)
        fig4=px.funnel_area(names=vc.index,
                            values=vc.values,
                            title=f"{scol} Funnel Area",
                            height=600)
        st.plotly_chart(fig4)
    else:
        tab1,tab2=st.tabs(["Univariate", "Bivariate"])
        with tab1:
            score=df[scol].describe()
            fig1 = px.histogram(df, x=scol, title=f"Distribution of {scol}")
            fig2 = px.box(df, x=scol, title=f"{scol} by {scol}")
            c1, c2, c3 = st.columns([1,3,3])
            c1.dataframe(score)
            c2.plotly_chart(fig1)
            c3.plotly_chart(fig2)
        with tab2:
            c1, c2 = st.columns(2)
            col2 = c1.selectbox("Select a column", 
                                        df.select_dtypes(include='number').columns.tolist())
            color = c2.selectbox("Select a color", 
                                        df.select_dtypes(exclude='number').columns.tolist())
            fig3 = px.scatter(df, x=scol, y=col2, 
                            color=color, 
                            title=f"{scol} vs {col2}", height=600)
            st.plotly_chart(fig3, use_container_width=True,)
