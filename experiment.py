# # import pandas as pd
# # import numpy as np
# # import matplotlib.pyplot as plt
# # import yfinance as yf
# # import os

# # # Fetch TSLA stock data for the last 3 months

# # share_name = "tatamotors.ns"

# # tsla = yf.download(share_name, period='3mo', interval='1d')
# # tsla.reset_index(inplace=True)
# # tsla['Price'] = tsla['Close']
# # tsla['Day'] = range(len(tsla))

# # # Bollinger Bands
# # tsla['MA20'] = tsla['Price'].rolling(window=20).mean()
# # tsla['STD20'] = tsla['Price'].rolling(window=20).std()
# # tsla['Upper'] = tsla['MA20'] + 2 * tsla['STD20']
# # tsla['Lower'] = tsla['MA20'] - 2 * tsla['STD20']

# # # Buy/Sell Signal Logic
# # buy_price = 30
# # target_return = 1.10
# # buy_signals = []
# # sell_signals = []
# # holding = False
# # entry_price = None

# # for i in range(len(tsla)):
# #     price = float(tsla.loc[i, 'Price'])  # Ensure scalar value
# #     if not holding and price >= buy_price:
# #         buy_signals.append((tsla.loc[i, 'Day'], price))
# #         entry_price = price
# #         holding = True
# #     elif holding and price >= entry_price * target_return:
# #         sell_signals.append((tsla.loc[i, 'Day'], price))
# #         holding = False

# # # Support/Resistance detection
# # support = tsla['Price'][(tsla['Price'].shift(1) > tsla['Price']) & (tsla['Price'].shift(-1) > tsla['Price'])]
# # resistance = tsla['Price'][(tsla['Price'].shift(1) < tsla['Price']) & (tsla['Price'].shift(-1) < tsla['Price'])]

# # # Plotting
# # plt.style.use('seaborn-v0_8')
# # plt.figure(figsize=(14, 7))
# # plt.plot(tsla['Day'], tsla['Price'], label='Close Price', color='blue')
# # plt.plot(tsla['Day'], tsla['Upper'], linestyle='--', color='orange', label='Bollinger Upper')
# # plt.plot(tsla['Day'], tsla['Lower'], linestyle='--', color='orange', label='Bollinger Lower')

# # # Buy/Sell markers with safe labeling
# # if buy_signals:
# #     first_buy_day = int(buy_signals[0][0])  # ✅ Force scalar
# #     for i, price in buy_signals:
# #         label = 'Buy Signal' if 2 == first_buy_day else ""
# #         plt.scatter(i, price, marker='^', color='green', s=120, label=label)

# # if sell_signals:
# #     first_sell_day = int(sell_signals[0][0])  # ✅ Force scalar
# #     for i, price in sell_signals:
# #         label = 'Sell Signal' if 1 == first_sell_day else ""
# #         plt.scatter(i, price, marker='v', color='red', s=120, label=label)

# # # Support/Resistance markers
# # plt.scatter(support.index, support, color='green', s=80, label='Support Level')
# # plt.scatter(resistance.index, resistance, color='red', s=80, label='Resistance Level')

# # graph_path = os.path.join('static', 'new.png')


# # plt.title(f'{share_name} Buy/Sell Signal Chart with Bollinger Bands')
# # plt.xlabel('Day')
# # plt.ylabel('Price (USD)')
# # plt.legend()
# # plt.grid(True)
# # plt.tight_layout()
# # print(f"Graph saved at: {graph_path}")
# # plt.savefig(graph_path)
# # plt.close()









# # import pandas as pd
# # import numpy as np
# # import matplotlib.pyplot as plt
# # import yfinance as yf

# # # --- Configuration ---
# # share_name = "tatamotors.ns"
# # period = '3mo'
# # interval = '1d'

