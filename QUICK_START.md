# 🚀 Quick Start Guide

## 🎯 **Choose Your Setup:**

### **Option 1: Local Only (No API Keys Required)**
Perfect if you want to use your local Ollama models without any API keys.

**Run:**
```bash
streamlit run local_only_app.py
```

**Available Models:**
- Gemma 3 4B (Local)
- Llama 3.2 3B (Local) 
- Llama 3.2 1B (Local)
- Mistral 7B (Local)
- CodeLlama 7B (Local)

**Requirements:**
- Ollama installed and running
- At least one model installed (e.g., `ollama pull gemma3:4b`)

---

### **Option 2: Cloud Models (Requires OpenRouter API Key)**
Use powerful cloud models like Claude, Gemini, etc.

**Setup API Key:**
```bash
export OPENROUTER_API_KEY='sk-or-v1-your-api-key-here'
```

**Run:**
```bash
streamlit run simple_enhanced_app.py
```

**Available Models:**
- Claude Sonnet 4.5
- Opus 4.1
- Gemini 2.5 Flash
- Gemini 2.5 Pro
- GPT-5
- Gemma 2 4B (cloud version)

---

### **Option 3: Original App (Guaranteed to Work)**
The original, stable version.

**Run:**
```bash
streamlit run app.py
```

---

## 🔧 **Quick Setup for Local Only:**

1. **Install Ollama:**
   ```bash
   brew install ollama  # macOS
   ```

2. **Start Ollama:**
   ```bash
   ollama serve
   ```

3. **Install a model:**
   ```bash
   ollama pull gemma3:4b
   ```

4. **Run the app:**
   ```bash
   streamlit run local_only_app.py
   ```

5. **Start optimizing tweets!** 🎉

---

## 🌐 **For Streamlit Cloud Deployment:**

**Use:** `simple_enhanced_app_fallback.py` as your main file

**Add your OpenRouter API key in Streamlit Cloud secrets:**
```toml
OPENROUTER_API_KEY = "sk-or-v1-your-api-key-here"
```

---

## 🆘 **Troubleshooting:**

**"OPENROUTER_API_KEY environment variable is required"**
- Use `local_only_app.py` instead, or
- Set up your OpenRouter API key

**"Ollama is not running"**
- Run `ollama serve` in a terminal
- Make sure Ollama is installed

**"Model not found"**
- Install the model: `ollama pull gemma3:4b`
- Check available models: `ollama list`

---

## 🎯 **Recommended for You:**

Since you want to use Gemma 3:4b locally, use:

```bash
streamlit run local_only_app.py
```

This will work perfectly with your local Ollama setup and Gemma 3:4b! 🚀
