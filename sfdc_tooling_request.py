import streamlit as st

TOOLING_QUERY = '/services/data/v62.0/tooling/query'
APEX_CLASSES_QUERY = "SELECT Name,Id FROM ApexClass WHERE NOT (Name LIKE '%test%')"
TEST_CLASSES_QUERY = "SELECT id, ApexClassOrTrigger.name, ApexTestClassId, TestMethodName, ApexTestClass.name from ApexCodeCoverage WHERE ApexClassOrTrigger.name IN"

api = st.session_state.sfdc_api

@staticmethod
def tooling_class_query():     
    return api.do_get(TOOLING_QUERY,APEX_CLASSES_QUERY)

@staticmethod
def tooling_test_suite_query():     
    return api.do_get(TOOLING_QUERY,TEST_CLASSES_QUERY)

