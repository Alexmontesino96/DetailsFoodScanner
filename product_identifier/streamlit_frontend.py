import streamlit as st
import asyncio
from product_schema.product import ProductOpenFoodFacts, ProductSpoonacular
from typing import Union
import requests
from services.search_product_by_name import ProductSearchParams 



st.title("Product Identifier")
st.write("This is a service to identify products based on their barcode.")


async def search_product_by_upc():
    with st.form(key='my_form'):
        upc_input = st.text_input(label='Enter the barcode of the product:')
        submit_button = st.form_submit_button(label='Submit')
    if submit_button:
        try:
            response = requests.get(f'http://127.0.0.1:8000/product-identifier/upc/{upc_input}')
            product = response.json()

        except Exception as e:
            st.write("An error occurred:", e)
            return
        if response.status_code == 200:

            st.write("Product found:")
            if product['image'] != 'N/A':
                st.image(product['image'], caption='Product Image', width=300)
            st.write(product)
        else:
            st.write("Product not found")

async def search_product_by_name():
    with st.form(key='search_by_name_form'):
        query = st.text_input(label='Enter the name of the product:', value='', key='query')
        offset = st.number_input(label='Enter the offset:', value=0, key='offset')
        number = st.number_input(label='Enter the number of products:', value=10, key='number')

        submit_button = st.form_submit_button(label='Submit')
    if submit_button:
        try:
            params = ProductSearchParams(query=query, offset=offset, number=number)
     
            response = requests.get(f'http://127.0.0.1:8000/product-identifier/search', params= {'query': params.query, 'offset': params.offset, 'number': params.number})
            product = response.json()
            product_result = product['searchResults'][1]['results']
            print(product_result)

        except Exception as e:
            st.write("An error occurred:", e)
            return
        
        if response.status_code == 200:
            st.write("Products found:")
            for p in product_result:
                st.write(p.get('name'))
                if p.get('image') != 'N/A':
                    st.image(p.get('image'), caption='Product Image', width=200)
                st.write(p.get('content'))
                st.write('-------------------')
        
        elif response.status_code == 404:
            st.write("Product not found")

        elif response.status_code == 500:
            st.write("Server error")
        
        else:
            st.write("An error occurred")
        return


async def frontend_receipt():
    st.write('This is the receipts page')
    input_receipt_id = st.text_input('Enter the receipt ID')
    button = st.button('Get receipt')
    if button:
        response = requests.get(f'http://127.0.0.1:9090/receipts/{input_receipt_id}')
        receipt = response.json()
        if receipt.get('image'):
            st.image(receipt['image'])
        if receipt.get('title'):
            st.write(receipt)


with st.sidebar:
    st.write('Select an option to continue:')
    option = st.selectbox(
        label='Select an option',
        options=['Search by barcode', 'Search by name', 'Get receipt'],
        placeholder='Select an option', 
        help='Disponible options: Search by barcode, Search by name, Get receipt',
        )

if option == 'Search by barcode':
    asyncio.run(search_product_by_upc())
elif option == 'Search by name':
    asyncio.run(search_product_by_name())
elif option == 'Get receipt':
    asyncio.run(frontend_receipt())
else:
    st.write('Choose an option to continue.')
