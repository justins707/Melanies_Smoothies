# Import python packages
import streamlit as st
import os

# Write directly to the app
st.subheader(f":cup_with_straw: Customize Your Smoothie")
st.write(
  """Choose up to 5 fruits for your custom Smoothie.
  """
)

cnx = st.connection("snowflake")
session = cnx.session
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

name_for_order = st.text_input('Enter your Name: ')
#st.write('The name for this order is:', name_for_order)

ingredients_list = st.multiselect('Choose ingredients:', my_dataframe, max_selections=5)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
    #st.write(ingredients_string)
    if ingredients_string:
        my_insert_statement = """ insert into smoothies.public.orders(ingredients, name, filled) values('""" + ingredients_string + """', '""" + name_for_order + """', 0)"""
        #st.write(my_insert_statement)
        
        submit_order = st.button('Submit Order')
        if submit_order:
            session.sql(my_insert_statement).collect()
            order_statement = """Your Smoothie is ordered, """ + name_for_order + """!""" 
            #st.write(order_statement,)
            st.success(order_statement, icon="✅")
