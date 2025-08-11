# Specific AI Trading Prompts Collection

## Overview
This document contains the specific AI trading prompts that have been tested and used for micro-cap stock trading strategies. These prompts are organized chronologically and by purpose for easy reference and implementation.

---

## Initial Portfolio Creation Prompts

### Prompt 1: Starting Research (Week 1)
```
You are a professional-grade portfolio strategist. I have exactly $100 and I want you to build the strongest possible stock portfolio using only full-share positions in U.S.-listed micro-cap stocks (market cap under $300M). Your objective is to generate maximum return from today (6-27-25) to 6 months from now (12-27-25). This is your timeframe, you may not make any decisions after the end date. Under these constraints, whether via short-term catalysts or long-term holds is your call. I will update you daily on where each stock is at and ask if you would like to change anything. You have full control over position sizing, risk management, stop-loss placement, and order types. You may concentrate or diversify at will. Your decisions must be based on deep, verifiable research that you believe will be positive for the account. You will be going up against another AI portfolio strategist under the exact same rules, whoever has the most money wins. Now, use deep research and create your portfolio.
```

**Usage**: Use this prompt to initiate portfolio creation with a new AI analyst
**Key Elements**: 
- $100 starting capital
- Micro-cap focus (under $300M market cap)
- 6-month timeframe (6-27-25 to 12-27-25)
- Full control over all trading decisions
- Deep research requirement

---

## Weekly Portfolio Revaluation Prompts

### Prompt 2: Week 2 Analysis
```
Reevaluate your portfolio. Research the current market and decide if you would like to add or drop any stocks or readjust. Remember you have complete control over your portfolio. Just remember you can only trade micro-caps.
```

**Usage**: Week 2 portfolio review
**Key Elements**: 
- Portfolio revaluation
- Market research
- Micro-cap constraint reminder

### Prompt 3: Week 3 Analysis
```
Reevaluate current portfolio and decide if you would like to make any changes.
```

**Usage**: Week 3 portfolio review
**Key Elements**: 
- Simple portfolio revaluation
- Change decision making

### Prompt 4: Week 4 Analysis
```
Alright, do you wanna use it today?
```

**Usage**: Week 4 portfolio review
**Key Elements**: 
- Weekend research availability check
- Simple decision prompt

### Prompt 5: Week 5+ Deep Research
```
Use deep research to reevaluate your portfolio. You can look for new tickers and check existing ones. You have complete control as long as it is a micro cap. You can buy sell anything as long as you have the capital available (right now you have 2.32 in cash). Remember your only goal is alpha.
```

**Usage**: Week 5 and beyond portfolio analysis
**Key Elements**: 
- Deep research requirement
- New stock discovery
- Existing position review
- Capital availability (2.32 in cash)
- Alpha generation focus

---

## Standard Weekly Deep Research Template

### Prompt 6: Weekly Deep Research Template
```
You are a professional grade portfolio analyst. Use deep research to reevaluate your portfolio. You can check current holdings and/or find new stocks. Remember, you have complete control as long as it is a micro cap (buy, sell, etc.). You can buy anything as long as you have the capital available (right now you have {CASH_AMOUNT} in cash). Here was the thesis for the current portfolio: {LAST_THESIS_SUMMARY}. Remember your only goal is alpha. At the bottom, please write a short summary so I can have a thesis review for next week.
```

**Usage**: Standard weekly deep research analysis
**Key Elements**: 
- Professional portfolio analyst role
- Deep research requirement
- Current holdings review
- New stock discovery
- Micro-cap constraint
- Capital availability variable
- Previous thesis context
- Alpha generation focus
- Weekly thesis summary requirement

---

## Portfolio Status Update Prompts

### Prompt 7: Portfolio Update Template for Changing Chats
```
You are a professional grade portfolio analyst. You have a portfolio (it is currently week X day Y), and this is your current portfolio: {PORTFOLIO_DICT}, with {CASH_AMOUNT} in cash. Currently, this is your return {ABOVE/BELOW} over the market: {RETURNS}. The last A.I. analyst had this thesis for current holdings: {LAST_THESIS}.

What changes, if any, would you like to make to your portfolio today?
```

**Usage**: When switching to a new AI analyst or chat session
**Key Elements**: 
- Professional portfolio analyst role
- Current week and day context
- Portfolio dictionary
- Cash amount
- Performance vs. market
- Previous analyst's thesis
- Change decision prompt

---

## Prompt Variables and Placeholders

### Required Variables
- `{CASH_AMOUNT}`: Current available cash (e.g., "2.32 in cash")
- `{PORTFOLIO_DICT}`: Current portfolio holdings in dictionary format
- `{LAST_THESIS_SUMMARY}`: Summary of the previous analyst's thesis
- `{WEEK_NUMBER}`: Current week number
- `{DAY_NUMBER}`: Current day number
- `{ABOVE/BELOW}`: Performance relative to market
- `{RETURNS}`: Specific return percentage or amount

### Example Portfolio Dictionary Format
```python
{
    "TICKER1": {
        "shares": 10,
        "current_price": 2.45,
        "entry_price": 2.30,
        "unrealized_pnl": 1.50
    },
    "TICKER2": {
        "shares": 5,
        "current_price": 1.80,
        "entry_price": 1.75,
        "unrealized_pnl": 0.25
    }
}
```

---

## Implementation Guidelines

### Daily Usage Pattern
1. **Morning**: Use portfolio update template to check for changes
2. **Mid-day**: Monitor positions and market conditions
3. **End of day**: Review performance and prepare for next day

### Weekly Usage Pattern
1. **Sunday**: Use deep research template for weekly analysis
2. **Monday-Friday**: Use daily portfolio update templates
3. **Friday**: Prepare thesis summary for next week

### Prompt Customization
- Replace all placeholder variables with actual data
- Adjust cash amounts based on current portfolio status
- Update week/day numbers as appropriate
- Include relevant market context when available

### Best Practices
1. **Consistency**: Use the same prompt structure for similar analyses
2. **Context**: Always include current portfolio status and cash availability
3. **Thesis Continuity**: Reference previous analyst's thesis for continuity
4. **Alpha Focus**: Emphasize the goal of generating alpha
5. **Micro-cap Constraint**: Always remind of the micro-cap trading restriction

---

## Integration with Trading Platform

### Automated Prompt Generation
These prompts can be integrated with your automated trading platform to:
- Generate daily trading decisions automatically
- Provide consistent portfolio analysis
- Maintain trading strategy continuity
- Track performance and thesis evolution

### Data Requirements
To use these prompts effectively, your platform needs:
- Real-time portfolio data
- Current cash balances
- Performance metrics
- Previous analyst thesis storage
- Market data integration

### Output Processing
The AI responses should be processed to:
- Extract trading decisions
- Update portfolio positions
- Store new thesis information
- Generate performance reports
- Trigger automated trades when appropriate

---

## Version History
- **v1.0**: Initial collection of specific AI trading prompts
- **Date**: December 2024
- **Source**: User-provided tested prompts
- **Purpose**: Micro-cap stock trading strategy implementation
