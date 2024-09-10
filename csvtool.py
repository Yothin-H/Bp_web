

import streamlit as st
import pandas as pd
import base64
import io
from PIL import Image
import subprocess

def run_vcftools_command(command):
    try:
        # Run the vcftools command and capture the output
        result = subprocess.run(
            command, shell=True, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return result.stdout, result.stderr
    except Exception as e:
        return "", str(e)

# Streamlit app
st.title("VCFtool Runner")
outputcol='out_final_col.csv'
tocol = "csvtool transpose "+'out_final.csv'+" > "+outputcol

# Text input for VCFtools command
command = st.text_input("Enter VCFtools command:", tocol)

if st.button("Run Command"):
    with st.spinner("Running command..."):
        stdout, stderr = run_vcftools_command(command)
        df=pd.read_csv(outputcol)
        st.write(df)
        
        if stdout:
            st.subheader("Standard Output")
            st.text(stdout)
            
            
        
        if stderr:
            st.subheader("Standard Error")
            st.text(stderr)


