import streamlit as st
from datetime import datetime
import time

st.set_page_config(
    page_title="Support Knowledge Copilot",
    page_icon="🤖",
    layout="wide"
)

# ----------------------------
# Demo Ask Function
# Replace this later with API call
# ----------------------------
def ask(question: str):
    """Temporary demo implementation for Streamlit Cloud."""

    question = question.strip()

    if question == "":
        return None

    time.sleep(0.8)

    return {
        "answer": f"""
### Answer

Based on the available documentation, the following information was retrieved for:

**{question}**

This Streamlit Cloud deployment is running in **Demo Mode**.

The production version performs:

- Hybrid Retrieval (Vector + BM25)
- Cross Encoder Reranking
- Citation Verification
- Confidence Scoring
- LangGraph Multi-Agent Orchestration
- Azure AI Search / pgvector
        """,

        "citations": [
            {
                "source": "Product_FAQ.md",
                "section": "Account Management",
                "page": 3,
                "support_verdict": "Supported"
            },
            {
                "source": "Troubleshooting_Guide.pdf",
                "section": "Authentication",
                "page": 8,
                "support_verdict": "Supported"
            }
        ],

        "confidence_score": 0.91,

        "what_i_could_not_verify": [
            "No evidence was found for customer-specific configuration."
        ]
    }


# ----------------------------
# Sidebar
# ----------------------------

st.sidebar.title("Enterprise AI Demo")

st.sidebar.markdown("""
### Features

✅ Hybrid Search

✅ BM25

✅ Vector Search

✅ Citation Verification

✅ Confidence Scoring

✅ LangGraph

✅ Enterprise RAG

✅ Streamlit Demo
""")

st.sidebar.divider()

st.sidebar.info(
    "Production version uses Azure AI Search, "
    "PostgreSQL + pgvector, LangGraph, "
    "MLflow and Langfuse."
)

# ----------------------------
# Main UI
# ----------------------------

st.title("🤖 Support Knowledge Copilot")

st.caption(
    "Enterprise RAG • Verified Citations • Hybrid Retrieval • Confidence Scoring"
)

question = st.text_area(
    "Ask a support question",
    placeholder="Example: How do I reset my MFA?"
)

if st.button("Ask", type="primary"):

    if question.strip() == "":
        st.warning("Please enter a question.")
        st.stop()

    with st.spinner("Searching enterprise knowledge..."):

        result = ask(question)

    st.success("Answer Generated")

    st.markdown(result["answer"])

    st.divider()

    st.subheader("Verified Citations")

    for c in result["citations"]:

        with st.expander(c["source"]):

            st.write(f"**Section:** {c['section']}")
            st.write(f"**Page:** {c['page']}")
            st.write(f"**Support Verdict:** {c['support_verdict']}")

    st.divider()

    st.subheader("Confidence Score")

    st.progress(result["confidence_score"])

    st.metric(
        "Confidence",
        f"{result['confidence_score']:.0%}"
    )

    st.divider()

    st.subheader("What I Could Not Verify")

    for item in result["what_i_could_not_verify"]:
        st.warning(item)

    st.divider()

    st.caption(
        f"Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

# ----------------------------
# Footer
# ----------------------------

st.divider()

st.markdown("""
### Enterprise Architecture

**Production Version Includes**

- Azure AI Search
- PostgreSQL + pgvector
- BM25 Hybrid Search
- Cross Encoder Reranking
- LangGraph Multi-Agent Workflow
- Citation Verification
- Confidence Scoring
- MLflow
- Langfuse
- Prometheus
- Grafana
- Kubernetes
- GitHub Actions
""")