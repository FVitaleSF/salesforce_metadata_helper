import streamlit as st

TOOLING_API_QUERY= '/services/data/v62.0/tooling/query'
TOOLING_API_ASYNCH_TEST = '/services/data/v62.0/tooling/runTestsAsynchronous'
APEX_CLASSES_QUERY = "SELECT Name,Id FROM ApexClass WHERE NOT (Name LIKE '%test%')"
TEST_CLASSES_QUERY = "SELECT MetadataComponentId, MetadataComponentName FROM MetadataComponentDependency WHERE RefMetadataComponentId IN "


def tooling_class_query(api):
    return api.do_get(TOOLING_API_QUERY,APEX_CLASSES_QUERY)


def tooling_test_suite_query(api,selected_classes):  
    query = test_class_query_builder(selected_classes)
    return api.do_get(TOOLING_API_QUERY,query)

def tooling_execute_test_asynch(api,full_select):
    test_batch = test_json_builder(full_select)
    return api.do_post(TOOLING_API_ASYNCH_TEST,test_batch)

def test_class_query_builder(selected_classes):
    formatted_classes = ",".join([f"'{cls}'" for cls in selected_classes])
    query = f"{TEST_CLASSES_QUERY}"+f" ({formatted_classes})"
    return query  

def test_json_builder(full_select):
    
    column_values = full_select['MetadataComponentName'].tolist()
    formatted_selection = ",".join([f"{cls}" for cls in column_values])
    test_batch = {
            "classNames": formatted_selection
        }
    return test_batch

