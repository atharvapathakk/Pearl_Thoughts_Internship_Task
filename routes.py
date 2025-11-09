import requests
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from extensions import db
import yfinance as yf
import matplotlib.pyplot as plt
import os
from flask import jsonify
import requests
import feedparser
from flask import render_template, request
from datetime import datetime
import urllib.parse
import google.generativeai as genai
from types import SimpleNamespace
import json
from google import genai
import numpy as np 
import pandas as pd
from datetime import datetime, timedelta
















#the commeneted code is for pyhton sql alchemy for storing db and belwo comented code their is firebase code for server database 


# Create Blueprint for the main routes
main = Blueprint('main', __name__)

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "MSC4JZ5TIYC8P80T")
NEWS_API_KEY = "3db8fcc3c31e405492f6849159dad9e6"  # Sign up at https://newsapi.org
geminiApiKey = "AIzaSyBW2Xwxxz4SK01_vUrTYhZ_8lc5p8YrT-A"



@main.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    # Fetch the user by ID
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return "User deleted successfully!", 200
    return "User not found!", 404


@main.route('/admin/view_users')
def view_users():
    # Fetch all users from the database
    users = User.query.all()
    return render_template('view_users.html', users=users)



# Route for login
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Retrieve the user from the database
        user = User.query.filter_by(username=username).first()

        # If the user exists and the password is correct
        if user and check_password_hash(user.password, password):
            login_user(user)  # Log the user in
            flash('Login successful!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Login failed. Check your username and/or password.', 'danger')

    return render_template('login.html')



@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose another.', 'danger')
            return redirect(url_for('main.signup'))

        # Hash password and create new user
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created!', 'success')
        return redirect(url_for('main.login'))

    return render_template('signup.html')


# Route for logout
@main.route('/logout')
@login_required  # Ensure the user must be logged in to access this route
def logout():
    print('user getting logged out ......')
    logout_user()  # Logs the user out
    return redirect(url_for('main.login'))  # Redirect to the login page after logout

# Protected route for logged-in users
@main.route('/index')
#@login_required
def index():
    return render_template('index.html')










# from flask import Blueprint, request, redirect, url_for, render_template, flash
# from flask_login import login_user, logout_user, login_required, current_user
# from werkzeug.security import generate_password_hash, check_password_hash
# from models import User  # Firestore-based User class

# main = Blueprint('main', __name__)

# ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "MSC4JZ5TIYC8P80T")
# NEWS_API_KEY = "3db8fcc3c31e405492f6849159dad9e6"
# geminiApiKey = "AIzaSyBW2Xwxxz4SK01_vUrTYhZ_8lc5p8YrT-A"


# # 🔥 View all users (Admin)
# @main.route('/admin/view_users')
# def view_users():
#     users_ref = User.users_ref.stream()
#     users = [doc.to_dict() for doc in users_ref]
#     return render_template('view_users.html', users=users)


# # 🔥 Delete a user (Admin)
# @main.route('/admin/delete_user/<email>', methods=['POST'])
# def delete_user(email):
#     user = User.get_user(email)
#     if user:
#         User.users_ref.document(email).delete()
#         return "User deleted successfully!", 200
#     return "User not found!", 404


# # 🔥 Signup
# @main.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))

#     if request.method == 'POST':
#         email = request.form['username']  # keep using "username" field for email
#         password = request.form['password']

#         existing_user = User.get_user(email)
#         if existing_user:
#             flash('User already exists. Please choose another.', 'danger')
#             return redirect(url_for('main.signup'))

#         User.create_user(email, password)
#         flash('Your account has been created!', 'success')
#         return redirect(url_for('main.login'))

#     return render_template('signup.html')


# # 🔥 Login
# @main.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))

#     if request.method == 'POST':
#         email = request.form['username']  # same "username" field
#         password = request.form['password']

#         user = User.get_user(email)
#         if user and user.check_password(password):
#             login_user(user)  # Requires User class to subclass UserMixin
#             flash('Login successful!', 'success')
#             return redirect(url_for('main.index'))
#         else:
#             flash('Login failed. Check your email and/or password.', 'danger')

#     return render_template('login.html')


# # 🔥 Logout
# @main.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('main.login'))


# # 🔒 Protected route
# @main.route('/index')
# @login_required
# def index():
#     return render_template('index.html')







@main.route("/Terms_of_service.html")
def terms():
    return render_template('Terms_of_service.html')



@main.route("/About_us.html")
def termss():
    return render_template('About_us.html')



@main.route("/Privacy_policy.html")
def termsis():
    return render_template('Privacy_policy.html')




#route for AI Assistant 
@main.route("/AI_Assistant" , methods = ['GET' , 'POST'])
def ai_assistant():
    if request.method == 'POST':
        user_prompt = request.form.get('user_prompt') 
        

        result = fetch_AI_Assistant(user_prompt)


        return render_template('Ai_Assistant.html', result=result , user_prompt = " ")

    return render_template('Ai_Assistant.html')





@main.route('/get_news', methods=['POST'])
def get_news():
    stock_symbol = request.form.get('stock_name', '').strip()
    stock_extension = request.form.get('country', '').strip()

    country_to_extension = {
        "India": ".ns",
        "USA": "",
        "United Kingdom": ".uk",
        "Germany": ".de",
        "Canada": ".ca",
        "Australia": ".aus"
    }

    if not stock_symbol:
        return "Error: Stock symbol is required.", 400
    if stock_extension not in country_to_extension:
        return f"Error: Invalid country selected: {stock_extension}.", 400

    stockExtension = country_to_extension[stock_extension]
    stock_name = f"{stock_symbol.lower()}{stockExtension}"

    news_data = fetch_news(stock_name)
    
    if not news_data:
        news_data = [{
            'title': "No recent news available",
            'publisher': "System",
            'link': "#",
            'providerPublishTime': datetime.now().strftime('%Y-%m-%d'),
            'summary': f"No news found for {stock_symbol}. Try a different stock symbol.",
            'image': ''
        }]
    
    return render_template('news.html', 
                         stock_name=stock_symbol, 
                         news_data=news_data)





@main.route("/Fake_News_Detector" , methods = ['GET' , 'POST'])
def fakeNewsInput():
    if request.method == 'POST':
        news_text = request.form.get('news_text')  # Extract input from form
        # Here you can run ML model or any logic
        

        result = fetch_fake_news_detector(news_text)


        return render_template('fake_news_detector.html', result=result, news_text=news_text)

    return render_template('fake_news_detector.html')



# Route for fetching dividends (ensure it's only defined once)
@main.route('/get_dividends', methods=['POST'])
#@login_required
def get_dividends():

    stock_symbol = request.form.get('stock_name', '').strip()
    stock_extension = request.form.get('country', '').strip()

    country_to_extension = {

        "India": ".ns",
        "USA": "",
        "United Kingdom": ".uk",
        "Germany": ".de",
        "Canada": ".ca",
        "Australia": ".aus"

    }

    if not stock_symbol:
        return "Error: Stock symbol is required.", 400
    if stock_extension not in country_to_extension:
        return f"Error: Invalid country selected: {stock_extension}.", 400

    stockExtension = country_to_extension[stock_extension]
    stock_name = f"{stock_symbol.lower()}{stockExtension}"

    dividend_data = fetch_dividends(stock_name)
    return render_template('dividend.html', stock_name=stock_name, dividend_data=dividend_data)

