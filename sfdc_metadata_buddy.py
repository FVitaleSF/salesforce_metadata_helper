import streamlit as st
from sfdc_login import *
from sfdc_tooling_response import *

def main():

    st.set_page_config(layout="wide",page_title="SFDC Metadata")

    if 'sfdc_api' not in st.session_state:
        st.session_state.sfdc_api = None
    
    if 'apex_classes' not in st.session_state:
        st.session_state.apex_classes = None
        
    sidebar_menu()

def get_apex_classes():
    try:
        st.session_state.apex_classes = get_class_properties(st.session_state.sfdc_api)
    except Exception as e:
        st.error(e)

def get_test_classes(selected_classes):
    api = st.session_state.sfdc_api
    try:
        return tooling_test_suite_query(api,selected_classes)
    except Exception as e:
        st.error(e)

def sidebar_menu():
    if st.session_state.sfdc_api == None:
        show_login()
    else:
        with st.sidebar:
            if st.button('Logout'):
                sfdc_logout()
            if st.session_state.apex_classes != None:
                class_selection_menu()

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

def class_selection_menu():
    selected_classes = st.multiselect('Choose Classes',options = st.session_state.apex_classes)
    if selected_classes:
        selected_tests = get_test_class_properties(st.session_state.sfdc_api,selected_classes)
        multi_select_unit_tests(selected_tests)
        if st.button('Run Tests'):
            st.info('Placeholder for test run')

def multi_select_unit_tests(selected_tests):
    return st.multiselect(
                'Test Classes', 
                options=list(selected_tests.keys()),
                format_func=lambda key: selected_tests[key]
            )

main()


