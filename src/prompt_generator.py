"""
AI Trading Prompt Generator

This module provides utilities for generating AI trading prompts dynamically
with current portfolio data, market context, and trading parameters.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union


class TradingPromptGenerator:
    """
    Generates AI trading prompts with dynamic portfolio and market data.
    """
    
    def __init__(self):
        """Initialize the prompt generator."""
        self.prompt_templates = self._load_prompt_templates()
    
    def _load_prompt_templates(self) -> Dict[str, str]:
        """Load prompt templates from configuration."""
        return {
            "initial_portfolio": """You are a professional-grade portfolio strategist. I have exactly ${capital} and I want you to build the strongest possible stock portfolio using only full-share positions in U.S.-listed micro-cap stocks (market cap under ${max_market_cap}M). Your objective is to generate maximum return from today ({start_date}) to {end_date}. This is your timeframe, you may not make any decisions after the end date. Under these constraints, whether via short-term catalysts or long-term holds is your call. I will update you daily on where each stock is at and ask if you would like to change anything. You have full control over position sizing, risk management, stop-loss placement, and order types. You may concentrate or diversify at will. Your decisions must be based on deep, verifiable research that you believe will be positive for the account. Remember your only goal is alpha. Now, use deep research and create your portfolio.""",
            
            "weekly_deep_research": """You are a professional grade portfolio analyst. Use deep research to reevaluate your portfolio. You can check current holdings and/or find new stocks. Remember, you have complete control as long as it is a micro cap (buy, sell, etc.). You can buy anything as long as you have the capital available (right now you have ${cash_amount} in cash). Here was the thesis for the current portfolio: {last_thesis}. Remember your only goal is alpha. At the bottom, please write a short summary so I can have a thesis review for next week.""",
            
            "portfolio_update": """You are a professional grade portfolio analyst. You have a portfolio (it is currently week {week_number} day {day_number}), and this is your current portfolio: {portfolio_dict}, with ${cash_amount} in cash. Currently, this is your return {above_below} over the market: {returns}. The last A.I. analyst had this thesis for current holdings: {last_thesis}.

What changes, if any, would you like to make to your portfolio today?""",
            
            "daily_review": """You are a professional portfolio analyst. Today is {date} and the market is currently {market_condition}. Your portfolio currently holds: {portfolio}. You have ${cash_amount} available for trading.

Based on today's market conditions, should you:
1. Hold current positions
2. Add new positions
3. Exit any positions
4. Adjust stop losses

Provide your reasoning and specific actions if any changes are recommended.""",
            
            "risk_management": """As a portfolio risk manager, review the current positions and their stop loss levels:

{portfolio_with_stops}

Current market conditions: {market_conditions}
Portfolio volatility: {volatility_level}

Recommend:
1. Stop loss adjustments for existing positions
2. New stop loss levels for positions without them
3. Trailing stop loss implementation
4. Time-based exit strategies""",
            
            "new_stock_research": """You are a micro-cap stock research analyst. Research and identify the top {num_stocks} micro-cap stocks (market cap under ${max_market_cap}M) that show the highest potential for alpha generation in the next {timeframe} days.

Consider:
- Technical indicators
- Fundamental analysis
- Recent news and catalysts
- Volume and price action
- Sector trends

