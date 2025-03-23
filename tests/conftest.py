import pytest
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Add any shared fixtures here if needed
@pytest.fixture
def sample_stock_data():
    return {
        "ticker": "AAPL",
        "price": 150.0,
        "volume": 1000000
    } 