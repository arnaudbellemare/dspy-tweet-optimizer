#!/usr/bin/env python3
"""
Test script for the Enhanced DSPy Tweet Optimizer.

This script tests the integration of all advanced features:
- Multi-LLM providers
- GEPA-ACE optimization
- Web search capabilities
- Enhanced modules
"""

import os
import sys
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_imports():
    """Test that all enhanced modules can be imported."""
    logger.info("Testing imports...")
    
    try:
        from advanced_llm_manager import advanced_llm_manager, setup_advanced_llm_system
        from enhanced_dspy_modules import get_enhanced_modules, initialize_enhanced_system
        from enhanced_constants import ADVANCED_MODELS, OPTIMIZATION_STRATEGIES
        from enhanced_ui_components import render_enhanced_custom_css
        logger.info("✅ All imports successful")
        return True
    except ImportError as e:
        logger.error(f"❌ Import failed: {e}")
        return False

def test_advanced_llm_manager():
    """Test the advanced LLM manager."""
    logger.info("Testing advanced LLM manager...")
    
    try:
        from advanced_llm_manager import setup_advanced_llm_system, advanced_llm_manager
        
        # Set up the system
        setup_advanced_llm_system()
        
        # Check status
        status = advanced_llm_manager.get_status()
        logger.info(f"✅ LLM Manager status: {len(status['providers'])} providers")
        
        # Test provider availability
        for provider_name, provider_info in status['providers'].items():
            status_icon = "🟢" if provider_info['available'] else "🔴"
            logger.info(f"  {status_icon} {provider_name}: {provider_info['type']}")
        
        return True
    except Exception as e:
        logger.error(f"❌ LLM Manager test failed: {e}")
        return False

def test_enhanced_modules():
    """Test the enhanced DSPy modules."""
    logger.info("Testing enhanced DSPy modules...")
    
    try:
        from enhanced_dspy_modules import get_enhanced_modules
        
        # Get enhanced modules
        enhanced_modules = get_enhanced_modules()
        
        if enhanced_modules:
            logger.info("✅ Enhanced modules loaded successfully")
            logger.info(f"  - Generator: {type(enhanced_modules['generator']).__name__}")
            logger.info(f"  - Evaluator: {type(enhanced_modules['evaluator']).__name__}")
            logger.info(f"  - Hybrid Optimizer: {type(enhanced_modules['hybrid_optimizer']).__name__}")
            return True
        else:
            logger.error("❌ Enhanced modules not available")
            return False
    except Exception as e:
        logger.error(f"❌ Enhanced modules test failed: {e}")
        return False

def test_gepa_ace():
    """Test GEPA-ACE optimization."""
    logger.info("Testing GEPA-ACE optimization...")
    
    try:
        from advanced_llm_manager import GEPAACEOptimizer
        
        optimizer = GEPAACEOptimizer()
        
        # Test context optimization
        test_context = "This is a very long context that needs to be optimized for better performance and efficiency."
        optimized = optimizer.optimize_context(
            prompt="Test prompt",
            context=test_context,
            target_length=50
        )
        
        logger.info(f"✅ GEPA-ACE optimization successful")
        logger.info(f"  Original length: {len(test_context)}")
        logger.info(f"  Optimized length: {len(optimized)}")
        
        # Test stats
        stats = optimizer.get_optimization_stats()
        logger.info(f"  Optimization stats: {stats}")
        
        return True
    except Exception as e:
        logger.error(f"❌ GEPA-ACE test failed: {e}")
        return False

def test_web_search():
    """Test web search functionality."""
    logger.info("Testing web search functionality...")
    
    try:
        from enhanced_dspy_modules import WebSearchModule
        
        web_search = WebSearchModule()
        
        # Test keyword extraction
        test_text = "AI and machine learning trends in 2024"
        keywords = web_search.extract_topic_keywords(test_text)
        
        logger.info(f"✅ Web search module loaded")
        logger.info(f"  Extracted keywords: {keywords}")
        
        # Test search (only if Perplexity API is available)
        if os.getenv("PERPLEXITY_API_KEY"):
            context = web_search.search_relevant_context("AI trends")
            if context:
                logger.info(f"  Web search successful: {len(context)} characters")
            else:
                logger.info("  Web search returned empty context")
        else:
            logger.info("  Perplexity API key not available - skipping web search test")
        
        return True
    except Exception as e:
        logger.error(f"❌ Web search test failed: {e}")
        return False

def test_optimization_strategies():
    """Test optimization strategies."""
    logger.info("Testing optimization strategies...")
    
    try:
        from enhanced_dspy_modules import HybridOptimizationModule
        from enhanced_constants import OPTIMIZATION_STRATEGIES
        
        hybrid_optimizer = HybridOptimizationModule()
        
        # Test available strategies
        available_strategies = hybrid_optimizer.get_available_strategies()
        logger.info(f"✅ Available strategies: {available_strategies}")
        
        # Test strategy configuration
        for strategy_key, strategy_info in OPTIMIZATION_STRATEGIES.items():
            logger.info(f"  - {strategy_info['name']}: {strategy_info['description']}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Optimization strategies test failed: {e}")
        return False

def test_configuration():
    """Test configuration and constants."""
    logger.info("Testing configuration...")
    
    try:
        from enhanced_constants import (
            ADVANCED_MODELS,
            OPTIMIZATION_STRATEGIES,
            GEPA_ACE_CONFIG,
            WEB_SEARCH_CONFIG,
            FEATURE_FLAGS
        )
        
        logger.info("✅ Configuration loaded successfully")
        logger.info(f"  - Advanced models: {len(ADVANCED_MODELS)}")
        logger.info(f"  - Optimization strategies: {len(OPTIMIZATION_STRATEGIES)}")
        logger.info(f"  - Feature flags: {len(FEATURE_FLAGS)}")
        
        # Test feature flags
        enabled_features = [k for k, v in FEATURE_FLAGS.items() if v]
        logger.info(f"  - Enabled features: {enabled_features}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Configuration test failed: {e}")
        return False

def test_environment():
    """Test environment setup."""
    logger.info("Testing environment setup...")
    
    # Check API keys
    perplexity_key = os.getenv("PERPLEXITY_API_KEY")
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    
    logger.info("✅ Environment check:")
    logger.info(f"  - Perplexity API: {'✅ Available' if perplexity_key else '❌ Not set'}")
    logger.info(f"  - OpenRouter API: {'✅ Available' if openrouter_key else '❌ Not set'}")
    
    # Check Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    logger.info(f"  - Python version: {python_version}")
    
    return True

def run_all_tests():
    """Run all tests."""
    logger.info("🚀 Starting Enhanced DSPy Tweet Optimizer Tests")
    logger.info("=" * 60)
    
    tests = [
        ("Environment Setup", test_environment),
        ("Imports", test_imports),
        ("Configuration", test_configuration),
        ("Advanced LLM Manager", test_advanced_llm_manager),
        ("Enhanced Modules", test_enhanced_modules),
        ("GEPA-ACE Optimization", test_gepa_ace),
        ("Web Search", test_web_search),
        ("Optimization Strategies", test_optimization_strategies),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"\n🧪 Running {test_name} test...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("📊 Test Results Summary:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"  {status} {test_name}")
        if result:
            passed += 1
    
    logger.info(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Enhanced system is ready to use.")
        logger.info("Run: streamlit run enhanced_app.py")
    else:
        logger.warning(f"⚠️  {total - passed} tests failed. Check the logs above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
