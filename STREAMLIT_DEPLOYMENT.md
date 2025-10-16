# Streamlit Cloud Deployment Guide

This guide will help you deploy the Enhanced DSPy Tweet Optimizer to Streamlit Cloud.

## 🚀 Quick Deployment

### 1. Prepare Your Repository

Make sure your repository contains:
- ✅ `enhanced_app.py` (main application)
- ✅ `requirements.txt` (dependencies)
- ✅ `.streamlit/config.toml` (Streamlit configuration)
- ✅ All Python modules (`.py` files)
- ✅ `README.md` (documentation)

### 2. Deploy to Streamlit Cloud

1. **Go to [Streamlit Cloud](https://share.streamlit.io/)**
2. **Sign in with your GitHub account**
3. **Click "New app"**
4. **Select your repository**
5. **Configure the app:**
   - **Main file path**: `enhanced_app.py`
   - **Branch**: `main` (or your default branch)
   - **Python version**: `3.11` (recommended)

### 3. Set Environment Variables (Optional)

For enhanced features, set these secrets in Streamlit Cloud:

#### **Perplexity API (for web search)**
- **Key**: `PERPLEXITY_API_KEY`
- **Value**: Your Perplexity API key

#### **OpenRouter API (for cloud models)**
- **Key**: `OPENROUTER_API_KEY`
- **Value**: Your OpenRouter API key

## 🔧 Configuration Options

### Basic Deployment (No API Keys)
- ✅ **Works out of the box**
- ✅ **Uses original DSPy functionality**
- ✅ **No external dependencies required**

### Enhanced Deployment (With API Keys)
- 🚀 **Web search capabilities**
- 🚀 **Cloud model access**
- 🚀 **Advanced optimization strategies**

## 📋 Deployment Checklist

### Before Deployment
- [ ] Repository is clean and organized
- [ ] All dependencies are in `requirements.txt`
- [ ] `enhanced_app.py` is the main file
- [ ] `.streamlit/config.toml` is configured
- [ ] README.md is updated

### After Deployment
- [ ] App loads without errors
- [ ] Basic tweet optimization works
- [ ] Enhanced features work (if API keys provided)
- [ ] Performance is acceptable

## 🐛 Troubleshooting

### Common Issues

#### **Import Errors**
```bash
# Check requirements.txt includes all dependencies
streamlit>=1.50.0
dspy>=3.0.3
pydantic>=2.12.2
requests>=2.32.5
```

#### **API Key Issues**
- Verify environment variables are set correctly
- Check API key permissions and quotas
- Test API keys locally first

#### **Performance Issues**
- Use smaller models for faster inference
- Enable caching in Streamlit
- Optimize context length

### Debug Mode

To debug issues, you can:

1. **Check Streamlit Cloud logs**
2. **Test locally first**:
   ```bash
   streamlit run enhanced_app.py
   ```
3. **Run system tests**:
   ```bash
   python test_enhanced_system.py
   ```

## 🔒 Security Considerations

### API Keys
- ✅ **Never commit API keys to repository**
- ✅ **Use Streamlit Cloud secrets**
- ✅ **Rotate keys regularly**
- ✅ **Monitor usage and costs**

### Data Privacy
- ✅ **No user data is stored permanently**
- ✅ **All processing is done in memory**
- ✅ **API calls are made securely**

## 📊 Monitoring

### Streamlit Cloud Metrics
- **App performance**
- **User engagement**
- **Error rates**
- **Resource usage**

### Custom Metrics
- **API usage tracking**
- **Cost monitoring**
- **Performance analytics**

## 🚀 Advanced Deployment

### Custom Domain
- Configure custom domain in Streamlit Cloud settings
- Update DNS records as needed

### Scaling
- Monitor resource usage
- Upgrade plan if needed
- Optimize for performance

### CI/CD Integration
- Set up GitHub Actions for automated deployment
- Configure environment-specific settings
- Implement automated testing

## 📚 Additional Resources

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [Streamlit Deployment Guide](https://docs.streamlit.io/deploy)
- [Environment Variables in Streamlit Cloud](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)

## 🎉 Success!

Once deployed, your Enhanced DSPy Tweet Optimizer will be available at:
`https://your-app-name.streamlit.app`

### Features Available:
- ✅ **Basic tweet optimization** (always works)
- ✅ **Enhanced features** (with API keys)
- ✅ **Multi-LLM support** (with configuration)
- ✅ **Web search** (with Perplexity API)
- ✅ **Advanced analytics** (with full setup)

---

**Need help?** Check the [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) for detailed setup instructions.
