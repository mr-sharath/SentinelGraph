import streamlit as st
import pandas as pd
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

# Professional Theme Configuration
st.set_page_config(page_title="SentinelGraph Ops Center", page_icon="🛡️", layout="wide")

# CSS for a "Dark Ops" professional look
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { background-color: #4CAF50; color: white; border-radius: 5px; width: 100%; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #3e4250; }
    </style>
    """, unsafe_allow_html=True)

class DashboardDB:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"), 
            auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
        )

    def query(self, cypher):
        with self.driver.session() as session:
            result = session.run(cypher)
            return [record.data() for record in result]

db = DashboardDB()

# --- HEADER SECTION ---
st.title("🛡️ SentinelGraph | Autonomous RCA Engine")
st.markdown("---")

# --- ARCHITECTURE & CONTEXT ---
with st.expander("ℹ️ System Architecture & Ontology", expanded=False):
    st.write("""
    **SentinelGraph** models your enterprise infrastructure as a living web.
    - **Service Nodes**: Tier-0/1 business applications (e.g., PaymentGateway).
    - **Infrastructure Nodes**: AWS/GCP resources (K8s Nodes, Postgres Instances).
    - **Incident Nodes**: Real-time health alerts affecting hardware.
    - **Relationships**: `[:DEPENDS_ON]` and `[:AFFECTS]` mapping the blast radius.
    """)

# --- OPS METRICS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Active Incidents", "1 Critical", delta_color="inverse")
col2.metric("Tier-0 Health", "100%", "Stable")
col3.metric("Infra Nodes", "200", "AWS-East")
col4.metric("Avg RCA Time", "1.2s", "-85%")

# --- INVESTIGATION HUB ---
st.subheader("🔍 Active Investigation Hub")
tab1, tab2 = st.tabs(["🚀 One-Click Scenarios", "💻 Expert Cypher Console"])

with tab1:
    c1, c2, c3 = st.columns(3)
    if c1.button("🔴 Replay INC-47 (Memory Leak)"):
        st.session_state.q = "MATCH (i:Incident {ticket_id: 'INC-47'})-[:AFFECTS]->(inf) OPTIONAL MATCH (s:Service)-[:DEPENDS_ON]->(inf) RETURN i.ticket_id as Ticket, inf.id as Failed_Node, s.name as Impacted_Service, s.criticality as Tier"
    
    if c2.button("🟡 Blast Radius: INFRA-199"):
        st.session_state.q = "MATCH (inf:Infrastructure {id: 'INFRA-199'})<-[:DEPENDS_ON]-(s:Service) RETURN inf.id as ID, inf.type as Type, s.name as Affected_Service"

    if c3.button("🟢 Region Health: us-east-1"):
        st.session_state.q = "MATCH (n:Infrastructure {region: 'us-east-1'}) RETURN n.type as Type, count(n) as Count"

with tab2:
    query = st.text_area("Custom Investigation Query", value=st.session_state.get('q', 'MATCH (n) RETURN n LIMIT 10'))
    if st.button("Execute Autonomous Search"):
        data = db.query(query)
        if data:
            st.table(pd.DataFrame(data))
        else:
            st.warning("No data found for this topology path.")