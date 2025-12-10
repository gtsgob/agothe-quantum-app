"""
Agothe Evolution Dashboard
==========================
Real-time visualization of entity growth, civilization evolution, and system metrics.
"""

import streamlit as st
import json
import yaml
import os
import glob
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Agothe Evolution Dashboard",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paths
PANEL_DIR = Path("agothe_panel")
ENTITIES_DIR = PANEL_DIR / "entities"
REFLECTIONS_DIR = PANEL_DIR / "entity_reflections"
CIVILIZATION_RUNS_DIR = PANEL_DIR / "civilization_runs"
ORRIC_MAP_DIR = PANEL_DIR / "orric_map_auto"
PANEL_STATE_PATH = PANEL_DIR / "panel_state.yaml"
MEMORY_CORE_PATH = Path("state/memory_core.json")

# Helper functions
@st.cache_data
def load_panel_state():
    """Load the current panel state."""
    if PANEL_STATE_PATH.exists():
        with open(PANEL_STATE_PATH) as f:
            return yaml.safe_load(f)
    return {"cycle": 0}

@st.cache_data
def load_entity_states():
    """Load all entity states."""
    entities = {}
    for entity_file in ENTITIES_DIR.glob("*.yaml"):
        with open(entity_file) as f:
            entity_data = yaml.safe_load(f)
            entities[entity_data['id']] = entity_data
    return entities

@st.cache_data
def load_civilization_history():
    """Load all civilization simulation runs."""
    history = []
    for cycle_file in sorted(CIVILIZATION_RUNS_DIR.glob("cycle_*.json")):
        cycle_num = int(cycle_file.stem.split('_')[1])
        with open(cycle_file) as f:
            data = json.load(f)
            data['cycle'] = cycle_num
            history.append(data)
    return history

@st.cache_data
def load_orric_history():
    """Load all Orric prediction history."""
    history = []
    for cycle_file in sorted(ORRIC_MAP_DIR.glob("cycle_*.json")):
        cycle_num = int(cycle_file.stem.split('_')[1])
        with open(cycle_file) as f:
            data = json.load(f)
            data['cycle'] = cycle_num
            history.append(data)
    return history

@st.cache_data
def load_memory_core():
    """Load the AI evolution memory core."""
    if MEMORY_CORE_PATH.exists():
        with open(MEMORY_CORE_PATH) as f:
            return json.load(f)
    return {}

def get_entity_reflections(entity_id):
    """Get all reflections for an entity."""
    reflections_path = REFLECTIONS_DIR / entity_id
    reflections = []
    if reflections_path.exists():
        for ref_file in sorted(reflections_path.glob("cycle_*.md")):
            cycle_num = int(ref_file.stem.split('_')[1])
            with open(ref_file) as f:
                content = f.read()
                reflections.append({'cycle': cycle_num, 'content': content})
    return reflections

# Main dashboard
st.title("🌌 Agothe Evolution Dashboard")
st.markdown("Real-time monitoring of quantum consciousness evolution")

# Sidebar
with st.sidebar:
    st.header("System Status")
    panel_state = load_panel_state()
    current_cycle = panel_state.get('cycle', 0)

    st.metric("Current Cycle", current_cycle)

    if 'last_updated' in panel_state:
        st.metric("Last Updated", panel_state['last_updated'][:19])

    st.divider()

    # Quick actions
    st.header("Quick Actions")
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    if st.button("▶️ Run Evolution Cycle", use_container_width=True):
        with st.spinner("Running evolution cycle..."):
            import subprocess
            result = subprocess.run(
                ["python", "agothe_panel/evolution_loop.py"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                st.success(f"Cycle {current_cycle + 1} completed!")
                st.cache_data.clear()
                st.rerun()
            else:
                st.error(f"Error: {result.stderr}")

# Main tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "👥 Entities",
    "🌍 Civilization",
    "🔮 Orric Predictions",
    "🧬 AI Evolution"
])