For each stock, provide:
1. Ticker symbol
2. Current price
3. Market cap
4. Key catalysts
5. Risk factors
6. Entry price recommendation
7. Stop loss level"""
        }
    
    def generate_initial_portfolio_prompt(
        self,
        capital: float = 100.0,
        max_market_cap: int = 300,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> str:
        """
        Generate the initial portfolio creation prompt.
        
        Args:
            capital: Starting capital amount
            max_market_cap: Maximum market cap in millions
            start_date: Start date for trading period
            end_date: End date for trading period
            
        Returns:
            Formatted prompt string
        """
        if start_date is None:
            start_date = datetime.now().strftime("%m-%d-%y")
        
        if end_date is None:
            end_date = (datetime.now() + timedelta(days=180)).strftime("%m-%d-%y")
        
        template = self.prompt_templates["initial_portfolio"]
        return template.format(
            capital=capital,
            max_market_cap=max_market_cap,
            start_date=start_date,
            end_date=end_date
        )
    
    def generate_weekly_deep_research_prompt(
        self,
        cash_amount: float,
        last_thesis: str
    ) -> str:
        """
        Generate the weekly deep research prompt.
        
        Args:
            cash_amount: Available cash amount
            last_thesis: Previous analyst's thesis summary
            
        Returns:
            Formatted prompt string
        """
        template = self.prompt_templates["weekly_deep_research"]
        return template.format(
            cash_amount=cash_amount,
            last_thesis=last_thesis
        )
    
    def generate_portfolio_update_prompt(
        self,
        week_number: int,
        day_number: int,
        portfolio_dict: Dict,
        cash_amount: float,
        above_below: str,
        returns: str,
        last_thesis: str
    ) -> str:
        """
        Generate the portfolio update prompt for changing chats.
        
        Args:
            week_number: Current week number
            day_number: Current day number
            portfolio_dict: Current portfolio holdings
            cash_amount: Available cash amount
            above_below: Performance relative to market (above/below)
            returns: Specific return amount/percentage
            last_thesis: Previous analyst's thesis
            
        Returns:
            Formatted prompt string
        """
        template = self.prompt_templates["portfolio_update"]
        return template.format(
            week_number=week_number,
            day_number=day_number,
            portfolio_dict=json.dumps(portfolio_dict, indent=2),
            cash_amount=cash_amount,
            above_below=above_below,
            returns=returns,
            last_thesis=last_thesis
        )
    
    def generate_daily_review_prompt(
        self,
        portfolio: Dict,
        cash_amount: float,
        market_condition: str = "normal",
        date: Optional[str] = None
    ) -> str:
        """
        Generate the daily portfolio review prompt.
        
        Args:
            portfolio: Current portfolio holdings
            cash_amount: Available cash amount
            market_condition: Current market condition
            date: Current date (defaults to today)
            
        Returns:
            Formatted prompt string
        """
        if date is None:
            date = datetime.now().strftime("%m/%d/%Y")
        
        template = self.prompt_templates["daily_review"]
        return template.format(
            date=date,
            market_condition=market_condition,
            portfolio=json.dumps(portfolio, indent=2),
            cash_amount=cash_amount
        )
    
    def generate_risk_management_prompt(
        self,
        portfolio_with_stops: Dict,
        market_conditions: str,
        volatility_level: str
    ) -> str:
        """
        Generate the risk management prompt.
        
        Args:
            portfolio_with_stops: Portfolio with current stop loss levels
            market_conditions: Current market conditions
            volatility_level: Current volatility level
            
        Returns:
            Formatted prompt string
        """
        template = self.prompt_templates["risk_management"]
        return template.format(
            portfolio_with_stops=json.dumps(portfolio_with_stops, indent=2),
            market_conditions=market_conditions,
            volatility_level=volatility_level
        )
    
    def generate_new_stock_research_prompt(
        self,
        num_stocks: int = 5,
        max_market_cap: int = 300,
        timeframe: int = 90
    ) -> str:
        """
        Generate the new stock research prompt.
        
        Args:
            num_stocks: Number of stocks to research
            max_market_cap: Maximum market cap in millions
            timeframe: Investment timeframe in days
            
        Returns:
            Formatted prompt string
        """
        template = self.prompt_templates["new_stock_research"]
        return template.format(
            num_stocks=num_stocks,
            max_market_cap=max_market_cap,
            timeframe=timeframe
        )
    
    def generate_custom_prompt(
        self,
        template_name: str,
        **kwargs
    ) -> str:
        """
        Generate a custom prompt using a template with custom parameters.
        
        Args:
            template_name: Name of the template to use
            **kwargs: Parameters to format the template with
            
        Returns:
            Formatted prompt string
            
        Raises:
            KeyError: If template_name doesn't exist
        """
        if template_name not in self.prompt_templates:
            raise KeyError(f"Template '{template_name}' not found. Available templates: {list(self.prompt_templates.keys())}")
        
        template = self.prompt_templates[template_name]
        return template.format(**kwargs)
    
    def add_custom_template(self, name: str, template: str):
        """
        Add a custom prompt template.
        
        Args:
            name: Name for the custom template
            template: Template string with placeholders
        """
        self.prompt_templates[name] = template
    
    def get_available_templates(self) -> List[str]:
        """
        Get list of available template names.
        
        Returns:
            List of template names
        """
        return list(self.prompt_templates.keys())
    
    def export_templates(self, filepath: str):
        """
        Export all templates to a JSON file.
        
        Args:
            filepath: Path to save the templates file
        """
        with open(filepath, 'w') as f:
            json.dump(self.prompt_templates, f, indent=2)
    
    def import_templates(self, filepath: str):
        """
        Import templates from a JSON file.
        
        Args:
            filepath: Path to the templates file to import
        """
        with open(filepath, 'r') as f:
            self.prompt_templates.update(json.load(f))


# Convenience functions for common prompt generation
def create_initial_portfolio_prompt(capital: float = 100.0) -> str:
    """Quick function to create initial portfolio prompt."""
    generator = TradingPromptGenerator()
    return generator.generate_initial_portfolio_prompt(capital=capital)


def create_weekly_research_prompt(cash_amount: float, last_thesis: str) -> str:
    """Quick function to create weekly research prompt."""
    generator = TradingPromptGenerator()
    return generator.generate_weekly_deep_research_prompt(cash_amount, last_thesis)


def create_portfolio_update_prompt(
    week: int,
    day: int,
    portfolio: Dict,
    cash: float,
    performance: str,
    returns: str,
    thesis: str
) -> str:
    """Quick function to create portfolio update prompt."""
    generator = TradingPromptGenerator()
    return generator.generate_portfolio_update_prompt(
        week, day, portfolio, cash, performance, returns, thesis
    )


if __name__ == "__main__":
    # Example usage
    generator = TradingPromptGenerator()
    
    # Generate initial portfolio prompt
    initial_prompt = generator.generate_initial_portfolio_prompt(capital=100.0)
    print("=== Initial Portfolio Prompt ===")
    print(initial_prompt)
    print("\n" + "="*50 + "\n")
    
    # Generate weekly research prompt
    weekly_prompt = generator.generate_weekly_deep_research_prompt(
        cash_amount=2.32,
        last_thesis="Focus on biotech micro-caps with FDA approval catalysts"
    )
    print("=== Weekly Research Prompt ===")
    print(weekly_prompt)
    print("\n" + "="*50 + "\n")
    
    # Generate portfolio update prompt
    portfolio = {
        "BIOT": {"shares": 10, "current_price": 2.45, "entry_price": 2.30},
        "TECH": {"shares": 5, "current_price": 1.80, "entry_price": 1.75}
    }
    
    update_prompt = generator.generate_portfolio_update_prompt(
        week_number=5,
        day_number=3,
        portfolio_dict=portfolio,
        cash_amount=2.32,
        above_below="above",
        returns="+15.2%",
        last_thesis="Biotech and tech micro-caps with strong growth potential"
    )
    print("=== Portfolio Update Prompt ===")
    print(update_prompt)
