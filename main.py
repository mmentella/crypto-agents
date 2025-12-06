import logging
import pandas as pd
from agents.market_data import MarketDataAgent
from agents.technical_analysis import TechnicalAnalysisAgent
from agents.strategy import StrategyAgent
from agents.execution import ExecutionAgent

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    setup_logging()
    logger = logging.getLogger("Main")

    logger.info("Starting Multi-Agent Trading System...")

    # Initialize Agents
    data_agent = MarketDataAgent(exchange_id='binance')
    ta_agent = TechnicalAnalysisAgent()
    strategy_agent = StrategyAgent()
    execution_agent = ExecutionAgent(initial_balance=10000)

    try:
        data_agent.initialize()
    except Exception as e:
        logger.error("Failed to initialize data agent. Exiting.")
        return

    # 1. Fetch Historical Data
    logger.info("Fetching historical data...")
    df = data_agent.process({'symbol': 'BTC/USDT', 'timeframe': '1h', 'limit': 500})
    
    if df is None:
        logger.error("No data received.")
        return

    logger.info(f"Fetched {len(df)} candles.")

    # 2. Backtest Loop
    # We simulate stepping through the data.
    # We need at least ~50 points for indicators (SMA-50) before we start trading.
    warmup = 52
    
    for i in range(warmup, len(df)):
        # Simulate 'current' data available up to index i
        current_slice = df.iloc[:i+1] # Pass copies if performance is an issue, but for <1000 rows it's fine
        
        # 3. Analysis
        # Note: In a real streaming system, we'd update indicators incrementally. 
        # Here we recalculate on the slice (inefficient but simple for MVP).
        analyzed_df = ta_agent.process(current_slice)
        
        if analyzed_df is None or analyzed_df.empty:
            continue

        # 4. Strategy
        signal = strategy_agent.process(analyzed_df)
        
        # 5. Execution
        if signal['action'] != 'HOLD':
            execution_agent.process(signal)

    # Final Report
    last_price = df.iloc[-1]['close']
    final_value = execution_agent.get_portfolio_value(last_price)
    logger.info("=========================================")
    logger.info(f"Backtest Complete.")
    logger.info(f"Initial Balance: $10000.00")
    logger.info(f"Final Value:     ${final_value:.2f}")
    logger.info(f"Total Trades:    {len(execution_agent.trades)}")
    logger.info("=========================================")

if __name__ == "__main__":
    main()
