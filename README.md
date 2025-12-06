# Multi-Agent Trading System

A modular, agent-based trading system written in Python. It uses specialized agents to fetch data, perform technical analysis, decide strategies, and execute trades (simulated).

## Features

- **Multi-Agent Architecture**: Decoupled agents for Data, Analysis, Strategy, and Execution.
- **Backtesting Engine**: Simulate strategies against historical data.
- **Technical Analysis**: Integrated with `ta` library for indicators (RSI, MACD, SMA).
- **Crypto Data**: Uses `ccxt` to fetch data from Binance (and other exchanges).
- **Extensible**: Easy to add new strategies or indicators.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mmentella/crypto-agents.git
   cd crypto-agents
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the backtest simulation:

```bash
python main.py
```

This will:
1. Fetch historical BTC/USDT data.
2. Calculate indicators.
3. Run the Strategy Agent on the data.
4. Execute simulated trades and print the final PnL.

## Project Structure

- `main.py`: Entry point and orchestration.
- `agents/`:
  - `market_data.py`: Fetches OHLCV data.
  - `technical_analysis.py`: Computes indicators.
  - `strategy.py`: Implements trading logic.
  - `execution.py`: Handles paper trading.

## License

MIT
