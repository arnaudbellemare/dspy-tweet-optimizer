#!/usr/bin/env python3
"""
Test script to simulate what models are available on Streamlit Cloud.
"""

import socket

def mock_ollama_unavailable():
    """Mock the scenario where Ollama is not available (like on Streamlit Cloud)."""
    # Temporarily override the is_ollama_available function
    import utils
    
    def mock_is_ollama_available():
        return False
    
    # Replace the function
    original_function = utils.is_ollama_available
    utils.is_ollama_available = mock_is_ollama_available
    
    try:
        # Test what models would be available
        available_models = utils.get_available_models()
        
        print("🌐 Streamlit Cloud Deployment - Available Models:")
        print("=" * 50)
        for name, model in available_models.items():
            print(f"✅ {name}: {model}")
        
        print(f"\n📊 Total models available: {len(available_models)}")
        
        # Check if any Ollama models are present
        ollama_models = [name for name, model in available_models.items() if model.startswith("ollama/")]
        if ollama_models:
            print(f"❌ Ollama models still present: {ollama_models}")
        else:
            print("✅ No Ollama models present (correct for cloud deployment)")
            
    finally:
        # Restore original function
        utils.is_ollama_available = original_function

def test_local_deployment():
    """Test what models are available locally (with Ollama running)."""
    import utils
    
    print("\n🏠 Local Deployment - Available Models:")
    print("=" * 50)
    
    available_models = utils.get_available_models()
    for name, model in available_models.items():
        print(f"✅ {name}: {model}")
    
    print(f"\n📊 Total models available: {len(available_models)}")
    
    # Check if Ollama models are present
    ollama_models = [name for name, model in available_models.items() if model.startswith("ollama/")]
    if ollama_models:
        print(f"✅ Ollama models available: {ollama_models}")
    else:
        print("❌ No Ollama models available")

if __name__ == "__main__":
    print("🧪 Testing Model Availability for Different Deployment Scenarios")
    print("=" * 70)
    
    test_local_deployment()
    mock_ollama_unavailable()
    
    print("\n" + "=" * 70)
    print("🎯 Summary:")
    print("- Local deployment: Shows all models including Ollama models")
    print("- Streamlit Cloud: Only shows cloud-compatible models")
    print("- Gemma 3:4b (Local) only appears when Ollama is running")
    print("- Gemma 2 4B is available via OpenRouter for cloud deployment")
