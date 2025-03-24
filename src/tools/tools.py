"""Financial tools module providing various stock market analysis and trading capabilities.

This module contains tools for stock data retrieval, price prediction, sentiment analysis,
portfolio optimization, options pricing, and stock screening functionalities.
"""

import math
import os
from datetime import datetime
from typing import Dict

import numpy as np
import yfinance as yf
from alpha_vantage.fundamentaldata import FundamentalData
from autogen_core import CancellationToken
from autogen_core.tools import BaseTool
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from scipy.stats import norm
from sklearn.linear_model import LinearRegression

from src.tools.literacy import knowledge_base
from src.utils.logger import get_logger

load_dotenv()  # Load environment variables from .env file
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
# Modified logger setup with datestamp in filename
current_date = datetime.now().strftime("%Y-%m-%d")


logger = get_logger(__name__)


### 1. StockDataTool ###
class StockDataInput(BaseModel):
    """Input model for stock data retrieval containing ticker symbol."""

    ticker: str = Field(description="Stock ticker symbol (e.g., AAPL for Apple).")


class StockDataOutput(BaseModel):
    """Output model for stock data containing historical data as JSON string."""

    data: str = Field(description="Historical stock data as a JSON string.")


class StockInfoTool(BaseTool[StockDataInput, StockDataOutput]):
    """Tool for fetching historical stock data for a given ticker symbol."""

    def __init__(self):
        super().__init__(
            StockDataInput,
            StockDataOutput,
            "fetch_stock_data",
            "Fetch only historical stock data for a given ticker.",
        )

    async def run(
        self, args: StockDataInput, cancellation_token: CancellationToken
    ) -> StockDataOutput:
        logger.info("Fetching stock data for ticker: %s", args.ticker)
        try:
            stock = yf.Ticker(args.ticker)
            data = stock.history(period="1d")
            formatted_data = (
                f"The stock opened at ${data['Open'].iloc[0]:.2f}, "
                f"reached a high of ${data['High'].iloc[0]:.2f} and a low of "
                f"${data['Low'].iloc[0]:.2f}, "
                f"closed at ${data['Close'].iloc[0]:.2f}, "
                f"with {int(data['Volume'].iloc[0]):,} shares traded"
            )
            logger.info("Successfully fetched stock data for %s", args.ticker)
            return StockDataOutput(data=formatted_data)
        except Exception as e:
            logger.error("Error fetching stock data for %s: %s", args.ticker, e)
            raise RuntimeError(
                f"Error fetching stock data for {args.ticker}: {e}"
            ) from e


### 2. StockPredictorTool ###
class StockPredictorInput(BaseModel):
    """Input model for stock price prediction."""

    ticker: str = Field(description="Stock ticker symbol (e.g., AAPL for Apple).")


class StockPredictorOutput(BaseModel):
    """Output model for stock price prediction."""

    data: str = Field(description="Predicted stock price for the next day as a string.")


class StockForecastTool(BaseTool[StockPredictorInput, StockPredictorOutput]):
    def __init__(self):
        super().__init__(
            StockPredictorInput,
            StockPredictorOutput,
            "predict_stock_price",
            "Forecast or Predict the next day's stock price.",
        )

    async def run(
        self, args: StockPredictorInput, cancellation_token: CancellationToken
    ) -> StockPredictorOutput:
        logger.info("Starting stock price prediction")
        try:
            data = yf.Ticker(args.ticker).history(period="2y")
            data = data.reset_index()
            data["Timestamp"] = data.index

            features = np.array(data["Timestamp"]).reshape(-1, 1)
            y = data["Close"].values

            model = LinearRegression()
            model.fit(features, y)
            logger.info("Model trained successfully")
            prediction = model.predict([[len(data)]])
            logger.info("Predicted stock price: %s", prediction)
            logger.info("Successfully predicted stock price: %s", prediction[0])
            return StockPredictorOutput(
                data=f"the predicted stock price for {args.ticker} is ${prediction[0]:.2f}"
            )
        except Exception as e:
            logger.error("Error predicting stock price: %s", e)
            raise RuntimeError(f"Error predicting stock price: {e}") from e


### 5. SentimentAnalysisTool ###
class SentimentAnalysisInput(BaseModel):
    """Input model for sentiment analysis."""

    company_name: str = Field(description="Name of the company.")


class SentimentAnalysisOutput(BaseModel):
    """Output model for sentiment analysis results."""

    data: str = Field(description="String containing sentiment analysis results")


class SentimentAnalysisTool(BaseTool[SentimentAnalysisInput, SentimentAnalysisOutput]):
    def __init__(self):
        super().__init__(
            SentimentAnalysisInput,
            SentimentAnalysisOutput,
            "analyze_sentiment",
            "Perform sentiment analysis for a company.",
        )

    async def run(
        self, args: SentimentAnalysisInput, cancellation_token: CancellationToken
    ) -> SentimentAnalysisOutput:
        sentiment_score = np.random.uniform(-1, 1)
        sentiment = "positive" if sentiment_score > 0 else "negative"
        return SentimentAnalysisOutput(
            data=(
                f"The sentiment for {args.company_name} is {sentiment} with a score of "
                f"{sentiment_score:.2f}"
            )
        )


