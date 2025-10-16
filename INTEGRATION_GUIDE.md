# Enhanced DSPy Tweet Optimizer - Integration Guide

This guide explains how to integrate the advanced AI frameworks (Perplexity, local LLMs, GEPA-ACE, Ax LLM) with the existing DSPy tweet optimizer.

## 🎯 What We've Built

### Core Integration Components

1. **Advanced LLM Manager** (`advanced_llm_manager.py`)
   - Unified interface for multiple LLM providers
   - Ollama integration for local processing
   - Perplexity API integration for web search
   - OpenRouter integration for cloud models
   - GEPA-ACE context optimization
   - Ax LLM framework for model orchestration

2. **Enhanced DSPy Modules** (`enhanced_dspy_modules.py`)
   - Web search capabilities for tweet optimization
   - Enhanced context awareness
   - Real-time information integration
   - Advanced reasoning with current trends

3. **Enhanced UI Components** (`enhanced_ui_components.py`)
   - Multi-provider status monitoring
   - Strategy selection interface
   - Performance metrics dashboard
   - Web context display

4. **Enhanced Application** (`enhanced_app.py`)
   - Complete integration of all advanced features
   - Hybrid optimization strategies
   - Real-time provider switching
   - Advanced analytics

## 🚀 Quick Start

### 1. Automated Setup
```bash
# Run the setup script
python setup_advanced_system.py
```

### 2. Manual Setup

#### Install Ollama (for local LLMs)
```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama
ollama serve

# Install models
ollama pull llama3.2:latest
ollama pull mistral:latest
```

#### Set up API Keys
```bash
# Perplexity API (for web search)
export PERPLEXITY_API_KEY='your-perplexity-key'

# OpenRouter API (for cloud models)
export OPENROUTER_API_KEY='your-openrouter-key'
```

### 3. Run the Enhanced System
```bash
# Test the system
python test_enhanced_system.py

# Run the enhanced application
streamlit run enhanced_app.py
```

## 🔧 Integration Architecture

### Multi-LLM Provider System

```python
from advanced_llm_manager import setup_advanced_llm_system, advanced_llm_manager

# Initialize the system
setup_advanced_llm_system()

# Use any provider
response = advanced_llm_manager.generate(
    prompt="Your prompt here",
    provider="ollama_llama3.2"  # or "perplexity_sonar", etc.
)
```

### GEPA-ACE Context Optimization

```python
from advanced_llm_manager import GEPAACEOptimizer

optimizer = GEPAACEOptimizer()
optimized_context = optimizer.optimize_context(
    prompt="Your prompt",
    context="Long context text...",
    target_length=1000
)
```

### Web Search Integration

```python
from enhanced_dspy_modules import WebSearchModule

web_search = WebSearchModule()
context = web_search.search_relevant_context("AI trends 2024")
```

### Enhanced Tweet Optimization

```python
from enhanced_dspy_modules import get_enhanced_modules

enhanced_modules = get_enhanced_modules()
generator = enhanced_modules["generator"]
evaluator = enhanced_modules["evaluator"]

# Generate with web context
tweet = generator.forward("Your input text")
```

## 🎯 Optimization Strategies

### 1. Local Fast Strategy
- **Use Case**: Quick, private processing
- **Providers**: Ollama models
- **Best For**: Personal use, sensitive content

```python
strategy = "local_fast"
response = advanced_llm_manager.generate(
    prompt="Your prompt",
    provider="ollama_llama3.2"
)
```

### 2. Web Enhanced Strategy
- **Use Case**: Current trends and real-time information
- **Providers**: Perplexity API
- **Best For**: Marketing, news, trending topics

```python
strategy = "web_enhanced"
response = advanced_llm_manager.generate(
    prompt="Your prompt",
    provider="perplexity_sonar",
    use_context_optimization=True
)
```

### 3. Hybrid Balanced Strategy
- **Use Case**: Automatic optimization
- **Providers**: All available providers
- **Best For**: Production use, maximum quality

```python
# Enable hybrid mode
advanced_llm_manager.set_hybrid_mode(True)

# Automatic provider selection
response = advanced_llm_manager.generate("Your prompt")
```

## 📊 Performance Monitoring

### Real-time Status
```python
status = advanced_llm_manager.get_status()
print(f"Available providers: {len(status['providers'])}")
print(f"Hybrid mode: {status['hybrid_mode']}")
```

### Performance Metrics
```python
ax_stats = status["ax_manager_stats"]
performance = ax_stats["performance_metrics"]

for provider, metrics in performance.items():
    print(f"{provider}: {metrics['successes']} successes, {metrics['failures']} failures")
```

## 🔍 Advanced Features

### 1. Custom Provider Integration

```python
from advanced_llm_manager import BaseLLMProvider, LLMConfig, LLMProvider

class CustomProvider(BaseLLMProvider):
    def generate(self, prompt: str, **kwargs) -> str:
        # Your custom implementation
        return "Generated response"
    
    def is_available(self) -> bool:
        return True

# Add custom provider
config = LLMConfig(provider=LLMProvider.OLLAMA, model_name="custom")
custom_provider = CustomProvider(config)
advanced_llm_manager.add_provider("custom", custom_provider)
```

