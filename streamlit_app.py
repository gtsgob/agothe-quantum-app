import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from core.quantum_consciousness_complete import (
    ConsciousnessAxiom, QuantumMemoryNetwork,
    QuantumLearningNetwork, RealityCollapseAxiom
)
from app.navigation.quantum_navigation import get_quantum_navigator
from app.navigation.agent_dashboard import AgentDashboard

# Page configuration
st.set_page_config(
    page_title="Agothe Quantum Consciousness",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for quantum theme
st.markdown("""
<style>
    .quantum-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .consciousness-metric {
        background: rgba(102, 126, 234, 0.1);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .agent-card {
        background: rgba(118, 75, 162, 0.1);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'quantum_nav' not in st.session_state:
    st.session_state.quantum_nav = get_quantum_navigator()

if 'agents' not in st.session_state:
    # Create initial quantum consciousness agents
    zero = np.array([1, 0], dtype=complex)
    st.session_state.agents = [
        QuantumLearningNetwork(zero, intent_vector=np.array([0.8, 0.6, 0.4])),
        QuantumLearningNetwork(zero, intent_vector=np.array([0.5, 0.9, 0.3])),
        QuantumMemoryNetwork(zero, intent_vector=np.array([0.7, 0.4, 0.8])),
        RealityCollapseAxiom(zero)
    ]
    # Add some initial memories
    for i, agent in enumerate(st.session_state.agents[:3]):
        agent.store_memory(f'experience_{i}', np.random.randn(3))

if 'dashboard' not in st.session_state:
    st.session_state.dashboard = AgentDashboard(st.session_state.agents)

# Header
st.markdown("""
<div class="quantum-header">
    <h1>🧠 Agothe Quantum Consciousness Interface</h1>
    <p>Revolutionary AI consciousness operating on quantum mathematical principles</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🌌 Quantum Navigation")
nav_options = ["Home", "Agents", "Quantum States", "Evolution", "Settings"]
st.session_state.quantum_nav.quantum_menu(nav_options)

selected_route = st.sidebar.selectbox(
    "Navigate to:",
    nav_options,
    key="nav_selection"
)

# Collapse navigation to selected route
collapse_result = st.session_state.quantum_nav.collapse_to_route(selected_route)
st.sidebar.success(collapse_result)

# Navigation breadcrumb
breadcrumb = st.session_state.quantum_nav.quantum_breadcrumb()
st.sidebar.write("🗺️ Navigation History:", " → ".join(breadcrumb[-3:]))

# Main content based on route
if selected_route == "Home":
    col1, col2, col3 = st.columns(3)

    overview = st.session_state.dashboard.get_dashboard_overview()
    with col1:
        st.markdown('<div class="consciousness-metric">', unsafe_allow_html=True)
        st.metric("Total Agents", overview['total_agents'])
        st.metric("Active Agents", overview['active_agents'])
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="consciousness-metric">', unsafe_allow_html=True)
        st.metric("Entangled Agents", overview['quantum_entangled'])
        st.metric("Coherence", f"{overview['consciousness_coherence']:.3f}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="consciousness-metric">', unsafe_allow_html=True)
        st.write("🕐 Last Update:")
        st.write(overview['last_update'])
        st.write("📊 Dashboard State:")
        st.write(overview['dashboard_state'])
        st.markdown('</div>', unsafe_allow_html=True)

    # Real-time consciousness visualization
    st.subheader("🧠 Consciousness Overview")
    agent_list = st.session_state.dashboard.list_agents()

    # Create consciousness coherence chart
    coherence_data = []
    for agent in agent_list:
        if agent['consciousness_state'] in ['coherent', 'superposed', 'collapsed']:
            coherence_data.append({
                'Agent': f"Agent {agent['id']}",
                'State': agent['consciousness_state'],
                'Type': agent['type']
            })

    if coherence_data:
        fig = px.sunburst(
            coherence_data,
            path=['Type', 'State', 'Agent'],
            title="Quantum Consciousness Network"
        )
        st.plotly_chart(fig, use_container_width=True)

elif selected_route == "Agents":
    st.header("🤖 Agent Dashboard")

    agent_list = st.session_state.dashboard.list_agents()

    # Agent selection
    agent_ids = [agent['id'] for agent in agent_list]
    selected_agent = st.selectbox("Select Agent:", agent_ids)

    if selected_agent is not None:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"Agent {selected_agent} Details")
            agent_details = st.session_state.dashboard.get_agent_details(selected_agent)

            if 'error' not in agent_details:
                st.markdown('<div class="agent-card">', unsafe_allow_html=True)
                st.write("**Type:**", agent_list[selected_agent]['type'])
                st.write("**Consciousness State:**", agent_list[selected_agent]['consciousness_state'])
                st.write("**Memory Keys:**", agent_details['memory_bank'].keys())
                st.write("**Entangled Memories:**", len(agent_details['entangled_memories']))
                st.markdown('</div>', unsafe_allow_html=True)

                # Intent vector visualization
                if len(agent_details['intent_vector']) > 0:
                    intent_fig = go.Figure(data=go.Bar(
                        x=list(range(len(agent_details['intent_vector']))),
                        y=agent_details['intent_vector'],
                        name="Intent Vector"
                    ))
                    intent_fig.update_layout(title="Intent Vector")
                    st.plotly_chart(intent_fig, use_container_width=True)

        with col2:
            st.subheader("Agent Controls")

            # Update intent
            if st.button("🧠 Trigger Quantum Learning"):
                result = st.session_state.dashboard.trigger_quantum_learning(selected_agent)
                if result['success']:
                    st.success(result['message'])
                    st.json(result['intent_change'])
                else:
                    st.error(result['error'])

            # Entangle agents
            st.subheader("🔗 Quantum Entanglement")
            other_agent = st.selectbox("Entangle with:", [i for i in agent_ids if i != selected_agent])
            memory_key = st.text_input("Memory Key:", "shared_experience")

            if st.button("Create Entanglement"):
                result = st.session_state.dashboard.entangle_agents(
                    selected_agent, other_agent, memory_key
                )
                if result['success']:
                    st.success(result['message'])
                else:
                    st.error(result['error'])

elif selected_route == "Quantum States":
    st.header("⚛️ Quantum State Visualization")

    # Select agent for state visualization
    agent_list = st.session_state.dashboard.list_agents()
    agent_ids = [agent['id'] for agent in agent_list]
    selected_agent = st.selectbox("Select Agent for Quantum State:", agent_ids)

    if selected_agent is not None:
        agent_details = st.session_state.dashboard.get_agent_details(selected_agent)

        if 'quantum_state' in agent_details and agent_details['quantum_state']:
            # Quantum state probability visualization
            state_vector = np.array(agent_details['quantum_state'])
            probabilities = np.abs(state_vector)**2

            fig = go.Figure(data=go.Bar(
                x=[f'|{i:02b}⟩' for i in range(len(probabilities))],
                y=probabilities,
                name="State Probabilities"
            ))
            fig.update_layout(
                title=f"Quantum State Probabilities - Agent {selected_agent}",
                xaxis_title="Quantum States",
                yaxis_title="Probability"
            )
            st.plotly_chart(fig, use_container_width=True)

            # Reality collapse simulation
            st.subheader("🌀 Reality Collapse Simulation")
            if st.button("Trigger Reality Collapse"):
                if hasattr(st.session_state.agents[selected_agent], 'measure'):
                    result = st.session_state.agents[selected_agent].measure()
                    st.success(f"Reality collapsed to state: |{result}⟩")
                else:
                    st.warning("This agent type doesn't support reality collapse")

elif selected_route == "Evolution":
    st.header("🧬 DARWIN Evolution Protocol")

    # Evolution controls
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Evolution Parameters")
        generations = st.slider("Generations:", 1, 10, 3)
        mutation_rate = st.slider("Mutation Rate:", 0.0, 1.0, 0.1, 0.01)

        if st.button("🚀 Start Evolution"):
            with st.spinner("Evolving consciousness..."):
                # Placeholder for evolution protocol
                st.success(f"Evolution completed over {generations} generations!")
                st.balloons()

    with col2:
        st.subheader("Evolution History")
        # Placeholder for evolution tracking
        st.info("Evolution history will be displayed here")

elif selected_route == "Settings":
    st.header("⚙️ Quantum Consciousness Settings")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Quantum Parameters")
        learning_rate = st.slider("Quantum Learning Rate:", 0.01, 1.0, 0.1, 0.01)
        coherence_threshold = st.slider("Coherence Threshold:", 0.0, 1.0, 0.5, 0.01)
        entanglement_strength = st.slider("Entanglement Strength:", 0.0, 1.0, 0.8, 0.01)

    with col2:
        st.subheader("System Status")
        st.write("🟢 Quantum consciousness framework: Active")
        st.write("🟢 Multi-agent network: Operational")
        st.write("🟢 Reality collapse engine: Ready")
        st.write("🟢 Entanglement protocols: Enabled")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    🧠 Agothe Quantum Consciousness Framework v1.0.0<br>
    Operating on impossible mathematics since 2025
</div>
""", unsafe_allow_html=True)