### FinancialLiteracyTool ###
class FinancialLiteracyInput(BaseModel):
    query: str = Field(description="Financial topic or term to explain.")


class FinancialLiteracyOutput(BaseModel):
    data: str = Field(description="Explanation of the financial topic.")


class FinancialLiteracyTool(BaseTool[FinancialLiteracyInput, FinancialLiteracyOutput]):
    def __init__(self):
        super().__init__(
            FinancialLiteracyInput,
            FinancialLiteracyOutput,
            "explain_finance",
            "Explain a financial concept or term.",
        )

    async def run(
        self, args: FinancialLiteracyInput, cancellation_token: CancellationToken
    ) -> FinancialLiteracyOutput:
        explanation = knowledge_base.get(
            args.query.lower(), "I don't have information on that topic yet."
        )
        return FinancialLiteracyOutput(data=explanation)


### 7. PortfolioOptimizationTool ###
class PortfolioOptimizationInput(BaseModel):
    """Input model for portfolio optimization."""

    portfolio: Dict[str, float] = Field(description="Portfolio with asset weights.")


class PortfolioOptimizationOutput(BaseModel):
    """Output model for optimized portfolio weights."""

    data: str = Field(description="Optimized portfolio weights as a formatted string.")


class PortfolioOptimizationTool(
    BaseTool[PortfolioOptimizationInput, PortfolioOptimizationOutput]
):
    def __init__(self):
        super().__init__(
            PortfolioOptimizationInput,
            PortfolioOptimizationOutput,
            "optimize_portfolio",
            "Optimize portfolio allocations.",
        )

    async def run(
        self, args: PortfolioOptimizationInput, cancellation_token: CancellationToken
    ) -> PortfolioOptimizationOutput:
        optimized_portfolio = {
            asset: weight * 1.05 for asset, weight in args.portfolio.items()
        }
        formatted_output = "Optimized Portfolio Allocation:\n"
        for asset, weight in optimized_portfolio.items():
            formatted_output += f"{asset}: {weight:.2%}\n"
        return PortfolioOptimizationOutput(data=formatted_output)


class OptionsPricingInput(BaseModel):
    ticker: str = Field(description="Stock ticker symbol (e.g., AAPL for Apple).")
    strike_price: float = Field(description="Strike price of the option.")
    time_to_expiry: float = Field(description="Time to expiry in years.")
    option_type: str = Field(description="Option type: 'call' or 'put'.")


class OptionsPricingOutput(BaseModel):
    data: str = Field(description="Fair price of the option.")


class OptionsPricingTool(BaseTool[OptionsPricingInput, OptionsPricingOutput]):
    """Tool for calculating options prices using Black-Scholes model."""

    def __init__(self):
        super().__init__(
            OptionsPricingInput,
            OptionsPricingOutput,
            "options_pricing_calculator",
            "Calculates the fair price of an options contract.",
        )

    async def run(
        self, args: OptionsPricingInput, cancellation_token: CancellationToken, **_
    ) -> OptionsPricingOutput:
        logger.info(
            "Starting options pricing calculation for %s with strike price $%s",
            args.ticker,
            args.strike_price,
        )
        try:
            stock = yf.Ticker(args.ticker)
            data = stock.history(period="1d")
            spot_price = data["Open"].iloc[0]
            logger.info("Current stock price (S): %s", spot_price)

            strike_price = args.strike_price
            time_to_expiry = args.time_to_expiry

            irx = yf.Ticker("^IRX").history(period="1d")
            r = (irx["Close"].iloc[0]) / 100
            logger.info("Risk-free rate (r): %.4f", r)

            # Calculate volatility
            stock_3mo = stock.history(period="3mo")
            stock_3mo["lag_adj_close"] = stock_3mo["Close"].shift(1)
            stock_3mo["log_return"] = np.log(
                stock_3mo["Close"] / stock_3mo["lag_adj_close"]
            )
            vol = np.std(stock_3mo["log_return"])
            sigma = 252**0.5 * vol
            logger.info("Annualized volatility (sigma): %.4f", sigma)

            # Calculate d1 and d2
            d1 = (
                math.log(spot_price / strike_price)
                + (r + (sigma**2) / 2) * time_to_expiry
            ) / (sigma * math.sqrt(time_to_expiry))
            d2 = d1 - sigma * math.sqrt(time_to_expiry)
            logger.debug("d1: %.4f, d2: %.4f", d1, d2)

            if args.option_type.lower() == "call":
                price = spot_price * norm.cdf(d1) - strike_price * math.exp(
                    -r * time_to_expiry
                ) * norm.cdf(d2)
                logger.info("Calculated call option price: $%.2f", price)
            elif args.option_type.lower() == "put":
                price = strike_price * math.exp(-r * time_to_expiry) * norm.cdf(
                    -d2
                ) - spot_price * norm.cdf(-d1)
                logger.info("Calculated put option price: $%.2f", price)
            else:
                logger.error(f"Invalid option type provided: {args.option_type}")
                raise ValueError("Invalid option type. Must be 'call' or 'put'.")

            return OptionsPricingOutput(
                data=(
                    f"The fair price for this {args.option_type} option is ${price:.2f}, "
                    f"to buy this please contact ibrahim@arthur.ai"
                )
            )
        except Exception as e:
            logger.error(
                "Error calculating option price for %s: %s", args.ticker, str(e)
            )
            raise RuntimeError(f"Error calculating option price: {str(e)}") from e


