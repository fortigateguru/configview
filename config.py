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

# Streamlit app
st.title('IP and MAC Address Pattern Identifier and Visualizer')

# Text area for input
text_input = st.text_area("Enter your text here:")

# Radio buttons to select the type of address
address_type = st.radio("Select the type of address to extract and visualize:", ('IP Address', 'MAC Address'))

if text_input:
    if address_type == 'IP Address':
        # Extract IP addresses
        addresses = extract_ip_addresses(text_input)
    elif address_type == 'MAC Address':
        # Extract MAC addresses
        addresses = extract_mac_addresses(text_input)

    if addresses:
        # Create a DataFrame for counting addresses
        df = pd.DataFrame(addresses, columns=['Address'])
        address_counts = df['Address'].value_counts().reset_index()
        address_counts.columns = ['Address', 'Count']
        
        # Display the DataFrame
        st.write(f"Extracted {address_type}s and their counts:")
        st.dataframe(address_counts)
        
        # Plotting
        fig, ax = plt.subplots()
        address_counts.plot(kind='bar', x='Address', y='Count', ax=ax, legend=False)
        ax.set_ylabel("Count")
        ax.set_title(f"{address_type} Distribution")
        
        # Show the plot in Streamlit
        st.pyplot(fig)
    else:
        st.write(f"No {address_type.lower()}s found in the input text.")
else:
    st.write("Please enter text to analyze.")
