import pytest
import sys
import os

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(__file__))

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up test environment variables."""
    os.environ.setdefault('ANTHROPIC_API_KEY', 'test_key_12345')
    yield
    # Cleanup if needed