# Route for fetching balance sheet (ensure it's only defined once)
@main.route("/get_balanceSheet", methods=['POST'])
def get_balanceSheet():

    stock_symbol = request.form.get('stock_name', '').strip()
    stock_extension = request.form.get('country', '').strip()

    country_to_extension = {
        "India": ".ns",
        "USA": "",
        "United Kingdom": ".uk",
        "Germany": ".de",
        "Canada": ".ca",
        "Australia": ".aus"
    }

    if not stock_symbol:
        return "Error: Stock symbol is required.", 400
    if stock_extension not in country_to_extension:
        return f"Error: Invalid country selected: {stock_extension}.", 400

    stockExtension = country_to_extension[stock_extension]
    stock_name = f"{stock_symbol.lower()}{stockExtension}"

    fetchBalanceSheet = fetch_balanceSheet(stock_name)
    return render_template('balanceSheet.html' , stock_name = stock_name , balanceSheetDict = fetchBalanceSheet)


@main.route('/get_Income_Statement', methods=['POST'])
def get_IncomeStatements():
    stock_symbol = request.form.get('stock_name', '').strip()
    stock_extension = request.form.get('country', '').strip()

    country_to_extension = {
        "India": ".ns",
        "USA": "",
        "United Kingdom": ".uk",
        "Germany": ".de",
        "Canada": ".ca",
        "Australia": ".aus"
    }

    if not stock_symbol:
        return "Error: Stock symbol is required.", 400
    if stock_extension not in country_to_extension:
        return f"Error: Invalid country selected: {stock_extension}.", 400

    stockExtension = country_to_extension[stock_extension]
    stock_name = f"{stock_symbol.lower()}{stockExtension}"

    fetch_IncomeStatements = fetch_Income_Statements(stock_name)
    return render_template('income_statement.html', stock_name=stock_name, incomeStatementDict=fetch_IncomeStatements)

@main.route("/get_stock_recommendation", methods=['POST'])
def get_stock_recommendation():
    stock_symbol = request.form.get('stock_name', '').strip()
    stock_extension = request.form.get('country', '').strip()

    country_to_extension = {
        "India": ".ns",
        "USA": "",
        "United Kingdom": ".uk",
        "Germany": ".de",
        "Canada": ".ca",
        "Australia": ".aus"
    }

    if not stock_symbol:
        return "Error: Stock symbol is required.", 400
    if stock_extension not in country_to_extension:
        return f"Error: Invalid country selected: {stock_extension}.", 400

    stockExtension = country_to_extension[stock_extension]
    stock_name = f"{stock_symbol.lower()}{stockExtension}"
    print(stock_name)  # Will output in the format tcs.ns
    # Add your logic to handle `stock_name` here

    categories, values = fetch_StockRecommendation(stock_name)
    return render_template(
        'stockRecommendation.html',
        stock_name=stock_name,
        categories=categories,
        values=values
    )


@main.route("/Financial_Analysis", methods=['POST'])
def get_Financial_Analysis():
    stock_symbol = request.form.get('stock_name', '').strip()
    stock_extension = request.form.get('country', '').strip()

    country_to_extension = {
        "India": ".ns",
        "USA": "",
        "United Kingdom": ".uk",
        "Germany": ".de",
        "Canada": ".ca",
        "Australia": ".aus"
    }

    if not stock_symbol:
        return "Error: Stock symbol is required.", 400
    if stock_extension not in country_to_extension:
        return f"Error: Invalid country selected: {stock_extension}.", 400

    stockExtension = country_to_extension[stock_extension]
    stock_name = f"{stock_symbol.lower()}{stockExtension}"

    print(f"Processing Financial Analysis for stock: {stock_name} (Country: {stock_extension})")

    try:
        # Fetch financial analysis
        analysis_data = fetch_FinancialAnalysis(stock_name)
        if analysis_data is None:
            return f"Could not load financial analysis for {stock_name}.", 500

        (
            total_revenue, cost_of_goods_sold, gross_profit_margin,
            operating_income_margin, operating_income, net_income,
            net_profit_margin, result
        ) = analysis_data

        categories, values = fetch_majorShareHoldersCount(stock_name)
        if categories is None or values is None:
            categories, values = [], []

        latestPrice = latest_price(stock_name) or "N/A"

        fast_info = fetch_fastInfo(stock_name)
        if fast_info is None:
            day_high = day_low = fifty_day_average = market_cap = xAxis = yAxis = priceHike = currency = "N/A"
        else:
            (
                day_high, day_low, fifty_day_average, market_cap,
                xAxis, yAxis, priceHike, currency
            ) = fast_info

        return render_template(
            'fundamental_Analysis.html',
            latestPrice=latestPrice,
            total_revenue=total_revenue,
            cost_of_goods_sold=cost_of_goods_sold,
            gross_profit_margin=gross_profit_margin,
            operating_income=operating_income,
            operating_income_margin=operating_income_margin,
            net_income=net_income,
            net_profit_margin=net_profit_margin,
            result=result,
            stock_name=stock_name,
            categories=categories,
            values=values,
            xAxis=xAxis,
            yAxis=yAxis,
            day_high=day_high,
            day_low=day_low,
            fifty_day_Average=fifty_day_average,
            market_cap=market_cap,
            currency=currency
        )
    except Exception as e:
        print(f"Error encountered: {e}")
        return "Internal Server Error: Unable to process request.", 500


@main.route("/Buy_And_sell_Signals" , methods = ['POST'])

def get_BuySellSignals():

    stock_symbol = request.form.get('stock_name', '').strip()
    stock_extension = request.form.get('country', '').strip()

    country_to_extension = {
        "India": ".ns",
        "USA": "",
        "United Kingdom": ".uk",
        "Germany": ".de",
        "Canada": ".ca",
        "Australia": ".aus"
    }

    if not stock_symbol:
        return "Error: Stock symbol is required.", 400
    if stock_extension not in country_to_extension:
        return f"Error: Invalid country selected: {stock_extension}.", 400

    stockExtension = country_to_extension[stock_extension]
    stock_name = f"{stock_symbol.lower()}{stockExtension}"

    buySellSignals = getTechnicalBuyAndSellSignals(stock_name)
    return render_template('TechnicalAnalysis.html', stock_name=stock_name,
                           BuySellSignalsAnalysis=getTechnicalBuyAndSellSignals)


# @main.route("/Portfolio_Analysis", methods=['GET', 'POST'])
# def portfolio_Analysis():
#     fetch_portfolio = None  # Default value

#     if request.method == 'POST':
#         user_prompt = request.form.get('user_prompt')