# # # Risk Management Parameters
# # INITIAL_STOP_LOSS_PCT = 0.05  # 5% initial stop-loss to limit max loss
# # TRAILING_STOP_PCT = 0.05     # 5% trailing stop to lock in profits
# # MIN_PROFIT_TAKE_PCT = 0.02   # Only sell based on indicator if at least 2% profit is secured

# # # Fetch stock data
# # # auto_adjust=True is the default and cleans up data (no need for the old 'Price' calculation)
# # tsla = yf.download(share_name, period=period, interval=interval) 
# # tsla.reset_index(inplace=True)
# # tsla['Price'] = tsla['Close'] # Keep this for consistency with the rest of the code
# # tsla['Day'] = range(len(tsla))

# # # --- 1. TECHNICAL INDICATORS ---

# # # Bollinger Bands (BB)
# # window_bb = 20
# # tsla['MA20'] = tsla['Price'].rolling(window=window_bb).mean()
# # tsla['STD20'] = tsla['Price'].rolling(window=window_bb).std()
# # tsla['Upper'] = tsla['MA20'] + 2 * tsla['STD20']
# # tsla['Lower'] = tsla['MA20'] - 2 * tsla['STD20']

# # # Relative Strength Index (RSI)
# # def calculate_rsi(data, window=14):
# #     delta = data.diff()
# #     up = delta.clip(lower=0)
# #     down = -1 * delta.clip(upper=0)
# #     # Exponential Moving Average for smoother RSI calculation
# #     ema_up = up.ewm(com=window - 1, adjust=False).mean()
# #     ema_down = down.ewm(com=window - 1, adjust=False).mean()
# #     rs = ema_up / ema_down
# #     return 100 - (100 / (1 + rs))

# # tsla['RSI'] = calculate_rsi(tsla['Price'])

# # # Moving Average Convergence Divergence (MACD)
# # tsla['MACD_Line'] = tsla['Price'].ewm(span=12, adjust=False).mean() - tsla['Price'].ewm(span=26, adjust=False).mean()
# # tsla['Signal_Line'] = tsla['MACD_Line'].ewm(span=9, adjust=False).mean()

# # # --- 2. ADVANCED BUY/SELL SIGNAL LOGIC ---
# # buy_signals_adv = [] # Stores (Day, Price)
# # sell_signals_adv = [] # Stores (Day, Price, Reason)
# # holding = False
# # entry_price = None
# # stop_loss_price = None

# # # We start the iteration after the required windows (MACD needs 26 periods minimum)
# # start_index = max(26, window_bb) 

# # for i in range(start_index, len(tsla)):
    
# #     # CORRECTED LINE: Using .item() to safely extract the scalar value (removes FutureWarning)
# #     current_price = tsla.loc[i, 'Price'].item()
    
# #     # We can skip the explicit NaN check since we start at start_index, 
# #     # but for safety, if you kept it, the fix is crucial:
# #     # if pd.isna(tsla.loc[i, 'MACD_Line']).all(): # Use .all() to resolve ambiguity
# #     #     continue

# #     # --- EXIT LOGIC (Priority over Entry) ---
# #     if holding:
        
# #         # 1. Update Trailing Stop-Loss
# #         potential_new_stop = current_price * (1 - TRAILING_STOP_PCT)
        
# #         # Only raise the stop-loss price, never lower it
# #         if potential_new_stop > stop_loss_price:
# #              stop_loss_price = potential_new_stop
        
# #         # 2. Check Stop-Loss Trigger (Max Loss or Trailing Stop Hit)
# #         if current_price <= stop_loss_price:
# #             sell_signals_adv.append((tsla.loc[i, 'Day'].item(), current_price, 'Stop-Loss Triggered'))
# #             holding = False
# #             entry_price = None
# #             stop_loss_price = None
# #             continue 

# #         # 3. Check Indicator-Based Sell Signal (Profit Taking/Reversal)
        
