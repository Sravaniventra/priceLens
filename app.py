'''import streamlit as st
import pandas as pd
import altair as alt
from scraper import scrape_url  # scrapers for Amazon, Flipkart, Myntra, Ajio
from database import (
    init_db,
    insert_product,
    insert_price,
    get_price_history,
    add_subscriber,
    get_subscribers,
)
from alerts import send_email_alert  # ✅ import email function

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="PriceLens – Price Comparison", layout="centered")

st.title("📊 PriceLens – Product Price Comparison")
st.write("Compare product prices across **Amazon, Flipkart, Myntra, Ajio**.")

# Initialize database
init_db()

# -------------------------
# Session State for Dynamic Inputs
# -------------------------
if "links" not in st.session_state:
    st.session_state.links = ["", ""]  # 2 compulsory links
if "emails" not in st.session_state:
    st.session_state.emails = ["", ""]  # one email per product

def add_link_box():
    st.session_state.links.append("")
    st.session_state.emails.append("")

# -------------------------
# Input Fields
# -------------------------
st.subheader("🔗 Enter Product Links & Email to Get Alerts")
for i in range(len(st.session_state.links)):
    st.session_state.links[i] = st.text_input(f"Product Link {i+1}", st.session_state.links[i])
    st.session_state.emails[i] = st.text_input(f"Alert Email for Product {i+1}", st.session_state.emails[i])

st.button("➕ Add another product", on_click=add_link_box)

# -------------------------
# Price Comparison
# -------------------------
st.subheader("💰 Price Comparison")

results = []

for i, url in enumerate(st.session_state.links):
    if url.strip():
        name, price = scrape_url(url)
        if name and price:
            site = url.split("/")[2].replace("www.", "")
            results.append((name, price, site))

            # ---- Save to Database ----
            product_id = insert_product(url, site, name)
            insert_price(product_id, price)

            # ---- Save Subscriber if Email Entered ----
            user_email = st.session_state.emails[i]
            if user_email.strip():
                add_subscriber(product_id, user_email)

            # ---- Get Price History (7 days) ----
            history = get_price_history(product_id, days=7)
            df = pd.DataFrame(history, columns=["date", "price"])

            # ---- Show History Chart ----
            st.write(f"**{name}** ({site}) → ₹{price:,.0f}")
            if not df.empty:
                df["date"] = pd.to_datetime(df["date"])
                df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0).clip(lower=0)
                df = df.sort_values("date")

                chart = (
                    alt.Chart(df)
                    .mark_line(point=True)
                    .encode(
                        x=alt.X(
                            "date:T",
                            title="Date",
                            axis=alt.Axis(format="%d %b %I%p", labelAngle=-45),
                        ),
                        y=alt.Y(
                            "price:Q",
                            title="Price (₹)",
                            scale=alt.Scale(zero=False),
                        ),
                        tooltip=[
                            alt.Tooltip("date:T", title="Date"),
                            alt.Tooltip("price:Q", title="Price (₹)"),
                        ],
                    )
                    .properties(width=650, height=350)
                    .interactive()
                )

                st.altair_chart(chart, use_container_width=True)

                # ✅ Notify if lowest in last 7 days
                if price == df["price"].min():
                    st.success("🎉 This is the **lowest price** in the past 7 days!")

                    # 🔔 Send Email to All Subscribers
                    subscribers = get_subscribers(product_id)
                    for sub_email in subscribers:
                        send_email_alert(
                            sub_email, name, site, price, df["price"].min(), 7
                        )

            else:
                st.info("No price history available yet.")

        else:
            st.error(f"❌ Could not fetch price for: {url}")

# -------------------------
# Best Deal Section
# -------------------------
if results:
    df_results = pd.DataFrame(results, columns=["Product", "Price", "Site"])
    min_row = df_results.loc[df_results["Price"].idxmin()]
    st.subheader("🏆 Best Deal")
    st.success(f"Lowest Price → **{min_row['Site']}** at ₹{min_row['Price']:,.0f}")
'''

