#1. Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

#2. Write directly to the app
st.title(":green_salad: My Parents New Healthy Diner :green_salad:")
st.write(
    """Make your custom Smoothie, choose the fruits that your :heart: desires!
    """
)

#13 🥋 Add a Name Box for Smoothie Orders
name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

#4. Get only the column we need
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

#5. Write dataframe into our streamlit page
st.dataframe(data=my_dataframe, use_container_width=True)

#6. Add multi-select from streamlit
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections=5
    )

# Our ingredients variable is an object or data type called a LIST.
# So it's a list in the traditional sense of the word, 
# but it is also a datatype or object called a LIST. 
# A LIST is different than a DATAFRAME which is also different 
# from a STRING!

#st.write(ingredients_list)
#st.text(ingredients_list)

#7. 🥋 Cleaning Up Empty Brackets. If ingredients have not yet been 
# chosen, there is no need to show this. 

#if ingredients_list:
        #st.write(ingredients_list)
        #st.text(ingredients_list)

#8. 🥋 Create a Place to Store Order Data (Done In worksheets)

#9. 📓 Changing the LIST to a STRING
# In order to convert the list to a string, we need to first 
# create a variable and then make sure Python thinks it 
# contains a string.

if ingredients_list:
    # WE DONT NEED ANYMORE AS WE WRITE LATER IN INGREDIENTS_STRING
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        #fuit_chosen = []
        ingredients_string += fruit_chosen + ' '
            
        #The += operator means "add this to what is already
        #in the variable" so each time the FOR Loop is 
        #repeated, a new fruit name is appended to the 
        #existing string. 

    #st.write(ingredients_string)

    #10. 🥋 Build a SQL Insert Statement & Test It

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()

    #12. 🥋 Add a Submit Button, otherwise every fruit selection
    # will create a new row in the orders table
    
    time_to_insert = st.button('Submit Order')

    #11. 🥋 Insert the Order into Snowflake
    #11. if ingredients_string:
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
	
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
    

