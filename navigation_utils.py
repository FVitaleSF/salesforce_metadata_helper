import streamlit as st
import pandas as pd
from sfdc_login import *
from sfdc_tooling_response import *

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

@st.dialog('Login')
def show_login():

        params = {}
        params['domain'] = st.text_input('Add endpoint',placeholder="your_domain")
        params["client_id"] = st.text_input('Add Client Id')
        params["client_secret"] = st.text_input('Add Client Secret')
           
        if not params['domain'] or not params["client_id"] or not params["client_secret"]:
            st.error("All fields are required!")
        elif st.button('Login'):
            sfdc_login(params=params)
            get_apex_classes()
            st.rerun()

def class_selection_menu():
    selected_classes = st.multiselect('Choose Classes',options = st.session_state.apex_classes)
    if selected_classes:
        st.session_state.unit_tests = get_test_class_properties(st.session_state.sfdc_api,selected_classes)       

def tests_selection_menu():
    df = pd.DataFrame(st.session_state.unit_tests)
    st.title('Classes Unit Tests')
    all_unit_tests = st.dataframe(df.set_index("MetadataComponentName"), selection_mode=["multi-row", "multi-column"],on_select="rerun",use_container_width=True)
    row_select = all_unit_tests.selection.rows
    full_select = df.iloc[row_select]
    st.title('Selected Unit Tests')
    st.dataframe(full_select.set_index("MetadataComponentName"))
    return full_select