#         # Call your analyzer function
#         fetch_portfolio = fetch_portfolio_analyzer(user_prompt)

#         # Render the same page with the result
#         return render_template(
#             'portfolioAnalysis.html',
#             user_prompt=user_prompt,
#             fetch_portfolio=fetch_portfolio
#         )

#     # GET request (initial load)
#     return render_template('portfolioAnalysis.html')


# @main.route("/Portfolio_Analysis", methods=['GET', 'POST'])
# def portfolio_Analysis():
#     if request.method == 'POST':
#         user_prompt = request.form.get('user_prompt')

#         (
#             invested_value, current_value, total_gain_value, total_loss_value,
#             total_gain_percent, total_loss_percent, overall_return_percent,
#             sector_allocation_percent_IT, sector_allocation_percent_Financials,
#             sector_allocation_percent_Energy, sector_allocation_percent_Consumer_Discretionary,
#             sector_allocation_percent_Consumer_Staples, sector_allocation_percent_Health_Care,
#             sector_allocation_percent_Industrials, sector_allocation_percent_Materials,
#             sector_allocation_percent_Communication_Services, sector_allocation_percent_Utilities,
#             sector_allocation_percent_Real_Estate, sector_allocation_percent_Real_Other,
#             summary, top_holdings , 
#         ) = fetch_portfolio_analyzer(user_prompt)

#         # You can now access any of them individually, for example:
#         print(invested_value, summary)


#         data = fetch_dversification_analysis(user_prompt)
#         print(data)

#         return render_template(
#             'portfolioAnalysis.html',
#             invested_value=invested_value,
#             current_value=current_value,
#             total_gain_value=total_gain_value,
#             total_loss_value=total_loss_value,
#             total_gain_percent=total_gain_percent,
#             total_loss_percent=total_loss_percent,
#             overall_return_percent=overall_return_percent,
#             sector_allocation_percent_IT=sector_allocation_percent_IT,
#             sector_allocation_percent_Financials=sector_allocation_percent_Financials,
#             sector_allocation_percent_Energy = sector_allocation_percent_Energy , 
#             sector_allocation_percent_Consumer_Discretionary = sector_allocation_percent_Consumer_Discretionary , 
#             sector_allocation_percent_Consumer_Staples = sector_allocation_percent_Consumer_Staples , 
#             sector_allocation_percent_Health_Care = sector_allocation_percent_Health_Care , 
#             sector_allocation_percent_Industrials = sector_allocation_percent_Industrials , 
#             sector_allocation_percent_Materials = sector_allocation_percent_Materials , 
#             sector_allocation_percent_Communication_Services = sector_allocation_percent_Communication_Services , 
#             sector_allocation_percent_Utilities = sector_allocation_percent_Utilities , 
#             sector_allocation_percent_Real_Estate = sector_allocation_percent_Real_Estate , 
#             sector_allocation_percent_Real_Other = sector_allocation_percent_Real_Other , 


#             summary=summary,
#             top_holdings=top_holdings
#         )

#     return render_template('portfolioAnalysis.html')



@main.route("/Portfolio_Analysis", methods=['GET', 'POST'])

def portfolio_Analysis():
    if request.method == 'POST':
        user_prompt = request.form.get('user_prompt')

        (
            invested_value, current_value, total_gain_value, total_loss_value,
            total_gain_percent, total_loss_percent, overall_return_percent,
            sector_allocation_percent_IT, sector_allocation_percent_Financials,
            sector_allocation_percent_Energy, sector_allocation_percent_Consumer_Discretionary,
            sector_allocation_percent_Consumer_Staples, sector_allocation_percent_Health_Care,
            sector_allocation_percent_Industrials, sector_allocation_percent_Materials,
            sector_allocation_percent_Communication_Services, sector_allocation_percent_Utilities,
            sector_allocation_percent_Real_Estate, sector_allocation_percent_Real_Other,
            percentNeed_in_IT, percentNeed_in_finance, percentNeed_in_energy,
            percentNeed_in_CD, percentNeed_in_CS, percentNeed_in_healthcare,
            percentNeed_in_industrials, percentNeed_in_materials,
            percentNeed_in_communication_services, percentNeed_in_utilities,
            percentNeed_in_real_estate, percentNeed_in_real_other,
            summary, top_holdings
        ) = fetch_portfolio_analyzer(user_prompt)

        # Debug prints
        print(invested_value, summary)

        # data = fetch_dversification_analysis(user_prompt)
        # print(data)

        return render_template(
            'portfolioAnalysis.html',
            invested_value=invested_value,
            current_value=current_value,
            total_gain_value=total_gain_value,
            total_loss_value=total_loss_value,
            total_gain_percent=total_gain_percent,
            total_loss_percent=total_loss_percent,
            overall_return_percent=overall_return_percent,
            
            sector_allocation_percent_IT=sector_allocation_percent_IT,
            sector_allocation_percent_Financials=sector_allocation_percent_Financials,
            sector_allocation_percent_Energy=sector_allocation_percent_Energy,
            sector_allocation_percent_Consumer_Discretionary=sector_allocation_percent_Consumer_Discretionary,
            sector_allocation_percent_Consumer_Staples=sector_allocation_percent_Consumer_Staples,
            sector_allocation_percent_Health_Care=sector_allocation_percent_Health_Care,
            sector_allocation_percent_Industrials=sector_allocation_percent_Industrials,
            sector_allocation_percent_Materials=sector_allocation_percent_Materials,
            sector_allocation_percent_Communication_Services=sector_allocation_percent_Communication_Services,
            sector_allocation_percent_Utilities=sector_allocation_percent_Utilities,
            sector_allocation_percent_Real_Estate=sector_allocation_percent_Real_Estate,
            sector_allocation_percent_Real_Other=sector_allocation_percent_Real_Other,

            summary=summary,
            top_holdings=top_holdings,

            percentNeed_in_IT=percentNeed_in_IT,
            percentNeed_in_finance=percentNeed_in_finance,
            percentNeed_in_energy=percentNeed_in_energy,
            percentNeed_in_CD=percentNeed_in_CD,
            percentNeed_in_CS=percentNeed_in_CS,
            percentNeed_in_healthcare=percentNeed_in_healthcare,
            percentNeed_in_industrials=percentNeed_in_industrials,
            percentNeed_in_materials=percentNeed_in_materials,
            percentNeed_in_communication_services=percentNeed_in_communication_services,
            percentNeed_in_utilities=percentNeed_in_utilities,
            percentNeed_in_real_estate=percentNeed_in_real_estate,
            percentNeed_in_real_other=percentNeed_in_real_other
        )

    return render_template('portfolioAnalysis.html')


































def latest_price(stock_name):
    try:
        latest_price = yf.Ticker(stock_name).history(period='1d')['Close'].iloc[-1]
        # Format the latest price to two decimal places
        latest_price_formatted = "{:.2f}".format(latest_price)
        # Return the formatted latest price as a string
        return str(latest_price_formatted)
    except Exception as e:
        print("Error fetching latest price:", e)
        return "N/A"  # Return "N/A" if there's an error fetching the latest price




