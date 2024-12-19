import streamlit as st
from sfdc_login import *
from sfdc_tooling_request import *
from sfdc_tooling_response import *

def main():

    st.set_page_config(layout="wide",page_title="SFDC Metadata")

    if 'sfdc_api' not in st.session_state:
        st.session_state.sfdc_api = None
    
    if 'apex_classes' not in st.session_state:
        st.session_state.apex_classes = None
        
    sidebar_menu()

    st.write(st.session_state.sfdc_api)
    st.write(st.session_state.apex_classes)

def get_apex_classes():
    try:
        st.session_state.apex_classes = tooling_class_query()
    except Exception as e:
        st.error(e)

def get_test_classes():
    return tooling_test_suite_query()

def sidebar_menu():
    if st.session_state.sfdc_api == None:
        show_login()
    else:
        with st.sidebar:
            if st.button('Logout'):
                sfdc_logout()

def show_login():

    with st.sidebar:
        params = {}
        params['domain'] = st.text_input('Add endpoint',placeholder="your_domain")
        params["client_id"] = st.text_input('Add Client Id')
        params["client_secret"] = st.text_input('Add Client Secret')
           
        if not params['domain'] or not params["client_id"] or not params["client_secret"]:
            st.error("All fields are required!")
        elif st.button('Login'):
            sfdc_login(params=params)
            get_apex_classes()

main()


