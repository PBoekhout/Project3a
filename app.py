from flask import Flask, render_template, request, flash, redirect, url_for
import Functions
import pygal
from datetime import datetime
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

#app route to main page
@app.route('/', methods=['GET', 'POST'])
def index():
    dataframe = pd.read_csv('stocks.csv')
    stock_symbols = dataframe['Symbol'].dropna().unique().tolist()
    stock_symbols.sort()
    chart_svg = None
    symbol = None

    #request method POST
    if request.method == 'POST':
        symbol = request.form.get('symbol').upper()
        chart_type = request.form.get('chart_type')
        time_option = request.form.get('time_option')
        interval = request.form.get('interval') if time_option == '1' else None
        start_date = request.form.get('start_date') if time_option != '1' else None
        end_date = request.form.get('end_date') if time_option != '1' else None

        errors = []
        if not symbol.isalnum():
            errors.append("Invalid symbol. Please enter a valid stock symbol.")
        if chart_type not in ['1', '2']:
            errors.append("Invalid chart type selected.")
        if time_option not in ['1', '2', '3', '4']:
            errors.append("Invalid time series option selected.")
        if time_option == '1' and interval not in ['1', '5', '15', '30', '60']:
            errors.append("Invalid interval selected for intraday data.")
        if time_option != '1':
            if not start_date or not end_date:
                errors.append("Please provide both start date and end date.")
            else:
                try:
                    datetime.strptime(start_date, '%Y-%m-%d')
                    datetime.strptime(end_date, '%Y-%m-%d')
                    if start_date > end_date:
                        errors.append("Start date cannot be after end date.")
                except ValueError:
                    errors.append("Invalid date format. Please use YYYY-MM-DD.")
        if errors:
            for error in errors:
                flash(error)
            return redirect(url_for('index'))

        try:
            data_filter = None
            if time_option == '1':
                data = Functions.TIME_SERIES_INTRADAY(symbol, interval)
                time_series_key = f'Time Series ({interval}min)'
                time_series_data = data.get(time_series_key, {})
                data_filter = time_series_data
            else:
                if time_option == '2':
                    data = Functions.TIME_SERIES_DAILY(symbol)
                elif time_option == '3':
                    data = Functions.TIME_SERIES_WEEKLY(symbol)
                elif time_option == '4':
                    data = Functions.TIME_SERIES_MONTHLY(symbol)
                data_key = next((key for key in data.keys() if "Time Series" in key), None)
                if data_key:
                    time_series_data = data[data_key]
                    data_filter = {date: values for date, values in time_series_data.items() if start_date <= date <= end_date}

            if not data_filter:
                flash("No data found for the given inputs.")
                return redirect(url_for('index'))

            dates = sorted(data_filter.keys())
            open_prices = [float(data_filter[date]['1. open']) for date in dates]
            high_prices = [float(data_filter[date]['2. high']) for date in dates]
            low_prices = [float(data_filter[date]['3. low']) for date in dates]
            close_prices = [float(data_filter[date]['4. close']) for date in dates]

            if chart_type == "1":
                chart = pygal.Bar(x_label_rotation=45)
            elif chart_type == "2":
                chart = pygal.Line(x_label_rotation=45)
            else:
                flash("Invalid chart type.")
                return redirect(url_for('index'))

            chart.add("Open", open_prices)
            chart.add("High", high_prices)
            chart.add("Low", low_prices)
            chart.add("Close", close_prices)
            chart.x_labels = dates

            if time_option == '1':
                chart.title = f"Stock data for {symbol} ({interval}min)"
                chart.x_labels_major_every = len(dates) // 10 or 1
            else:
                chart.title = f"Stock data for {symbol}: {start_date} to {end_date}"

            chart_svg = chart.render_data_uri()

        except Exception as e:
            flash(f"There was an error {str(e)}")
            return redirect(url_for('index'))

    return render_template('index.html', stock_symbols=stock_symbols, chart_svg=chart_svg, symbol=symbol)

app.run(host="0.0.0.0")
