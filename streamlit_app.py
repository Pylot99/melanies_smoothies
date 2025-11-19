import streamlit as st

# Write directly to the app
st.title(f"Customize Your Smoothie :cup_with_straw: {st.__version__}")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be", name_on_order)

# ✅ Use st.connection (singular)
cnx = st.connection("snowflake")
session = cnx.session()

# Load fruit options as a list
fruit_df = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    .select("FRUIT_NAME")
    .sort("FRUIT_NAME")
    .to_pandas()
)
fruit_list = fruit_df["FRUIT_NAME"].tolist()

# Let user pick up to 5 ingredients
ingredients_list = st.multiselect(
    "Choose up to five ingredients:",
    fruit_list,
    max_selections=5,
)

if ingredients_list and name_on_order:
    ingredients_string = " ".join(ingredients_list)

    my_insert_stmt = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS (INGREDIENTS, NAME_ON_ORDER)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")
