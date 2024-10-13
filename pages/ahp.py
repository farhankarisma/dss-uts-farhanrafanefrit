import streamlit as st
import pandas as pd
import numpy as np

# Function to calculate the priority index for the criteria or alternatives
def ahp_attributes(ahp_df):
    sum_array = np.array(ahp_df.sum(numeric_only=True))
    cell_by_sum = ahp_df.div(sum_array, axis=1)
    priority_df = pd.DataFrame(cell_by_sum.mean(axis=1), columns=['priority index'])
    return priority_df

# Function to check the consistency ratio
def consistency_ratio(priority_index, ahp_df):
    random_matrix = {1: 0, 2: 0, 3: 0.58, 4: 0.9, 5: 1.12, 6: 1.24, 7: 1.32,
                     8: 1.41, 9: 1.45, 10: 1.49, 11: 1.51, 12: 1.48, 13: 1.56,
                     14: 1.57, 15: 1.59, 16: 1.605, 17: 1.61, 18: 1.615, 19: 1.62, 20: 1.625}

    consistency_df = ahp_df.multiply(priority_index['priority index'].values, axis=1)
    consistency_df['sum_of_col'] = consistency_df.sum(axis=1)
    lambda_max_df = consistency_df['sum_of_col'].div(priority_index['priority index'])
    lambda_max = lambda_max_df.mean()
    consistency_index = (lambda_max - len(ahp_df.index)) / (len(ahp_df.index) - 1)
    consistency_ratio_value = consistency_index / random_matrix[len(ahp_df.index)]
    
    st.write(f'The Consistency Index is: {consistency_index:.3f}')
    st.write(f'The Consistency Ratio is: {consistency_ratio_value:.3f}')
    
    if consistency_ratio_value < 0.1:
        st.success('The model is consistent.')
    else:
        st.warning('The model is not consistent.')
    return consistency_ratio_value

# Streamlit app
st.title('AHP (Analytical Hierarchy Process) Calculator')

# User input for criteria
st.subheader('Step 1: Define Criteria')
num_criteria = st.number_input('Enter the number of criteria:', min_value=1, max_value=20, step=1)

criteria_names = []
for i in range(num_criteria):
    criteria_name = st.text_input(f'Enter name for Criterion {i+1}:')
    criteria_names.append(criteria_name)

# User input for pairwise comparison matrix
st.subheader('Step 2: Pairwise Comparison Matrix for Criteria')
ahp_df = pd.DataFrame(np.ones((num_criteria, num_criteria)), columns=criteria_names, index=criteria_names)

st.write("Fill in the upper triangular matrix (values will be mirrored):")
for i in range(num_criteria):
    for j in range(i + 1, num_criteria):
        ahp_df.iloc[i, j] = st.number_input(f'Comparison: {criteria_names[i]} vs {criteria_names[j]}', min_value=0.1, max_value=10.0, step=0.1)
        ahp_df.iloc[j, i] = 1 / ahp_df.iloc[i, j]

# Calculate priority index and consistency ratio
priority_index_attr = ahp_attributes(ahp_df)
st.subheader('Priority Index for Criteria')
st.write(priority_index_attr)

st.subheader('Consistency Check')
consistency_ratio(priority_index_attr, ahp_df)

# User input for alternatives and attributes comparison
st.subheader('Step 3: Define Alternatives and Pairwise Comparison for Each Attribute')
num_alternatives = st.number_input('Enter the number of alternatives:', min_value=1, max_value=20, step=1)

alternative_names = []
for i in range(num_alternatives):
    alternative_name = st.text_input(f'Enter name for Alternative {i+1}:')
    alternative_names.append(alternative_name)

# Initialize DataFrames for each attribute comparison
attribute_priority_dfs = {}
for criterion in criteria_names:
    st.subheader(f'Pairwise Comparison for {criterion}')
    attribute_df = pd.DataFrame(np.ones((num_alternatives, num_alternatives)), columns=alternative_names, index=alternative_names)
    
    st.write(f"Fill in the upper triangular matrix for {criterion} (values will be mirrored):")
    for i in range(num_alternatives):
        for j in range(i + 1, num_alternatives):
            attribute_df.iloc[i, j] = st.number_input(f'{criterion}: {alternative_names[i]} vs {alternative_names[j]}', min_value=0.1, max_value=10.0, step=0.1)
            attribute_df.iloc[j, i] = 1 / attribute_df.iloc[i, j]
    
    # Calculate priority index for each attribute
    attribute_priority_df = ahp_attributes(attribute_df)
    attribute_priority_dfs[criterion] = attribute_priority_df
    st.write(f'Priority Index for {criterion}')
    st.write(attribute_priority_df)

# Combine results
st.subheader('Step 4: Final Scores for Alternatives')
suppl_df = pd.concat(attribute_priority_dfs, axis=1)
suppl_norm_df = suppl_df.multiply(priority_index_attr['priority index'].values, axis=1)
suppl_norm_df['Sum'] = suppl_norm_df.sum(axis=1)

st.write('Final Scores for Alternatives:')
st.write(suppl_norm_df.sort_values(by='Sum', ascending=False))