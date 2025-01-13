from pydantic_ai import Agent
from pydantic import BaseModel
import yfinance as yf


class StockSellBuy(BaseModel):
    symbol:str
    price:float
    prev_price:float 
    action:str  

stock_agent = Agent(
    "groq:llama-3.1-70b-versatile",
    result_type=StockSellBuy,
    system_prompt="Act as a finicial assistant and give exact answer to the question asked by the user"
)

@stock_agent.tool_plain
def action_on_stock(symbol: str):
    ticker = yf.Ticker(symbol)
    price = ticker.fast_info.last_price
    prev_price = ticker.fast_info.previous_close
    if(price - prev_price)>0:
        action="Sell"
    else:
        action="Buy"           
    return action, prev_price, price



result = stock_agent.run_sync("Should I buy or sell Google shares?")
print(result.data.prev_price)
print(result.data.price)
print(result.data.action)


