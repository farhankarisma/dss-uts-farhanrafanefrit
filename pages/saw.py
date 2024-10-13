import streamlit as st
import numpy as np
import pandas as pd

# Function to normalize decision matrix for SAW
def normalize_matrix(decision_matrix, criteria_types):
    normalized_matrix = np.copy(decision_matrix)
    for i in range(decision_matrix.shape[1]):
        if criteria_types[i] == 'benefit':
            normalized_matrix[:, i] = decision_matrix[:, i] / decision_matrix[:, i].max()
        elif criteria_types[i] == 'cost':
            normalized_matrix[:, i] = decision_matrix[:, i].min() / decision_matrix[:, i]
    return normalized_matrix

# Function to calculate SAW scores
def saw_method(decision_matrix, weights, criteria_types):
    normalized_matrix = normalize_matrix(decision_matrix, criteria_types)
    final_scores = np.dot(normalized_matrix, weights)
    return normalized_matrix, final_scores

# Streamlit UI
st.set_page_config(page_title="Simple Additive Weighting (SAW) Calculator", page_icon="📊", layout="centered")
st.title("📊 Simple Additive Weighting (SAW) Calculator")
st.write("This tool helps you calculate the final scores of alternatives using the **Simple Additive Weighting (SAW)** method for **Decision Support System (DSS)** problems.")

# Input number of alternatives and criteria
st.sidebar.header("Input Data")
num_alternatives = st.sidebar.number_input("Number of Alternatives", min_value=2, value=3)
num_criteria = st.sidebar.number_input("Number of Criteria", min_value=2, value=3)

# Input candidate names
st.sidebar.subheader("Alternative Names")
candidate_names = []
for i in range(num_alternatives):
    candidate_names.append(st.sidebar.text_input(f"Alternative {i+1} Name", f"Alternative {i+1}"))

# Input criteria names and types
st.sidebar.subheader("Criteria")
criteria_names = []
criteria_types = []
for i in range(num_criteria):
    criteria_names.append(st.sidebar.text_input(f"Criteria {i+1} Name", f"Criteria {i+1}"))
    criteria_types.append(st.sidebar.selectbox(f"Type of Criteria {i+1}", ['benefit', 'cost'], key=f"criteria_type_{i}"))

# Input decision matrix
st.sidebar.subheader("Decision Matrix")
decision_matrix = []
for i in range(num_alternatives):
    decision_matrix.append(
        st.sidebar.text_input(f"Enter scores for {candidate_names[i]} (comma-separated)", 
                              value=",".join(["0" for _ in range(num_criteria)]))
    )

# Input weights
weights_input = st.sidebar.text_input("Enter the weights for each criterion (comma-separated)", 
                                      value=",".join(["1" for _ in range(num_criteria)]))

# Convert input data to numpy arrays
decision_matrix = np.array([list(map(float, row.split(','))) for row in decision_matrix])
weights = np.array(list(map(float, weights_input.split(','))))
criteria_types = np.array(criteria_types)

# Main content area
st.header("Simple Additive Weighting (SAW) Calculation Results")

if st.button("🔍 Calculate SAW"):
    # Display the initial decision matrix
    st.subheader("Step 1: Initial Decision Matrix")
    decision_df = pd.DataFrame(decision_matrix, columns=criteria_names, index=candidate_names)
    st.write(decision_df)

    # Perform SAW calculation
    normalized_matrix, final_scores = saw_method(decision_matrix, weights, criteria_types)

    # Display the normalized matrix
    st.subheader("Step 2: Normalized Decision Matrix")
    normalized_df = pd.DataFrame(normalized_matrix, columns=criteria_names, index=candidate_names)
    st.write(normalized_df)

    # Display the weights applied to the normalized matrix
    st.subheader("Step 3: Weighted Normalized Matrix")
    weighted_normalized_matrix = normalized_matrix * weights
    weighted_normalized_df = pd.DataFrame(weighted_normalized_matrix, columns=criteria_names, index=candidate_names)
    st.write(weighted_normalized_df)

    # Create a dataframe for final results
    result_df = pd.DataFrame({
        'Alternative': candidate_names,
        'Final Score': final_scores
    })

    # Sort the results by Final Score in descending order (highest rank first)
    result_df = result_df.sort_values(by='Final Score', ascending=False).reset_index(drop=True)

    # Add a new column 'Rank' starting from 1
    result_df['Rank'] = result_df.index + 1

    # Display final scores and ranking
    st.subheader("Step 4: Final Scores and Rankings")
    st.write(result_df)

    # Plotting the scores
    st.subheader("Graphical Representation of Final Scores")
    st.bar_chart(result_df[['Final Score']].set_index(result_df['Alternative']))

    # Highlight the best alternative
    best_alternative = result_df.iloc[0]['Alternative']
    st.subheader(f"🏆 Best Alternative: **{best_alternative}**")
    st.write("The alternative with the highest score is selected based on the calculated results.")

else:
    st.info("Please enter the decision matrix, weights, and criteria types, then click **Calculate SAW** to see the results.")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("Created with ❤️ using Streamlit.", unsafe_allow_html=True)