# #         macd_sell_condition = tsla.loc[i, 'MACD_Line'].item() < tsla.loc[i, 'Signal_Line'].item()
# #         rsi_overbought = tsla.loc[i, 'RSI'].item() >= 70
# #         bb_upper_touch = current_price >= tsla.loc[i, 'Upper'].item()
        
# #         # Combined Sell Condition: Momentum loss AND Overbought condition
# #         if (macd_sell_condition and (rsi_overbought or bb_upper_touch)):
             
# #              if entry_price is not None and current_price >= entry_price * (1 + MIN_PROFIT_TAKE_PCT):
# #                  sell_signals_adv.append((tsla.loc[i, 'Day'].item(), current_price, 'Indicator Reversal'))
# #                  holding = False
# #                  entry_price = None
# #                  stop_loss_price = None
        
# #     # --- ENTRY LOGIC ---
# #     if not holding:
        
# #         macd_buy_condition = tsla.loc[i, 'MACD_Line'].item() > tsla.loc[i, 'Signal_Line'].item()
# #         rsi_oversold = tsla.loc[i, 'RSI'].item() <= 30
# #         bb_lower_touch = current_price <= tsla.loc[i, 'Lower'].item()
        
# #         # Combined Buy Signal: Momentum shift AND Oversold condition
# #         if macd_buy_condition and (rsi_oversold or bb_lower_touch):
# #             buy_signals_adv.append((tsla.loc[i, 'Day'].item(), current_price))
# #             holding = True
# #             entry_price = current_price
# #             # Set initial stop-loss based on entry price
# #             stop_loss_price = current_price * (1 - INITIAL_STOP_LOSS_PCT)


# # # --- 3. Plotting ---

# # plt.style.use('seaborn-v0_8')
# # fig, ax = plt.subplots(figsize=(14, 7))

# # # Price and Bollinger Bands
# # ax.plot(tsla['Day'], tsla['Price'], label='Close Price', color='blue', linewidth=1.5)
# # ax.plot(tsla['Day'], tsla['MA20'], color='grey', label='MA20')
# # ax.plot(tsla['Day'], tsla['Upper'], linestyle='--', color='orange', label='Bollinger Upper')
# # ax.plot(tsla['Day'], tsla['Lower'], linestyle='--', color='orange', label='Bollinger Lower')

# # # Buy/Sell markers with dynamic labeling
# # buy_days = [s[0] for s in buy_signals_adv]
# # buy_prices = [s[1] for s in buy_signals_adv]
# # sell_days = [s[0] for s in sell_signals_adv]
# # sell_prices = [s[1] for s in sell_signals_adv]

# # # Only label the first signal for the legend, then plot the rest without labels
# # if buy_signals_adv:
# #     ax.scatter(buy_days[0], buy_prices[0], marker='^', color='green', s=120, label='Buy Signal (Entry)', zorder=5)
# #     ax.scatter(buy_days[1:], buy_prices[1:], marker='^', color='green', s=120, zorder=5)

# # if sell_signals_adv:
# #     ax.scatter(sell_days[0], sell_prices[0], marker='v', color='red', s=120, label='Sell Signal (Exit)', zorder=5)
# #     ax.scatter(sell_days[1:], sell_prices[1:], marker='v', color='red', s=120, zorder=5)

# # ax.set_title(f'{share_name} Advanced Buy/Sell Signals with BB, RSI, & MACD (Risk-Managed)')
# # ax.set_xlabel('Day')
# # ax.set_ylabel('Price (INR)')
# # ax.legend(loc='upper left')
# # ax.grid(True)
# # plt.tight_layout()
# # plt.show()












# import json
# from google import genai

# def fetch_AI_Assistant(user_prompt):
#     client = genai.Client(api_key="AIzaSyAL_WV2kPHgDlhU9QkB9IXCv5TuiNUs3Ws")

#     MODEL_NAME = "gemini-2.5-pro"

#     SYSTEM_INSTRUCTION = """
#     You are a financial data assistant.

