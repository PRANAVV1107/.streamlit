import streamlit as st
import datetime
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from streamlit_datalist import stDatalist
from datetime import datetime
from streamlit_js_eval import streamlit_js_eval
from streamlit_autorefresh import st_autorefresh

# Establish the Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)
e_data = conn.read(worksheet="Sheet1", use_cols=list(range(9)), ttl=5)

# List for options
dd = ["select"] + list(range(1, 11))
dd.append('other')

# List of field names
fields = ['Chipping Machine', 'Roller', 'Mixer', 'Lifting Machine', 'Other Machines']

timestamp = datetime.now()

with st.form(key="machinery", clear_on_submit=True):

    submit_button = st.form_submit_button(label="Submit")
    st.title("Machinery Details")
    supervisor_name = st.text_input(label="Supervisor Name*")
    project_name = st.text_input(label="Project Name*")
    field_values = []
    for field_name in fields:
        field_value = st.text_input(f"Enter {field_name}: ")
        if field_value == 'select':
            st.warning(f"Please select a value for {field_name}")
            st.stop()
        elif field_value == 'other':
            other_value = st.text_input(f"Enter details for {field_name}: ")
            if not other_value:
                st.warning(f"Please enter details for {field_name}")
                st.stop()
            field_values.append(other_value)
        else:
            field_values.append(field_value)
    #return field_values

    if submit_button:
        if not project_name or not supervisor_name or not field_values:
            st.warning("Please submit all mandatory fields")
            st.stop()
        else:
            st.write("Submitted Values:")
            st.write("Project/Site Name:", project_name)
            st.write("Supervisor Name:", supervisor_name)
            st.write("timestamp:" , pd.Timestamp.now()) 
            for field_name, field_value in zip(fields, field_values):
                st.write(f"{field_name}: {field_value}")

            data = pd.DataFrame([field_values], columns=fields)
            data['Project Name'] = project_name
            data['Supervisor Name'] = supervisor_name
            data['timestamp'] = timestamp
            df = pd.concat([data, e_data], ignore_index=True)
            st.write("Final DataFrame:", df)

            conn.update(worksheet="Sheet1", data = df)
            
            st.success("submitted!")
            time.sleep(3)
            st.rerun()
            streamlit_js_eval(js_expressions="parent.window.location.reload()")
            st_autorefresh(interval=1, limit=1, key="fizzbuzzcounter")
            
            
