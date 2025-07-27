<<<<<<< HEAD
<<<<<<< HEAD
import streamlit as st
import json

# Load incident data
with open("incident_data.json", "r", encoding="utf-8") as f:
    incidents = json.load(f)

st.title("🇮🇳 AI-Powered Cybersecurity Incident Monitor - India")

# Sidebar to select incident
incident_titles = [incident["title"] for incident in incidents]
selected_title = st.sidebar.selectbox("Select an Incident", incident_titles)

# Get selected incident
selected_incident = next((i for i in incidents if i["title"] == selected_title), None)

if selected_incident:
    st.subheader(selected_incident["title"])

    st.markdown("### 📰 Full News Content")
    st.write(selected_incident.get("summary", "No article content available."))

    st.markdown("### 🧠 Extracted Entities")
    entities = selected_incident.get("named_entities", [])

    if entities:
        for ent in entities:
            st.markdown(f"- **{ent['label']}**: {ent['text']}")
    else:
        st.info("No entities extracted for this article.")

    st.markdown("### 🛡️ Raw IOCs")
    iocs = selected_incident.get("iocs", {})
    st.write(f"**IPs:** {iocs.get('ips', [])}")
    st.write(f"**URLs:** {iocs.get('urls', [])}")
    st.write(f"**Suspicious Files:** {iocs.get('files', [])}")

    st.markdown("### 🚨 Severity")
    st.write(f"**Severity Level:** {selected_incident.get('severity', 'Unknown')}")
else:
    st.warning("No incident selected.")
=======
=======
>>>>>>> aef2ec7 (Initial commit for AI Cyber Incident Monitor)
import streamlit as st
import json

# Load incident data
with open("incident_data.json", "r", encoding="utf-8") as f:
    incidents = json.load(f)

st.title("🇮🇳 AI-Powered Cybersecurity Incident Monitor - India")

# Sidebar to select incident
incident_titles = [incident["title"] for incident in incidents]
selected_title = st.sidebar.selectbox("Select an Incident", incident_titles)

# Get selected incident
selected_incident = next((i for i in incidents if i["title"] == selected_title), None)

if selected_incident:
    st.subheader(selected_incident["title"])

    st.markdown("### 📰 Full News Content")
    st.write(selected_incident.get("summary", "No article content available."))

    st.markdown("### 🧠 Extracted Entities")
    entities = selected_incident.get("named_entities", [])

    if entities:
        for ent in entities:
            st.markdown(f"- **{ent['label']}**: {ent['text']}")
    else:
        st.info("No entities extracted for this article.")

    st.markdown("### 🛡️ Raw IOCs")
    iocs = selected_incident.get("iocs", {})
    st.write(f"**IPs:** {iocs.get('ips', [])}")
    st.write(f"**URLs:** {iocs.get('urls', [])}")
    st.write(f"**Suspicious Files:** {iocs.get('files', [])}")

    st.markdown("### 🚨 Severity")
    st.write(f"**Severity Level:** {selected_incident.get('severity', 'Unknown')}")
else:
    st.warning("No incident selected.")
<<<<<<< HEAD
>>>>>>> aef2ec7 (Initial commit for AI Cyber Incident Monitor)
=======
>>>>>>> aef2ec7 (Initial commit for AI Cyber Incident Monitor)