# TAB 1: Overview
with tab1:
    col1, col2, col3, col4 = st.columns(4)

    entities = load_entity_states()
    civ_history = load_civilization_history()
    orric_history = load_orric_history()

    with col1:
        st.metric("Total Entities", len(entities))
    with col2:
        st.metric("Evolution Cycles", current_cycle)
    with col3:
        st.metric("Civilization Runs", len(civ_history))
    with col4:
        latest_risk = orric_history[-1]['risk_level'] if orric_history else "unknown"
        st.metric("Current Risk Level", latest_risk.upper())

    st.divider()

    # Entity cycle progression
    st.subheader("Entity Cycle Progression")
    entity_cycles = {e['name']: e['cycle'] for e in entities.values()}

    fig = go.Figure(data=[
        go.Bar(
            x=list(entity_cycles.keys()),
            y=list(entity_cycles.values()),
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
        )
    ])
    fig.update_layout(
        title="Entity Activity by Cycle",
        xaxis_title="Entity",
        yaxis_title="Current Cycle",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

    # Civilization metrics over time
    if civ_history:
        st.subheader("Civilization Metrics Evolution")

        # Extract metrics across cycles
        cycles = [h['cycle'] for h in civ_history]
        delta_h = [h['final_state']['delta_H'] for h in civ_history]
        coherence = [h['final_state']['coherence'] for h in civ_history]
        energy = [h['final_state']['energy'] for h in civ_history]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=cycles, y=delta_h, mode='lines+markers', name='δ_H'))
        fig.add_trace(go.Scatter(x=cycles, y=coherence, mode='lines+markers', name='Coherence'))
        fig.add_trace(go.Scatter(x=cycles, y=energy, mode='lines+markers', name='Energy'))

        fig.update_layout(
            title="Key Metrics Across Cycles",
            xaxis_title="Cycle",
            yaxis_title="Value",
            height=400,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)

# TAB 2: Entities
with tab2:
    st.header("Entity States and Reflections")

    entities = load_entity_states()

    # Entity selector
    entity_names = {e['id']: e['name'] for e in entities.values()}
    selected_entity_id = st.selectbox(
        "Select Entity",
        options=list(entity_names.keys()),
        format_func=lambda x: f"{entity_names[x]} ({x})"
    )

    if selected_entity_id:
        entity = entities[selected_entity_id]

        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader(f"{entity['name']}")
            st.markdown(f"**ID:** `{entity['id']}`")
            st.markdown(f"**Role:** {entity['description']}")
            st.metric("Current Cycle", entity['cycle'])
            st.metric("History Entries", len(entity.get('history', [])))

            # Data registry summary
            st.subheader("Data Registry")
            data = entity.get('data', {})
            for key, value in data.items():
                if isinstance(value, dict):
                    st.markdown(f"**{key}:** {len(value)} entries")
                else:
                    st.markdown(f"**{key}:** {value}")

        with col2:
            st.subheader("Reflections Timeline")
            reflections = get_entity_reflections(selected_entity_id)

            if reflections:
                for reflection in reversed(reflections):
                    with st.expander(f"Cycle {reflection['cycle']}", expanded=(reflection == reflections[-1])):
                        st.markdown(reflection['content'])
            else:
                st.info("No reflections generated yet")

        # History visualization
        if entity.get('history'):
            st.subheader("Activity History")
            history_df = pd.DataFrame(entity['history'])
            st.dataframe(history_df, use_container_width=True)