#     Given a user's textual description of their stock portfolio (including quantities, prices, and company names),
#     you must calculate and return the following information **strictly in JSON format**:

#     {
#       "invested_value": <float>,
#       "current_value": <float>,
#       "total_gain_value": <float>,
#       "total_loss_value": <float>,
#       "total_gain_percent": <float>,
#       "total_loss_percent": <float>,
#       "overall_return_percent": <float>,
#       "sector_allocation_percent": {
#           "Information_Technology": <float>,
#           "Financials": <float>,
#           "Energy": <float>,
#           "Consumer_Discretionary": <float>,
#           "Consumer_Staples": <float>,
#           "Health_Care": <float>,
#           "Industrials": <float>,
#           "Materials": <float>,
#           "Communication_Services": <float>,
#           "Utilities": <float>,
#           "Real_Estate": <float>,
#           "Other": <float>
#       },
#       "top_holdings": [
#           {"symbol": "<ticker>", "sector": "<sector_name>", "weight_percent": <float>}
#       ],
#       "summary": "<short summary of the portfolio>"
#     }
#     """

#     chat = client.chats.create(
#         model=MODEL_NAME,
#         config={"system_instruction": SYSTEM_INSTRUCTION}
#     )

#     response = chat.send_message(user_prompt)


#     return response.text










# from types import SimpleNamespace

# def ai_fetcher(x = fetch_AI_Assistant(USER_INPUT)):

#     print(x)

#     def safe_json_loads(raw_text):

#         cleaned = raw_text.strip()

#         if cleaned.startswith("```"):

#             cleaned = cleaned.strip("`")
#             cleaned = cleaned.replace("json", "", 1).strip()

#         return json.loads(cleaned)

#     # usage
#     data = safe_json_loads(x)
 
#     invested_value = data["invested_value"]
#     current_value = data["current_value"]

#     total_gain_value = data["total_gain_value"]
#     total_loss_value = data["total_loss_value"]

#     total_gain_percent = data["total_gain_percent"]
#     total_loss_percent = data["total_loss_percent"]

#     overall_return_percent = data["overall_return_percent"]

#     sector_allocation_percent_IT = data["sector_allocation_percent"]["Information_Technology"]
#     sector_allocation_percent_Financials = data["sector_allocation_percent"]["Financials"]
#     sector_allocation_percent_Energy = data["sector_allocation_percent"]["Energy"]
#     sector_allocation_percent_Consumer_Discretionary = data["sector_allocation_percent"]["Consumer_Discretionary"]
#     sector_allocation_percent_Consumer_Staples = data["sector_allocation_percent"]["Consumer_Staples"]
#     sector_allocation_percent_Health_Care = data["sector_allocation_percent"]["Health_Care"]
#     sector_allocation_percent_Industrials = data["sector_allocation_percent"]["Industrials"]
#     sector_allocation_percent_Materials = data["sector_allocation_percent"]["Materials"]
#     sector_allocation_percent_Communication_Services = data["sector_allocation_percent"]["Communication_Services"]
#     sector_allocation_percent_Utilities = data["sector_allocation_percent"]["Utilities"]
#     sector_allocation_percent_Real_Estate = data["sector_allocation_percent"]["Real_Estate"]
#     sector_allocation_percent_Real_Other = data["sector_allocation_percent"]["Other"]

#     summary = data["summary"]

#     top_holdings = []

#     for stock in data["top_holdings"]:

#         top_holdings.append({

#             "symbol": stock["symbol"],
#             "sector": stock["sector"],
#             "weight_percent": stock["weight_percent"]

#         })

#     print("this is invested value : " , data["invested_value"])


