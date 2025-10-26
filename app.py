import streamlit as st
import pandas as pd
import random

st.title("Business Finder")

location = st.text_input("City:", "Nashville, TN")
industry = st.selectbox("Industry:", ["All", "Food", "Auto", "Retail", "Health", "Tech"])

if st.button("Search"):
    data = []
    for i in range(1000):
        data.append({
            "Name": f"Business {i+1}",
            "Type": random.choice(["Restaurant", "Shop", "Service"]),
            "Age": random.randint(1, 20),
            "Revenue": f"${random.randint(50, 500)}K"
        })
    
    st.write(f"Found {len(data)} businesses in {location}")
    df = pd.DataFrame(data)
    st.dataframe(df)
    st.write(f"Average age: {df['Age'].mean():.1f} years")

st.write("Demo data only")
