"""
Enhanced UI components for advanced LLM integration.

This module extends the original UI components to support:
- Multiple LLM provider selection
- Optimization strategy selection
- Real-time provider status
- Advanced performance metrics
- Web context display
"""

import streamlit as st
import time
from typing import Dict, List, Optional, Any
from advanced_llm_manager import advanced_llm_manager
from enhanced_constants import (
    ADVANCED_MODELS,
    OPTIMIZATION_STRATEGIES,
    ENHANCED_UI_CONFIG,
    INTEGRATION_STATUS,
    PERFORMANCE_METRICS
)
from ui_components import (
    render_custom_css,
    render_main_header,
    render_category_management,
    render_best_tweet_display,
    render_generator_inputs,
    render_evaluator_inputs,
    render_optimization_stats,
    render_latest_evaluation,
    render_score_history
)

def render_enhanced_custom_css():
    """Render enhanced CSS with additional styling for advanced features."""
    render_custom_css()  # Include original CSS
    
    additional_css = """
    <style>
    /* Enhanced provider status indicators */
    .provider-status {
        padding: 0.5rem;
        border-radius: 0.5rem;
        margin: 0.25rem 0;
        font-size: 0.9rem;
    }
    
    .provider-available {
        background-color: #1a4d1a;
        border-left: 4px solid #00ff00;
        color: #ffffff;
    }
    
    .provider-unavailable {
        background-color: #4d1a1a;
        border-left: 4px solid #ff0000;
        color: #ffffff;
    }
    
    /* Strategy selector styling */
    .strategy-card {
        border: 1px solid #444;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: #2a2a2a;
    }
    
    .strategy-card.selected {
        border-color: #ff0000;
        background-color: #3a2a2a;
    }
    
    /* Performance metrics styling */
    .metrics-container {
        background-color: #1a1a1a;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .metric-item {
        display: flex;
        justify-content: space-between;
        padding: 0.25rem 0;
        border-bottom: 1px solid #333;
    }
    
    .metric-item:last-child {
        border-bottom: none;
    }
    
    /* Web context display */
    .web-context {
        background-color: #2a2a2a;
        border-left: 4px solid #0066cc;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.5rem;
    }
    
    .web-context h4 {
        color: #0066cc;
        margin-top: 0;
    }
    
    /* Advanced controls */
    .advanced-controls {
        background-color: #1a1a1a;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .control-group {
        margin: 0.5rem 0;
    }
    
    .control-label {
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 0.25rem;
    }
    </style>
    """
    
    st.markdown(additional_css, unsafe_allow_html=True)

def render_provider_status():
    """Render real-time provider status indicators."""
    if not ENHANCED_UI_CONFIG.get("show_provider_status", True):
        return
    
    st.subheader("🔌 Provider Status")
    
    status = advanced_llm_manager.get_status()
    
    for provider_name, provider_info in status["providers"].items():
        if provider_info["available"]:
            status_class = "provider-available"
            status_icon = "🟢"
        else:
            status_class = "provider-unavailable"
            status_icon = "🔴"
        
        st.markdown(f"""
        <div class="provider-status {status_class}">
            {status_icon} <strong>{provider_name}</strong> - {provider_info["type"]}
        </div>
        """, unsafe_allow_html=True)
    
    # Show hybrid mode status
    if status["hybrid_mode"]:
        st.markdown(f"""
        <div class="provider-status provider-available">
            🟢 <strong>Hybrid Mode</strong> - Automatic provider selection enabled
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="provider-status provider-unavailable">
            🟡 <strong>Hybrid Mode</strong> - Single provider mode
        </div>
        """, unsafe_allow_html=True)

