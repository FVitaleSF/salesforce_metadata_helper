import streamlit as st
import pandas as pd
import json
from sfdc_tooling_request import *


def get_class_properties(api):
    parsed_result = tooling_class_query(api)
    classes = {}
    for i in parsed_result['records']:
        classes[(i['Name'])] = i['Id']
    return classes

def get_test_class_properties(api,selected_classes):
    parsed_result = tooling_test_suite_query(api,selected_classes)
    return parse_code_coverage_result(parsed_result)
    

def parse_code_coverage_result(parsed_result):
  
    records = parsed_result["records"]

    parsed_data = []
    for record in records:
        parsed_data.append({
            "MetadataComponentId": record["MetadataComponentId"],
            "MetadataComponentName": record["MetadataComponentName"]
        })

    return parsed_data
    

     