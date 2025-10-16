#!/usr/bin/env python3
"""
Debug version of the enhanced app to test functionality.
"""

import streamlit as st
import sys
import traceback

# Page configuration
st.set_page_config(
    page_title="Debug DSPy Tweet Optimizer",
    layout="wide"
)

def main():
    st.title("🐛 Debug DSPy Tweet Optimizer")
    
    # Test basic functionality
    st.subheader("Basic Tests")
    
    # Test 1: Session State
    if 'test_counter' not in st.session_state:
        st.session_state.test_counter = 0
    
    if st.button("Test Session State"):
        st.session_state.test_counter += 1
        st.success(f"Session state works! Counter: {st.session_state.test_counter}")
    
    # Test 2: Input and Button
    st.subheader("Input Test")
    test_input = st.text_input("Enter some text:", key="test_input")
    
    if st.button("Test Button Click"):
        if test_input.strip():
            st.success(f"Button clicked! Input: '{test_input}'")
        else:
            st.warning("Please enter some text!")
    
    # Test 3: Optimization Trigger
    st.subheader("Optimization Trigger Test")
    
    if 'last_optimized' not in st.session_state:
        st.session_state.last_optimized = ""
    
    if st.button("Test Optimization Trigger"):
        if test_input.strip():
            st.session_state.last_optimized = ""
            st.success("Optimization trigger set!")
            st.rerun()
        else:
            st.warning("Please enter some text first!")
    
    # Show current state
    st.subheader("Current State")
    st.write(f"Test input: '{test_input}'")
    st.write(f"Last optimized: '{st.session_state.last_optimized}'")
    st.write(f"Should optimize: {test_input.strip() != st.session_state.last_optimized}")
    
    # Test 4: Import Tests
    st.subheader("Import Tests")
    
    try:
        from dspy_modules import TweetGeneratorModule, TweetEvaluatorModule
        st.success("✅ Original DSPy modules imported")
    except Exception as e:
        st.error(f"❌ Original DSPy modules failed: {e}")
    
    try:
        from enhanced_dspy_modules import get_enhanced_modules
        st.success("✅ Enhanced DSPy modules imported")
    except Exception as e:
        st.error(f"❌ Enhanced DSPy modules failed: {e}")
    
    try:
        from advanced_llm_manager import setup_advanced_llm_system
        st.success("✅ Advanced LLM manager imported")
    except Exception as e:
        st.error(f"❌ Advanced LLM manager failed: {e}")
    
    # Test 5: Simple Optimization Test
    st.subheader("Simple Optimization Test")
    
    if st.button("Test Simple Optimization"):
        try:
            from dspy_modules import TweetGeneratorModule
            generator = TweetGeneratorModule()
            st.success("✅ Generator created successfully")
            
            # Test generation
            test_result = generator.forward("Test tweet optimization")
            st.success(f"✅ Generation successful: '{test_result[:50]}...'")
            
        except Exception as e:
            st.error(f"❌ Simple optimization failed: {e}")
            st.code(traceback.format_exc())

if __name__ == "__main__":
    main()
