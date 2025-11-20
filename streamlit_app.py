import streamlit as st

st.title(f"Customize Your Smoothie :cup_with_straw: {st.__version__}")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be", name_on_order)

# Connect to Snowflake using Streamlit's connection API
conn = st.connection("snowflake", type="snowflake")

# Load fruit options (SELECT is fine with conn.query)
fruit_df = conn.query(
    "SELECT FRUIT_NAME FROM SMOOTHIES.PUBLIC.FRUIT_OPTIONS ORDER BY FRUIT_NAME"
)
fruit_list = fruit_df["FRUIT_NAME"].tolist()

# Let the user pick up to 5 ingredients
ingredients_list = st.multiselect(
    "Choose up to five ingredients:",
    fruit_list,
    max_selections=5,
)

if ingredients_list and name_on_order:
    ingredients_string = " ".join(ingredients_list)

    if st.button("Submit Order"):
        # Use the Snowpark session for non-SELECT statements
        session = conn.session

        insert_sql = f"""
            INSERT INTO SMOOTHIES.PUBLIC.ORDERS (INGREDIENTS, NAME_ON_ORDER)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """

        session.sql(insert_sql).collect()  # execute INSERT

        st.success(
            f"Your Smoothie is ordered, {name_on_order}! "
            f"Ingredients: {ingredients_string}",
            icon="✅",
        )
