import streamlit as st
from sfdc_tooling_request import *


def get_class_properties(api):
    parsed_result = tooling_class_query(api)
    classes = {}
    for i in parsed_result['records']:
        classes[(i['Name'])] = i['Id']
    return classes

def get_test_class_properties(api,selected_classes):
    parsed_result = tooling_test_suite_query(api,selected_classes)
    apex_test_classes = {}
    for p in parsed_result['records']:
            apex_test_class_id = p.get('ApexTestClassId')
            apex_test_class_name = p.get('ApexTestClass', {}).get('Name')
            
            apex_test_classes[apex_test_class_id] = apex_test_class_name
    return apex_test_classes