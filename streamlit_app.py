# Import packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Title
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie")


name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be", name_on_order)
# Snowflake session
session = get_active_session()

# Get fruit list from table
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
fruit_list = [row["FRUIT_NAME"] for row in my_dataframe.collect()]  # convert to Python list

# Multiselect widget
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

# Initialize ingredients_string early to avoid NameError
ingredients_string = ''

# If user selected ingredients, build string
if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)

# Construct SQL insert
my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders(ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}')
"""

#st.write(my_insert_stmt);
#st.stop();

# Submit button
if st.button('Submit Order'):
    if ingredients_list:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")

    else:
        st.warning("Please select at least one ingredient before submitting.")