#     return invested_value , current_value , total_gain_value , total_loss_value , total_gain_percent , total_loss_percent , overall_return_percent , sector_allocation_percent_IT , sector_allocation_percent_Financials ,   sector_allocation_percent_Energy , sector_allocation_percent_Consumer_Discretionary , sector_allocation_percent_Consumer_Staples , sector_allocation_percent_Health_Care , sector_allocation_percent_Industrials , sector_allocation_percent_Materials , sector_allocation_percent_Communication_Services , sector_allocation_percent_Utilities , sector_allocation_percent_Real_Estate , sector_allocation_percent_Real_Other , summary , top_holdings



# USER_INPUT = """
# Here is my portfolio:

# - Infosys Ltd: Qty 10, Buy Avg ₹1450, Current Price ₹1650
# - HDFC Bank: Qty 8, Buy Avg ₹1550, Current Price ₹1750
# - Reliance Industries: Qty 6, Buy Avg ₹2400, Current Price ₹2450
# - ITC Ltd: Qty 15, Buy Avg ₹450, Current Price ₹490
# - Tata Motors: Qty 12, Buy Avg ₹650, Current Price ₹580
# - Sun Pharma: Qty 10, Buy Avg ₹1100, Current Price ₹1240
# - IRCTC: Qty 5, Buy Avg ₹600, Current Price ₹670
# """



# print(ai_fetcher())



# #below is the same code but is written by ai logic 


# # import json
# # from google import genai

# # def fetch_AI_Assistant(user_prompt):
# #     client = genai.Client(api_key="AIzaSyAL_WV2kPHgDlhU9QkB9IXCv5TuiNUs3Ws")

# #     MODEL_NAME = "gemini-2.5-pro"

# #     SYSTEM_INSTRUCTION = """
# #     You are a financial data assistant.

# #     Given a user's textual description of their stock portfolio (including quantities, prices, and company names),
# #     you must calculate and return the following information **strictly in JSON format**:

# #     {
# #       "invested_value": <float>,
# #       "current_value": <float>,
# #       "total_gain_value": <float>,
# #       "total_loss_value": <float>,
# #       "total_gain_percent": <float>,
# #       "total_loss_percent": <float>,
# #       "overall_return_percent": <float>,
# #       "sector_allocation_percent": {
# #           "Information_Technology": <float>,
# #           "Financials": <float>,
# #           "Energy": <float>,
# #           "Consumer_Discretionary": <float>,
# #           "Consumer_Staples": <float>,
# #           "Health_Care": <float>,
# #           "Industrials": <float>,
# #           "Materials": <float>,
# #           "Communication_Services": <float>,
# #           "Utilities": <float>,
# #           "Real_Estate": <float>,
# #           "Other": <float>
# #       },
# #       "top_holdings": [
# #           {"symbol": "<ticker>", "sector": "<sector_name>", "weight_percent": <float>}
# #       ],
# #       "summary": "<short summary of the portfolio>"
# #     }
# #     """

# #     chat = client.chats.create(
# #         model=MODEL_NAME,
# #         config={"system_instruction": SYSTEM_INSTRUCTION}
# #     )

# #     response = chat.send_message(user_prompt)

# #     # ✅ Extract only the text content
# #     try:
# #         if hasattr(response, 'text'):
# #             x = response.text
# #         else:
# #             x = response.candidates[0].content.parts[0].text
# #     except Exception as e:
# #         print("Error extracting text:", e)
# #         return None

# #     def safe_json_loads(raw_text):
# #         cleaned = raw_text.strip()

# #         if cleaned.startswith("```"):
# #             cleaned = cleaned.strip("`")
# #             cleaned = cleaned.replace("json", "", 1).strip()

# #         return json.loads(cleaned)

# #     # usage
# #     data = safe_json_loads(x)

# #     invested_value = data["invested_value"]
# #     current_value = data["current_value"]

# #     total_gain_value = data["total_gain_value"]
# #     total_loss_value = data["total_loss_value"]

# #     total_gain_percent = data["total_gain_percent"]
# #     total_loss_percent = data["total_loss_percent"]

# #     overall_return_percent = data["overall_return_percent"]

