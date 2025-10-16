#!/usr/bin/env python3
"""
Test script to verify Gemma 3:4b configuration.
"""

import sys
import os

def test_configuration():
    """Test the Gemma 3:4b configuration."""
    print("🧪 Testing Gemma 3:4b Configuration")
    print("=" * 50)
    
    # Test 1: Import enhanced constants
    try:
        from enhanced_constants import ADVANCED_MODELS, AX_LLM_CONFIG
        print("✅ Enhanced constants imported successfully")
        
        # Check if Gemma 3:4b is configured
        if "Ollama Gemma 3 4B" in ADVANCED_MODELS:
            gemma_config = ADVANCED_MODELS["Ollama Gemma 3 4B"]
            print(f"✅ Gemma 3:4b found in configuration")
            print(f"   Model: {gemma_config['model']}")
            print(f"   Provider: {gemma_config['provider']}")
            print(f"   Capabilities: {gemma_config['capabilities']}")
        else:
            print("❌ Gemma 3:4b not found in ADVANCED_MODELS")
            
        # Check fallback provider
        if AX_LLM_CONFIG.get("fallback_provider") == "ollama_gemma3_4b":
            print("✅ Fallback provider correctly set to ollama_gemma3_4b")
        else:
            print(f"❌ Fallback provider incorrect: {AX_LLM_CONFIG.get('fallback_provider')}")
            
    except Exception as e:
        print(f"❌ Error importing enhanced constants: {e}")
    
    # Test 2: Import advanced LLM manager
    try:
        from advanced_llm_manager import AdvancedLLMManager, LLMConfig, LLMProvider
        print("✅ Advanced LLM manager imported successfully")
        
        # Test creating a Gemma 3:4b config
        gemma_config = LLMConfig(
            provider=LLMProvider.OLLAMA,
            model_name="gemma3:4b",
            base_url="http://localhost:11434"
        )
        print("✅ Gemma 3:4b LLM config created successfully")
        
    except Exception as e:
        print(f"❌ Error with advanced LLM manager: {e}")
    
    # Test 3: Import enhanced DSPy modules
    try:
        from enhanced_dspy_modules import HybridOptimizationModule
        print("✅ Enhanced DSPy modules imported successfully")
        
        # Test creating optimization module
        opt_module = HybridOptimizationModule()
        if opt_module.optimization_strategies.get("local_fast") == "ollama_gemma3_4b":
            print("✅ Local fast strategy correctly configured for Gemma 3:4b")
        else:
            print(f"❌ Local fast strategy incorrect: {opt_module.optimization_strategies.get('local_fast')}")
            
    except Exception as e:
        print(f"❌ Error with enhanced DSPy modules: {e}")
    
    # Test 4: Check if Ollama is available
    print("\n🔍 Checking Ollama Availability:")
    try:
        import subprocess
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ Ollama is installed: {result.stdout.strip()}")
            
            # Check if Gemma 3:4b is available
            list_result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
            if list_result.returncode == 0:
                if 'gemma3:4b' in list_result.stdout:
                    print("✅ Gemma 3:4b model is installed")
                else:
                    print("⚠️  Gemma 3:4b model not found in installed models")
                    print("   Available models:")
                    for line in list_result.stdout.split('\n'):
                        if line.strip():
                            print(f"   - {line.strip()}")
            else:
                print("❌ Could not list Ollama models")
        else:
            print("❌ Ollama not found or not working")
    except subprocess.TimeoutExpired:
        print("❌ Ollama command timed out")
    except FileNotFoundError:
        print("❌ Ollama not installed")
    except Exception as e:
        print(f"❌ Error checking Ollama: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Configuration Test Complete!")

def show_setup_instructions():
    """Show setup instructions for Gemma 3:4b."""
    print("\n📋 Setup Instructions for Gemma 3:4b:")
    print("=" * 50)
    
    print("1. Install Ollama:")
    print("   macOS: brew install ollama")
    print("   Linux: curl -fsSL https://ollama.ai/install.sh | sh")
    print("   Windows: Download from https://ollama.ai/download")
    
    print("\n2. Start Ollama service:")
    print("   ollama serve")
    
    print("\n3. Install Gemma 3:4b model:")
    print("   ollama pull gemma3:4b")
    
    print("\n4. Verify installation:")
    print("   ollama list")
    
    print("\n5. Test the model:")
    print("   ollama run gemma3:4b")
    
    print("\n6. Run your enhanced app:")
    print("   streamlit run simple_enhanced_app.py")

if __name__ == "__main__":
    test_configuration()
    show_setup_instructions()