def render_optimization_strategy_selector():
    """Render optimization strategy selector."""
    if not ENHANCED_UI_CONFIG.get("strategy_selector", True):
        return None
    
    st.subheader("🎯 Optimization Strategy")
    
    # Get available strategies
    available_strategies = []
    for strategy_key, strategy_info in OPTIMIZATION_STRATEGIES.items():
        # Check if strategy is available based on provider availability
        providers_available = True
        for provider in strategy_info["providers"]:
            if provider not in [p.split("_")[0] for p in advanced_llm_manager.providers.keys()]:
                providers_available = False
                break
        
        if providers_available:
            available_strategies.append((strategy_key, strategy_info))
    
    if not available_strategies:
        st.warning("No optimization strategies available. Please configure LLM providers.")
        return None
    
    # Create strategy options
    strategy_options = {f"{info['name']} - {info['description']}": key 
                      for key, info in available_strategies}
    
    selected_strategy_display = st.selectbox(
        "Choose optimization strategy:",
        options=list(strategy_options.keys()),
        help="Select the optimization approach based on your needs"
    )
    
    selected_strategy = strategy_options[selected_strategy_display]
    
    # Show strategy details
    strategy_info = OPTIMIZATION_STRATEGIES[selected_strategy]
    
    with st.expander("Strategy Details"):
        st.write(f"**Description:** {strategy_info['description']}")
        st.write(f"**Providers:** {', '.join(strategy_info['providers'])}")
        st.write(f"**Web Search:** {'Enabled' if strategy_info['use_web_search'] else 'Disabled'}")
        st.write(f"**Context Optimization:** {'Enabled' if strategy_info['use_context_optimization'] else 'Disabled'}")
    
    return selected_strategy

def render_provider_selector():
    """Render LLM provider selector."""
    if not ENHANCED_UI_CONFIG.get("provider_selector", True):
        return None
    
    st.subheader("🤖 LLM Provider")
    
    # Get available providers
    available_providers = []
    for provider_name, provider in advanced_llm_manager.providers.items():
        if provider.is_available():
            available_providers.append(provider_name)
    
    if not available_providers:
        st.warning("No LLM providers available. Please check your configuration.")
        return None
    
    # Create provider options with descriptions
    provider_options = {}
    for provider_name in available_providers:
        provider_type = type(advanced_llm_manager.providers[provider_name]).__name__
        provider_options[f"{provider_name} ({provider_type})"] = provider_name
    
    selected_provider_display = st.selectbox(
        "Choose LLM provider:",
        options=list(provider_options.keys()),
        help="Select the specific LLM provider to use"
    )
    
    selected_provider = provider_options[selected_provider_display]
    
    return selected_provider

def render_performance_metrics():
    """Render advanced performance metrics."""
    if not ENHANCED_UI_CONFIG.get("show_performance_metrics", True):
        return
    
    st.subheader("📊 Performance Metrics")
    
    status = advanced_llm_manager.get_status()
    ax_stats = status.get("ax_manager_stats", {})
    performance_metrics = ax_stats.get("performance_metrics", {})
    
    if not performance_metrics:
        st.info("No performance data available yet.")
        return
    
    # Create metrics display
    for provider_name, metrics in performance_metrics.items():
        with st.expander(f"📈 {provider_name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Successes", metrics.get("successes", 0))
                st.metric("Failures", metrics.get("failures", 0))
            
            with col2:
                total_requests = metrics.get("successes", 0) + metrics.get("failures", 0)
                if total_requests > 0:
                    success_rate = (metrics.get("successes", 0) / total_requests) * 100
                    st.metric("Success Rate", f"{success_rate:.1f}%")
                else:
                    st.metric("Success Rate", "N/A")
    
    # GEPA-ACE optimization stats
    gepa_stats = status.get("gepa_ace_stats", {})
    if gepa_stats.get("total_optimizations", 0) > 0:
        with st.expander("🧠 GEPA-ACE Optimization Stats"):
            st.metric("Total Optimizations", gepa_stats["total_optimizations"])
            st.metric("Avg Compression Ratio", f"{gepa_stats.get('average_compression_ratio', 0):.2f}")
            st.metric("Total Context Saved", 
                     f"{gepa_stats.get('total_original_length', 0) - gepa_stats.get('total_optimized_length', 0)} chars")

