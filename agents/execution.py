from agents.base_agent import BaseAgent

class ExecutionAgent(BaseAgent):
    def __init__(self, name: str = "Execution", initial_balance: float = 10000.0):
        super().__init__(name)
        self.balance = initial_balance
        self.position = 0.0 # Amount of asset held
        self.trades = []

    def process(self, signal: dict):
        """
        Executes trade based on signal.
        """
        if not signal or signal['action'] == 'HOLD':
            return

        price = signal.get('price')
        if not price:
            self.logger.error("Signal missing price")
            return

        action = signal['action']
        
        if action == 'BUY':
            if self.balance > 0:
                amount_to_buy = self.balance / price
                self.position += amount_to_buy
                self.balance = 0
                self.trades.append({
                    'type': 'BUY',
                    'price': price,
                    'amount': amount_to_buy,
                    'reason': signal.get('reason')
                })
                self.logger.info(f"EXECUTED BUY: {amount_to_buy:.6f} @ {price:.2f}. Reason: {signal.get('reason')}")
            else:
                self.logger.warning("Insufficient funds to BUY")

        elif action == 'SELL':
            if self.position > 0:
                sale_value = self.position * price
                self.balance += sale_value
                
                self.trades.append({
                    'type': 'SELL',
                    'price': price,
                    'amount': self.position,
                    'pl': (sale_value - 10000), # Simple PnL since start logic is flawed if multiple trades; simplification for now
                    'reason': signal.get('reason')
                })
                self.logger.info(f"EXECUTED SELL: {self.position:.6f} @ {price:.2f}. Balance: {self.balance:.2f}")
                self.position = 0
            else:
                self.logger.warning("No position to SELL")
        
    def get_portfolio_value(self, current_price):
        return self.balance + (self.position * current_price)
