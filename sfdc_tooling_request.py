import streamlit as st

TOOLING_API= '/services/data/v62.0/tooling/query'
APEX_CLASSES_QUERY = "SELECT Name,Id FROM ApexClass WHERE NOT (Name LIKE '%test%')"
TEST_CLASSES_QUERY = "SELECT id, ApexClassOrTrigger.name, ApexTestClassId, TestMethodName, ApexTestClass.name from ApexCodeCoverage WHERE ApexClassOrTrigger.name IN"

def test_class_query_builder(selected_classes):
    formatted_classes = ",".join([f"'{cls}'" for cls in selected_classes])
    query = f"{TEST_CLASSES_QUERY}"+f" ({formatted_classes})"
    return query

def tooling_class_query(api):
    return api.do_get(TOOLING_API,APEX_CLASSES_QUERY)


def tooling_test_suite_query(api,selected_classes):
    
    query = test_class_query_builder(selected_classes)
    return api.do_get(TOOLING_API,query)

