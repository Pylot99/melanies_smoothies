import streamlit as st
import requests

st.title(f"Customize Your Smoothie :cup_with_straw: {st.__version__}")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be", name_on_order)

# Connect to Snowflake using Streamlit's connection API
conn = st.connection("snowflake", type="snowflake")

# 🔹 Get the Snowpark session
session = conn.session()

# Load fruit options - conn.query already returns a Pandas DataFrame
fruit_df = conn.query(
    "SELECT FRUIT_NAME FROM SMOOTHIES.PUBLIC.FRUIT_OPTIONS ORDER BY FRUIT_NAME"
)

# Optional: show the DataFrame for debugging
# st.dataframe(fruit_df)

# Convert to a plain Python list
fruit_list = fruit_df["FRUIT_NAME"].tolist()

# Let the user pick up to 5 ingredients
ingredients_list = st.multiselect(
    "Choose up to five ingredients:",
    fruit_list,
    max_selections=5,
)

if ingredients_list and name_on_order:
    # Build a single string of ingredients
    ingredients_string = " ".join(ingredients_list)

    # Nutrition info section
    st.subheader("Nutrition Information")

    # 🔹 Call your Smoothiefroot API for each fruit selected
    for fruit_chosen in ingredients_list:
        smoothiefroot_response = requests.get(
            f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen.lower()}"
        )

        st.write(f"Smoothiefroot data for **{fruit_chosen}**:")
        st.dataframe(
            data=smoothiefroot_response.json(),
            use_container_width=True,
        )

    # Only run the insert when the button is clicked
    if st.button("Submit Order"):
        # Basic escaping of single quotes to avoid breaking the SQL
        safe_ingredients = ingredients_string.replace("'", "''")
        safe_name = name_on_order.replace("'", "''")

        insert_sql = f"""
            INSERT INTO SMOOTHIES.PUBLIC.ORDERS (INGREDIENTS, NAME_ON_ORDER)
            VALUES ('{safe_ingredients}', '{safe_name}')
        """

        # 🔹 Use Snowpark session for the INSERT
        session.sql(insert_sql).collect()

        st.success(
            f"Your Smoothie is ordered, {name_on_order}! "
            f"Ingredients: {ingredients_string}",
            icon="✅",
        )
