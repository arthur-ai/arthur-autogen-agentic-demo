"""
Test suite for the tools module.

This module contains test cases for the tools implemented in the `src.tools` module.
The tests cover various functionalities including stock forecasting, sentiment analysis,

"""
import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from src.tools.tools import (
    StockForecastTool,
    SentimentAnalysisTool,
    FinancialLiteracyTool,
    OptionsPricingTool,
    StockPredictorInput,
    SentimentAnalysisInput,
    SentimentAnalysisOutput,
    FinancialLiteracyInput,
    FinancialLiteracyOutput,
    OptionsPricingInput
)

@pytest.fixture
def mock_stock_data():
    return pd.DataFrame({
        'Open': [100] * 10,
        'Close': [101] * 10,
        'High': [102] * 10,
        'Low': [99] * 10,
        'Volume': [1000000] * 10,
        'Timestamp': pd.date_range(start='2023-01-01', periods=10)
    })

@pytest.fixture
def mock_irx_data():
    return pd.DataFrame({
        'Close': [0.05],  # 5% interest rate
    })

@pytest.mark.asyncio
async def test_stock_forecast_tool():
    with patch('yfinance.Ticker') as mock_ticker:
        # Setup mock
        mock_instance = MagicMock()
        mock_instance.history.return_value = pd.DataFrame({
            'Close': [100, 101, 102],
            'Timestamp': pd.date_range(start='2023-01-01', periods=3)
        })
        mock_ticker.return_value = mock_instance
        
        tool = StockForecastTool()
        result = await tool.run(StockPredictorInput(ticker="AAPL"), MagicMock())
        
        assert isinstance(result.data, str)
        assert "AAPL" in result.data
        assert "$" in result.data

@pytest.mark.asyncio
async def test_sentiment_analysis_tool():
    tool = SentimentAnalysisTool()
    result = await tool.run(SentimentAnalysisInput(company_name="Apple"), MagicMock())
    
    assert isinstance(result.data, str)
    assert "Apple" in result.data
    assert any(word in result.data.lower() for word in ["positive", "negative"])
    assert isinstance(float(result.data.split()[-1].strip()), float)  # Check if score is a float

@pytest.mark.asyncio
async def test_financial_literacy_tool():
    tool = FinancialLiteracyTool()
    result = await tool.run(FinancialLiteracyInput(query="ETF"), MagicMock())
    
    assert isinstance(result.data, str)
    assert len(result.data) > 0

@pytest.mark.asyncio
async def test_options_pricing_tool():
    with patch('yfinance.Ticker') as mock_ticker:
        # Setup stock data mock
        stock_instance = MagicMock()
        stock_instance.history.return_value = pd.DataFrame({
            'Open': [100],
            'Close': [101],
            'lag_adj_close': [99],
            'log_return': [0.01]
        })
        
        # Setup IRX data mock
        irx_instance = MagicMock()
        irx_instance.history.return_value = pd.DataFrame({
            'Close': [2.5]  # 2.5% interest rate
        })
        
        # Configure mock to return different instances for different tickers
        def get_ticker(ticker):
            return irx_instance if ticker == "^IRX" else stock_instance
        mock_ticker.side_effect = get_ticker
        
        tool = OptionsPricingTool()
        result = await tool.run(
            OptionsPricingInput(
                ticker="AAPL",
                strike_price=100.0,
                time_to_expiry=0.25,
                option_type="call"
            ),
            MagicMock()
        )
        
        assert isinstance(result.data, str)
        assert "call" in result.data.lower()
        assert "$" in result.data

@pytest.mark.asyncio
async def test_options_pricing_tool_put_option():
    with patch('yfinance.Ticker') as mock_ticker:
        # Similar setup as above but testing put option
        stock_instance = MagicMock()
        stock_instance.history.return_value = pd.DataFrame({
            'Open': [100],
            'Close': [101],
            'lag_adj_close': [99],
            'log_return': [0.01]
        })
        
        irx_instance = MagicMock()
        irx_instance.history.return_value = pd.DataFrame({
            'Close': [2.5]
        })
        
        def get_ticker(ticker):
            return irx_instance if ticker == "^IRX" else stock_instance
        mock_ticker.side_effect = get_ticker
        
        tool = OptionsPricingTool()
        result = await tool.run(
            OptionsPricingInput(
                ticker="AAPL",
                strike_price=100.0,
                time_to_expiry=0.25,
                option_type="put"
            ),
            MagicMock()
        )
        
        assert isinstance(result.data, str)
        assert "put" in result.data.lower()
        assert "$" in result.data 