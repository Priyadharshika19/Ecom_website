import pandas as pd
import openpyxl
from streamlit_star_rating import st_star_rating
import pymongo
client=pymongo.MongoClient("mongodb+srv://priya:generate@cluster0.m4kzbjb.mongodb.net/?retryWrites=true&w=majority")
db=client["e_com"]
col=db["ecom"]
db1=client["admin"]
col1=db["admin"]
db2=client["products"]
col2=db["products"]
dict1={'user':[],'pwd':[]}

import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")
page_bg_img= """
<style>
[data-testid="stAppViewContainer"]
{
text-align: left;
background-color: #ebdabe;
}
[data-testid="stHeader"]
{
background-color: #5A83A8;
}
[data-testid="stSidebar"]
{
text-decoration-color: #e84d4c;
background-color: #5A83A8;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
st.title('Shopping World')
with st.sidebar:
    selected_page = option_menu(
        "Ecommerce",
        ("Create Account","User page","Admin page",'About','Contact details')
    )
#create acc
if selected_page == "Create Account":
    st.write('Create your new account here')
    c01, c02, c03 = st.columns([1, 2, 1])
    with c02:
        with st.form("my_form", clear_on_submit=True):
            st.write('New account')
            Fname = st.text_input('Fullname')
            Lname = st.text_input('Lastname')
            mail = st.text_input('Email address')
            phone = st.text_input('Phone number')
            u_name = st.text_input('Username')
            paswd = st.text_input('Password')
            submitted3 = st.form_submit_button('Submit')
            if submitted3:
                dict3 = {"Firstname": [], "Lastname": [], "Email": [], 'Phone Number': [], 'Username': [],
                         'Password': []}
                dict3["Firstname"].append(Fname)
                dict3["Lastname"].append(Lname)
                dict3["Email"].append(mail)
                dict3["Phone Number"].append(phone)
                dict3["Username"].append(u_name)
                dict3["Password"].append(paswd)
                count = 0
                for ele in col.find({}):
                    if ele['Firstname'][0] == dict3["Firstname"][0] and ele['Lastname'][0] == dict3["Lastname"][
                        0] and ele['Email'][0] == dict3["Email"][0] and ele['Phone Number'][0] == \
                            dict3["Phone Number"][0] and ele['Username'][0] == dict3["Username"][0] and \
                            ele['Password'][0] == dict3["Password"][0]:
                        count += 1
                if count == 0:
                    col.insert_one(dict3)
                    st.write('Successfully Registered')
                else:
                    st.write('Already Exist')
                    st.write('Go to login page')


#admin work
if selected_page == "Admin page":
    tab1, tab2, tab3 = st.tabs(['Admin Login','Products','Upload file'])
    with tab1:
        st.write('Shopping.com')
        with st.form("my_form1", clear_on_submit=True):
            Ausername = st.text_input('Admin name')
            Apassword = st.text_input('Admin Password')
            submitted1 = st.form_submit_button("login")
            if submitted1:
                count1 = 0
                for elemt in col1.find({}):
                    if elemt['admin'] == Ausername and elemt['password'] == Apassword:
                        count1 += 1
                if count1 == 1:
                    st.write('Successfully logged in')
                else:
                    st.write('Unauthorized login')
    with tab3:

        uploaded_file = st.file_uploader("Choose a XLSX file", type="xlsx")

        if uploaded_file:
            df = pd.read_excel(uploaded_file)
            #languages = df.loc[:,:]
            st.write(df)
            st.write(len(df))
            for y in range(len(df)):
                s=df.loc[y,:].to_dict()
                s = {k.strip(): v for (k, v) in s.items()}
                st.write(s)
                col2.insert_one(s)
    with tab2:
        st.write('Product')
        with st.form("my_form2", clear_on_submit=True):
            Pname = st.text_input('Name')
            Bcode = st.text_input('Barcode')
            Brand = st.text_input('Brand')
            Description = st.text_input('Description')
            Price = st.text_input('Price')
            Available = st.text_input('Available')
            submitted2 = st.form_submit_button('Submit')
            if submitted2:
                dict1 = {"name": '', "barcode": '', "brand": '', 'description': '', 'price': '', 'available': ''}
                dict1["name"]=Pname
                dict1["barcode"]=Bcode
                dict1["brand"]=Brand
                dict1["description"]=Description
                dict1["price"]=Price
                dict1["available"]=Available
                count = 0
                for eleme in col2.find({}):
                    if eleme['name'] == dict1["name"] and eleme['barcode'] == \
                            dict1["barcode"] and eleme['brand'] == dict1["brand"] and \
                            eleme['description'] == dict1["description"] and eleme['price'] == dict1["price"] and eleme['available'] == dict1["available"]:
                        count += 1
                if count == 0:
                    col2.insert_one(dict1)
                    st.write('Successfully uploaded')
                else:
                    col2.delete_one(dict1)
                    col2.insert_one(dict1)
                    st.write('Already Exist and Successfully Replaced')
        name_lst=[]
        for i in col2.find({}):
            name_lst.append(i['name'])

        select1=st.selectbox('Products List',name_lst)
        for j in col2.find({}):
            if j['name'] == select1:
                st.dataframe(j)
#user page
if selected_page == "User page":

    tab1, tab2, = st.tabs(['User login', 'Products'])
    with tab1:
        with st.form("my_form2", clear_on_submit=True):
            username = st.text_input('Username')
            password = st.text_input('Password')
            submitted2 = st.form_submit_button("login")
            if submitted2:
                count1 = 0
                for elem in col.find({}):
                    if elem['Username'][0] == username and elem['Password'][0] == password:
                        count1 += 1
                if count1 == 0:
                    st.write('Username/Password not exist')
                else:
                    st.write('Logged in')
    with tab2:
        st.write('Shop your favourite products')
        name_lst1 = []
        for k in col2.find({}):
            name_lst1.append(k['name'])
        select2 = st.selectbox('Products List', name_lst1)
        for l in col2.find({}):
            if l['name'] == select2:
                st.dataframe(l)
                stars = st_star_rating(label="Please rate you experience", maxValue=5, defaultValue=3, key="rating", emoticons=True)
                st.balloons()
                st.write('Thank you for your valuable feedback')
                col2.update_one({
                    '_id': l['_id']
                }, {
                    '$set': {
                        'rating': stars
                    }
                }, upsert=False)
#about
if selected_page == 'About':
    st.write('>>Welcome to Shopping World')
    st.write('''>>Shopping worlds marketplace offers over 150 million products across 80+ categories. With a focus on empowering and delighting every Indian by delivering value through technology and innovation''')
#Contact us
if selected_page == 'Contact details':
    st.write("**Ecommerce Project**")
    st.write(">>Created by: Priyadharshika.M")
    st.write(">>Linkedin page: https://www.linkedin.com/in/priyadharshika-m-176204269/")
    st.write(">>Github Page: https://github.com/Priyadharshika19")