def fetch_fake_news_detector(user_prompt):



    from google import genai

    # 1. Initialize the client (as shown in the previous answer)
    # Note: It's best practice to set the API key as an environment variable (GEMINI_API_KEY)
    # and let genai.Client() pick it up automatically.
    client = genai.Client(api_key="AIzaSyBxmfx0h214tSL_DlUQMheL9bsMrgBNH9s")

    # 2. ✅ CHANGE THE MODEL ID
    # The old model: 'gemini-1.5-pro-latest' ❌
    # The new model: 'gemini-2.5-pro' ✅
    MODEL_NAME = 'gemini-2.5-flash' 

    # Define the system instruction for the model's personality and role
    serverPrompt = """
You are a stock news detector. Your role is to determine if stock news provided via text/links is fake or true. Analyze the content of the provided links or text to verify its authenticity, cross-referencing with reliable sources if necessary. If the input contains both links and text, analyze both for consistency and accuracy.

If the user input is unrelated to stock news thrugh texts or financial markets, respond with:

'Sorry, I can only analyze stock news provided via links or text. Please provide valid stock news content.'   
    """


    # Replace {user_prompt} with the actual variable holding the user's question
    #user_prompt = "What is a P/E ratio?"

    # 3. Create a chat using the client object with the correct model and system instruction
    # (Assuming you are using the correct, modern google-genai library)
    chat = client.chats.create(
        model=MODEL_NAME,
        config={"system_instruction": serverPrompt}
    )

    response = chat.send_message(user_prompt)

    return response.text












#     # Configure the Gemini client
#     genai.configure(api_key="AIzaSyBW2Xwxxz4SK01_vUrTYhZ_8lc5p8YrT-A")

#     model = genai.GenerativeModel('gemini-1.5-pro')

#     serverPrompt = f"""
# You are a stock news detector. Your role is to determine if stock news provided via text/links is fake or true. Analyze the content of the provided links or text to verify its authenticity, cross-referencing with reliable sources if necessary. If the input contains both links and text, analyze both for consistency and accuracy.

# If the user input is unrelated to stock news thrugh texts or financial markets, respond with:

# 'Sorry, I can only analyze stock news provided via links or text. Please provide valid stock news content.' Here is the user prompt:    {user_prompt}
#     """

#     # Create a chat
#     chat = model.start_chat(history=[])

#     response = chat.send_message(serverPrompt)

#     return response.text






def fetch_news(stock_symbol):
    """Fetch news from Yahoo Finance RSS feed"""
    try:
        # URL encode the stock symbol
        encoded_symbol = urllib.parse.quote(stock_symbol)
        rss_url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={encoded_symbol}&region=US&lang=en-US"
        
        feed = feedparser.parse(rss_url)
        news_items = []
        
        for entry in feed.entries[:10]:  # Get first 3 articles
            # Parse and format the publication date
            published = ""
            if hasattr(entry, 'published_parsed'):
                published = datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%d %H:%M')
            
            news_items.append({
                'title': entry.get('title', 'No title available'),
                'publisher': 'Yahoo Finance',
                'link': entry.get('link', '#'),
                'providerPublishTime': published,
                'summary': entry.get('summary', 'No summary available'),
                'image': get_image_from_description(entry.get('description', ''))
            })
        
        return news_items
    
    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        return []

def get_image_from_description(description):
    """Extract image URL from HTML description if available"""
    if '<img' in description:
        start = description.find('src="') + 5
        end = description.find('"', start)
        return description[start:end]
    return ''



# def fetch_news(stock_name):

#     url = f"https://newsapi.org/v2/everything?q={stock_name}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"

#     try:
#         response = requests.get(url)
#         news_data = response.json()

#         if news_data.get("status") == "ok":
#             articles = news_data.get("articles", [])
#             return [{
#                 "title": article.get("title", "No Title"),
#                 "providerPublishTime": article.get("publishedAt", "Unknown Date"),
#                 "publisher": article.get("source", {}).get("name", "Unknown Source"),
#                 "summary": article.get("description", "No summary available."),
#                 "link": article.get("url"),
#                 "image": article.get("urlToImage", "")
#             } for article in articles[:10]]
#         else:
#             print("News API error:", news_data.get("message", "Unknown error"))
#             return []
#     except Exception as e:
#         print("Error fetching news:", e)
#         return []
    
def fetch_dividends(stock_name):
    try:
        data = yf.Ticker(stock_name).dividends
        dividend_data = data.to_dict()
        return dividend_data
    except Exception as e:
        return str(e)

def fetch_balanceSheet(stock_name):
    try:
        balanceSheet = yf.Ticker(stock_name).balance_sheet
        balanceSheetData = balanceSheet.to_dict()
        return balanceSheetData
    except Exception as e:
        return str(e)

def fetch_Income_Statements(stock_name):
    try:
        incomeStatementsData = yf.Ticker(stock_name).income_stmt
        incomeStatementDict = incomeStatementsData.to_dict()
        return incomeStatementDict
    except Exception as e:
        return str(e)


def fetch_StockRecommendation(stock_name):
    try:
        reccomendationData = yf.Ticker(stock_name).recommendations

        rowColumn_Array = []

        for index, row in reccomendationData.iterrows():
            for column in reccomendationData.columns:
                rowColumn_Array.append(row[column])

        # Prepare data for Chart.js
        categories = ['STRONG BUY ', 'BUY ', 'HOLD', 'SELL', 'STRONG SELL']
        values = [
            rowColumn_Array[19],
            rowColumn_Array[20],
            rowColumn_Array[21],
            rowColumn_Array[22],
            rowColumn_Array[23]
        ]

        return categories, values
    except Exception as e:
        return str(e), []


def fetch_majorShareHoldersCount(stock_name):

    #graph_path = os.path.join('static', 'Major_Share_Holder_Count_Graph.png')
    try:
        major_shareholder_Count_data = yf.Ticker(stock_name).get_major_holders()
        index_Array = []
        rowColumn_Array = []

        for index, row in major_shareholder_Count_data.iterrows():
            # print("Holder:", index)
            index_Array.append(index)

            for column in major_shareholder_Count_data.columns:
                # print("this is column ",column + ":", row[column])
                rowColumn_Array.append(row[column])

        categories = [index_Array[0], index_Array[1], index_Array[2], index_Array[3]]
        values = [rowColumn_Array[0], rowColumn_Array[1], rowColumn_Array[2], rowColumn_Array[3]]


        return categories , values

    except Exception as e:
        return str(e), []


