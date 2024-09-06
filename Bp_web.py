

import streamlit as st
import pandas as pd
import base64
import io
from PIL import Image
from datetime import datetime

#---------------------------------#

st.set_page_config(page_title='The Drug Resistant Database of *Burkholderia pseudomallei*',layout='wide')

image = Image.open('bp_logo2.jpg')
st.image(image, use_column_width=True)
#st.image(image, width=900)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #DFDFDF; 
    }
    .stMarkdown h3 {
        color: black !important;  /* Subheader text color set to black */
    }
    .stMarkdown p {
        color: black !important;  /* Paragraph text color follows the theme */
    }
    .stMarkdown h1 {
        color: black !important;  /* Subheader text color set to black */
    }
    .stAlert p {
        color: #3989E2 !important;  /* st.info() text color set to black */
    }
    </style>
    """,
    unsafe_allow_html=True
)

#---------------------------------#
# Sidebar - Collects user input features into dataframe
with st.sidebar.header('1. Upload your VCF data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input VCF file", type=["csv",'vcf'])

# Sidebar - Specify parameter settings
with st.sidebar.header('2. Set Parameters'):
    quality_filter = st.sidebar.slider('Quality score of variant (Q>20 is recommended)', 0, 100, 20, 5)
    another_param = st.sidebar.text_input('Enter quality score if you want > 100:')

#---------------------------------#
# Model building
def predicted(test):
    data=pd.read_csv('/archive2/k_orawee/Taow/streamlit/gene_database.csv')
    # Convert columns to string to ensure consistent data types
    test['#CHROM'] = test['#CHROM'].astype(str)
    data['Sequence_Ref'] = data['Sequence_Ref'].astype(str)

    test['POS'] = test['POS'].astype(str)
    data['Chromosome position'] = data['Chromosome position'].astype(str)

    # Adding an index column to `data` for reference
    data['index'] = data.index

    # Merging the two DataFrames after ensuring the data types are consistent
    merged_df = test.merge(
        data,
        left_on=['#CHROM', 'POS','REF','ALT'],
        right_on=['Sequence_Ref', 'Chromosome position','Reference Nucleotide','Alternative Nucleotide'],
        how='inner'
    )

    aa=int(quality_filter)
    aa2=None
    '''
    try:
    # Check if another_param is a digit and less than or equal to the max of 'QUAL'
        if another_param.strip().isdigit() and (int(another_param) <= int(merged_df['QUAL'].max())):
            aa2 = int(another_param)
        else:
            # If another_param is not valid, show a message in the sidebar
            st.sidebar.info(f"Maximum quality of your data is: {int(merged_df['QUAL'].max())}")
    except Exception as e:
        # Catch any other exceptions and display a message
        st.sidebar.error("An error occurred while processing the quality filter.")
    '''
    if aa2 is not None:
        merged_df2=merged_df.query('QUAL>=@aa2')
    else :
        merged_df2=merged_df.query('QUAL>=@aa')
        
    mm=merged_df2[['Gene','POS','REF','ALT','QUAL','Positive Ref Codon','Positive Alt Codon','Nucleotide change','Amino acid change','Drug','AST','Reference']]
    
    st.subheader('Summary of drug resistance prediction')

    druglist = ['Ceftazidime', 'Meropenem','Imipenem','Co-trimoxazole','Amoxycillin/Clavulanic acid']
    interpretlist = ['Susceptible', 'Susceptible','Susceptible', 'Susceptible','Susceptible']
    drugchoice=['First-line','First-line','Second-line','Second-line','Second-line']
    fstdrug = pd.DataFrame({
        'Drug': druglist,
        'Interpretation': interpretlist,
        'Drug of Choice' : drugchoice
    })
    drug_index = {drug: idx for idx, drug in enumerate(druglist)}

    def update_interpretation(drug, ast, current_value):
        if ast == 'Resistance':
            return 'Resistance'
        elif ast == 'Intermediate' and current_value != 'Resistance':
            return 'Intermediate'
        return current_value

    for i, row in mm.iterrows():
        drug = row['Drug']
        ast = row['AST']
        if drug in drug_index:
            index = drug_index[drug]
            fstdrug.at[index, 'Interpretation'] = update_interpretation(drug, ast, fstdrug.at[index, 'Interpretation'])
    fstdrug.reset_index(drop=True)
    fstdrug.index = fstdrug.index + 1
    
    #fstdrug = fstdrug.style.applymap(lambda x: f"background-color: {'green' if x=='Susceptible' else 'red'}", subset='Interpretation')
    
    def bold_text(value):
        return 'font-weight: bold'

    def highlight_cells(value):
        if value == 'Susceptible':
            return 'background-color: green; color: white'
        elif value == 'Resistance':
            return 'background-color: red; color: white'
        else:
            return 'background-color: blue; color: white'

    # Apply bold text styling to the 'Drug' column
    styled_fstdrug = fstdrug.style.applymap(bold_text, subset=['Drug'])

    # Apply conditional formatting to the 'Interpretation' column
    styled_fstdrug = styled_fstdrug.applymap(highlight_cells, subset=['Interpretation'])
    st.write(styled_fstdrug)
    styled_fstdrug2=styled_fstdrug.data
    st.markdown(filedownload(styled_fstdrug2,'summary.csv'), unsafe_allow_html=True)


    st.subheader('The first line drugs')
    for i in range(len(mm)):
        matches1 = mm.query('Drug == "Ceftazidime" or Drug == "Meropenem"').reset_index(drop=True)
    
    matches1.index = matches1.index + 1

    st.write(matches1)
    st.markdown(filedownload(matches1,'first_line.csv'), unsafe_allow_html=True)
    
    
    st.subheader('The second line drugs')
    for i in range(len(mm)):
        matches2 = mm.query('Drug == "Imipenem" or Drug == "Co-trimoxazole" or Drug == "Amoxycillin/Clavulanic acid"').reset_index(drop=True)
    matches2.index = matches2.index + 1

    st.write(matches2)
    st.markdown(filedownload(matches2,'second_line.csv'), unsafe_allow_html=True)
    return mm

    

# Download CSV data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download={filename}>Download {filename} File</a>'
    return href

def imagedownload(plt, filename):
    s = io.BytesIO()
    plt.savefig(s, format='pdf', bbox_inches='tight')
    plt.close()
    b64 = base64.b64encode(s.getvalue()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:image/png;base64,{b64}" download={filename}>Download {filename} File</a>'
    return href

#---------------------------------#
st.write("""
# The Drug Resistant Database of *Burkholderia pseudomallei*

This is a tool for genotypic drug resistance prediction developed by **Yothin Hinwan**.

""")


#---------------------------------#
# Main panel

# Displays the dataset
st.subheader('Upload your VCF file')

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file,sep='\t')
    st.markdown('**1.1. Glimpse of dataset**')
    st.write(df.head(5))
    a=predicted(df)
else:
    st.info('Awaiting for VCF file to be uploaded.')
    if st.button('Press to use Example Dataset'):
        df=pd.read_csv('/archive2/k_orawee/Taow/streamlit/example.vcf',sep='\t')

        st.markdown('The in-house dataset is used as the example.')
        st.write(df.head(5))

        a=predicted(df)
