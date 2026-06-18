# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session 
from snowflake.snowpark.functions import col
from snowflake.snowpark.functions import when_matched
import os

# Write directly to the app
st.title(f":cup_with_straw: Pending Smoothie Orders")
st.write(
  """Orders that need to be filled!
  """
)
session = get_active_session()
df=session.table("smoothies.public.orders").filter(col("Filled")==0).collect()
my_dataframe = pd.DataFrame(df)

if my_dataframe.empty:
    st.success('There are no pending orders right now.', icon=":material/thumb_up:")
else:
    editable_df = st.data_editor(my_dataframe, hide_index=True)

    submitted = st.button('Submit')

    if submitted:
        st.success("You filled an order", icon=":material/thumb_up:")
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
        og_dataset.merge(edited_dataset
                     , (og_dataset['UID'] == edited_dataset['UID'])
                     , [when_matched().update({'FILLED': edited_dataset['FILLED']})]
                    )