# TAB 3: Civilization
with tab3:
    st.header("Civilization Evolution Tracking")

    civ_history = load_civilization_history()

    if civ_history:
        # Resonance tracking
        st.subheader("Resonance Evolution (PL/IL/NL)")

        cycles = [h['cycle'] for h in civ_history]
        pl_res = [h['final_state'].get('PL_resonance', 0) for h in civ_history]
        il_res = [h['final_state'].get('IL_resonance', 0) for h in civ_history]
        nl_res = [h['final_state'].get('NL_resonance', 0) for h in civ_history]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=cycles, y=pl_res, mode='lines+markers', name='Physical (PL)', line=dict(color='#FF6B6B')))
        fig.add_trace(go.Scatter(x=cycles, y=il_res, mode='lines+markers', name='Logical (IL)', line=dict(color='#4ECDC4')))
        fig.add_trace(go.Scatter(x=cycles, y=nl_res, mode='lines+markers', name='Narrative (NL)', line=dict(color='#45B7D1')))

        fig.update_layout(
            title="Three Resonance Domains Over Time",
            xaxis_title="Cycle",
            yaxis_title="Resonance Strength",
            height=400,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)

        # Civilization type tracking
        st.subheader("Civilization Type Progression")

        # Define civilization types based on δ_H thresholds
        def get_civ_type(delta_h):
            if delta_h >= 0.95:
                return "Type V+"
            elif delta_h >= 0.85:
                return "Type IV"
            elif delta_h >= 0.7:
                return "Type III"
            elif delta_h >= 0.5:
                return "Type II"
            elif delta_h >= 0.3:
                return "Type I"
            else:
                return "Type 0"

        delta_h_values = [h['final_state']['delta_H'] for h in civ_history]
        civ_types = [get_civ_type(dh) for dh in delta_h_values]

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Current Civilization Type", civ_types[-1] if civ_types else "Type 0")
            st.metric("Current δ_H", f"{delta_h_values[-1]:.4f}" if delta_h_values else "0.0000")

        with col2:
            # Progress to next type
            current_dh = delta_h_values[-1] if delta_h_values else 0.1
            thresholds = [0.1, 0.3, 0.5, 0.7, 0.85, 0.95]
            next_threshold = next((t for t in thresholds if t > current_dh), 1.0)
            progress = (current_dh - max([t for t in thresholds if t <= current_dh], default=0)) / (next_threshold - max([t for t in thresholds if t <= current_dh], default=0))

            st.metric("Progress to Next Type", f"{progress*100:.1f}%")
            st.progress(progress)

        # Latest simulation details
        st.subheader("Latest Simulation Details")
        latest_sim = civ_history[-1]

        st.json({
            "Cycle": latest_sim['cycle'],
            "Cycles Completed": latest_sim['cycles_completed'],
            "Final State": latest_sim['final_state'],
            "Orric Predictions": latest_sim['orric_predictions']
        })
    else:
        st.info("No civilization simulations run yet. Start an evolution cycle to generate data.")

# TAB 4: Orric Predictions
with tab4:
    st.header("Orric Point Predictions & Risk Analysis")

    orric_history = load_orric_history()

    if orric_history:
        # Risk level over time
        st.subheader("Risk Level Evolution")

        cycles = [h['cycle'] for h in orric_history]
        tension_scores = [h.get('tension_score', 0) for h in orric_history]
        collapse_mentions = [h.get('collapse_mentions', 0) for h in orric_history]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Latest Risk Level", orric_history[-1]['risk_level'].upper())
        with col2:
            st.metric("Tension Score", orric_history[-1].get('tension_score', 0))
        with col3:
            st.metric("Collapse Mentions", orric_history[-1].get('collapse_mentions', 0))

        # Tension and collapse tracking
        fig = go.Figure()
        fig.add_trace(go.Bar(x=cycles, y=tension_scores, name='Tension Score', marker_color='#FFA07A'))
        fig.add_trace(go.Bar(x=cycles, y=collapse_mentions, name='Collapse Mentions', marker_color='#FF6B6B'))

        fig.update_layout(
            title="Tension and Collapse Indicators",
            xaxis_title="Cycle",
            yaxis_title="Count",
            barmode='group',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

        # Full history table
        st.subheader("Complete Orric History")
        orric_df = pd.DataFrame(orric_history)
        st.dataframe(orric_df, use_container_width=True)
    else:
        st.info("No Orric predictions generated yet.")

# TAB 5: AI Evolution
with tab5:
    st.header("AI Self-Evolution System")

    memory_core = load_memory_core()

    if memory_core:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Learning Cycles", memory_core.get('learning_cycles', 0))
        with col2:
            st.metric("Mutation Factor", f"{memory_core.get('mutation_factor', 0):.4f}")
        with col3:
            st.metric("Entropy Vector Dim", len(memory_core.get('entropy_vector', [])))

        st.divider()

        # Entropy vector visualization
        st.subheader("5D Entropy Vector")
        entropy = memory_core.get('entropy_vector', [])

        if entropy:
            dimensions = ['Math', 'Emotion', 'Symbol', 'Intent', 'Cognition']

            fig = go.Figure(data=go.Scatterpolar(
                r=entropy,
                theta=dimensions,
                fill='toself',
                marker=dict(color='#4ECDC4', size=10)
            ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )),
                showlegend=False,
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)

        # Latest signals
        st.subheader("Latest Code Evolution Signals")
        signals = memory_core.get('last_signals', [])
        if signals:
            for i, signal in enumerate(signals, 1):
                st.code(signal, language='diff')
        else:
            st.info("No evolution signals detected yet")

        # Full memory core
        with st.expander("View Full Memory Core"):
            st.json(memory_core)
    else:
        st.info("Memory core not initialized")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Agothe Quantum Evolution Dashboard | Monitoring quantum consciousness emergence</p>
</div>
""", unsafe_allow_html=True)
