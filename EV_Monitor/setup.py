"""
Setup script for EV Neighborhood Monitor

This script helps set up the EV monitoring application with proper dependencies
and environment configuration.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_environment_variables():
    """Check for required environment variables."""
    print("\n🔑 Checking environment variables...")
    
    required_vars = {
        "ANTHROPIC_API_KEY": "Required for Strands Agents"
    }
    
    optional_vars = {
        "GOOGLE_MAPS_API_KEY": "Optional for enhanced traffic data"
    }
    
    all_good = True
    
    for var, description in required_vars.items():
        if os.getenv(var):
            print(f"✅ {var}: Set")
        else:
            print(f"❌ {var}: Not set - {description}")
            all_good = False
    
    for var, description in optional_vars.items():
        if os.getenv(var):
            print(f"✅ {var}: Set")
        else:
            print(f"⚠️  {var}: Not set - {description}")
    
    return all_good

def create_env_template():
    """Create a .env template file."""
    env_template = """# EV Neighborhood Monitor Environment Variables

# Required: Anthropic API Key for Strands Agents
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional: Google Maps API Key for enhanced traffic data
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here

# Optional: Other API keys for real data sources
EV_SALES_API_KEY=your_ev_sales_api_key_here
CHARGING_NETWORK_API_KEY=your_charging_network_api_key_here
"""
    
    env_file = Path(".env.template")
    if not env_file.exists():
        with open(env_file, "w") as f:
            f.write(env_template)
        print(f"✅ Created {env_file} - Copy to .env and add your API keys")
    else:
        print(f"ℹ️  {env_file} already exists")

def run_tests():
    """Run basic tests to verify setup."""
    print("\n🧪 Running basic tests...")
    
    try:
        # Test imports
        import strands
        import mcp
        print("✅ Core imports successful")
        
        # Test configuration
        from config import ANTHROPIC_API_KEY, MCP_SERVER_PORT
        print("✅ Configuration loaded")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def print_usage_instructions():
    """Print usage instructions."""
    print("\n📋 Usage Instructions:")
    print("=" * 50)
    print("1. Set your ANTHROPIC_API_KEY environment variable:")
    print("   export ANTHROPIC_API_KEY='your_api_key_here'")
    print("\n2. Run the main application:")
    print("   python ev_monitor_app.py")
    print("\n3. Or run the demo queries:")
    print("   python demo_queries.py")
    print("\n4. For enhanced traffic data, set GOOGLE_MAPS_API_KEY:")
    print("   export GOOGLE_MAPS_API_KEY='your_google_api_key_here'")
    print("\n📚 Example queries:")
    print("- How many EVs are in my neighborhood around coordinates 37.7749, -122.4194?")
    print("- Find charging stations within 5 miles of Seattle")
    print("- What are the EV sales trends in California?")
    print("- Analyze traffic patterns for EV areas")

def main():
    """Main setup function."""
    print("🚗 EV Neighborhood Monitor Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Check environment variables
    env_ok = check_environment_variables()
    
    # Create environment template
    create_env_template()
    
    # Run tests
    if not run_tests():
        return False
    
    print("\n🎉 Setup completed!")
    
    if not env_ok:
        print("\n⚠️  Warning: Some required environment variables are not set.")
        print("Please set your ANTHROPIC_API_KEY before running the application.")
    
    print_usage_instructions()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)