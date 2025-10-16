# 🚀 Quick Setup Guide - Perplexity + Local Gemma 2 4B

This guide will help you set up the Enhanced DSPy Tweet Optimizer with your Perplexity API key and local Gemma 2 4B model.

## 🔑 **Step 1: Add Your Perplexity API Key**

### **For Streamlit Cloud Deployment:**
1. Go to your Streamlit Cloud app dashboard
2. Click on **"Settings"** or **"Secrets"**
3. Add a new secret:
   - **Key**: `PERPLEXITY_API_KEY`
   - **Value**: Your Perplexity API key (starts with `pplx-...`)

### **For Local Development:**
```bash
export PERPLEXITY_API_KEY='pplx-your-api-key-here'
```

## 🤖 **Step 2: Set Up Local Gemma 2 4B**

### **Install Ollama (if not already installed):**
```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows: Download from https://ollama.ai/download
```

### **Start Ollama Service:**
```bash
ollama serve
```

### **Install Gemma 2 4B Model:**
```bash
ollama pull gemma2:4b
```

### **Verify Installation:**
```bash
ollama list
```
You should see `gemma2:4b` in the list.

## 🎯 **Step 3: Test Your Setup**

### **Run the Test Script:**
```bash
python3 test_enhanced_system.py
```

### **Expected Output:**
```
✅ Ollama provider added successfully
✅ Perplexity provider added successfully
✅ Enhanced system initialized successfully
```

## 🚀 **Step 4: Run the Application**

### **Local Development:**
```bash
streamlit run enhanced_app.py
```

### **Streamlit Cloud:**
1. Push your code to GitHub
2. Deploy to Streamlit Cloud
3. Add your Perplexity API key in the secrets section

## 🎛️ **Available Features with Your Setup:**

### **Local Fast Strategy:**
- ✅ **Uses Gemma 2 4B** for fast, private processing
- ✅ **No internet required** for basic optimization
- ✅ **Free to use** (no API costs)

### **Web Enhanced Strategy:**
- 🚀 **Uses Perplexity** for real-time web search
- 🚀 **Current trends and information** for tweet optimization
- 🚀 **Enhanced context** from web sources

### **Hybrid Balanced Strategy:**
- 🎯 **Automatic selection** between Gemma 2 4B and Perplexity
- 🎯 **Best of both worlds** - local speed + web intelligence
- 🎯 **Smart routing** based on task requirements

## 🔧 **Configuration Details:**

### **Your Local Model:**
- **Model**: `gemma2:4b` (Gemma 2 4B)
- **Provider**: Ollama
- **Capabilities**: Text generation, local processing, fast inference
- **Base URL**: `http://localhost:11434`

### **Your Web Search:**
- **Provider**: Perplexity API
- **Model**: `llama-3.1-sonar-small-128k-online`
- **Capabilities**: Web search, real-time info, text generation

## 🎉 **What You'll Get:**

### **Basic Tweet Optimization:**
- ✅ Generate optimized tweets from your input
- ✅ Hill-climbing algorithm for continuous improvement
- ✅ Custom evaluation categories
- ✅ Real-time progress tracking

### **Enhanced Features:**
- 🚀 **Web-aware optimization** using current trends
- 🚀 **Local processing** for privacy and speed
- 🚀 **Hybrid intelligence** combining both approaches
- 🚀 **Advanced analytics** and performance monitoring

## 🐛 **Troubleshooting:**

### **Ollama Issues:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama if needed
ollama serve
```

### **Perplexity API Issues:**
- Verify your API key is correct
- Check your Perplexity account has credits
- Ensure the key starts with `pplx-`

### **Model Issues:**
```bash
# Reinstall Gemma 2 4B if needed
ollama pull gemma2:4b

# Check available models
ollama list
```

## 📊 **Performance Expectations:**

### **Local Gemma 2 4B:**
- ⚡ **Fast inference** (2-5 seconds per generation)
- 🔒 **Private processing** (no data leaves your machine)
- 💰 **Free to use** (no API costs)
- 🧠 **Good quality** for most tweet optimization tasks

### **Perplexity Web Search:**
- 🌐 **Real-time information** (current trends, news, events)
- 📈 **Enhanced context** for better optimization
- 💡 **Trend awareness** for viral potential
- ⏱️ **Slightly slower** (5-10 seconds with web search)

## 🎯 **Success Indicators:**

After setup, you should see:
- ✅ **Provider Status**: Both Ollama and Perplexity showing as available
- ✅ **Strategy Options**: Local Fast, Web Enhanced, and Hybrid Balanced
- ✅ **Optimization Working**: Tweets being generated and improved
- ✅ **Web Context**: Real-time information being used (with Perplexity)

---

## 🎉 **You're All Set!**

Your Enhanced DSPy Tweet Optimizer is now configured with:
- 🤖 **Local Gemma 2 4B** for fast, private processing
- 🌐 **Perplexity API** for web search and current trends
- 🎯 **Hybrid optimization** for the best of both worlds

**Start optimizing tweets with the power of local AI and real-time web intelligence!** 🚀