import streamlit as st
import pandas as pd
import altair as alt
from scraper import scrape_url  # scrapers for Amazon, Flipkart, Myntra, Ajio
from database import (
    init_db,
    insert_product,
    insert_price,
    get_price_history,
    add_subscriber,
    get_subscribers,
)
from alerts import send_email_alert  
# Page Config
st.set_page_config(page_title="PriceLens – Price Comparison", layout="centered")

st.title("📊 PriceLens – Product Price Comparison")
st.write("Compare product prices across **Amazon, Flipkart, Myntra, Ajio**.")

# Initialize database
init_db()

# Session State for Dynamic Inputs
if "links" not in st.session_state:
    st.session_state.links = ["", ""]  # 2 compulsory links
if "emails" not in st.session_state:
    st.session_state.emails = ["", ""]  # one email per product

def add_link_box():
    st.session_state.links.append("")
    st.session_state.emails.append("")
# Input Fields
st.subheader("🔗 Enter Product Links & Email to Get Alerts")
for i in range(len(st.session_state.links)):
    st.session_state.links[i] = st.text_input(
        f"Product Link {i+1}", st.session_state.links[i]
    )
    st.session_state.emails[i] = st.text_input(
        f"Alert Email for Product {i+1}", st.session_state.emails[i]
    )

st.button("➕ Add another product", on_click=add_link_box)

# Price Comparison
st.subheader("💰 Price Comparison")

results = []

for i, url in enumerate(st.session_state.links):
    if url.strip():
        name, price = scrape_url(url)
        if name and price:
            site = url.split("/")[2].replace("www.", "")
            results.append((name, price, site))

            #  Save to Database 
            product_id = insert_product(url, site, name)
            insert_price(product_id, price)

            #  Save Subscriber if Email Entered 
            user_email = st.session_state.emails[i]
            if user_email.strip():
                add_subscriber(product_id, user_email)

            #  Get Price History (7 days) 
            history = get_price_history(product_id, days=7)
            df = pd.DataFrame(history, columns=["date", "price"])

            #  Show History Chart 
            st.write(f"**{name}** ({site}) → ₹{price:,.0f}")
            if not df.empty:
                df["date"] = pd.to_datetime(df["date"])
                df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0).clip(lower=0)
                df = df.sort_values("date")

                chart = (
                    alt.Chart(df)
                    .mark_line(point=True)
                    .encode(
                        x=alt.X(
                            "date:T",
                            title="Date",
                            axis=alt.Axis(format="%d %b %I%p", labelAngle=-45),
                        ),
                        y=alt.Y(
                            "price:Q",
                            title="Price (₹)",
                            scale=alt.Scale(zero=False),
                        ),
                        tooltip=[
                            alt.Tooltip("date:T", title="Date"),
                            alt.Tooltip("price:Q", title="Price (₹)"),
                        ],
                    )
                    .properties(width=650, height=350)
                    .interactive()
                )

                st.altair_chart(chart, use_container_width=True)

                #Notify if lowest in last 7 days
                min_price = df["price"].min()
                if price == min_price:
                    st.success("🎉 This is the **lowest price** in the past 7 days!")

                    # Send Email to All Subscribers (only when lowest price detected)
                    subscribers = get_subscribers(product_id)
                    for sub_email in subscribers:
                        send_email_alert(
                            sub_email,
                            name,
                            site,
                            price,
                            min_price,
                            7
                        )

            else:
                st.info("No price history available yet.")

        else:
            st.error(f"❌ Could not fetch price for: {url}")

# Best Deal Section
if results:
    df_results = pd.DataFrame(results, columns=["Product", "Price", "Site"])
    min_row = df_results.loc[df_results["Price"].idxmin()]
    st.subheader("🏆 Best Deal")
    st.success(f"Lowest Price → **{min_row['Site']}** at ₹{min_row['Price']:,.0f}")