def render_web_context_display(web_context: str):
    """Render web context information."""
    if not ENHANCED_UI_CONFIG.get("show_web_context", True) or not web_context:
        return
    
    st.markdown("""
    <div class="web-context">
        <h4>🌐 Web Context</h4>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("View Web Context", expanded=False):
        st.write(web_context)
        st.caption("Real-time web information used for tweet optimization")

def render_advanced_controls():
    """Render advanced control panel."""
    st.subheader("⚙️ Advanced Controls")
    
    with st.expander("System Configuration", expanded=False):
        # Hybrid mode toggle
        hybrid_mode = st.checkbox(
            "Enable Hybrid Mode",
            value=advanced_llm_manager.hybrid_mode,
            help="Automatically select the best provider for each request"
        )
        
        if hybrid_mode != advanced_llm_manager.hybrid_mode:
            advanced_llm_manager.set_hybrid_mode(hybrid_mode)
            st.rerun()
        
        # Feature toggles
        col1, col2 = st.columns(2)
        
        with col1:
            st.checkbox("Enable Web Search", value=True, help="Use web search for enhanced context")
            st.checkbox("Enable Context Optimization", value=True, help="Use GEPA-ACE for context optimization")
        
        with col2:
            st.checkbox("Enable Performance Tracking", value=True, help="Track provider performance metrics")
            st.checkbox("Enable Advanced Categories", value=True, help="Use enhanced evaluation categories")
    
    with st.expander("Provider Management", expanded=False):
        # Provider-specific settings
        for provider_name, provider in advanced_llm_manager.providers.items():
            if provider.is_available():
                st.write(f"**{provider_name}**")
                
                if hasattr(provider, 'list_models'):
                    try:
                        models = provider.list_models()
                        if models:
                            st.write(f"Available models: {', '.join(models[:3])}{'...' if len(models) > 3 else ''}")
                    except:
                        pass

def render_enhanced_optimization_stats(iteration_count: int, best_score: float, 
                                     no_improvement_count: int, patience: int,
                                     current_strategy: str = None, current_provider: str = None):
    """Render enhanced optimization statistics."""
    # Call original stats renderer
    render_optimization_stats(iteration_count, best_score, no_improvement_count, patience)
    
    # Add enhanced information
    if current_strategy:
        strategy_info = OPTIMIZATION_STRATEGIES.get(current_strategy, {})
        st.info(f"🎯 **Strategy:** {strategy_info.get('name', current_strategy)}")
    
    if current_provider:
        st.info(f"🤖 **Provider:** {current_provider}")

def render_enhanced_sidebar():
    """Render enhanced sidebar with all advanced controls."""
    with st.sidebar:
        st.header("🔧 Advanced Configuration")
        
        # Provider status
        render_provider_status()
        
        st.divider()
        
        # Strategy selector
        selected_strategy = render_optimization_strategy_selector()
        
        st.divider()
        
        # Provider selector
        selected_provider = render_provider_selector()
        
        st.divider()
        
        # Performance metrics
        render_performance_metrics()
        
        st.divider()
        
        # Advanced controls
        render_advanced_controls()
    
    return selected_strategy, selected_provider

def render_enhanced_main_interface():
    """Render the enhanced main interface."""
    # Render enhanced header
    render_main_header()
    
    # Add enhanced features indicator
    st.markdown("""
    <div style="background-color: #2a2a2a; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;">
        <h4 style="color: #ff0000; margin: 0;">🚀 Enhanced Mode Active</h4>
        <p style="margin: 0.5rem 0 0 0; color: #cccccc;">
            Advanced LLM integration with Perplexity, local models, and GEPA-ACE optimization
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_system_status_banner():
    """Render system status banner at the top."""
    status = advanced_llm_manager.get_status()
    
    # Count available providers
    available_count = sum(1 for info in status["providers"].values() if info["available"])
    total_count = len(status["providers"])
    
    if available_count == 0:
        status_color = "#ff0000"
        status_text = "No providers available"
    elif available_count < total_count:
        status_color = "#ffaa00"
        status_text = f"{available_count}/{total_count} providers available"
    else:
        status_color = "#00ff00"
        status_text = f"All {total_count} providers available"
    
    st.markdown(f"""
    <div style="background-color: {status_color}20; border-left: 4px solid {status_color}; 
                padding: 0.5rem 1rem; margin: 0.5rem 0; border-radius: 0.25rem;">
        <strong>System Status:</strong> {status_text}
    </div>
    """, unsafe_allow_html=True)