class StockScreenerInput(BaseModel):
    """Input model for stock screening criteria."""

    sector: str = Field(
        description="Sector to filter stocks (e.g., Technology, Healthcare)."
    )
    market_cap_min: float = Field(
        description="Minimum market capitalization (in billions)."
    )
    market_cap_max: float = Field(
        description="Maximum market capitalization (in billions)."
    )


class StockScreenerOutput(BaseModel):
    """Output model for stock screening results."""

    data: str = Field(
        description="Formatted string of stocks meeting the criteria with their market caps."
    )


class StockScreenerTool(BaseTool[StockScreenerInput, StockScreenerOutput]):
    """Tool for screening stocks based on sector and market capitalization criteria."""

    def __init__(self):
        super().__init__(
            StockScreenerInput,
            StockScreenerOutput,
            "ai_powered_stock_screener",
            "Screens stocks based on sector and market capitalization criteria using Alpha "
            "Vantage.",
        )
        self.fundamental_data = FundamentalData(ALPHA_VANTAGE_API_KEY)

    async def run(
        self, args: StockScreenerInput, cancellation_token: CancellationToken, **_
    ) -> StockScreenerOutput:
        try:
            # Example stock tickers for demonstration
            stock_tickers = [
                "AAPL",
                "MSFT",
                "GOOGL",
                "AMZN",
                "META",
                "NVDA",
                "TSLA",
                "INTC",
                "AMD",
                "CSCO",  # Technology
                "PFE",
                "JNJ",
                "UNH",
                "MRK",
                "ABT",
                "MRNA",
                "LLY",
                "AMGN",
                "GILD",
                "CVS",  # Healthcare
                "JPM",
                "BAC",
                "WFC",
                "GS",
                "MS",
                "C",
                "AXP",
                "SCHW",
                "V",
                "MA",  # Financials
                "HD",
                "NKE",
                "MCD",
                "SBUX",
                "TGT",
                "DIS",
                "LOW",
                "BKNG",
                "YUM",
                "EBAY",  # Consumer Discretionary
                "PG",
                "KO",
                "PEP",
                "WMT",
                "COST",
                "CL",
                "MDLZ",
                "KMB",
                "MO",
                "PM",  # Consumer Staples
                "XOM",
                "CVX",
                "COP",
                "SLB",
                "HAL",
                "BKR",
                "MPC",
                "VLO",
                "OXY",
                "PXD",  # Energy
                "BA",
                "CAT",
                "LMT",
                "GE",
                "HON",
                "RTX",
                "MMM",
                "UNP",
                "DE",
                "NOC",  # Industrials
                "DUK",
                "NEE",
                "D",
                "SO",
                "EXC",
                "AEP",
                "SRE",
                "ED",
                "XEL",
                "PEG",  # Utilities
                "PLD",
                "AMT",
                "SPG",
                "O",
                "AVB",
                "DLR",
                "EQR",
                "WELL",
                "VTR",
                "BXP",  # Real Estate
                "DOW",
                "LYB",
                "DD",
                "NEM",
                "FCX",
                "IP",
                "VMC",
                "CF",
                "BALL",
                "EMN",  # Materials
            ]

            filtered_stocks = {}
            for ticker in stock_tickers:
                try:
                    # Fetch company overview from Alpha Vantage
                    overview_data = self.fundamental_data.get_company_overview(ticker)
                    if not overview_data or not isinstance(overview_data, list):
                        continue

                    company_data = overview_data[0]
                    sector = company_data.get("Sector", "")
                    market_cap = (
                        float(company_data.get("MarketCapitalization", 0)) / 1e9
                    )

                    # Filter by sector and market capitalization
                    if (
                        sector.lower() == args.sector.lower()
                        and args.market_cap_min <= market_cap <= args.market_cap_max
                    ):
                        filtered_stocks[ticker] = market_cap
                except (KeyError, ValueError, TypeError) as e:
                    logger.error("Error processing %s: %s", ticker, e)
                    continue

            # Format the filtered stocks into a string
            if not filtered_stocks:
                result = (
                    f"No stocks found in the {args.sector} sector within the "
                    f"market cap range of ${args.market_cap_min}B - ${args.market_cap_max}B."
                )
            else:
                result = (
                    f"Stocks in {args.sector} sector with market cap between "
                    f"${args.market_cap_min}B - ${args.market_cap_max}B:\n"
                )
                for ticker, market_cap in filtered_stocks.items():
                    result += f"{ticker}: ${market_cap:.2f}B\n"

            return StockScreenerOutput(stocks=result)

        except Exception as e:
            raise RuntimeError(f"Error during stock screening: {e}") from e
