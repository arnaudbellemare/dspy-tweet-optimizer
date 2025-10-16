#!/usr/bin/env python3
"""
Streamlit Cloud Compatible DSPy Tweet Optimizer

This version is designed specifically for Streamlit Cloud deployment.
It uses a simple demo mode that doesn't require any API keys or external services.
"""

import streamlit as st
import time
import random

# Page configuration
st.set_page_config(
    page_title="DSPy Tweet Optimizer - Cloud Demo",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background-color: #2a2a2a;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .main-header h1 {
        color: #ff0000;
        margin: 0;
    }
    .main-header p {
        margin: 0.5rem 0 0 0;
        color: #cccccc;
    }
    .tweet-container {
        background-color: #2a2a2a;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 4px solid #00ff00;
    }
    .demo-notice {
        background-color: #ffeb3b;
        color: #000;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'input_text' not in st.session_state:
        st.session_state.input_text = ""
    if 'optimized_tweets' not in st.session_state:
        st.session_state.optimized_tweets = []
    if 'categories' not in st.session_state:
        st.session_state.categories = ["Engagement", "Clarity", "Viral Potential", "Brand Voice"]
    if 'optimization_running' not in st.session_state:
        st.session_state.optimization_running = False

def generate_demo_tweet(original_text: str) -> str:
    """Generate a demo optimized tweet (simulated optimization)."""
    # Simple demo optimization - just make it more tweet-like
    words = original_text.split()
    
    # Add some demo optimizations
    optimizations = [
        "🚀 ",
        "💡 ",
        "🔥 ",
        "✨ ",
        "🎯 ",
        "⚡ ",
        "🌟 ",
        "💪 "
    ]
    
    # Add emoji at the beginning
    emoji = random.choice(optimizations)
    
    # Make it shorter if too long
    if len(original_text) > 200:
        words = words[:25]  # Take first 25 words
        original_text = " ".join(words)
    
    # Add hashtags
    hashtags = ["#AI", "#Tech", "#Innovation", "#Future", "#Digital", "#Smart"]
    selected_hashtags = random.sample(hashtags, 2)
    
    optimized = f"{emoji}{original_text} {' '.join(selected_hashtags)}"
    
    # Ensure it's under 280 characters
    if len(optimized) > 280:
        optimized = optimized[:277] + "..."
    
    return optimized

def main():
    """Main application entry point."""
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 DSPy Tweet Optimizer - Cloud Demo</h1>
        <p>AI-powered tweet optimization (Demo Mode)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Demo notice
    st.markdown("""
    <div class="demo-notice">
        <strong>📢 Demo Mode:</strong> This is a simplified version for Streamlit Cloud. 
        For full functionality with real AI optimization, use the local version with Ollama.
    </div>
    """, unsafe_allow_html=True)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Enter Your Original Tweet")
        
        # Text input area
        input_text = st.text_area(
            "Type your tweet concept here:",
            placeholder="Enter the text you want to optimize into a tweet...",
            height=150,
            key="main_input"
        )
        
        # Optimization button
        if st.button("🧠 Optimize Tweet", use_container_width=True, type="primary"):
            if input_text.strip():
                st.session_state.optimization_running = True
                st.session_state.input_text = input_text.strip()
                
                # Simulate optimization process
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i in range(5):
                    progress_bar.progress((i + 1) / 5)
                    status_text.text(f"Optimizing... Step {i + 1}/5")
                    time.sleep(0.5)
                
                # Generate optimized tweet
                optimized_tweet = generate_demo_tweet(input_text)
                st.session_state.optimized_tweets.append({
                    'original': input_text,
                    'optimized': optimized_tweet,
                    'timestamp': time.time()
                })
                
                progress_bar.progress(1.0)
                status_text.text("✅ Optimization complete!")
                st.session_state.optimization_running = False
                st.rerun()
            else:
                st.warning("Please enter some text first!")
        
        # Display optimized tweets
        if st.session_state.optimized_tweets:
            st.subheader("🎯 Optimized Tweets")
            
            for i, tweet_data in enumerate(reversed(st.session_state.optimized_tweets[-3:])):  # Show last 3
                with st.expander(f"Optimized Tweet #{len(st.session_state.optimized_tweets) - i}", expanded=(i == 0)):
                    st.markdown(f"""
                    <div class="tweet-container">
                        <strong>Original:</strong><br>
                        {tweet_data['original']}<br><br>
                        <strong>Optimized:</strong><br>
                        {tweet_data['optimized']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Tweet metrics (demo)
                    col_eng, col_clar, col_viral = st.columns(3)
                    with col_eng:
                        st.metric("Engagement", f"{random.randint(70, 95)}%", "↗️")
                    with col_clar:
                        st.metric("Clarity", f"{random.randint(80, 98)}%", "↗️")
                    with col_viral:
                        st.metric("Viral Potential", f"{random.randint(60, 90)}%", "↗️")
    
    with col2:
        st.subheader("⚙️ Settings")
        
        # Categories
        st.write("**Evaluation Categories:**")
        for category in st.session_state.categories:
            st.write(f"• {category}")
        
        # Demo features
        st.subheader("🎮 Demo Features")
        st.write("• **Emoji Enhancement**: Adds relevant emojis")
        st.write("• **Length Optimization**: Keeps under 280 chars")
        st.write("• **Hashtag Addition**: Adds trending hashtags")
        st.write("• **Engagement Boost**: Improves viral potential")
        
        # Clear button
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.optimized_tweets = []
            st.rerun()
        
        # Instructions
        st.subheader("📖 How to Use")
        st.write("1. Enter your tweet concept")
        st.write("2. Click 'Optimize Tweet'")
        st.write("3. View the optimized result")
        st.write("4. Compare metrics")
        
        # Local version info
        st.subheader("🏠 Full Version")
        st.info("""
        For the full AI-powered version with real optimization:
        
        1. Clone the repository locally
        2. Install Ollama
        3. Run: `streamlit run local_only_app.py`
        
        This gives you access to Gemma 3:4b and other local models!
        """)

if __name__ == "__main__":
    main()
