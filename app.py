import streamlit as st
import pandas as pd
import requests
import time

st.title("Business Finder")

location = st.text_input("City:", "Nashville, TN")
industry = st.selectbox("Industry:", ["All", "Food", "Auto", "Retail", "Health", "Tech"])

if st.button("Search"):
    with st.spinner("Finding real businesses..."):
        # Get coordinates
        geocode_url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json&limit=1"
        try:
            geo_response = requests.get(geocode_url, timeout=10)
            geo_data = geo_response.json()
            if geo_data:
                lat = float(geo_data[0]['lat'])
                lon = float(geo_data[0]['lon'])
                
                # Search for businesses
                overpass_url = "http://overpass-api.de/api/interpreter"
                query = f"""
                [out:json][timeout:25];
                (
                  node["shop"](around:5000,{lat},{lon});
                  node["amenity"~"^(restaurant|cafe|bar|fast_food)$"](around:5000,{lat},{lon});
                  node["office"](around:5000,{lat},{lon});
                );
                out meta;
                """
                
                response = requests.post(overpass_url, data=query, timeout=30)
                data = response.json()
                
                businesses = []
                for element in data.get('elements', []):
                    tags = element.get('tags', {})
                    name = tags.get('name', 'Unnamed Business')
                    
                    # Determine type
                    if 'shop' in tags:
                        biz_type = tags['shop'].title()
                    elif 'amenity' in tags:
                        biz_type = tags['amenity'].title()
                    elif 'office' in tags:
                        biz_type = 'Office'
                    else:
                        biz_type = 'Business'
                    
                    businesses.append({
                        'Name': name,
                        'Type': biz_type,
                        'Address': tags.get('addr:street', 'N/A'),
                        'Phone': tags.get('phone', 'N/A')
                    })
                
                if businesses:
                    st.write(f"Found {len(businesses)} real businesses in {location}")
                    df = pd.DataFrame(businesses)
                    st.dataframe(df)
                else:
                    st.write("No businesses found in this area")
            else:
                st.error("Location not found")
        except Exception as e:
            st.error(f"Error: {str(e)}")
