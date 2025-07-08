import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@st.cache_resource
def initialize_agent():
    """Initialize the SQL agent with caching"""
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0
        )
        
        db_url = os.getenv("DATABASE_URL")
        db = SQLDatabase.from_uri(db_url)
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        
        agent_executor = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=True,
            agent_type="openai-tools"
        )
        
        return agent_executor, None
    except Exception as e:
        return None, str(e)

@st.cache_data
def get_database_schema():
    """Get database schema information"""
    try:
        db_url = os.getenv("DATABASE_URL")
        
        # Parse connection parameters from URL
        import re
        match = re.match(r'postgresql\+psycopg2://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)', db_url)
        if not match:
            return None
        
        user, password, host, port, database = match.groups()
        
        conn = psycopg2.connect(
            host=host,
            port=int(port),
            database=database,
            user=user,
            password=password
        )
        
        cur = conn.cursor()
        
        # Get database name
        cur.execute("SELECT current_database();")
        db_name = cur.fetchone()[0]
        
        # Get all tables with their columns
        cur.execute("""
            SELECT 
                t.table_name,
                c.column_name,
                c.data_type,
                c.is_nullable,
                c.column_default
            FROM information_schema.tables t
            JOIN information_schema.columns c ON t.table_name = c.table_name
            WHERE t.table_schema = 'public' AND t.table_type = 'BASE TABLE'
            ORDER BY t.table_name, c.ordinal_position;
        """)
        
        results = cur.fetchall()
        
        # Organize data by table
        schema = {
            'database_name': db_name,
            'tables': {}
        }
        
        for table_name, column_name, data_type, is_nullable, column_default in results:
            if table_name not in schema['tables']:
                schema['tables'][table_name] = []
            
            schema['tables'][table_name].append({
                'column_name': column_name,
                'data_type': data_type,
                'is_nullable': is_nullable,
                'column_default': column_default
            })
        
        cur.close()
        conn.close()
        
        return schema
        
    except Exception as e:
        st.error(f"Error getting schema: {e}")
        return None

def ask_question(question: str, agent):
    """Ask a question about the Pagila database"""
    try:
        result = agent.invoke({"input": question})
        return result["output"]
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="🎬 Pagila Database Q&A", layout="wide")

st.title("🎬 Pagila Database Q&A")
st.markdown("Ask questions about movies, actors, rentals, and more from the Pagila database!")

# Create sidebar for database schema
with st.sidebar:
    st.markdown(
        """
        <style>
        .sidebar .stButton > button {
            text-align: left !important;
            justify-content: flex-start !important;
            padding-left: 0.5rem !important;
        }
        .stButton > button {
            text-align: left !important;
            justify-content: flex-start !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.header("📊 Database Explorer")
    
    # Get and display schema
    schema = get_database_schema()
    
    if schema:
        # Database info
        st.markdown(f"**💾 Database:** `{schema['database_name']}`")
        st.markdown(f"**📋 Tables:** {len(schema['tables'])}")
        st.markdown("---")
        
        # Search/filter tables
        search_table = st.text_input("🔍 Search tables:", placeholder="Filter tables...")
        
        # Display tables with tree-like structure
        filtered_tables = {k: v for k, v in schema['tables'].items() 
                          if search_table.lower() in k.lower()} if search_table else schema['tables']
        
        for table_name, columns in filtered_tables.items():
            # Table header with icon and count
            table_icon = "🎬" if "film" in table_name else "👥" if "actor" in table_name or "customer" in table_name else "📋"
            
            # Create expandable section with > arrow
            table_key = f"table_{table_name}"
            if table_key not in st.session_state:
                st.session_state[table_key] = False
            
            # Table header button with left alignment
            arrow = "▼" if st.session_state[table_key] else "▶"
            
            if st.button(f"{arrow} {table_icon} {table_name} ({len(columns)} columns)", key=f"btn_{table_name}", use_container_width=True):
                st.session_state[table_key] = not st.session_state[table_key]
            
            # Show columns if expanded
            if st.session_state[table_key]:
                for col in columns:
                    # Column type styling
                    type_color = {
                        'integer': '🔢',
                        'character varying': '🔤', 
                        'text': '📝',
                        'timestamp': '⏰',
                        'date': '📅',
                        'boolean': '✅',
                        'numeric': '🔢'
                    }
                    
                    icon = type_color.get(col['data_type'], '📎')
                    required = "Required" if col['is_nullable'] == 'NO' else "Optional"
                    
                    # Single line column display with left alignment
                    st.markdown(f"&nbsp;&nbsp;{icon} `{col['column_name']}` - {col['data_type']} - {required}")
    else:
        st.error("⚠️ Could not load database schema")
    
    # Connection info at bottom
    st.markdown("---")
    st.caption("🔗 Connected to Local PostgreSQL")
    st.caption("🏠 Host: localhost:5432")

# Main content area
st.header("💬 Natural Language Database Query")

# Initialize agent with error handling
with st.spinner("Initializing database connection..."):
    agent, error = initialize_agent()
    
    if error:
        st.error(f"⚠️ Database Connection Failed: {error}")
        st.error("🔒 Please ensure PostgreSQL is running and database is accessible")
        st.stop()

# Quick start section
st.subheader("🚀 Quick Start")
st.markdown("Click on any sample question below or type your own:")

# Sample questions for Pagila database
sample_questions = [
    "How many movies are available?",
    "Show me some comedy movies",
    "List the top 5 actors with most films",
    "Which customer has rented the most films?",
    "What are the most popular movie categories?",
    "Show me all movies released after 2005"
]

# Create 3 columns for better layout
cols = st.columns(3)
for i, question in enumerate(sample_questions):
    with cols[i % 3]:
        if st.button(question, key=question, use_container_width=True):
            st.session_state.user_question = question

st.markdown("---")

# Main query section
st.subheader("❓ Ask Your Question")

# Main input
user_question = st.text_area(
    "Enter your question about the database:", 
    value=st.session_state.get('user_question', ''),
    placeholder="e.g., How many comedy movies are there? or Show me actors who appeared in more than 10 films",
    height=100
)

# Ask button
if st.button("💬 Ask Question", type="primary", use_container_width=True):
    if user_question:
        with st.spinner("🤖 AI is analyzing your question and generating SQL..."):
            answer = ask_question(user_question, agent)
            
            # Display answer with better formatting
            st.markdown("### 📊 Results:")
            
            with st.container():
                # Clean up the answer for better display
                clean_answer = answer.replace('```sql', '').replace('```', '').strip()
                
                # If it's a simple count or number, highlight it
                if clean_answer.isdigit():
                    st.metric("Result", clean_answer)
                elif "rows" in clean_answer.lower() or "records" in clean_answer.lower():
                    st.info(clean_answer)
                elif "|" in clean_answer and "\n" in clean_answer:
                    # If it looks like a table, format as code
                    st.code(clean_answer)
                else:
                    st.write(clean_answer)
            
            # Clear session state
            if 'user_question' in st.session_state:
                del st.session_state.user_question
    else:
        st.warning("⚠️ Please enter a question!")

# Footer
st.markdown("---")
st.markdown("💡 **Tips:**")
st.markdown("- Use the **Database Explorer** on the left to browse tables and columns")
st.markdown("- Ask questions in **natural language** - the AI will convert them to SQL")
st.markdown("- Try questions about **movies, actors, categories, rentals, customers, and payments**")
st.markdown("- Be specific for better results: *'Show me comedy movies from 2005'* vs *'Show movies'*")