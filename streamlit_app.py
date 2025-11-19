import streamlit as st
import importlib.util

st.title("snowflake:", importlib.util.find_spec("snowflake"))
st.write("snowflake.connector:", importlib.util.find_spec("snowflake.connector"))


import streamlit as st

# Title and instructions
st.title(f"Customize Your Smoothie :cup_with_straw: {st.__version__}")
st.write("Choose the fruits you want in your custom Smoothie!")

# Name on order
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be", name_on_order)

# ✅ Connect to Snowflake using Streamlit's connections API
# Uses [connections.snowflake] from your secrets
conn = st.connection("snowflake", type="snowflake")

# Get fruit options as a pandas DataFrame
fruit_df = conn.query(
    "SELECT FRUIT_NAME FROM SMOOTHIES.PUBLIC.FRUIT_OPTIONS ORDER BY FRUIT_NAME"
)

# Convert to a plain Python list for the multiselect
fruit_list = fruit_df["FRUIT_NAME"].tolist()

# Let the user pick up to 5 ingredients
ingredients_list = st.multiselect(
    "Choose up to five ingredients:",
    fruit_list,
    max_selections=5,
)

if ingredients_list and name_on_order:
    # Build ingredients string from selected fruits
    ingredients_string = " ".join(ingredients_list)

    # Button to submit the order
    if st.button("Submit Order"):
        # Simple insert; for a toy app, f-string is OK
        insert_sql = f"""
            INSERT INTO SMOOTHIES.PUBLIC.ORDERS (INGREDIENTS, NAME_ON_ORDER)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """

        conn.query(insert_sql)

        st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")
