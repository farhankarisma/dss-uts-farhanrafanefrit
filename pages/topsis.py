import streamlit as st
import pandas as pd
import numpy as np

# Function to normalize the decision matrix
def normalize_matrix(matrix):
    return matrix / np.sqrt((matrix**2).sum(axis=0))

# Function to calculate the distance to the ideal positive and negative solutions
def calculate_distance(matrix, ideal_solution):
    return np.sqrt(((matrix - ideal_solution) ** 2).sum(axis=1))

# Main TOPSIS function
def topsis(alternative_data, weights, is_benefit_criteria):
    # 1. Normalize the decision matrix
    normalized_matrix = normalize_matrix(alternative_data.iloc[:, 1:].astype(float))
    st.subheader('Normalized Matrix')
    st.write(normalized_matrix)

    # 2. Apply weights to the normalized matrix
    weighted_matrix = normalized_matrix * weights
    st.subheader('Weighted Matrix')
    st.write(weighted_matrix)

    # 3. Determine ideal positive and negative solutions
    ideal_positive = np.zeros(weighted_matrix.shape[1])
    ideal_negative = np.zeros(weighted_matrix.shape[1])

    for i in range(weighted_matrix.shape[1]):
        if is_benefit_criteria[i]:
            ideal_positive[i] = weighted_matrix.iloc[:, i].max()
            ideal_negative[i] = weighted_matrix.iloc[:, i].min()
        else:
            ideal_positive[i] = weighted_matrix.iloc[:, i].min()
            ideal_negative[i] = weighted_matrix.iloc[:, i].max()

    st.subheader('Ideal Positive and Negative Solutions')
    ideal_df = pd.DataFrame({
        'Criterion': alternative_data.columns[1:],  
        'Ideal Positive': ideal_positive,
        'Ideal Negative': ideal_negative
    })
    st.write(ideal_df)

    # 4. Calculate the distance to the ideal positive and negative solutions
    distance_to_positive = calculate_distance(weighted_matrix, ideal_positive)
    distance_to_negative = calculate_distance(weighted_matrix, ideal_negative)

    st.subheader('Distance to Ideal Positive and Negative Solutions')
    distance_df = pd.DataFrame({
        'Alternative': alternative_data['index'],
        'Distance to Ideal Positive': distance_to_positive,
        'Distance to Ideal Negative': distance_to_negative
    })
    st.write(distance_df)

    # 5. Calculate relative closeness to the ideal positive solution
    relative_closeness = distance_to_negative / (distance_to_positive + distance_to_negative)

    # Handle potential NaN values in relative_closeness (e.g., if both distances are zero)
    relative_closeness = np.nan_to_num(relative_closeness, nan=0.0)

    # Add results to the dataframe
    alternative_data['Closeness Coefficient'] = relative_closeness

    # Ensure 'Closeness Coefficient' has no NaN values before ranking
    if alternative_data['Closeness Coefficient'].isnull().any():
        st.error("Calculation resulted in NaN values. Please check input data for accuracy.")
    else:
        alternative_data['Ranking'] = alternative_data['Closeness Coefficient'].rank(ascending=False, method='min').astype(int)
        alternative_data['Conclusion'] = ''
        for index, row in alternative_data.iterrows():
            if row['Ranking'] == 1:
                alternative_data.at[index, 'Conclusion'] = 'Selected alternative'
            else:
                alternative_data.at[index, 'Conclusion'] = f'Not selected, rank {row["Ranking"]}'
    
    return alternative_data

# Streamlit app setup
st.title('📊 TOPSIS Calculator')

# Sidebar inputs
st.sidebar.header("TOPSIS Input Data")
num_alternatives = st.sidebar.number_input('Enter the number of alternatives', min_value=2, step=1)
num_criteria = st.sidebar.number_input('Enter the number of criteria', min_value=2, step=1)

# Alternative names
alternatives = [st.sidebar.text_input(f'Alternative {i+1} Name', f'Alternative {i+1}') for i in range(num_alternatives)]

# Criteria names
criteria = [st.sidebar.text_input(f'Criterion {j+1} Name', f'C{j+1}') for j in range(num_criteria)]

# Weights and criteria type using selectbox
weights = [st.sidebar.number_input(f'Weight for {criteria[j]}', min_value=0.0, max_value=1.0, step=0.01) for j in range(num_criteria)]
is_benefit_criteria = [st.sidebar.selectbox(f'{criteria[j]} is:', ['Benefit', 'Cost']) == 'Benefit' for j in range(num_criteria)]

# Scores input
alternative_data = pd.DataFrame(index=alternatives, columns=criteria)
for i in range(num_alternatives):
    for j in range(num_criteria):
        alternative_data.loc[alternatives[i], criteria[j]] = st.sidebar.number_input(f'Score of {alternatives[i]} for {criteria[j]}', min_value=0.0, step=0.1)

# Run TOPSIS
if st.sidebar.button('Run TOPSIS'):
    result = topsis(alternative_data.reset_index(), np.array(weights), is_benefit_criteria)
    st.subheader('TOPSIS Ranking Results')
    st.write(result[['index', 'Closeness Coefficient', 'Ranking', 'Conclusion']].rename(columns={'index': 'Alternative'}))