### 2. Custom Optimization Strategies

```python
from enhanced_constants import OPTIMIZATION_STRATEGIES

# Add custom strategy
OPTIMIZATION_STRATEGIES["custom_strategy"] = {
    "name": "Custom Strategy",
    "description": "Your custom optimization approach",
    "providers": ["ollama", "perplexity"],
    "use_web_search": True,
    "use_context_optimization": True
}
```

### 3. Advanced Context Optimization

```python
from advanced_llm_manager import GEPAACEOptimizer

optimizer = GEPAACEOptimizer()

# Custom optimization parameters
optimized = optimizer.optimize_context(
    prompt="Your prompt",
    context="Your context",
    target_length=500,  # Custom target length
    compression_ratio=0.8  # Custom compression
)
```

## 🧪 Testing and Validation

### System Tests
```bash
# Run comprehensive tests
python test_enhanced_system.py

# Test specific components
python -c "from advanced_llm_manager import setup_advanced_llm_system; setup_advanced_llm_system()"
```

### Provider Tests
```bash
# Test Ollama
ollama list
curl http://localhost:11434/api/tags

# Test Perplexity
curl -H "Authorization: Bearer $PERPLEXITY_API_KEY" https://api.perplexity.ai/models

# Test OpenRouter
curl -H "Authorization: Bearer $OPENROUTER_API_KEY" https://openrouter.ai/api/v1/models
```

## 🚀 Deployment Options

### Local Development
```bash
streamlit run enhanced_app.py --server.port 8501
```

### Production Deployment
```bash
# Docker deployment
docker build -t enhanced-tweet-optimizer .
docker run -p 8501:8501 enhanced-tweet-optimizer

# Cloud deployment
# Deploy to Streamlit Cloud, AWS, GCP, or Azure
```

## 🔧 Configuration

### Environment Variables
```bash
# Required for Perplexity
PERPLEXITY_API_KEY=your-key

# Required for OpenRouter
OPENROUTER_API_KEY=your-key

# Optional Ollama configuration
OLLAMA_BASE_URL=http://localhost:11434
```

### Configuration Files
- `enhanced_constants.py`: Main configuration
- `advanced_config.json`: Runtime configuration
- `.env`: Environment variables

## 🐛 Troubleshooting

### Common Issues

#### Ollama Not Starting
```bash
# Check installation
ollama --version

# Start service
ollama serve

# Check status
curl http://localhost:11434/api/tags
```

#### API Key Issues
```bash
# Check environment variables
echo $PERPLEXITY_API_KEY
echo $OPENROUTER_API_KEY

# Test API keys
python -c "import os; print('Keys available:', bool(os.getenv('PERPLEXITY_API_KEY')))"
```

#### Import Errors
```bash
# Install dependencies
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.11+
```

## 📈 Performance Optimization

### For Local Processing
- Use smaller models for faster inference
- Enable GPU acceleration if available
- Adjust context length based on needs

### For Web Search
- Cache search results to reduce API calls
- Use specific search queries for better results
- Monitor API usage and costs

### For Hybrid Mode
- Monitor provider performance metrics
- Adjust routing rules based on usage patterns
- Use fallback providers for reliability

## 🤝 Contributing

### Development Setup
```bash
# Clone repository
git clone https://github.com/arnaudbellemare/dspy-tweet-optimizer.git
cd dspy-tweet-optimizer

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run enhanced tests
python test_enhanced_system.py
```

### Adding New Providers
1. Create a new provider class inheriting from `BaseLLMProvider`
2. Implement `generate()` and `is_available()` methods
3. Add provider to the manager using `add_provider()`
4. Update configuration in `enhanced_constants.py`

### Adding New Strategies
1. Define strategy in `OPTIMIZATION_STRATEGIES`
2. Implement strategy logic in `HybridOptimizationModule`
3. Add UI components for strategy selection
4. Update tests and documentation

## 📚 Additional Resources

- [DSPy Documentation](https://github.com/stanfordnlp/dspy)
- [Ollama Documentation](https://ollama.ai/docs)
- [Perplexity API Documentation](https://docs.perplexity.ai/)
- [OpenRouter Documentation](https://openrouter.ai/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 🎉 Conclusion

The Enhanced DSPy Tweet Optimizer successfully integrates:

✅ **Local LLMs** via Ollama for private, fast processing  
✅ **Perplexity API** for real-time web search and context  
✅ **GEPA-ACE** for advanced context optimization  
✅ **Ax LLM** framework for intelligent model orchestration  
✅ **Hybrid optimization** strategies for maximum flexibility  
✅ **Advanced UI** with real-time monitoring and analytics  

This creates a powerful, flexible system that can adapt to different use cases while maintaining the original DSPy tweet optimization capabilities.

---

**Ready to get started?** Run `python setup_advanced_system.py` to begin!
