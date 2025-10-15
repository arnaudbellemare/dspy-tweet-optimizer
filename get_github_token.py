#!/usr/bin/env python3
"""Get GitHub access token from Replit connection."""

import os
import sys
import requests
import json

def get_github_token():
    """Get GitHub token from Replit connection."""
    hostname = os.getenv("REPLIT_CONNECTORS_HOSTNAME")
    
    # Get authentication token
    x_replit_token = None
    if os.getenv("REPL_IDENTITY"):
        x_replit_token = f"repl {os.getenv('REPL_IDENTITY')}"
    elif os.getenv("WEB_REPL_RENEWAL"):
        x_replit_token = f"depl {os.getenv('WEB_REPL_RENEWAL')}"
    
    if not x_replit_token:
        print("Error: REPL_IDENTITY or WEB_REPL_RENEWAL not found", file=sys.stderr)
        return None
    
    if not hostname:
        print("Error: REPLIT_CONNECTORS_HOSTNAME not found", file=sys.stderr)
        return None
    
    # Fetch connection settings
    url = f"https://{hostname}/api/v2/connection?include_secrets=true&connector_names=github"
    
    try:
        response = requests.get(
            url,
            headers={
                'Accept': 'application/json',
                'X_REPLIT_TOKEN': x_replit_token
            }
        )
        response.raise_for_status()
        
        data = response.json()
        items = data.get('items', [])
        
        if not items:
            print("Error: No GitHub connection found", file=sys.stderr)
            return None
        
        connection = items[0]
        settings = connection.get('settings', {})
        
        # Try different token locations
        access_token = (
            settings.get('access_token') or 
            settings.get('oauth', {}).get('credentials', {}).get('access_token')
        )
        
        if not access_token:
            print("Error: Access token not found in connection settings", file=sys.stderr)
            print(f"Available settings keys: {list(settings.keys())}", file=sys.stderr)
            return None
        
        return access_token
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching connection: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    token = get_github_token()
    if token:
        print(token)
        sys.exit(0)
    else:
        sys.exit(1)