def fetch_FinancialAnalysis(stock_name):

    try :

        balance_sheet = yf.Ticker(stock_name).balance_sheet
        income_statement = yf.Ticker(stock_name).financials

        latest_date = balance_sheet.columns[0]
        # print(balance_sheet)
        # print(income_statement)

        print('CASH FLOW ANALYSIS OF THE COMAPTY')
        print('---------------------------------------------------------------------------------------------------------')

        #print(balance_sheet)

        #current assets f the company
        cash_and_cash_equivalents = balance_sheet.loc['Cash And Cash Equivalents', latest_date]
        accounts_receivable = balance_sheet.loc['Net Receivables', latest_date] if 'Net Receivables' in balance_sheet.index else 0
        inventory = balance_sheet.loc['Inventory', latest_date] if 'Inventory' in balance_sheet.index else 0
        prepaid_assets = balance_sheet.loc['Prepaid Expenses', latest_date] if 'Prepaid Expenses' in balance_sheet.index else 0
        other_current_assets = balance_sheet.loc['Other Current Assets', latest_date] if 'Other Current Assets' in balance_sheet.index else 0
        current_assets = cash_and_cash_equivalents + accounts_receivable + inventory + prepaid_assets + other_current_assets

        #current liabilaities of the comapny
        accounts_payable = balance_sheet.loc['Accounts Payable', latest_date] if 'Accounts Payable' in balance_sheet.index else 0
        current_debt = balance_sheet.loc['Short Long Term Debt', latest_date] if 'Short Long Term Debt' in balance_sheet.index else 0
        other_current_liabilities = balance_sheet.loc['Other Current Liabilities', latest_date] if 'Other Current Liabilities' in balance_sheet.index else 0
        current_liabilities = accounts_payable + current_debt + other_current_liabilities

        #curent ratio
        current_ratio = current_assets / current_liabilities

        #profit margin
        net_income = income_statement.loc['Net Income', latest_date] if 'Net Income' in income_statement.index else 0
        total_revenue = income_statement.loc['Total Revenue', latest_date] if 'Total Revenue' in income_statement.index else 0
        profit_margin = (net_income / total_revenue) * 100 if total_revenue != 0 else 0


        #shareholder equity
        total_shareholders_equity = balance_sheet.loc['Total Stockholder Equity', latest_date] if 'Total Stockholder Equity' in balance_sheet.index else 0

        #roe ca;culation its workin progress
        roe = (net_income / total_shareholders_equity) * 100 if total_shareholders_equity != 0 else 0

        # Total Debt
        total_debt = balance_sheet.loc['Total Debt', latest_date] if 'Total Debt' in balance_sheet.index else 0

        # Total Assets
        total_assets = balance_sheet.loc['Total Assets', latest_date] if 'Total Assets' in balance_sheet.index else 0

        #debt ratoo calcuation
        debt_ratio = (total_debt / total_assets) * 100 if total_assets != 0 else 0

        #Liquidty ratio
        quick_ratio = (current_assets - inventory) / current_liabilities if current_liabilities != 0 else 0
        #cash ratio
        cash_ratio = cash_and_cash_equivalents / current_liabilities if current_liabilities != 0 else 0


        print('financial statements ')
        print('---------------------------------------------------------------------------------------------------------')
        # Revenue
        total_revenue = income_statement.loc['Total Revenue', latest_date] if 'Total Revenue' in income_statement.index else 0

        # Cost of Goods Sold
        cost_of_goods_sold = income_statement.loc['Cost Of Revenue', latest_date] if 'Cost Of Revenue' in income_statement.index else 0

        # Grosss Profit Margin
        gross_profit_margin = ((total_revenue - cost_of_goods_sold) / total_revenue) * 100 if total_revenue != 0 else 0


        operating_income = income_statement.loc['Operating Income', latest_date] if 'Operating Income' in income_statement.index else 0

        # Operating Income Margin
        operating_income_margin = (operating_income / total_revenue) * 100 if total_revenue != 0 else 0


        # Net Income
        net_income = income_statement.loc['Net Income', latest_date] if 'Net Income' in income_statement.index else 0

        # Net Profit Margin
        net_profit_margin = (net_income / total_revenue) * 100 if total_revenue != 0 else 0


        total_revenue
        cost_of_goods_sold
        gross_profit_margin
        operating_income_margin
        operating_income
        net_income
        net_profit_margin



        if current_ratio > 1 and profit_margin > 0 and debt_ratio < 50:

           result = f"{stock_name.upper()} Share Seems to be Fundamentally Strong according to Our Analysis "




        else :

            result = 'Company seems Fundamentally Weak More Analysis Should be Executed '

        return total_revenue , \
            cost_of_goods_sold , \
            gross_profit_margin , \
            operating_income_margin , \
            operating_income , \
            net_income , \
            net_profit_margin , \
            result

    except Exception as e :

        print('Could not load the details Due to error : {e}')

def fetch_fastInfo(stock_name):
    # Fetch fast_info for the ticker
    operation = yf.Ticker(stock_name).fast_info

    print(operation)

    # Access and print the 'dayHigh' value
    if 'dayHigh' and 'dayLow' and 'fiftyDayAverage' and 'marketCap' and 'quoteType' and 'yearChange' in operation:
        day_high = operation['dayHigh']
        day_low = operation['dayLow']
        fifty_day_average = operation['fiftyDayAverage']
        market_cap = operation['marketCap']
        year_high = operation['yearHigh']
        year_low = operation['yearLow']
        currency = operation['currency']

        xAxis = ['yearhigh', 'yearlow']
        yAxis = [year_high, year_low]

        # calculation profiit for percent return in yaer
        priceHike = ((year_high - year_low) / year_high) * 100

    else:
        print("Key 'dayHigh' not found in fast_info.")


    return  day_high,\
            day_low, \
            fifty_day_average,\
            market_cap, \
            xAxis,\
            yAxis ,\
            priceHike,\
            currency



