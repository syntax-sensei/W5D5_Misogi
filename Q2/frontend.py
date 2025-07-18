import streamlit as st
import sys
import os
from app import query_database, create_sql_chat_agent

# Page configuration
st.set_page_config(
    page_title="Quick Commerce Price Comparison",
    page_icon="🛒",
    layout="centered"
)

# Title and description
st.title("🛒 Quick Commerce Price Comparison")
st.markdown("Ask questions about prices across different apps like Blinkit, Zepto, Instamart, etc.")

# Sample questions
st.sidebar.header("📝 Sample Questions")
sample_questions = [
    "Which app has cheapest onions right now?",
    "Compare fruit prices between Zepto and Instamart",
    f"Show products with 30%+ discount on Blinkit",
    "Find best deals for ₹1000 grocery list",
    "What are the most expensive vegetables?",
    "Which platform has the lowest delivery charges?"
]

for i, question in enumerate(sample_questions):
    if st.sidebar.button(f"📌 {question}", key=f"sample_{i}"):
        st.session_state.user_question = question

# Initialize session state
if 'user_question' not in st.session_state:
    st.session_state.user_question = ""

# Main input area
st.markdown("### 💬 Ask Your Question")
user_input = st.text_input(
    "Enter your question:",
    value=st.session_state.user_question,
    placeholder="e.g., Which app has the cheapest tomatoes?",
    help="Ask anything about product prices, discounts, or comparisons across apps"
)

# Clear button
if st.button("🗑️ Clear"):
    st.session_state.user_question = ""
    st.rerun()

# Submit button and processing
if st.button("🔍 Search", type="primary") and user_input.strip():
    
    with st.spinner("🤖 Analyzing your question and searching the database..."):
        try:
            # Get the answer
            result = query_database(user_input.strip())
            
            # Display results
            st.markdown("### 📊 Results")
            
            if result and not result.startswith("Error"):
                st.success("✅ Query completed successfully!")
                st.markdown("**Answer:**")
                st.info(result)
            else:
                st.error("❌ Sorry, I couldn't process your question.")
                st.error(result)
                
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")

# Database info in sidebar
with st.sidebar:
    st.markdown("---")
    st.header("🗄️ Database Info")
    
    try:
        agent = create_sql_chat_agent()
        if agent:
            st.success("✅ Database Connected")
            
            # Show available tables
            from langchain_community.utilities import SQLDatabase
            script_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(script_dir, "qc.db")
            db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
            
            tables = db.get_usable_table_names()
            st.write(f"📋 **Tables:** {len(tables)}")
            
            with st.expander("View Tables"):
                for table in tables:
                    st.write(f"• {table}")
        else:
            st.error("❌ Database Connection Failed")
            
    except Exception as e:
        st.error(f"❌ Database Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "💡 Tip: Try asking specific questions about prices, discounts, or comparisons between apps"
    "</div>", 
    unsafe_allow_html=True
) 