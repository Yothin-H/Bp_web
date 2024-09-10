

import streamlit as st
import pandas as pd
import base64
import io
from PIL import Image
import subprocess


# Streamlit app
st.title("VCFtool Runner")
#outputcol='out_final_col.csv'
tocol = "csvtool transpose out_final.csv"

# Text input for VCFtools command
command = subprocess.call(tocol, shell=True)


if st.button("Run Command"):
    with st.spinner("Running command..."):
        command = subprocess.call(tocol, shell=True)
        df=pd.read_csv(command)
        st.write(df)
        
else:
    pass
