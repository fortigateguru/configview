import streamlit as st
import re
import pandas as pd
import matplotlib.pyplot as plt

# Function to extract IP addresses using regex
def extract_ip_addresses(text):
    ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    return ip_pattern.findall(text)

# Streamlit app
st.title('IP Address Pattern Identifier and Visualizer')

# Text area for input
text_input = st.text_area("Enter your text here:")

if text_input:
    # Extract IP addresses
    ip_addresses = extract_ip_addresses(text_input)
    
    if ip_addresses:
        # Create a DataFrame for counting IP addresses
        df = pd.DataFrame(ip_addresses, columns=['IP Address'])
        ip_counts = df['IP Address'].value_counts().reset_index()
        ip_counts.columns = ['IP Address', 'Count']
        
        # Display the DataFrame
        st.write("Extracted IP Addresses and their counts:")
        st.dataframe(ip_counts)
        
        # Plotting
        fig, ax = plt.subplots()
        ip_counts.plot(kind='bar', x='IP Address', y='Count', ax=ax, legend=False)
        ax.set_ylabel("Count")
        ax.set_title("IP Address Distribution")
        
        # Show the plot in Streamlit
        st.pyplot(fig)
    else:
        st.write("No IP addresses found in the input text.")
else:
    st.write("Please enter text to analyze.")
