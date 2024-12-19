import streamlit as st
from Salesforce_REST import Salesforce_REST


def sfdc_login(params):
    try:
        st.session_state.sfdc_api = Salesforce_REST(params)
        st.success('You succesfully logged in!')
    except Exception as e:
        st.error(f"There was an issue connecting to Salesforce: {e}")

def sfdc_logout():
    sfdc_api = st.session_state.sfdc_api
    sfdc_api.revoke_auth()
    st.session_state.sfdc_api = None
    st.info('You succesfully logged out!')



