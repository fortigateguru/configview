import streamlit as st
import re
import pandas as pd
import matplotlib.pyplot as plt

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

# Streamlit app
st.title('Network Configuration Pattern Identifier and Visualizer')

# Text area for input
text_input = st.text_area("Enter your configuration text here:")

# Radio buttons to select the type of information to extract
info_type = st.radio(
    "Select the type of information to extract and visualize:",
    ('IP Address', 'MAC Address', 'Hostname', 'Interface Status', 'VLAN')
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
    else:
        st.write(f"No {info_type.lower()}s found in the input text.")
else:
    st.write("Please enter text to analyze.")