def getTechnicalBuyAndSellSignals(share_name):

    # import yfinance as yf
    # import pandas as pd
    # import numpy as np
    # import matplotlib.pyplot as plt
    #
    # # Fetch stock data
    # def get_stock_data(stock_symbol, interval='1h', period='5d'):
    #     try:
    #         data = yf.download(tickers=stock_symbol, interval=interval, period=period)
    #         data.reset_index(inplace=True)
    #         data.rename(columns={'Datetime': 'Datetime', 'Close': 'Close'}, inplace=True)
    #         return data
    #     except Exception as e:
    #         print(f"Error fetching stock data: {e}")
    #         return None
    #
    # # Identify support and resistance
    # def calculate_support_resistance(data):
    #     data['Support'] = np.nan
    #     data['Resistance'] = np.nan
    #     for i in range(1, len(data) - 1):
    #         if data['Close'].iloc[i] < data['Close'].iloc[i - 1] and data['Close'].iloc[i] < data['Close'].iloc[i + 1]:
    #             data.loc[data.index[i], 'Support'] = data['Close'].iloc[i]
    #         if data['Close'].iloc[i] > data['Close'].iloc[i - 1] and data['Close'].iloc[i] > data['Close'].iloc[i + 1]:
    #             data.loc[data.index[i], 'Resistance'] = data['Close'].iloc[i]
    #     return data
    #
    # # Add advanced technical indicators
    # def add_indicators(data):
    #     delta = data['Close'].diff()
    #     gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    #     loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    #     rs = gain / loss
    #     data['RSI'] = 100 - (100 / (1 + rs))
    #     data['EMA_12'] = data['Close'].ewm(span=12, adjust=False).mean()
    #     data['EMA_26'] = data['Close'].ewm(span=26, adjust=False).mean()
    #     data['MACD'] = data['EMA_12'] - data['EMA_26']
    #     data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()
    #     data['BB_Mid'] = data['Close'].rolling(window=20).mean()
    #     data['BB_Upper'] = data['BB_Mid'] + 2 * data['Close'].rolling(window=20).std()
    #     data['BB_Lower'] = data['BB_Mid'] - 2 * data['Close'].rolling(window=20).std()
    #     data['ATR'] = data['High'] - data['Low']
    #     return data
    #
    # # Detect patterns
    # def detect_patterns(data):
    #     data['Pattern'] = ''
    #     for i in range(2, len(data) - 2):
    #         if data['Close'].iloc[i - 2] < data['Close'].iloc[i - 1] > data['Close'].iloc[i] and \
    #                 data['Close'].iloc[i + 1] < data['Close'].iloc[i] > data['Close'].iloc[i + 2]:
    #             data.loc[i, 'Pattern'] = 'Head and Shoulders Top'
    #         if data['Close'].iloc[i - 2] > data['Close'].iloc[i - 1] < data['Close'].iloc[i] and \
    #                 data['Close'].iloc[i + 1] > data['Close'].iloc[i] < data['Close'].iloc[i + 2]:
    #             data.loc[i, 'Pattern'] = 'Inverse Head and Shoulders'
    #     return data
    #
    # # Generate buy/sell signals
    # def generate_signals(data, profit_threshold=0.015, stop_loss_threshold=0.007):
    #     """
    #     Generates buy and sell signals based on multiple indicators.
    #     """
    #     data['Signal'] = 0  # Default: Hold
    #     buy_price = None  # Track the buy price for sell conditions
    #
    #     for i in range(1, len(data)):
    #
    #         # Generate buy signal
    #         if buy_price is None:
    #             if (data['RSI'].iloc[i] < 35 and data['Close'].iloc[i] <= data['Support'].iloc[i]) or \
    #                     (data['Pattern'].iloc[i] == 'Inverse Head and Shoulders'):
    #                 buy_price = data['Close'].iloc[i]
    #                 data.loc[i, 'Signal'] = 1  # Buy signal
    #         else:
    #             # Generate sell signals
    #             current_price = data['Close'].iloc[i]
    #             if current_price >= buy_price * (1 + profit_threshold):  # Profit-taking
    #                 data.loc[i, 'Signal'] = -1
    #                 buy_price = None
    #             elif current_price <= buy_price * (1 - stop_loss_threshold):  # Stop-loss
    #                 data.loc[i, 'Signal'] = -1
    #                 buy_price = None
    #             elif data['Pattern'].iloc[i] == 'Head and Shoulders Top':  # Pattern confirmation
    #                 data.loc[i, 'Signal'] = -1
    #                 buy_price = None
    #
    #     return data
    #
    # # Plot the data
    # def plot_signals(data, stock_symbol):
    #     plt.figure(figsize=(14, 7))
    #     plt.plot(data['Datetime'], data['Close'], label='Close Price', alpha=0.5, color='blue')
    #     plt.scatter(data['Datetime'][data['Signal'] == 1],
    #                 data['Close'][data['Signal'] == 1],
    #                 color='green', label='Buy Signal', marker='^', alpha=1)
    #     plt.scatter(data['Datetime'][data['Signal'] == -1],
    #                 data['Close'][data['Signal'] == -1],
    #                 color='red', label='Sell Signal', marker='v', alpha=1)
    #
    #
    #     graph_path = os.path.join('static', 'TechnicalAnalysisWithBuyAndSellSignals.png')
    #
    #
    #     plt.plot(data['Datetime'], data['BB_Upper'], label='Bollinger Upper', linestyle='--', alpha=0.7, color='orange')
    #     plt.plot(data['Datetime'], data['BB_Lower'], label='Bollinger Lower', linestyle='--', alpha=0.7, color='orange')
    #     plt.scatter(data['Datetime'], data['Support'], color='cyan', label='Support Levels', alpha=0.7)
    #     plt.scatter(data['Datetime'], data['Resistance'], color='magenta', label='Resistance Levels', alpha=0.7)
    #     plt.title(f"{stock_symbol} Advanced Buy/Sell Signals")
    #     plt.xlabel("Datetime")
    #     plt.ylabel("Price")
    #     plt.legend()
    #     plt.grid()
    #     print(f"Graph saved at: {graph_path}")
    #     plt.savefig(graph_path)
    #     plt.close()
    #
    #
    #
    # # Main function
    # def main(stock_symbol):
    #     data = get_stock_data(stock_symbol)
    #     if data is not None:
    #         data = calculate_support_resistance(data)
    #         data = add_indicators(data)
    #         data = detect_patterns(data)
    #         data = generate_signals(data)
    #         plot_signals(data, stock_symbol)
    #
    # # Example usage
    # # if __name__ == "__main__":
    # #     # stock_symbol = 'ebay'  # Example stock
    # #     #
    # #     # main(stock_symbol)
    # #
    #
    #
    # return main(stock_name)



    














    import matplotlib
    matplotlib.use('Agg')  # ✅ Prevent MacOS NSWindow crash

    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import yfinance as yf
    import os


    save_dir="static"
    # Ensure static directory exists
    os.makedirs(save_dir, exist_ok=True)

    # Fetch stock data
    tsla = yf.download(share_name, period='3mo', interval='1d', auto_adjust=True)
    tsla.reset_index(inplace=True)
    tsla['Price'] = tsla['Close']
    tsla['Day'] = range(len(tsla))

    # Bollinger Bands
    tsla['MA20'] = tsla['Price'].rolling(window=20).mean()
    tsla['STD20'] = tsla['Price'].rolling(window=20).std()
    tsla['Upper'] = tsla['MA20'] + 2 * tsla['STD20']
    tsla['Lower'] = tsla['MA20'] - 2 * tsla['STD20']

    # Buy/Sell logic
    buy_price = 30
    target_return = 1.10
    buy_signals = []
    sell_signals = []
    holding = False
    entry_price = None

    for i in range(len(tsla)):
        price = float(tsla.loc[i, 'Price'].item())  # ✅ safe scalar extraction
        if not holding and price >= buy_price:
            buy_signals.append((tsla.loc[i, 'Day'], price))
            entry_price = price
            holding = True
        elif holding and price >= entry_price * target_return:
            sell_signals.append((tsla.loc[i, 'Day'], price))
            holding = False

    # Support & Resistance
    support = tsla['Price'][(tsla['Price'].shift(1) > tsla['Price']) & (tsla['Price'].shift(-1) > tsla['Price'])]
    resistance = tsla['Price'][(tsla['Price'].shift(1) < tsla['Price']) & (tsla['Price'].shift(-1) < tsla['Price'])]

    # Plotting
    plt.style.use('seaborn-v0_8')
    plt.figure(figsize=(14, 7))
    plt.plot(tsla['Day'], tsla['Price'], label='Close Price', color='blue')
    plt.plot(tsla['Day'], tsla['Upper'], linestyle='--', color='orange', label='Bollinger Upper')
    plt.plot(tsla['Day'], tsla['Lower'], linestyle='--', color='orange', label='Bollinger Lower')

    # Buy/Sell markers
    for i, price in buy_signals:
        plt.scatter(i, price, marker='^', color='green', s=120, label='Buy Signal')
    for i, price in sell_signals:
        plt.scatter(i, price, marker='v', color='red', s=120, label='Sell Signal')

    # Support/Resistance markers
    plt.scatter(support.index, support, color='green', s=80, label='Support Level')
    plt.scatter(resistance.index, resistance, color='red', s=80, label='Resistance Level')

    plt.title(f'{share_name.upper()} Buy/Sell Signal Chart with Bollinger Bands')
    plt.xlabel('Day')
    plt.ylabel('Price (In Your Local Currency)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    graph_path = os.path.join(save_dir, 'chart.png')
    plt.savefig(graph_path)
    plt.close()

    print(f"✅ Chart saved at: {graph_path}")
    return graph_path




    print("hello")

def fetch_AI_Assistant(user_prompt):
    from google import genai

    # 1. Initialize the client (as shown in the previous answer)
    # Note: It's best practice to set the API key as an environment variable (GEMINI_API_KEY)
    # and let genai.Client() pick it up automatically.
    client = genai.Client(api_key="AIzaSyBxmfx0h214tSL_DlUQMheL9bsMrgBNH9s")

    # 2. ✅ CHANGE THE MODEL ID
    # The old model: 'gemini-1.5-pro-latest' ❌
    # The new model: 'gemini-2.5-pro' ✅
    MODEL_NAME = 'gemini-2.5-pro' 

    # Define the system instruction for the model's personality and role
    SYSTEM_INSTRUCTION = f"""
    You are a stock information provider for beginners or explainer of stock concepts and also explain how your mindset should be while investing in stocks through Benjamin Graham concepts/Warren Buffett. Do not take their names explicitly. Your role is to provide stock information or stock concepts to the user. If the user input is unrelated to 
    stock information / financial markets , respond with: sorry, i dont have permission to provide information on subject you asked.
    """

    # Replace {user_prompt} with the actual variable holding the user's question
    #user_prompt = "What is a P/E ratio?"

    # 3. Create a chat using the client object with the correct model and system instruction
    # (Assuming you are using the correct, modern google-genai library)
    chat = client.chats.create(
        model=MODEL_NAME,
        config={"system_instruction": SYSTEM_INSTRUCTION}
    )

    response = chat.send_message(user_prompt)

    return response.text








#fucntion for analyzing portfolio analysis
def fetch_portfolio_analyzer(user_prompt):
    client = genai.Client(api_key="AIzaSyAL_WV2kPHgDlhU9QkB9IXCv5TuiNUs3Ws")

    MODEL_NAME = "gemini-2.5-pro"

    # SYSTEM_INSTRUCTION = """
    # You are a financial data assistant.

    # Given a user's textual description of their stock portfolio (including quantities, prices, and company names),
    # you must calculate and return the following information **strictly in JSON format**:

    # {
    #   "number_of_holdings_in_entire_portfolio": <int>,
    #   "invested_value": <float>,
    #   "current_value": <float>,
    #   "total_gain_value": <float>,
    #   "total_loss_value": <float>,
    #   "total_gain_percent": <float>,
    #   "total_loss_percent": <float>,
    #   "overall_return_percent": <float>,
    #   "sector_allocation_percent": {
    #       "Information_Technology": <float>,
    #       "Financials": <float>,
    #       "Energy": <float>,
    #       "Consumer_Discretionary": <float>,
    #       "Consumer_Staples": <float>,
    #       "Health_Care": <float>,
    #       "Industrials": <float>,
    #       "Materials": <float>,
    #       "Communication_Services": <float>,
    #       "Utilities": <float>,
    #       "Real_Estate": <float>,
    #       "Other": <float>
    #   },
    #   "top_holdings": [
    #       {"symbol": "<ticker>", "sector": "<sector_name>", "weight_percent": <float>}
    #   ],
    #   "summary": "<short summary of the portfolio>"
    # }
    # """





    SYSTEM_INSTRUCTION = """
    You are a financial data assistant.

    Given a user's textual description of their stock portfolio (including quantities, prices, and company names),
    you must calculate and return the following information **strictly in JSON format**:

    {
    "number_of_holdings_in_entire_portfolio": <int>,
    "invested_value": <float>,
    "current_value": <float>,
    "total_gain_value": <float>,
    "total_loss_value": <float>,
    "total_gain_percent": <float>,
    "total_loss_percent": <float>,
    "overall_return_percent": <float>,
    "sector_allocation_percent": {
        "Information_Technology": <float>,
        "Financials": <float>,
        "Energy": <float>,
        "Consumer_Discretionary": <float>,
        "Consumer_Staples": <float>,
        "Health_Care": <float>,
        "Industrials": <float>,
        "Materials": <float>,
        "Communication_Services": <float>,
        "Utilities": <float>,
        "Real_Estate": <float>,
        "Other": <float>
    },
    "top_holdings": [
        {
        "symbol": "<ticker>",
        "sector": "<sector_name>",
        "weight_percent": <float>
        }
    ],
    "summary": "<short summary of the portfolio>",

    // ✅ NEW: Combined stock names with country extensions
    "stock_identifiers_with_extension": ["<stock_name_1.ext>", "<stock_name_2.ext>", "..."]
    }
    """









    chat = client.chats.create(
        model=MODEL_NAME,
        config={"system_instruction": SYSTEM_INSTRUCTION}
    )

    response = chat.send_message(user_prompt)

    # ✅ Extract only the text content
    try:
        if hasattr(response, 'text'):
            x = response.text
        else:
            x = response.candidates[0].content.parts[0].text
    except Exception as e:
        print("Error extracting text:", e)
        return None

    def safe_json_loads(raw_text):
        cleaned = raw_text.strip()

        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            cleaned = cleaned.replace("json", "", 1).strip()

        return json.loads(cleaned)

    # usage
    data = safe_json_loads(x)

    invested_value = data["invested_value"]
    current_value = data["current_value"]

    total_gain_value = data["total_gain_value"]
    total_loss_value = data["total_loss_value"]

    total_gain_percent = data["total_gain_percent"]
    total_loss_percent = data["total_loss_percent"]

    overall_return_percent = data["overall_return_percent"]

    sector_allocation_percent_IT = data["sector_allocation_percent"]["Information_Technology"]
    sector_allocation_percent_Financials = data["sector_allocation_percent"]["Financials"]
    sector_allocation_percent_Energy = data["sector_allocation_percent"]["Energy"]
    sector_allocation_percent_Consumer_Discretionary = data["sector_allocation_percent"]["Consumer_Discretionary"]
    sector_allocation_percent_Consumer_Staples = data["sector_allocation_percent"]["Consumer_Staples"]
    sector_allocation_percent_Health_Care = data["sector_allocation_percent"]["Health_Care"]
    sector_allocation_percent_Industrials = data["sector_allocation_percent"]["Industrials"]
    sector_allocation_percent_Materials = data["sector_allocation_percent"]["Materials"]
    sector_allocation_percent_Communication_Services = data["sector_allocation_percent"]["Communication_Services"]
    sector_allocation_percent_Utilities = data["sector_allocation_percent"]["Utilities"]
    sector_allocation_percent_Real_Estate = data["sector_allocation_percent"]["Real_Estate"]
    sector_allocation_percent_Real_Other = data["sector_allocation_percent"]["Other"]

    summary = data["summary"]

    number_of_holdings = data["number_of_holdings_in_entire_portfolio"]

    stock_symbol_data = data["stock_identifiers_with_extension"]


    print("number of holdings ", number_of_holdings)

    
    

    top_holdings = []

    for stock in data["top_holdings"]:
        top_holdings.append({
            "symbol": stock["symbol"],
            "sector": stock["sector"],
            "weight_percent": stock["weight_percent"]
        })    

    print("this is invested value :", data["invested_value"])


    total_allocation_in_each_sector = 100/number_of_holdings
    percentNeed_in_IT = total_allocation_in_each_sector - sector_allocation_percent_IT
    percentNeed_in_finance = total_allocation_in_each_sector - sector_allocation_percent_Financials
    percentNeed_in_energy = total_allocation_in_each_sector - sector_allocation_percent_Energy
    percentNeed_in_CD = total_allocation_in_each_sector - sector_allocation_percent_Consumer_Discretionary
    percentNeed_in_CS = total_allocation_in_each_sector - sector_allocation_percent_Consumer_Staples
    percentNeed_in_healthcare = total_allocation_in_each_sector - sector_allocation_percent_Health_Care
    percentNeed_in_industrials = total_allocation_in_each_sector - sector_allocation_percent_Industrials
    percentNeed_in_materials = total_allocation_in_each_sector - sector_allocation_percent_Materials 
    percentNeed_in_communication_services = total_allocation_in_each_sector - sector_allocation_percent_Communication_Services
    percentNeed_in_utilities = total_allocation_in_each_sector - sector_allocation_percent_Utilities
    percentNeed_in_real_estate = total_allocation_in_each_sector - sector_allocation_percent_Real_Estate
    percentNeed_in_real_other = total_allocation_in_each_sector - sector_allocation_percent_Real_Other





    x =  computation_of_SD_for_portfolio_analysis(stock_symbol_data)
    print("this is stock symbol data : " , stock_symbol_data)
    print("this is portfolio SD : " , x)






    return (
        invested_value,
        current_value,
        total_gain_value,
        total_loss_value,
        total_gain_percent,
        total_loss_percent,
        overall_return_percent,

        sector_allocation_percent_IT,
        sector_allocation_percent_Financials,
        sector_allocation_percent_Energy,
        sector_allocation_percent_Consumer_Discretionary,
        sector_allocation_percent_Consumer_Staples,
        sector_allocation_percent_Health_Care,
        sector_allocation_percent_Industrials,
        sector_allocation_percent_Materials,
        sector_allocation_percent_Communication_Services,
        sector_allocation_percent_Utilities,
        sector_allocation_percent_Real_Estate,
        sector_allocation_percent_Real_Other,

        percentNeed_in_IT,
        percentNeed_in_finance,
        percentNeed_in_energy,
        percentNeed_in_CD,
        percentNeed_in_CS,
        percentNeed_in_healthcare,
        percentNeed_in_industrials,
        percentNeed_in_materials,
        percentNeed_in_communication_services,
        percentNeed_in_utilities,
        percentNeed_in_real_estate,
        percentNeed_in_real_other,

        summary,
        top_holdings
    )









#still indevelopeing phase 
def computation_of_SD_for_portfolio_analysis(tickers):
    if not isinstance(tickers, list):
        raise ValueError("Tickers must be a list, e.g. ['TCS.NS', 'INFY.NS']")

    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=365)

    valid_tickers = []
    for t in tickers:
        try:
            info = yf.Ticker(t).history(period="1mo")
            if not info.empty:
                valid_tickers.append(t)
        except:
            continue

    if not valid_tickers:
        print("❌ No valid tickers found.")
        return

    print(f"✅ Valid tickers ({len(valid_tickers)}): {valid_tickers}")

    data = yf.download(valid_tickers, start=start_date, end=end_date, auto_adjust=True)['Close']

    if data.empty:
        print("❌ No data fetched. Check connection or Yahoo API limits.")
        return

    returns = data.pct_change().dropna()
    weights = np.ones(len(valid_tickers)) / len(valid_tickers)
    cov_matrix = returns.cov()

    portfolio_var = np.dot(weights.T, np.dot(cov_matrix, weights))
    portfolio_sd = np.sqrt(portfolio_var)
    annualized_sd = portfolio_sd * np.sqrt(252)
    individual_sds = (returns.std() * np.sqrt(252)).sort_values(ascending=False)

    print(f"\n📊 Annualized Portfolio SD: {round(annualized_sd * 100, 2)} %")
    print("\n📈 Individual Stock SDs (Annualized):\n")
    print(individual_sds)
    print("this is portfolio sd " , portfolio_sd)

    return portfolio_sd











