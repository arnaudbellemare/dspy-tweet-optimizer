#!/usr/bin/env python3
"""
Setup script for the Enhanced DSPy Tweet Optimizer.

This script helps users configure:
- Ollama installation and setup
- Perplexity API key configuration
- OpenRouter API key setup
- System verification and testing
"""

import os
import sys
import subprocess
import json
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class AdvancedSystemSetup:
    """Setup manager for the enhanced system."""
    
    def __init__(self):
        self.config_file = "advanced_config.json"
        self.setup_log = []
    
    def log(self, message: str, level: str = "INFO"):
        """Log setup messages."""
        print(f"[{level}] {message}")
        self.setup_log.append(f"[{level}] {message}")
    
    def check_python_version(self) -> bool:
        """Check if Python version is compatible."""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 11):
            self.log(f"Python {version.major}.{version.minor} detected. Python 3.11+ required.", "ERROR")
            return False
        
        self.log(f"Python {version.major}.{version.minor} detected - compatible", "SUCCESS")
        return True
    
    def install_dependencies(self) -> bool:
        """Install required dependencies."""
        self.log("Installing enhanced dependencies...")
        
        dependencies = [
            "requests>=2.32.5",
            "dspy>=3.0.3",
            "streamlit>=1.50.0",
            "pydantic>=2.12.2"
        ]
        
        try:
            for dep in dependencies:
                self.log(f"Installing {dep}...")
                result = subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                                      capture_output=True, text=True)
                if result.returncode != 0:
                    self.log(f"Failed to install {dep}: {result.stderr}", "ERROR")
                    return False
            
            self.log("All dependencies installed successfully", "SUCCESS")
            return True
            
        except Exception as e:
            self.log(f"Error installing dependencies: {e}", "ERROR")
            return False
    
    def check_ollama_installation(self) -> Tuple[bool, str]:
        """Check if Ollama is installed and running."""
        self.log("Checking Ollama installation...")
        
        # Check if ollama command exists
        try:
            result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                self.log(f"Ollama found: {version}", "SUCCESS")
                
                # Check if Ollama service is running
                try:
                    response = requests.get("http://localhost:11434/api/tags", timeout=5)
                    if response.status_code == 200:
                        self.log("Ollama service is running", "SUCCESS")
                        return True, version
                    else:
                        self.log("Ollama service not responding", "WARNING")
                        return False, version
                except requests.exceptions.RequestException:
                    self.log("Ollama service not running. Please start it with: ollama serve", "WARNING")
                    return False, version
            else:
                self.log("Ollama not found in PATH", "ERROR")
                return False, ""
                
        except FileNotFoundError:
            self.log("Ollama not installed", "ERROR")
            return False, ""
    
    def install_ollama_models(self) -> bool:
        """Install recommended Ollama models."""
        self.log("Installing recommended Ollama models...")
        
        recommended_models = [
            "llama3.2:latest",
            "mistral:latest",
            "codellama:latest"
        ]
        
        success_count = 0
        for model in recommended_models:
            try:
                self.log(f"Installing {model}...")
                result = subprocess.run(["ollama", "pull", model], 
                                      capture_output=True, text=True, timeout=300)
                if result.returncode == 0:
                    self.log(f"Successfully installed {model}", "SUCCESS")
                    success_count += 1
                else:
                    self.log(f"Failed to install {model}: {result.stderr}", "WARNING")
            except subprocess.TimeoutExpired:
                self.log(f"Timeout installing {model} - this is normal for large models", "WARNING")
            except Exception as e:
                self.log(f"Error installing {model}: {e}", "WARNING")
        
        if success_count > 0:
            self.log(f"Installed {success_count}/{len(recommended_models)} models", "SUCCESS")
            return True
        else:
            self.log("No models installed successfully", "ERROR")
            return False
    
    def setup_perplexity_api(self) -> bool:
        """Guide user through Perplexity API setup."""
        self.log("Setting up Perplexity API...")
        
        print("\n" + "="*60)
        print("PERPLEXITY API SETUP")
        print("="*60)
        print("1. Go to https://www.perplexity.ai/settings/api")
        print("2. Create an account or sign in")
        print("3. Generate an API key")
        print("4. Copy the API key")
        print("="*60)
        
        api_key = input("Enter your Perplexity API key (or press Enter to skip): ").strip()
        
        if api_key:
            # Test the API key
            try:
                headers = {"Authorization": f"Bearer {api_key}"}
                response = requests.get("https://api.perplexity.ai/models", headers=headers, timeout=10)
                
                if response.status_code == 200:
                    self.log("Perplexity API key is valid", "SUCCESS")
                    return self.save_api_key("PERPLEXITY_API_KEY", api_key)
                else:
                    self.log(f"Invalid Perplexity API key: {response.status_code}", "ERROR")
                    return False
            except Exception as e:
                self.log(f"Error testing Perplexity API: {e}", "ERROR")
                return False
        else:
            self.log("Skipping Perplexity API setup", "INFO")
            return True
    
    def setup_openrouter_api(self) -> bool:
        """Guide user through OpenRouter API setup."""
        self.log("Setting up OpenRouter API...")
        
        print("\n" + "="*60)
        print("OPENROUTER API SETUP")
        print("="*60)
        print("1. Go to https://openrouter.ai/")
        print("2. Create an account or sign in")
        print("3. Go to Keys section")
        print("4. Generate an API key")
        print("5. Copy the API key")
        print("="*60)
        
        api_key = input("Enter your OpenRouter API key (or press Enter to skip): ").strip()
        
        if api_key:
            # Test the API key
            try:
                headers = {"Authorization": f"Bearer {api_key}"}
                response = requests.get("https://openrouter.ai/api/v1/models", headers=headers, timeout=10)
                
                if response.status_code == 200:
                    self.log("OpenRouter API key is valid", "SUCCESS")
                    return self.save_api_key("OPENROUTER_API_KEY", api_key)
                else:
                    self.log(f"Invalid OpenRouter API key: {response.status_code}", "ERROR")
                    return False
            except Exception as e:
                self.log(f"Error testing OpenRouter API: {e}", "ERROR")
                return False
        else:
            self.log("Skipping OpenRouter API setup", "INFO")
            return True
    
    def save_api_key(self, key_name: str, api_key: str) -> bool:
        """Save API key to environment file."""
        try:
            env_file = Path(".env")
            
            # Read existing .env file
            env_content = ""
            if env_file.exists():
                env_content = env_file.read_text()
            
            # Update or add the API key
            lines = env_content.split('\n')
            key_found = False
            
            for i, line in enumerate(lines):
                if line.startswith(f"{key_name}="):
                    lines[i] = f"{key_name}={api_key}"
                    key_found = True
                    break
            
            if not key_found:
                lines.append(f"{key_name}={api_key}")
            
            # Write back to file
            env_file.write_text('\n'.join(lines))
            self.log(f"Saved {key_name} to .env file", "SUCCESS")
            
            # Also set environment variable for current session
            os.environ[key_name] = api_key
            
            return True
            
        except Exception as e:
            self.log(f"Error saving API key: {e}", "ERROR")
            return False
    
    def create_advanced_config(self) -> bool:
        """Create advanced configuration file."""
        self.log("Creating advanced configuration...")
        
        config = {
            "version": "1.0.0",
            "setup_date": str(Path().cwd()),
            "features": {
                "ollama_enabled": False,
                "perplexity_enabled": False,
                "openrouter_enabled": False,
                "web_search_enabled": False,
                "context_optimization_enabled": True,
                "hybrid_mode_enabled": True
            },
            "models": {
                "ollama_models": [],
                "default_ollama_model": "llama3.2:latest",
                "default_perplexity_model": "llama-3.1-sonar-small-128k-online",
                "default_openrouter_model": "openrouter/anthropic/claude-sonnet-4.5"
            },
            "optimization": {
                "default_strategy": "hybrid_balanced",
                "max_iterations": 10,
                "patience": 5,
                "use_web_search": True,
                "use_context_optimization": True
            }
        }
        
        # Update config based on what's available
        ollama_available, ollama_version = self.check_ollama_installation()
        config["features"]["ollama_enabled"] = ollama_available
        
        if os.getenv("PERPLEXITY_API_KEY"):
            config["features"]["perplexity_enabled"] = True
            config["features"]["web_search_enabled"] = True
        
        if os.getenv("OPENROUTER_API_KEY"):
            config["features"]["openrouter_enabled"] = True
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            self.log(f"Configuration saved to {self.config_file}", "SUCCESS")
            return True
            
        except Exception as e:
            self.log(f"Error creating configuration: {e}", "ERROR")
            return False
    
    def test_system(self) -> bool:
        """Test the enhanced system."""
        self.log("Testing enhanced system...")
        
        try:
            # Import and test advanced modules
            from advanced_llm_manager import setup_advanced_llm_system
            from enhanced_dspy_modules import initialize_enhanced_system
            
            # Set up system
            setup_advanced_llm_system()
            enhanced_modules = initialize_enhanced_system()
            
            # Test basic functionality
            if enhanced_modules:
                self.log("Enhanced system test passed", "SUCCESS")
                return True
            else:
                self.log("Enhanced system test failed", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"System test failed: {e}", "ERROR")
            return False
    
    def run_setup(self) -> bool:
        """Run the complete setup process."""
        self.log("Starting Enhanced DSPy Tweet Optimizer Setup", "INFO")
        self.log("="*60, "INFO")
        
        success = True
        
        # Check Python version
        if not self.check_python_version():
            return False
        
        # Install dependencies
        if not self.install_dependencies():
            success = False
        
        # Check Ollama
        ollama_available, _ = self.check_ollama_installation()
        if ollama_available:
            self.install_ollama_models()
        
        # Setup APIs
        if not self.setup_perplexity_api():
            success = False
        
        if not self.setup_openrouter_api():
            success = False
        
        # Create configuration
        if not self.create_advanced_config():
            success = False
        
        # Test system
        if not self.test_system():
            success = False
        
        # Final report
        self.log("="*60, "INFO")
        if success:
            self.log("Setup completed successfully!", "SUCCESS")
            self.log("You can now run: streamlit run enhanced_app.py", "INFO")
        else:
            self.log("Setup completed with warnings/errors", "WARNING")
            self.log("Check the log above for details", "INFO")
        
        return success

def main():
    """Main setup function."""
    setup = AdvancedSystemSetup()
    
    print("Enhanced DSPy Tweet Optimizer Setup")
    print("="*50)
    print("This script will help you configure the enhanced system with:")
    print("- Ollama for local LLM processing")
    print("- Perplexity API for web search")
    print("- OpenRouter API for cloud models")
    print("- Advanced optimization features")
    print("="*50)
    
    response = input("Continue with setup? (y/N): ").strip().lower()
    if response in ['y', 'yes']:
        setup.run_setup()
    else:
        print("Setup cancelled.")

if __name__ == "__main__":
    main()
