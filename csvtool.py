import streamlit as st
import pandas as pd
import base64
import io
from PIL import Image
import subprocess
import os  # Importing the missing os module

def run_vcftools_command(command):
    try:
        # Run the vcftools command and capture the output
        result = subprocess.run(
            command, shell=True, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return result.stdout, result.stderr
    except FileNotFoundError:
        return "", "Command not found. Please check if vcftools is installed and in your PATH."
    except Exception as e:
        return "", f"An unexpected error occurred: {str(e)}"

# Streamlit app
st.title("VCFtools Runner")
output_path = st.text_input("Enter output path:", "output.txt")

# Safely construct the output paths
output_col_path = os.path.join(output_path, 'out_final_col.csv')
tocol_command = '$(csvtool transpose out_final.csv)'

# Text input for VCFtools command
command = st.text_input("Enter VCFtools command:", tocol_command)

# Ensure the output path is safe
if not os.path.isabs(output_path):
    output_path = os.path.join(os.getcwd(), output_path)

# Append output redirection to the command
command_with_output = f"{command} --out {output_path}"

if st.button("Run Command"):
    with st.spinner("Running command..."):
        stdout, stderr = run_vcftools_command(command_with_output)
        
        if stdout:
            st.subheader("Standard Output")
            st.text(stdout)
        
        if stderr:
            st.subheader("Standard Error")
            st.text(stderr)

    # Provide the user with a link to download the output file, if applicable
    if os.path.exists(output_path):
        st.subheader("Download Output")
        with open(output_path, "rb") as file:
            st.download_button("Download File", file, file_name=os.path.basename(output_path))
