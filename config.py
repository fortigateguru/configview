import streamlit as st
import re
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

# Function to extract IP addresses using regex
def extract_ip_addresses(text):
    ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    return ip_pattern.findall(text)

# Function to extract MAC addresses using regex
def extract_mac_addresses(text):
    mac_pattern = re.compile(r'\b(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})\b')
    return mac_pattern.findall(text)

# Function to extract hostnames using regex
def extract_hostnames(text):
    hostname_pattern = re.compile(r'hostname\s+(\S+)')
    return hostname_pattern.findall(text)

# Function to extract interface statuses using regex
def extract_interfaces(text):
    interface_pattern = re.compile(r'interface\s+(\S+)\n.*?status\s+(\S+)', re.DOTALL)
    return interface_pattern.findall(text)

# Function to extract VLAN information using regex
def extract_vlans(text):
    vlan_pattern = re.compile(r'vlan\s+(\d+)\s+name\s+(\S+)')
    return vlan_pattern.findall(text)

# Function to extract routing table entries using regex
def extract_routes(text):
    route_pattern = re.compile(r'ip route\s+(\S+)\s+(\S+)\s+(\S+)')
    return route_pattern.findall(text)

# Streamlit app
st.title('Advanced Network Configuration Pattern Identifier and Visualizer')

# File uploader for configuration files
uploaded_file = st.file_uploader("Choose a configuration file", type=['txt', 'cfg'])

if uploaded_file:
    # Read the file content
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    text_input = stringio.read()

    # Radio buttons to select the type of information to extract
    info_type = st.radio(
        "Select the type of information to extract and visualize:",
        ('IP Address', 'MAC Address', 'Hostname', 'Interface Status', 'VLAN', 'Routing Table')
    )

    if text_input:
        if info_type == 'IP Address':
            data = extract_ip_addresses(text_input)
        elif info_type == 'MAC Address':
            data = extract_mac_addresses(text_input)
        elif info_type == 'Hostname':
            data = extract_hostnames(text_input)
        elif info_type == 'Interface Status':
            data = extract_interfaces(text_input)
        elif info_type == 'VLAN':
            data = extract_vlans(text_input)
        elif info_type == 'Routing Table':
            data = extract_routes(text_input)

        if data:
            if info_type in ['IP Address', 'MAC Address', 'Hostname']:
                df = pd.DataFrame(data, columns=['Data'])
                counts = df['Data'].value_counts().reset_index()
                counts.columns = ['Data', 'Count']
                st.write(f"Extracted {info_type}s and their counts:")
                st.dataframe(counts)
                fig, ax = plt.subplots()
                counts.plot(kind='bar', x='Data', y='Count', ax=ax, legend=False)
                ax.set_ylabel("Count")
                ax.set_title(f"{info_type} Distribution")
                st.pyplot(fig)
            elif info_type == 'Interface Status':
                df = pd.DataFrame(data, columns=['Interface', 'Status'])
                st.write("Extracted Interface Statuses:")
                st.dataframe(df)
                fig, ax = plt.subplots()
                status_counts = df['Status'].value_counts().reset_index()
                status_counts.columns = ['Status', 'Count']
                status_counts.plot(kind='bar', x='Status', y='Count', ax=ax, legend=False)
                ax.set_ylabel("Count")
                ax.set_title("Interface Status Distribution")
                st.pyplot(fig)
            elif info_type == 'VLAN':
                df = pd.DataFrame(data, columns=['VLAN ID', 'Name'])
                st.write("Extracted VLAN Information:")
                st.dataframe(df)
                fig, ax = plt.subplots()
                vlan_counts = df['VLAN ID'].value_counts().reset_index()
                vlan_counts.columns = ['VLAN ID', 'Count']
                vlan_counts.plot(kind='bar', x='VLAN ID', y='Count', ax=ax, legend=False)
                ax.set_ylabel("Count")
                ax.set_title("VLAN Distribution")
                st.pyplot(fig)
            elif info_type == 'Routing Table':
                df = pd.DataFrame(data, columns=['Destination', 'Gateway', 'Interface'])
                st.write("Extracted Routing Table Entries:")
                st.dataframe(df)
                fig, ax = plt.subplots()
                dest_counts = df['Destination'].value_counts().reset_index()
                dest_counts.columns = ['Destination', 'Count']
                dest_counts.plot(kind='bar', x='Destination', y='Count', ax=ax, legend=False)
                ax.set_ylabel("Count")
                ax.set_title("Routing Table Distribution")
                st.pyplot(fig)
        else:
            st.write(f"No {info_type.lower()}s found in the input text.")
else:
    st.write("Please upload a configuration file to analyze.")
