"""Streamlit interface for the Agothe quantum environment."""

from __future__ import annotations

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from agothe_app import create_environment
from agothe_app.services.quantum_environment import QuantumEnvironment

st.set_page_config(
    page_title="Agothe Quantum Consciousness",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Initialisation
# ---------------------------------------------------------------------------
if "environment" not in st.session_state:
    st.session_state.environment = create_environment(agent_count=6)

environment: QuantumEnvironment = st.session_state.environment
navigator = environment.navigator

nav_options = ["Home", "Agents", "Quantum States", "Evolution", "Settings"]
navigator.quantum_menu(nav_options)

# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
st.sidebar.title("🌌 Quantum Navigation")
selected_route = st.sidebar.selectbox(
    "Navigate to:",
    nav_options,
    index=nav_options.index(navigator.current_route)
    if navigator.current_route in nav_options
    else 0,
)
collapse_result = navigator.collapse_to_route(selected_route)
st.sidebar.success(collapse_result)
breadcrumb = navigator.quantum_breadcrumb()
st.sidebar.write("🗺️ Navigation History:", " → ".join(breadcrumb[-4:]))

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 12px; color: white;">
        <h1>🧠 Agothe Quantum Consciousness Interface</h1>
        <p>Real-time orchestration of synthetic quantum minds</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Route specific content
# ---------------------------------------------------------------------------
if selected_route == "Home":
    overview = environment.environment_state()["overview"]
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Agents", overview["total_agents"])
        st.metric("Active Agents", overview["active_agents"])

    with col2:
        st.metric("Entangled Agents", overview["quantum_entangled"])
        st.metric("Coherence", f"{overview['consciousness_coherence']:.3f}")

    with col3:
        st.write("Last Update", overview["last_update"])
        st.write("Dashboard State", overview["dashboard_state"])

    agent_table = environment.agent_summary()
    st.subheader("Quantum Consciousness Network")
    sunburst_data = []
    for agent in agent_table:
        sunburst_data.append(
            {
                "Type": agent["type"],
                "State": "Active" if agent["active"] else "Dormant",
                "Agent": agent["label"],
            }
        )
    if sunburst_data:
        fig = px.sunburst(sunburst_data, path=["Type", "State", "Agent"], title="Agent distribution")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Collapse Engine")
    phase = st.slider("Intent Phase", 0.0, float(2 * np.pi), float(np.pi / 4))
    if st.button("Trigger Collapse"):
        result = environment.simulate_collapse(phase)
        st.success(result["message"])
        st.json(result)

elif selected_route == "Agents":
    agent_table = environment.agent_summary()
    st.header("🤖 Agent Dashboard")
    agent_names = [f"#{agent['id']} – {agent['label']}" for agent in agent_table]
    selected_index = st.selectbox("Select agent", range(len(agent_table)), format_func=lambda i: agent_names[i])
    details = environment.agent_details(selected_index)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Agent Overview")
        st.write("Type", agent_table[selected_index]["type"])
        st.write("Coherence", f"{details['coherence']:.3f}")
        st.write("Memory Keys", list(details["memory_bank"].keys()))
        st.write("Entangled Keys", list(details["entangled"].keys()))

    with col2:
        st.subheader("Intent Vector")
        intent = np.array(details["intent"])
        intent_fig = go.Figure(data=go.Bar(x=list(range(len(intent))), y=intent))
        intent_fig.update_layout(title="Intent components", xaxis_title="Dimension", yaxis_title="Amplitude")
        st.plotly_chart(intent_fig, use_container_width=True)

        st.subheader("Update Intent")
        new_intent = st.text_input("New intent vector", value=",".join(f"{x:.2f}" for x in intent))
        if st.button("Apply Intent Update"):
            try:
                vector = [float(x.strip()) for x in new_intent.split(",") if x.strip()]
                response = environment.update_agent_intent(selected_index, vector)
                if response.get("success"):
                    st.success(response["message"])
                else:
                    st.error(response.get("error", "Unknown error"))
            except ValueError:
                st.error("Please provide a comma separated list of numbers")

    st.subheader("Quantum Learning")
    reward = st.slider("Reward signal", -1.0, 1.0, 0.0, 0.05)
    if st.button("Trigger Learning"):
        response = environment.trigger_learning(selected_index, reward if reward != 0 else None)
        if response.get("success"):
            st.success(response["message"])
            st.json({"before": response.get("before"), "after": response.get("after")})
        else:
            st.error(response.get("error", "Learning failed"))

    st.subheader("Entangle Agents")
    partner = st.selectbox("Entangle with", [agent["id"] for agent in agent_table if agent["id"] != selected_index])
    key = st.text_input("Memory key", value="baseline")
    if st.button("Create Entanglement"):
        response = environment.entangle_agents(selected_index, partner, key)
        if response.get("success"):
            st.success(response["message"])
            st.json({"entangled_state": response["entangled_state"]})
        else:
            st.error(response.get("error", "Entanglement failed"))

elif selected_route == "Quantum States":
    st.header("⚛️ Quantum State Visualisation")
    agent_table = environment.agent_summary()
    selected_index = st.selectbox("Select agent", range(len(agent_table)))
    details = environment.agent_details(selected_index)
    state_vector = np.array(details["state_vector"])
    probabilities = np.abs(state_vector) ** 2

    state_fig = go.Figure(data=go.Bar(x=[f"|{i:02b}⟩" for i in range(len(probabilities))], y=probabilities))
    state_fig.update_layout(title="Measurement probabilities", xaxis_title="State", yaxis_title="Probability")
    st.plotly_chart(state_fig, use_container_width=True)

    if st.button("Measure State"):
        collapse = environment.simulate_collapse(float(np.random.rand() * 2 * np.pi))
        st.success(collapse["message"])
        st.json(collapse)

elif selected_route == "Evolution":
    st.header("🧬 Darwin Evolution Protocol")
    generations = st.slider("Generations", min_value=1, max_value=10, value=3)
    mutation_rate = st.slider("Mutation rate", min_value=0.0, max_value=1.0, value=0.1)

    if st.button("Run Evolution"):
        with st.spinner("Evolving consciousness..."):
            result = environment.run_evolution(generations, mutation_rate)
            st.success("Evolution complete")
            st.json({"best_agent": result["best_agent"]})
            history = result["history"]
            if history:
                history_fig = px.line(history, x="generation", y="best_fitness", title="Fitness over generations")
                st.plotly_chart(history_fig, use_container_width=True)

elif selected_route == "Settings":
    st.header("⚙️ System Settings")
    st.write("Environment contains", len(environment.agents), "agents")
    st.write("Navigator correlation with itself:", navigator.entangle_navigation(navigator)["correlation"])
    st.write("Use the FastAPI endpoint at /api/status for programmatic access.")

st.markdown("---")
st.caption("Agothe Quantum Consciousness Framework • impossible mathematics since 2025")