#FOR PORTFOLIO INSIGHTS BUTTON IDEA 


#in portfolio insights the user wil add each stock and all his portfolio then click generate then we will provide them with all the web charts like which stock 
#is more sector is more also ai analysis on how your portfolio should e which is risky and which is not etc like that everything ai will predict and give all the reports all financial stamenets of hsi protfolio etc 







#demo data 
#Qty. 20 • Buy avg. 58.20 +145.36% ASHOKLEY +1,692.00 Invested 1,164.00 LTP 142.80 Qty. 10 • Buy avg. 211.91 -24.40% BIRLACABLE -517.10 Invested 2,119.10 LTP 160.20 Qty. 15 • Buy avg. 217.50 +79.49% COALINDIA +2,593.50 Invested 3,262.50 LTP 390.40 Qty. 10 • Buy avg. 79.25 +306.60% ETERNAL +2,429.95 Invested 792.55 LTP 322.25 Qty. 8 • Buy avg. 216.15 +77.26% EXIDEIND +1,336.00 Invested 1,729.20 LTP 383.15 Qty. 10 • Buy avg. 113.86 +61.87% GAIL +704.40 Invested 1,138.60 LTP 184.30 Qty. 20 • Buy avg. 772.40 +28.36% HDFCBANK +4,381.00 Invested 15,448.00 LTP 991.45 Qty. 7 • Buy avg. 1,960.00 +23.06% HYUNDAI +3,163.30 Invested 13,720.00