# #     sector_allocation_percent_IT = data["sector_allocation_percent"]["Information_Technology"]
# #     sector_allocation_percent_Financials = data["sector_allocation_percent"]["Financials"]
# #     sector_allocation_percent_Energy = data["sector_allocation_percent"]["Energy"]
# #     sector_allocation_percent_Consumer_Discretionary = data["sector_allocation_percent"]["Consumer_Discretionary"]
# #     sector_allocation_percent_Consumer_Staples = data["sector_allocation_percent"]["Consumer_Staples"]
# #     sector_allocation_percent_Health_Care = data["sector_allocation_percent"]["Health_Care"]
# #     sector_allocation_percent_Industrials = data["sector_allocation_percent"]["Industrials"]
# #     sector_allocation_percent_Materials = data["sector_allocation_percent"]["Materials"]
# #     sector_allocation_percent_Communication_Services = data["sector_allocation_percent"]["Communication_Services"]
# #     sector_allocation_percent_Utilities = data["sector_allocation_percent"]["Utilities"]
# #     sector_allocation_percent_Real_Estate = data["sector_allocation_percent"]["Real_Estate"]
# #     sector_allocation_percent_Real_Other = data["sector_allocation_percent"]["Other"]

# #     summary = data["summary"]

# #     top_holdings = []

# #     for stock in data["top_holdings"]:
# #         top_holdings.append({
# #             "symbol": stock["symbol"],
# #             "sector": stock["sector"],
# #             "weight_percent": stock["weight_percent"]
# #         })

# #     print("this is invested value :", data["invested_value"])

# #     return (invested_value, current_value, total_gain_value, total_loss_value,
# #             total_gain_percent, total_loss_percent, overall_return_percent,
# #             sector_allocation_percent_IT, sector_allocation_percent_Financials,
# #             sector_allocation_percent_Energy, sector_allocation_percent_Consumer_Discretionary,
# #             sector_allocation_percent_Consumer_Staples, sector_allocation_percent_Health_Care,
# #             sector_allocation_percent_Industrials, sector_allocation_percent_Materials,
# #             sector_allocation_percent_Communication_Services, sector_allocation_percent_Utilities,
# #             sector_allocation_percent_Real_Estate, sector_allocation_percent_Real_Other,
# #             summary, top_holdings)

import yfinance as yf
import numpy as np
import pandas as pd

tickers = [
    "ASHOKLEY.NS", "BIRLACABLE.NS", "COALINDIA.NS", "EXIDEIND.NS",
    "GAIL.NS", "HDFCBANK.NS", "IOC.NS", "IRFC.NS", "ITC.NS", "ITCHOTELS.NS",
    "JUBLFOOD.NS", "LICI.NS", "MANKIND.NS", "NHPC.NS", "NTPC.NS", "OLECTRA.NS",
    "ONGC.NS", "PERSISTENT.NS", "PFC.NS", "POWERGRID.NS", "RELIANCE.NS",
    "RPOWER.NS", "RVNL.NS", "TATAPOWER.NS", "TATASTEEL.NS", "TATATECH.NS",
    "TCS.NS"
]

# ✅ Fixed line
data = yf.download(tickers, start="2024-11-01", end="2025-11-01", auto_adjust=True)['Close']

# Compute daily returns
returns = data.pct_change().dropna()

# Equal weights
weights = np.ones(len(tickers)) / len(tickers)

# Covariance matrix
cov_matrix = returns.cov()

# Portfolio SD
portfolio_var = np.dot(weights.T, np.dot(cov_matrix, weights))
portfolio_sd = np.sqrt(portfolio_var)
annualized_sd = portfolio_sd * np.sqrt(252)

# Individual SDs
individual_sds = (returns.std() * np.sqrt(252)).sort_values(ascending=False)

print("📊 Annualized Portfolio SD:", round(annualized_sd * 100, 2), "%\n")
print("📈 Individual Stock SDs (Annualized):\n")
print(individual_sds)
