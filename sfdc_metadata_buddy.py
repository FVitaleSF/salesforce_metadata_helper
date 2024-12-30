import streamlit as st
from sfdc_login import *
from sfdc_tooling_response import *
import pandas as pd

def main():
    
    tab_icon = "icons\heart-svgrepo-com.svg"
    st.set_page_config(layout="wide",page_title="SFDC Buddy",page_icon = tab_icon)
    init()       
    sidebar_menu()

    if st.session_state.sfdc_api == None:
        show_login()

    if st.session_state.unit_tests != None:
        main_screen_test_exec()

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
        with st.sidebar:
                if st.button('Logout'):
                    sfdc_logout()
                if st.session_state.apex_classes != None:
                    class_selection_menu()

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
    selected_classes = st.multiselect('Choose Classes',options = list(st.session_state.apex_classes))
    selected_ids = [st.session_state.apex_classes[name] for name in selected_classes]
    if selected_ids:  
        st.session_state.unit_tests = get_test_class_properties(st.session_state.sfdc_api,selected_ids)       

def tests_selection_menu():
    df = pd.DataFrame(st.session_state.unit_tests)
    st.title('Classes Unit Tests')
    all_unit_tests = st.dataframe(df.set_index("MetadataComponentName"), selection_mode=["multi-row", "multi-column"],on_select="rerun",use_container_width=True)
    row_select = all_unit_tests.selection.rows
    full_select = df.iloc[row_select]
    st.title('Selected Unit Tests')
    st.dataframe(full_select.set_index("MetadataComponentName"))
    return full_select

def main_screen_test_exec():

    full_select = tests_selection_menu()
    if st.button('Run Tests'):
            try:                 
                api = st.session_state.sfdc_api
                st.write(tooling_execute_test_asynch(api,full_select))
            except Exception as e:
                 st.error(e)
    if st.button('Refresh'):
            st.session_state.unit_tests = None
            st.rerun()


def init():
    if 'sfdc_api' not in st.session_state:
        st.session_state.sfdc_api = None
    
    if 'apex_classes' not in st.session_state:
        st.session_state.apex_classes = None
    
    if 'unit_tests' not in st.session_state:
        st.session_state.unit_tests = None

    if 'test_list' not in st.session_state:
        st.session_state.test_list = None

    if 'icons' not in st.session_state:
        st.session_state.icons = {
        "Close":"icons\close-svgrepo-com.svg",
        "Search":"icons\search-svgrepo-com.svg",
        "Refresh":"icons\refresh-svgrepo-com.svg",
        "Success":"icons\selection-on-svgrepo-com.svg",
        "Run":"icons\play-svgrepo-com.svg"
        }

if __name__ == "__main__":
    main()


