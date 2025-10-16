# 🔑 Perplexity API Key Setup Guide

## 📍 **Where to Add Your Perplexity API Key**

### **Option 1: Streamlit Cloud (For Deployment)**

1. **Go to your Streamlit Cloud dashboard**
   - Visit: https://share.streamlit.io/
   - Sign in with your GitHub account

2. **Select your app**
   - Click on your deployed app

3. **Access Settings**
   - Click on the **"Settings"** button (gear icon)
   - Or go to the **"Secrets"** tab

4. **Add the API Key**
   - Click **"Add new secret"**
   - **Key**: `PERPLEXITY_API_KEY`
   - **Value**: Your Perplexity API key (starts with `pplx-...`)

5. **Save and Restart**
   - Click **"Save"**
   - Your app will automatically restart with the new secret

### **Option 2: Local Development**

#### **Method 1: Environment Variable**
```bash
export PERPLEXITY_API_KEY='pplx-your-api-key-here'
```

#### **Method 2: .env File**
Create a `.env` file in your project root:
```
PERPLEXITY_API_KEY=pplx-your-api-key-here
```

#### **Method 3: Streamlit Secrets (Local)**
Create `.streamlit/secrets.toml`:
```toml
PERPLEXITY_API_KEY = "pplx-your-api-key-here"
```

## 🎯 **What Your Perplexity API Key Enables**

### **Web Search Features:**
- ✅ **Real-time information** gathering
- ✅ **Current trends** and news integration
- ✅ **Enhanced context** for tweet optimization
- ✅ **Trend awareness** for viral potential

### **Optimization Strategies:**
- 🚀 **Web Enhanced Strategy**: Uses Perplexity for real-time context
- 🚀 **Hybrid Balanced Strategy**: Combines local Gemma 3 4B + Perplexity
- 🚀 **Smart Routing**: Automatically selects best provider

## 🔍 **How to Get Your Perplexity API Key**

1. **Go to Perplexity AI**
   - Visit: https://www.perplexity.ai/

2. **Sign up or Sign in**
   - Create an account or log in

3. **Go to API Settings**
   - Visit: https://www.perplexity.ai/settings/api

4. **Generate API Key**
   - Click "Generate API Key"
   - Copy the key (starts with `pplx-`)

5. **Add Credits (if needed)**
   - Perplexity API requires credits
   - Add credits to your account for usage

## 🧪 **Test Your Setup**

### **Check if API Key is Working:**
```bash
python3 -c "
import os
key = os.getenv('PERPLEXITY_API_KEY')
if key:
    print('✅ Perplexity API key is set')
    print(f'Key starts with: {key[:10]}...')
else:
    print('❌ Perplexity API key not found')
"
```

### **Test Enhanced System:**
```bash
python3 test_enhanced_system.py
```

Look for:
```
✅ Perplexity provider added successfully
✅ Web search module loaded
```

## 🎛️ **Configuration in the App**

Once your API key is set, you'll see:

### **Provider Status:**
- 🟢 **Perplexity Sonar**: Available for web search

### **Available Strategies:**
- **Local Fast**: Uses Gemma 3 4B only
- **Web Enhanced**: Uses Perplexity for web search
- **Hybrid Balanced**: Automatically selects best provider

### **Enhanced Features:**
- **Web Context Display**: Shows real-time information used
- **Trend Awareness**: Incorporates current events and trends
- **Advanced Analytics**: Tracks web search usage

## 💡 **Usage Tips**

### **For Best Results:**
1. **Use Hybrid Balanced Strategy** for automatic optimization
2. **Enable Web Search** for trending topics and current events
3. **Monitor Performance** to see which provider works best
4. **Check Web Context** to see what information is being used

### **Cost Management:**
- **Perplexity API** charges per request
- **Local Gemma 3 4B** is free to use
- **Hybrid mode** balances cost and quality

## 🐛 **Troubleshooting**

### **API Key Not Working:**
- ✅ Verify the key starts with `pplx-`
- ✅ Check you have credits in your Perplexity account
- ✅ Ensure the key is set correctly in Streamlit Cloud secrets

### **Web Search Not Available:**
- ✅ Check provider status in the app
- ✅ Verify API key is accessible
- ✅ Test with a simple request

### **Performance Issues:**
- ✅ Web search adds 2-5 seconds to processing time
- ✅ Use Local Fast strategy for speed
- ✅ Use Web Enhanced for quality

---

## 🎉 **You're Ready!**

With your Perplexity API key configured, you now have:
- 🤖 **Local Gemma 3 4B** for fast, private processing
- 🌐 **Perplexity Web Search** for real-time information
- 🎯 **Hybrid Intelligence** for optimal results

**Your Enhanced DSPy Tweet Optimizer is now fully powered!** 🚀
