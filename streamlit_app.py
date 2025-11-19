# Import python packages
import streamlit as st

# Write directly to the app
st.title(f"Customize Your Smoothie :cup_with_straw: {st.__version__}")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be", name_on_order)

# Get Snowflake connection & session
cnx = st.connection("snowflake")
session = cnx.session()

# Get fruit options from Snowflake
fruit_df = session.sql("""
    SELECT FRUIT_NAME
    FROM smoothies.public.fruit_options
    ORDER BY FRUIT_NAME
""").to_pandas()

fruit_list = fruit_df["FRUIT_NAME"].tolist()

# Let user pick up to 5 ingredients
ingredients_list = st.multiselect(
    "Choose up to five ingredients:",
    fruit_list,
    max_selections=5
)

if ingredients_list:
    # Build ingredients string
    ingredients_string = " ".join(ingredients_list)

    # Build insert statement
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    # Show a submit button
    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")
