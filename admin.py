import streamlit as st
from pymongo import MongoClient
import pandas as pd
import base64
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

load_dotenv()

mongo_url=os.getenv("Mongo_url")
# MongoDB connection
client = MongoClient(f"mongodb+srv://{mongo_url}")
db = client["CampusGuard"]
collection = db["neuralgo"]

data = {
    'Timestamp': [],
    'Customer Name': [],
    'Call Rating': [],
    'Feedback Category': [],
    'Feedback Details': [],
    'Agent ID': [],
    'Complaint ID': []
}

# Main display logic
st.title("Customer Feedback Retrieval")
feedback_categories = ["Cancellation", "Flight Reschedule", "Flight Refund Related", "Flight Delay Complaint", "Staff Behavior Complaint", "Miscellaneous", "All"]
filter_category = st.selectbox("**Filter by Feedback Category**", feedback_categories, index=len(feedback_categories) - 1)

if filter_category != "All":
    feedbacks = collection.find({"feedback_category": filter_category})
else:
    feedbacks = collection.find({})

for feedback in feedbacks:
    st.subheader(f"Feedback Category: {feedback['feedback_category']}")
    st.write(f"Customer Name: {feedback['customer_name']}")
    st.write(f"Call Rating: {feedback['call_rating']}")
    st.write(f"Feedback Details: {feedback['feedback_details']}")
    st.write(f"Agent ID: {feedback['agent_id']}")
    st.write(f"Complaint ID: {feedback['complaint_id']}")
    st.write(f"Timestamp: {feedback['timestamp']}")

    st.write("-" * 20)

    data['Timestamp'].append(feedback['timestamp'])
    data['Customer Name'].append(feedback['customer_name'])
    data['Call Rating'].append(feedback['call_rating'])
    data['Feedback Category'].append(feedback['feedback_category'])
    data['Feedback Details'].append(feedback['feedback_details'])
    data['Agent ID'].append(feedback['agent_id'])
    data['Complaint ID'].append(feedback['complaint_id'])

df = pd.DataFrame(data)

# Save to CSV
csv_file = "customer_feedback.csv"
df.to_csv(csv_file, index=False)

with st.sidebar:
    st.markdown(f"Download the CSV file [here](data:text/csv;base64,{base64.b64encode(open(csv_file, 'rb').read()).decode()}), Right-click and save-as.")

    if st.button("Analyze"):
        df = pd.read_csv("customer_feedback.csv")

        # Count unique feedback categories
        unique_categories = df['Feedback Category'].unique()
        st.write("Unique Feedback Categories:", unique_categories)

        # Count occurrences of each feedback category
        category_counts = df['Feedback Category'].value_counts()

        # Plot bar chart
        fig, ax = plt.subplots()
        ax.bar(category_counts.index, category_counts.values)
        ax.set_xlabel('Feedback Category')
        ax.set_ylabel('Count')
        ax.set_title('Feedback Counts by Category')
        ax.tick_params(axis='x', rotation=45)  
        plt.tight_layout()

        # Display the plot using Streamlit
        st.pyplot(fig)
