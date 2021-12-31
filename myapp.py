import streamlit as st
import requests, json
import math

endpoint = st.sidebar.selectbox("Endpoints", ["Assets","Events","Rarity"])
st.header(f"OpenSea NFT Explorer - {endpoint}")

st.sidebar.subheader("Filters")
collection = st.sidebar.text_input("Collection")
owner = st.sidebar.text_input("Owner")

if endpoint == "Assets":
    params = {}

    if collection != "":
        params["collection"] = collection

    if owner != "":
        params["owner"] = owner

    r = requests.get("https://api.opensea.io/api/v1/assets", params=params)

    response = r.json()

    for asset in response["assets"]:
        st.write(f"{asset['name']} (#{asset['token_id']})")
        if asset["sell_orders"] is not None:
            sell_order = asset["sell_orders"][0]
            if sell_order["side"] == 1:
                currency_sym = sell_order["payment_token_contract"]["symbol"]
                currency_decimals = sell_order["payment_token_contract"]["decimals"]
                price = float(sell_order["current_price"]) / math.pow(10, currency_decimals)
                st.write(f"Buy Now: {price} {currency_sym}")

        st.image(asset["image_url"])

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)