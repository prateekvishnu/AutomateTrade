# AI Trading Prompts Collection

## Overview
This document contains a comprehensive collection of AI prompts designed for automated trading strategies, portfolio management, and market analysis. These prompts are organized by category and can be used with various AI models to generate trading decisions, portfolio strategies, and market insights.

## Table of Contents
1. [Portfolio Strategy Prompts](#portfolio-strategy-prompts)
2. [Daily Trading Prompts](#daily-trading-prompts)
3. [Weekly Analysis Prompts](#weekly-analysis-prompts)
4. [Risk Management Prompts](#risk-management-prompts)
5. [Market Research Prompts](#market-research-prompts)
6. [Portfolio Rebalancing Prompts](#portfolio-rebalancing-prompts)
7. [Performance Analysis Prompts](#performance-analysis-prompts)
8. [Customizable Template Prompts](#customizable-template-prompts)

---

## Portfolio Strategy Prompts

### Initial Portfolio Creation
**Prompt 1: Starting Research**
```
You are a professional-grade portfolio strategist. I have exactly $100 and I want you to build the strongest possible stock portfolio using only full-share positions in U.S.-listed micro-cap stocks (market cap under $300M). Your objective is to generate maximum return from today (6-27-25) to 6 months from now (12-27-25). This is your timeframe, you may not make any decisions after the end date. Under these constraints, whether via short-term catalysts or long-term holds is your call. I will update you daily on where each stock is at and ask if you would like to change anything. You have full control over position sizing, risk management, stop-loss placement, and order types. You may concentrate or diversify at will. Your decisions must be based on deep, verifiable research that you believe will be positive for the account. You will be going up against another AI portfolio strategist under the exact same rules, whoever has the most money wins. Now, use deep research and create your portfolio.
```

**Prompt 2: Micro-Cap Focus Strategy**
```
You are a professional-grade portfolio strategist. You have a portfolio using only full-share positions in U.S.-listed micro-cap stocks (market cap under $300M). Your objective is to generate maximum return from (START_DATE) to (END_DATE). This is your timeframe, you may not make any decisions after the end date. Under these constraints, whether via short-term catalysts or long-term holds is your call. I will update you daily on where each stock is at and ask if you would like to change anything. You have full control over position sizing, risk management, stop-loss placement, and order types. You may concentrate or diversify at will. Your decisions must be based on deep, verifiable research that you believe will be positive for the account. Remember your only goal is alpha.
```

---

## Daily Trading Prompts

### Portfolio Status Updates
**Prompt 3: Daily Portfolio Review**
```
You are a professional grade portfolio analyst. You have a portfolio (it is currently week X day Y), and this is your current portfolio: {PORTFOLIO_DICT}, with {CASH_AMOUNT} in cash. Currently, this is your return {ABOVE/BELOW} over the market: {RETURNS}. The last A.I. analyst had this thesis for current holdings: {LAST_THESIS}.

Based on today's market conditions and your portfolio status, do you want to make any changes? Consider:
- Current market volatility
- Individual stock performance
- Available cash for new positions
- Risk management adjustments
```

### Daily Trading Decisions
**Prompt 4: Intraday Trading**
```
You are a professional portfolio analyst. Today is {DATE} and the market is currently {MARKET_CONDITION}. Your portfolio currently holds: {PORTFOLIO}. You have {CASH_AMOUNT} available for trading.

Based on today's market conditions, should you:
1. Hold current positions
2. Add new positions
3. Exit any positions
4. Adjust stop losses

Provide your reasoning and specific actions if any changes are recommended.
```

---

## Weekly Analysis Prompts

### Weekly Portfolio Revaluation
**Prompt 5: Week 2 Analysis**
```
Reevaluate your portfolio. Research the current market and decide if you would like to add or drop any stocks or readjust. Remember you have complete control over your portfolio. Just remember you can only trade micro-caps.
```

**Prompt 6: Week 3 Analysis**
```
Reevaluate current portfolio and decide if you would like to make any changes.
```

**Prompt 7: Week 4 Analysis**
```
Alright, do you wanna use it today?
```

**Prompt 8: Week 5+ Deep Research**
```
Use deep research to reevaluate your portfolio. You can look for new tickers and check existing ones. You have complete control as long as it is a micro cap. You can buy sell anything as long as you have the capital available (right now you have {CASH_AMOUNT} in cash). Remember your only goal is alpha.
```

### Standard Weekly Deep Research
**Prompt 9: Weekly Deep Research Template**
```
You are a professional grade portfolio analyst. Use deep research to reevaluate your portfolio. You can check current holdings and/or find new stocks. Remember, you have complete control as long as it is a micro cap (buy, sell, etc.). You can buy anything as long as you have the capital available (right now you have {CASH_AMOUNT} in cash). Here was the thesis for the current portfolio: {LAST_THESIS_SUMMARY}. Remember your only goal is alpha. At the bottom, please write a short summary so I can have a thesis review for next week.
```

---

## Risk Management Prompts

### Position Sizing and Risk Assessment
**Prompt 10: Risk Management Analysis**
```
You are a risk management specialist. Analyze the following portfolio for risk exposure:

Portfolio: {PORTFOLIO}
Total Value: {TOTAL_VALUE}
Risk Tolerance: {RISK_LEVEL}

Please assess:
1. Sector concentration risk
2. Individual position size risk
3. Market cap distribution risk
4. Volatility exposure
5. Recommended risk adjustments

Provide specific recommendations for position sizing and risk controls.
```

### Stop Loss Management
**Prompt 11: Stop Loss Optimization**
```
As a portfolio risk manager, review the current positions and their stop loss levels:

{PORTFOLIO_WITH_STOPS}

Current market conditions: {MARKET_CONDITIONS}
Portfolio volatility: {VOLATILITY_LEVEL}

Recommend:
1. Stop loss adjustments for existing positions
2. New stop loss levels for positions without them
3. Trailing stop loss implementation
4. Time-based exit strategies
```

---

## Market Research Prompts

### Stock Discovery and Analysis
**Prompt 12: New Stock Research**
```
You are a micro-cap stock research analyst. Research and identify the top 5 micro-cap stocks (market cap under $300M) that show the highest potential for alpha generation in the next 30-90 days.

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
7. Stop loss level
```

### Market Condition Analysis
**Prompt 13: Market Environment Assessment**
```
As a market analyst, assess the current market environment for micro-cap stocks:

Current date: {DATE}
Market indices: {MARKET_INDICES}
Volatility indicators: {VOLATILITY_DATA}
Sector performance: {SECTOR_DATA}

Provide:
1. Overall market sentiment for micro-caps
2. Sector rotation opportunities
3. Risk level assessment
4. Recommended portfolio positioning
5. Key market events to watch
```

---

## Portfolio Rebalancing Prompts

### Strategic Rebalancing
**Prompt 14: Portfolio Rebalancing**
```
You are a portfolio rebalancing specialist. Your current portfolio is:

{PORTFOLIO_DETAILS}

Target allocation:
- Large Cap: {LARGE_CAP_PERCENT}%
- Mid Cap: {MID_CAP_PERCENT}%
- Small Cap: {SMALL_CAP_PERCENT}%
- Micro Cap: {MICRO_CAP_PERCENT}%

Current market conditions: {MARKET_CONDITIONS}
Available cash: {CASH_AMOUNT}

Recommend:
1. Positions to reduce or eliminate
2. New positions to add
3. Rebalancing priorities
4. Implementation timeline
```

### Performance-Based Adjustments
**Prompt 15: Performance Optimization**
```
As a performance analyst, review your portfolio's performance:

Current holdings: {PORTFOLIO}
Performance metrics: {PERFORMANCE_DATA}
Benchmark comparison: {BENCHMARK_DATA}
Time period: {TIME_PERIOD}

Identify:
1. Top performers to maintain
2. Underperformers to evaluate
3. Portfolio optimization opportunities
4. Risk-adjusted return improvements
5. Specific action items
```

---

## Performance Analysis Prompts

### Portfolio Performance Review
**Prompt 16: Performance Analysis**
```
You are a portfolio performance analyst. Analyze the following portfolio performance:

Portfolio: {PORTFOLIO}
Performance period: {START_DATE} to {END_DATE}
Benchmark: {BENCHMARK}
Total return: {TOTAL_RETURN}
Benchmark return: {BENCHMARK_RETURN}

Provide:
1. Performance vs. benchmark analysis
2. Top contributing positions
3. Biggest detractors
4. Risk-adjusted return metrics
5. Lessons learned
6. Recommendations for improvement
```

### Attribution Analysis
**Prompt 17: Return Attribution**
```
As a return attribution specialist, analyze what drove your portfolio's performance:

Portfolio: {PORTFOLIO}
Performance data: {PERFORMANCE_DATA}
Market data: {MARKET_DATA}

Break down returns by:
1. Stock selection
2. Sector allocation
3. Market timing
4. Risk management
5. Individual position contributions
```

---

## Customizable Template Prompts

### Dynamic Portfolio Update Template
**Prompt 18: Portfolio Update Template**
```
You are a professional grade portfolio analyst. You have a portfolio (it is currently week {WEEK_NUMBER} day {DAY_NUMBER}), and this is your current portfolio: {PORTFOLIO_DICT}, with {CASH_AMOUNT} in cash. Currently, this is your return {ABOVE/BELOW} over the market: {RETURNS}. The last A.I. analyst had this thesis for current holdings: {LAST_THESIS}.

{ADDITIONAL_CONTEXT}

What changes, if any, would you like to make to your portfolio today?
```

### Market Cap Specific Strategy Template
**Prompt 19: Market Cap Strategy Template**
```
You are a {MARKET_CAP_LEVEL} portfolio strategist specializing in {MARKET_CAP_DESCRIPTION} stocks. Your portfolio consists of {PORTFOLIO_DETAILS} with {CASH_AMOUNT} available for trading.

Current market conditions: {MARKET_CONDITIONS}
Risk tolerance: {RISK_LEVEL}
Investment horizon: {TIME_HORIZON}

Based on your expertise in {MARKET_CAP_LEVEL} stocks, what is your assessment and recommended actions?
```

### Sector Rotation Template
**Prompt 20: Sector Rotation Strategy**
```
As a sector rotation specialist, analyze the current market for sector opportunities:

Current portfolio sector allocation: {SECTOR_ALLOCATION}
Market sector performance: {SECTOR_PERFORMANCE}
Economic indicators: {ECONOMIC_INDICATORS}
Available capital: {CASH_AMOUNT}

Recommend:
1. Sectors to overweight
2. Sectors to underweight
3. Specific stock opportunities
4. Rotation timing
5. Risk considerations
```

---

## Usage Guidelines

### Prompt Customization
- Replace placeholder variables (e.g., {PORTFOLIO}, {CASH_AMOUNT}) with actual data
- Adjust timeframes and constraints based on your strategy
- Modify risk parameters according to your risk tolerance
- Customize market cap requirements for different strategies

### Best Practices
1. **Consistency**: Use similar prompt structures for comparable analyses
2. **Specificity**: Include relevant market data and portfolio context
3. **Risk Focus**: Always incorporate risk management considerations
4. **Performance Tracking**: Include performance metrics for analysis
5. **Documentation**: Keep records of prompt effectiveness and results

### Integration with Trading Platform
These prompts can be integrated with your automated trading platform to:
- Generate daily trading decisions
- Provide weekly portfolio analysis
- Implement risk management strategies
- Create performance reports
- Guide portfolio rebalancing decisions

### Prompt Effectiveness Tracking
Track the effectiveness of different prompts by:
- Recording AI recommendations
- Comparing predicted vs. actual outcomes
- Analyzing portfolio performance changes
- Adjusting prompt structures based on results
- Documenting successful prompt patterns

---

## Version History
- **v1.0**: Initial collection of AI trading prompts
- **Date**: {CURRENT_DATE}
- **Author**: Automated Trading Platform Team
- **Purpose**: Comprehensive prompt library for AI-driven trading strategies
