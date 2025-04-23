import streamlit as st
import urllib.parse
import requests

@st.cache_data
def query_pubchem_api(compound_name):
    # make a GET HTTP request to the PubChem API
    urlencode_compound_name = urllib.parse.quote(compound_name)
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{urlencode_compound_name}/property/MolecularFormula,Title/JSON"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
        return data["PropertyTable"]["Properties"][0] if "PropertyTable" in data else None
    else:
        st.error(f"Error fetching data for {compound_name}: {response.status_code}")
        return None

def add_compound(compound_name):
    compound_data = query_pubchem_api(compound_name)

    print(compound_data) # debugging
    
    if compound_data:
        st.session_state.compounds.append(compound_data)
        st.success(f"Compound '{compound_name}' added!")
    else:
        st.error(f"Failed to fetch data for {compound_name}")
    
def analyze():
    # Placeholder for analysis logic
    st.success("Analysis complete!")
    analyze_results = {
        "toxicity": "Low",
        "atom_economy": "High",
    }
    return analyze_results

with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("# Compound list")

        if "compounds" not in st.session_state:
            st.session_state.compounds = []
            st.write("No compounds found. Please add some compounds.")
        else:    
            for compound in st.session_state.compounds:
                st.write(compound.get("MolecularFormula"))

        st.text_input("Enter compound name", key="compound_name")
        if st.button("Add Compound"):
            compound_name = st.session_state.compound_name
            add_compound(compound_name)
            st.rerun()
    with col2:
        st.write('# solvants')
        if st.button("Add Solvant"):
            None
        st.write('# catalyzers')
        if st.button("Add catalyzer"):
            None        
       


    with col3:
        st.write('# Conditions') 
        temp = st.slider("Temperature (°C)", 0, 300, 25)
        pressure = st.slider("Pressure (bar)", 0, 50, 1)
        if (st.button("Run Analysis")):
            result = analyze()
            st.session_state.result = result
            st.rerun()
 
with st.container():
    st.write("# Analysis results")
    result = st.session_state.get("result")
    if result:
        st.write(f"Toxicity: {result['toxicity']}")
        st.write(f"Atom Economy: {result['atom_economy']}")
    else:
        st.write("No analysis results available.")
