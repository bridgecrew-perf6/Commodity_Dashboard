import numpy as np
import pandas as pd
import datetime as dt
from pandas.tseries.offsets import BMonthEnd, BDay
from datetime import date
import plotly
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
# import 
import pandas_ta as ta
from ta import add_all_ta_features
import quandl
import streamlit as st

# Page Configuration
st.set_page_config(layout='centered', initial_sidebar_state='expanded')

# Header
st.image('https://i.imgur.com/2UVBzv8.png', use_column_width=True)

st.markdown('This web application is intended to provide an interactive view of '
            'the most liquid commodity markets. Historical price data has been '
            'compiled from each of the corresponding futures exchanges and is pulled '
            'using the Quandl API. Modify the output by selecting an end date and page view '
            'from the sidebar. Additional interactive parameters will be available on each page.')

# Sidebar Header
st.sidebar.markdown('## Interactive User Selection')
st.sidebar.markdown('For each widget, make a selection to alter the dashboard output.')
today = st.sidebar.text(dt.datetime.today())
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.subheader('End Date')

# Sidebar Default End Date = last business day of previous month
offset = BMonthEnd()
default_date = offset.rollback(date.today())

# Sidebar End Date
end_date = st.sidebar.date_input(
    'Select end date:', value=default_date, max_value=dt.datetime.today()-BDay(1))
start_date = end_date - dt.timedelta(days=365)

# Sidebar Page View Widget
st.sidebar.subheader('Page View')
radio = st.sidebar.radio('Select page view:', [
                         'Performance History', 'Technical Analysis', 'Sentiment Analysis', 'Macro Analysis'], key=1)
if radio == 'Performance History':
    st.markdown('### Page View: Performance History')
elif radio == 'Technical Analysis':
    st.markdown('### Page View: Technical Analysis')
elif radio == 'Sentiment Analysis':
    st.markdown('### Page View: Sentiment Analysis')
elif radio == 'Macro Analysis':
    st.markdown('### Page View: Macro Analysis')
else:
    st.error('User must select Page View to populate application.')

# Static Lists
commodity_list = ['Brent Crude Oil',
                  'Cocoa',
                  'Coffee C',
                  'Copper',
                  'Corn',
                  'Cotton',
                  'Gasoil',
                  'Gasoline',
                  'Gold',
                  'Heating Oil',
                  'KC HRW Wheat',
                  'Lead',
                  'Lean Hogs',
                  'Live Cattle',
                  'Natural Gas',
                  'Platinum',
                  'Silver',
                  'Soybean Meal',
                  'Soybean Oil',
                  'Soybeans',
                  'Sugar No. 11',
                  'Wheat',
                  'WTI Crude Oil',
                  'Zinc',
                  'BCOM',
                  'BCOM Ags',
                  'BCOM Energy',
                  'BCOM Industrial Metals',
                  'BCOM Precious Metals'
                  ]
                  
contract1_codes = ['CHRIS/ICE_B1.4',
                   'CHRIS/ICE_CC1.4',
                   'CHRIS/ICE_KC1.4',
                   'CHRIS/CME_HG1.4',
                   'CHRIS/CME_C1.4',
                   'CHRIS/ICE_CT1.4',
                   'CHRIS/ICE_G1.4',
                   'CHRIS/CME_RB1.4',
                   'CHRIS/CME_GC1.4',
                   'CHRIS/CME_HO1.4',
                   'CHRIS/CME_KW1.4',
                   'CHRIS/SHFE_PB1.6',
                   'CHRIS/CME_LN1.4',
                   'CHRIS/CME_LC1.4',
                   'CHRIS/CME_NG1.4',
                   'CHRIS/CME_PL1.4',
                   'CHRIS/CME_SI1.4',
                   'CHRIS/CME_SM1.4',
                   'CHRIS/CME_BO1.4',
                   'CHRIS/CME_S1.4',
                   'CHRIS/ICE_SB1.4',
                   'CHRIS/CME_W1.4',
                   'CHRIS/CME_CL1.4',
                   'CHRIS/SHFE_ZN1.6',
                   'CHRIS/CME_AW1.4',
                   'CHRIS/EUREX_FCAG1.4',
                   'CHRIS/EUREX_FCEN1.4',
                   'CHRIS/EUREX_FCIN1.4',
                   'CHRIS/EUREX_FCPR1.4'
                   ]

contract3_codes = ['CHRIS/ICE_B3.4',
                   'CHRIS/ICE_CC3.4',
                   'CHRIS/ICE_KC3.4',
                   'CHRIS/CME_HG3.4',
                   'CHRIS/CME_C3.4',
                   'CHRIS/ICE_CT3.4',
                   'CHRIS/ICE_G3.4',
                   'CHRIS/CME_RB3.4',
                   'CHRIS/CME_GC3.4',
                   'CHRIS/CME_HO3.4',
                   'CHRIS/CME_KW3.4',
                   'CHRIS/SHFE_PB3.6',
                   'CHRIS/CME_LN3.4',
                   'CHRIS/CME_LC3.4',
                   'CHRIS/CME_NG3.4',
                   'CHRIS/CME_PL3.4',
                   'CHRIS/CME_SI3.4',
                   'CHRIS/CME_SM3.4',
                   'CHRIS/CME_BO3.4',
                   'CHRIS/CME_S3.4',
                   'CHRIS/ICE_SB3.4',
                   'CHRIS/CME_W3.4',
                   'CHRIS/CME_CL3.4',
                   'CHRIS/SHFE_ZN3.6',
                   'CHRIS/CME_AW2.4',
                   'CHRIS/EUREX_FCAG2.4',
                   'CHRIS/EUREX_FCEN2.4',
                   'CHRIS/EUREX_FCIN2.4',
                   'CHRIS/EUREX_FCPR2.4'
                   ]

sector_list = ['Energy',
               'Agriculture',
               'Agriculture',
               'Industrial Metals',
               'Agriculture',
               'Agriculture',
               'Energy',
               'Energy',
               'Precious Metals',
               'Energy',
               'Agriculture',
               'Industrial Metals',
               'Agriculture',
               'Agriculture',
               'Energy',
               'Precious Metals',
               'Precious Metals',
               'Agriculture',
               'Agriculture',
               'Agriculture',
               'Agriculture',
               'Agriculture',
               'Energy',
               'Industrial Metals',
               'Index',
               'Index',
               'Index',
               'Index',
               'Index'
               ]

cot_codes = ['CFTC/073732_FO_ALL.1',
             'CFTC/083731_FO_ALL.1',
             'CFTC/085692_FO_ALL.1',
             'CFTC/002602_FO_ALL.1',
             'CFTC/111659_FO_ALL.1',
             'CFTC/033661_FO_ALL.1',
             'CFTC/088691_FO_ALL.1',
             'CFTC/022651_FO_ALL.1',
             'CFTC/001612_FO_ALL.1',
             'CFTC/054642_FO_ALL.1',
             'CFTC/057642_FO_ALL.1',
             'CFTC/023651_FO_ALL.1',
             'CFTC/076651_FO_ALL.1',
             'CFTC/084691_FO_ALL.1',
             'CFTC/026603_FO_ALL.1',
             'CFTC/007601_FO_ALL.1',
             'CFTC/005602_FO_ALL.1',
             'CFTC/080732_FO_ALL.1',
             'CFTC/001602_FO_ALL.1',
             'CFTC/067651_FO_ALL.1',
             'CFTC/073732_FO_ALL.7',
             'CFTC/083731_FO_ALL.7',
             'CFTC/085692_FO_ALL.7',
             'CFTC/002602_FO_ALL.7',
             'CFTC/111659_FO_ALL.7',
             'CFTC/033661_FO_ALL.7',
             'CFTC/088691_FO_ALL.7',
             'CFTC/022651_FO_ALL.7',
             'CFTC/001612_FO_ALL.7',
             'CFTC/054642_FO_ALL.7',
             'CFTC/057642_FO_ALL.7',
             'CFTC/023651_FO_ALL.7',
             'CFTC/076651_FO_ALL.7',
             'CFTC/084691_FO_ALL.7',
             'CFTC/026603_FO_ALL.7',
             'CFTC/007601_FO_ALL.7',
             'CFTC/005602_FO_ALL.7',
             'CFTC/080732_FO_ALL.7',
             'CFTC/001602_FO_ALL.7',
             'CFTC/067651_FO_ALL.7',
             'CFTC/073732_FO_ALL.8',
             'CFTC/083731_FO_ALL.8',
             'CFTC/085692_FO_ALL.8',
             'CFTC/002602_FO_ALL.8',
             'CFTC/111659_FO_ALL.8',
             'CFTC/033661_FO_ALL.8',
             'CFTC/088691_FO_ALL.8',
             'CFTC/022651_FO_ALL.8',
             'CFTC/001612_FO_ALL.8',
             'CFTC/054642_FO_ALL.8',
             'CFTC/057642_FO_ALL.8',
             'CFTC/023651_FO_ALL.8',
             'CFTC/076651_FO_ALL.8',
             'CFTC/084691_FO_ALL.8',
             'CFTC/026603_FO_ALL.8',
             'CFTC/007601_FO_ALL.8',
             'CFTC/005602_FO_ALL.8',
             'CFTC/080732_FO_ALL.8',
             'CFTC/001602_FO_ALL.8',
             'CFTC/067651_FO_ALL.8'
             ]



# Prep Quandl
quandl.ApiConfig.api_key = '9VzBgrp8GAG3XPUrNY_X'
codes = contract1_codes + contract3_codes

# Pull Data
@st.cache(persist=True)
def get_prices(start_date, end_date, symbols=codes):
    # Pull prices using the Quandl API
    px = quandl.get(symbols, start_date=start_date, end_date=end_date)
    px = px.fillna(method='ffill').fillna(method='bfill')

    # Modify the column names
    px.columns = px.columns.str.split('_').str[1].str.split(
        '-').str[0].str.rstrip().to_list()

    # Identify the columns assigned to the 1st and 3rd contracts
    cols1 = []
    cols3 = []
    for col in px.columns:
        if '1' in col:
            cols1.append(col)
        else:
            cols3.append(col)

    # Create separate dataframes
    prices = px[cols1]
    prices.columns = commodity_list
    prices3 = px[cols3]
    prices3.columns = commodity_list

    return prices, prices3

# Remove BCOM and BCOM subindices from primary df
all_prices = get_prices(start_date, end_date)[0]
all_prices3 = get_prices(start_date, end_date)[1]
all_returns = all_prices.pct_change()[1:]
all_returns3 = all_prices3.pct_change()[1:]

filter_yes = all_prices.columns[all_prices.columns.str.contains('BCOM')]
filter_no = all_prices.columns[~all_prices.columns.str.contains('BCOM')]

prices = all_prices[filter_no]
prices3 = all_prices3[filter_no]

returns = prices.pct_change()[1:]
returns3 = prices3.pct_change()[1:]

index_prices = all_prices[filter_yes]
index_returns = index_prices.pct_change()[1:]

# Define start dates for each timeframe
first_bds = pd.date_range(start_date, end_date, freq='BMS')
date_mtd = first_bds[-1]
date_qtd = prices.resample('Q').last().index[-2] + dt.timedelta(days=1)
date_ytd = first_bds[-end_date.month]
date_yr1 = end_date - dt.timedelta(days=365)

# Create indexed dataframe for each timeframe
prices_mtd = prices.loc[date_mtd:, :]
prices_qtd = prices.loc[date_qtd:, :]
prices_ytd = prices.loc[date_ytd:, :]
prices_yr1 = prices.loc[date_yr1:, :]

returns_mtd = returns.loc[date_mtd:, :]
returns_qtd = returns.loc[date_qtd:, :]
returns_ytd = returns.loc[date_ytd:, :]
returns_yr1 = returns.loc[date_yr1:, :]

all_returns_mtd = all_returns.loc[date_mtd:, :]
all_returns_qtd = all_returns.loc[date_qtd:, :]
all_returns_ytd = all_returns.loc[date_ytd:, :]
all_returns_yr1 = all_returns.loc[date_yr1:, :]





### PAGE VIEW: Performance History ###

if radio == 'Performance History':
    @st.cache(persist=True)
    def stats(index='yes'):
        # Format as percentages
        def format_text(x):
            return '{:.3}%'.format(100*x)

        if index == 'yes':
            # Calculate returns
            last = pd.Series(all_prices.iloc[-1], name='Spot Price').astype(float).round(2)
            last3 = pd.Series(all_prices3.iloc[-1], name='3rd Contract').astype(float).round(2)
            min = pd.Series(all_prices.min(), name='Min').astype(float).round(2)
            max = pd.Series(all_prices.max(), name='Max').astype(float).round(2)
            a = pd.Series((1+all_returns_mtd).prod()-1, name='MTD').apply(format_text)
            b = pd.Series((1+all_returns_qtd).prod()-1, name='QTD').apply(format_text)
            c = pd.Series((1+all_returns_ytd).prod()-1, name='YTD').apply(format_text)
            d = pd.Series((1+all_returns_yr1).prod()-1, name='1 YEAR').apply(format_text)

            # Combine
            df1 = pd.concat([last, last3, min, max], axis=1)
            df1['Curve'] = np.where(last > last3, 'Backwardation', 'Contango')
            df2 = pd.concat([a, b, c, d], axis=1)

        else:
            # Calculate returns
            last = pd.Series(prices.iloc[-1], name='Spot Price').astype(float).round(2)
            last3 = pd.Series(prices3.iloc[-1], name='3rd Contract').astype(float).round(2)
            min = pd.Series(prices.min(), name='Min').astype(float).round(2)
            max = pd.Series(prices.max(), name='Max').astype(float).round(2)
            a = pd.Series((1+returns_mtd).prod()-1, name='MTD').apply(format_text)
            b = pd.Series((1+returns_qtd).prod()-1, name='QTD').apply(format_text)
            c = pd.Series((1+returns_ytd).prod()-1, name='YTD').apply(format_text)
            d = pd.Series((1+returns_yr1).prod()-1, name='1 YEAR').apply(format_text)

            # Combine
            df1 = pd.concat([last, last3, min, max], axis=1)
            df1['Curve'] = np.where(last > last3, 'Backwardation', 'Contango')
            df2 = pd.concat([a, b, c, d], axis=1)

        return df1, df2

    # Commodity Index Summary
    st.write('')
    st.header('» Index Summary')
    st.write('The following charts are designed to provide a high-level snapshot '
             ' of recent commodity performance. The Bloomberg Commodity Index (BCOM) is comprised of '
             '23 constituents, spread across 4 primary commodity sectors: Agriculture, Energy, Industrial '
             'Metals, and Precious Metals. Please make sure to select the desired timeframe using the slider widget.')

    # Plot index and subindex
    timeframe = st.select_slider('', ['MTD', 'QTD', 'YTD', '1 YEAR'], key=2)
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1, column_widths=[
                        550, 550], row_heights=[400], subplot_titles=('BCOM Price', 'BCOM Subindex Returns (%)'))

    if timeframe == 'MTD':
        line_data = all_prices.loc[date_mtd:, 'BCOM']
    elif timeframe == 'QTD':
        line_data = all_prices.loc[date_qtd:, 'BCOM']
    elif timeframe == 'YTD':
        line_data = all_prices.loc[date_ytd:, 'BCOM']
    elif timeframe == '1 YEAR':
        line_data = all_prices.loc[date_yr1:, 'BCOM']
    else:
        st.error('User must select timeframe to populate chart.')

    bar_data = stats()[1].loc['BCOM Ags':, timeframe]

    fig.add_trace(go.Scatter(x=line_data.index,
                             y=line_data.values), row=1, col=1)
    fig.add_trace(go.Bar(x=['Agriculture', 'Energy', 'Industrial Metals',
                            'Precious Metals'], y=bar_data.values), row=1, col=2)
    fig.update_traces(marker_color='rgb(58,42,300)',
                      marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.7)
    fig.update_layout(template='plotly_white', showlegend=False,
                      margin=dict(l=0, r=0, t=20, b=0), height=400)
    st.plotly_chart(fig)

    # Commodity Price Range
    st.write('')
    st.header('» Commodity Price Range')
    st.write('Select all commodities or a unique subset of commodities for review. '
             'The table will populate with various historical prices to help describe the current environment. '
             'The active front-month futures contract is used as a proxy for the spot price. Min and max are calculated over the '
             'previous 12 month period. Curve describes the current state of the futures term structure based on '
             'the differential between the 1st contract and 3rd contract.')
    st.write('')

    if st.checkbox('View All Commodities?', value=True, key=3):
        data = stats(index='No')[0]
    else:
        cmdty_select = st.multiselect(
            'Select Commodities From List', commodity_list, key=4)
        data = stats(index='No')[0].loc[cmdty_select, :]

    st.dataframe(data, width=700, height=800)

    # Commodity Performance
    st.write('')
    st.write('')
    st.header('» Commodity Performance')
    st.write('Select all commodities or a unique subset of commodities for review. '
             'The chart will populate with historical returns for the designated timeframe. The user '
             'may choose between two different chart types and may view the underlying data.')

    # Plot Historical Performance
    timeframe = st.select_slider('', ['MTD', 'QTD', 'YTD', '1 YEAR'], key=5)
    if timeframe == 'MTD':
        df = prices_mtd
    elif timeframe == 'QTD':
        df = prices_qtd
    elif timeframe == 'YTD':
        df = prices_ytd
    elif timeframe == '1 YEAR':
        df = prices_yr1
    else:
        st.error('User must select timeframe in order to populate performance history.')

    # Plot Parameters
    if st.checkbox('View All Commodities?', value=True, key=6):
        df_plot = df
    else:
        cmdty_select = st.multiselect(
            'Select Commodities From List', commodity_list, key=7)
        df_plot = df[cmdty_select]

    visual_type = st.radio('', ['Bar Chart', 'Line Chart'], key=8)
    st.write('')

    # Plot1 Performance History
    if visual_type == 'Bar Chart':
        fig_data = (100 * ((df_plot/df_plot.iloc[0]).iloc[-1] - 1)).sort_values()
        fig = px.bar(fig_data,
                     color=fig_data.values,
                     width=800,
                     height=500,
                     orientation='h',
                     labels={'index': '', 'value': 'Total Return', 'color': ''},
                     template='plotly_white'
                     )

        fig.update_layout(showlegend=False, font_size=12, margin=dict(l=0, r=0, t=0, b=0))
        fig.update_xaxes(ticksuffix='%')
        st.plotly_chart(fig)

    # Plot2 Performance History
    elif visual_type == 'Line Chart':
        fig = px.line(100*(df_plot/df_plot.iloc[0]-1),
                      width=800,
                      height=500,
                      labels={'variable': ''},
                      template='plotly_white'
                      )

        fig.update_yaxes(title='Normalized Return', ticksuffix='%')
        fig.update_xaxes(title='Date')
        fig.update_layout(font_size=12, margin=dict(l=0, r=0, t=0, b=0))
        fig.update_traces(marker_line_width=3)
        st.plotly_chart(fig)

    # Show underlying data
    if st.checkbox('Show Underlying Data?', key=9):
        st.dataframe(stats(index='No')[1])

    # Page Footer
    st.write('')
    st.write('')
    st.write('---')
    st.image('https://i.imgur.com/OoRGfxB.png', use_column_width=True)



    

### PAGE VIEW: Technical Analysis ###

if radio == 'Technical Analysis':

    # Price range
    st.header('» Price Ranking')
    st.write('For each commodity, the current price is compared to the maximum price '
             'over the designated timeframe. For example, if the price rank of Gold equals 70% on a YTD basis, '
             'then the price of Gold is currently 70% of the maximum value registered since the beginning of the calendar year. '
             'The chart can be used to identify relative value opportunities on an individual and sector-level basis.')

    timeframe2 = st.select_slider('', ['MTD', 'QTD', 'YTD', '1 YEAR'], key=10)

    def price_range():
        # Calculate price as a percent of range
        def price_range_calc(prices):
            last = prices[-1]
            low = prices.min()
            high = prices.max()
            range = (last-low) / (high-low)
            return range

        # Identify range based on slider widget
        if timeframe2 == 'MTD':
            df = prices_mtd
        elif timeframe2 == 'QTD':
            df = prices_qtd
        elif timeframe2 == 'YTD':
            df = prices_ytd
        elif timeframe2 == '1 YEAR':
            df = prices_yr1
        else:
            st.error('User must select timeframe in order to populate performance history.')

        # Apply range calculation to sliced df
        range_timeframe2 = df.apply(price_range_calc)
        fig_data = range_timeframe2.sort_values()*100

        return fig_data.round(2)

    # Plot Price Range
    fig_data = pd.Series(price_range(), name='%ofRange')
    sec = [i for i in sector_list if i != 'Index']
    name = [i for i in commodity_list if 'BCOM' not in i]
    dic = {'Sector':sec, 'Name':name}
    sectors = pd.DataFrame(dic).set_index('Name')
    
    df = pd.merge(sectors, fig_data, right_index=True,
                  left_index=True).sort_values('%ofRange')

    fig = px.bar(x=df.index,
                 y=df['%ofRange'],
                 height=500,
                 width=800,
                 template='plotly_white',
                 color=df['Sector'],
                 labels={'color': 'Sector', 'y': '', }
                 )

    fig.update_yaxes(title='Price as a Percent of the {} Range'.format(
        timeframe2), ticksuffix='%')
    fig.update_xaxes(title='')
    fig.update_layout(font_size=12, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig)

    # Moving Averages
    st.header('» Moving Averages')
    st.write('First, select a single commodity or index to analyze. Next, select Simple or Exponential moving average. '
             'Simple will take the mean of the previous x number of days, treating all data points with equal prominence. '
             'Exponential places greater weight and significance on the most recent data points. Lastly, use the slider widget '
             'to select the number of days to use in calculating the moving average windows. In general, a shorter window may create a '
             'more timely signal; howevever, it is often at the expense of reliability.')

    cmdty = st.selectbox('Select a commodity:', commodity_list, key=11)
    ma_type = st.radio('', options=[
                       'Simple Moving Average (SMA)', 'Exponential Moving Average (EMA)'], key=12)

    # Split View Into Columns
    col1, col2 = st.beta_columns([1, 1])
    with col1:
        ma_days1 = st.slider('Moving Average #1', min_value=5,
                             max_value=100, step=5, key=13)
    with col2:
        ma_days2 = st.slider('Moving Average #2', min_value=5,
                             max_value=100, step=5, key=14)

    @st.cache(persist=True)
    def moving_average():
        # Copy prices
        data = {'Price': pd.Series(all_prices[cmdty].fillna(method='ffill'))}

        # Account for window type
        if ma_type == 'Exponential Moving Average (EMA)':
            data['EMA1'] = pd.Series(
                ta.ema(all_prices[cmdty], length=ma_days1))
            data['EMA2'] = pd.Series(
                ta.ema(all_prices[cmdty], length=ma_days2))
        else:
            data['SMA1'] = pd.Series(
                ta.sma(all_prices[cmdty], length=ma_days1))
            data['SMA2'] = pd.Series(
                ta.sma(all_prices[cmdty], length=ma_days2))

        df = pd.concat(data, axis=1)
        return df

    # Plot Moving Averages
    fig_data = moving_average()
    fig = px.line(fig_data, template='plotly_white', labels={
                  'variable': '', 'value': '', 'Date': ''}, width=800, height=400)
    fig.update_layout(showlegend=True, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig)

    # Momentum Indicators
    st.header('» Momentum Indicators')
    st.write('First, select a single commodity or index to analyze. Next, select a desired set of technical indicators. '
             'The parameters for MACD and RSI are fixed to the industry standards, 12-26-9 periods for MACD and 14 periods for '
             'RSI. The lookback period for Momentum must be selected using the slider widget. For further explanation regarding the use '
             'of technical indicators and oscillators, please refer to investopedia.com or stockcharts.com.')

    cmdty = st.selectbox('Select a commodity:', commodity_list, key=15)

    # Split View Into Columns
    col1, col2 = st.beta_columns([1, 1])
    with col1:
        widget_macd = st.checkbox('MACD Oscillator', value=True, key=16)
        widget_rsi = st.checkbox('RSI Oscillator', value=True, key=17)
    with col2:
        widget_mom = st.checkbox('Momentum Oscillator', value=True, key=18)
        widget_mom_slider = st.slider(
            'Select momentum lookback in days', min_value=5, max_value=100, step=5, key=19)

    # Calculate Momentum Indicators with TA-Lib
    @st.cache(persist=True)
    def technical_analysis():
        data = {'Price': pd.Series(all_prices[cmdty].fillna(method='ffill'))}
       
        if widget_mom:
            data['Momentum'] = pd.Series(
                ta.mom(all_prices[cmdty], length=widget_mom_slider))
        if widget_macd:
            data['MACD'] = pd.Series(ta.macd(all_prices[cmdty], fast=12, slow=26, signal=9)[0])
        if widget_rsi:
            data['RSI'] = pd.Series(ta.rsi(all_prices[cmdty], length=14))
            
        df = pd.concat(data, axis=1)
        return df

    # Plot Technical Analysis Chart
    df = technical_analysis()
    fig = make_subplots(rows=len(df.columns), cols=1,
                        shared_xaxes=True, vertical_spacing=0.03)
    fig.add_trace(go.Scatter(
        x=df.index, y=df['Price'].values, name='Price'), row=1, col=1)

    j = 2
    for col in df.columns[1:]:
        fig.add_trace(go.Scatter(
            x=df.index, y=df[col].values, name=df[col].name), row=j, col=1)
        if col == 'RSI':
            fig.add_shape(type='rect', x0=df.index[0], y0=30, x1=df.index[-1], y1=70, line=dict(
                color='Blue', width=2), fillcolor='LightSkyBlue', row=j, col=1)
        elif col in ['Momentum','MACD']:
            fig.add_shape(type='line', x0=df.index[0], y0=0, x1=df.index[-1], y1=0, line=dict(
                color='Blue', width=2), row=j, col=1)
        j += 1

    fig.update_layout(height=500, width=800, template='simple_white',
                      showlegend=True, margin=dict(l=0, r=0, t=0, b=0))
    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True, nticks=7)
    st.plotly_chart(fig)

    # Page Footer
    st.write('')
    st.write('')
    st.write('---')
    st.image('https://i.imgur.com/OoRGfxB.png', use_column_width=True)





### PAGE VIEW: Sentiment Analysis ###

if radio == 'Sentiment Analysis':

    # Pull commitment of traders
    st.header('» Net Speculative Positioning')
    st.write('Commitment of Traders data for futures comes from the US Commodity Futures Trading Commission (CFTC), '
             'an independent regulatory agency of the U.S. government. The figures represent reported net positions held by '
             'money managers/speculators and exclude all commodities traded on foreign exchanges. Data is updated weekly '
             'on Fridays at 5:00 pm ET. As an aggegration of all commodities in the dataset, the first chart may be used as a proxy '
             'for investor sentiment towards the broader commodity asset class. A rising trend may indicate bullish sentiment, '
             'and a falling trend may indicate bearish sentiment.')
   
    # Pull Data
    @st.cache(persist=True)
    def get_positioning(start_date, end_date, symbols=cot_codes):
        # Pull prices using the Quandl API
        df = quandl.get(symbols, start_date=start_date, end_date=end_date)
        df = df.fillna(method='ffill').fillna(method='bfill')

        # Modify the column names
        df.columns = df.columns.str.replace('FO_ALL - Open Interest', 'Open').str.replace(
            'FO_ALL - Money Manager Longs', 'Long').str.replace('FO_ALL - Money Manager Shorts', 'Short').str.replace('CFTC/', '').to_list()

        # Identify the columns assigned to the 1st and 3rd contracts
        oi = []
        long = []
        short = []
        for col in df.columns:
            if 'Open' in col:
                oi.append(col)
            elif 'Long' in col:
                long.append(col)
            elif 'Short' in col:
                short.append(col)

        map = {'073732': 'Cocoa',
               '083731': 'Coffee C',
               '085692': 'Copper',
               '002602': 'Corn',
               '111659': 'Gasoline',
               '033661': 'Cotton',
               '088691': 'Gold',
               '022651': 'Heating Oil',
               '001612': 'KC HRW Wheat',
               '054642': 'Lean Hogs',
               '057642': 'Live Cattle',
               '023651': 'Natural Gas',
               '076651': 'Platinum',
               '084691': 'Silver',
               '026603': 'Soybean Meal',
               '007601': 'Soybean Oil',
               '005602': 'Soybeans',
               '080732': 'Sugar No. 11',
               '001602': 'Wheat',
               '067651': 'WTI Crude Oil'
               }

        # Create separate dataframes
        df_oi = df[oi]
        df_oi.columns = df_oi.columns.str.replace('_Open', '')
        df_oi.rename(columns=map, inplace=True)

        df_long = df[long]
        df_long.columns = df_long.columns.str.replace('_Long', '')
        df_long.rename(columns=map, inplace=True)

        df_short = df[short]
        df_short.columns = df_short.columns.str.replace('_Short', '')
        df_short.rename(columns=map, inplace=True)

        df_net = df_long - df_short

        return df_oi, df_long, df_short, df_net

    df_net = get_positioning(start_date, end_date)[3]
    cmdty_v2 = st.selectbox('Select a commodity:', df_net.columns, key=20)

    if st.checkbox('Show Underlying Data?', key=21):
        st.dataframe(df_net)

    # Plot net length subplots
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1, column_widths=[500, 500], row_heights=[
                        400], subplot_titles=('Net Length: Aggregate', 'Net Length: {}'.format(cmdty_v2)))
    fig.add_trace(
        go.Bar(x=df_net.index, y=df_net.sum(axis=1).values), row=1, col=1)
    fig.add_trace(go.Scatter(x=df_net.index,
                             y=df_net[cmdty_v2].values), row=1, col=2)
    fig.update_layout(template='plotly_white', showlegend=False,
                      margin=dict(l=0, r=0, t=20, b=0), height=350)

    for i in fig['layout']['annotations']:
        i['font'] = dict(size=14)

    st.plotly_chart(fig)
    st.write('')
    st.write('')

    # Contrarian Scatter Plot
    st.header('» Finding the Extremes: Price & Positioning')
    st.write('The following scatter plot is intended to identify individual commodities '
             'that are susceptible to reversal. The y-axis ranks price as a percentage of the previous '
             '12 month range. The x-axis ranks net speculative positioning as a percentage of the previous '
             '12 month range. Assuming a contrarian viewpoint, commodities in the lower left-hand quadrant '
             'may be considered oversold, and those in the upper right-hand quandrant may be considered overbought.')

    # Convert net length to percentiles
    df_net_percentile = df_net.rank(pct=True).round(2)

    # Convert prices to percentiles
    prices_percentile = prices.rank(pct=True).round(2)
    prices_percentile = prices_percentile[df_net_percentile.columns.to_list()]

    # Prep scatter plot
    x_list = df_net_percentile.last('1D').values.tolist()
    y_list = prices_percentile.last('1D').values.tolist()
    x_vals = [x for y in x_list for x in y]
    y_vals = [x for y in y_list for x in y]
    labels = prices_percentile.columns.values.tolist()

    # Plot scatter plot
    fig = px.scatter(x=x_vals, y=y_vals, text=labels, template='plotly_white',
                     width=800, height=500, range_x=[-0.1, 1.1], range_y=[-0.1, 1.1], opacity=0.75)
    
    fig.add_trace(go.Scatter(x=[0, 0.2], y=[0.2, 0.2], mode="lines"))
    fig.add_trace(go.Scatter(x=[0.2, 0.2], y=[0, 0.2], mode="lines"))
    fig.add_trace(go.Scatter(x=[0.8, 1], y=[0.8, 0.8], mode="lines"))
    fig.add_trace(go.Scatter(x=[0.8, 0.8], y=[0.8, 1], mode="lines"))

    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                      showlegend=False,
                      xaxis=dict(tickmode='array', tickvals=[0, 0.2, 0.4, 0.6, 0.8, 1], ticktext=[
                                 '0%', '20%', '40%', '60%', '80%', '100%']),
                      yaxis=dict(tickmode='array', tickvals=[0, 0.2, 0.4, 0.6, 0.8, 1], ticktext=[
                          '0%', '20%', '40%', '60%', '80%', '100%'])
                      )

    fig.update_traces(textposition='top center', marker_size=9)
    fig.update_xaxes(
        title='Net Speculative Length (As a Percent of the 1 Year Range)', ticksuffix='%')
    fig.update_yaxes(
        title='Price (As a Percent of the 1 Year Range)', ticksuffix='%')
    st.plotly_chart(fig)

    # Page Footer
    st.write('')
    st.write('')
    st.write('---')
    st.image('https://i.imgur.com/OoRGfxB.png', use_column_width=True)





### PAGE VIEW: Macro Analysis ###

if radio == 'Macro Analysis':

    # 5 year lookback
    st.header('» US Macro Landscape')
    st.write('Here we review several US economic data points, all of which '
             'are widely tracked and considered to play a material role in the performance '
             'of the US financial markets. The timeframe has been extended to better visualize '
             'secular trends.')
    st.write('')

    # Prep data pull
    macro_codes = ['CHRIS/CME_AW1.4',
                   'RATEINF/INFLATION_USA',
                   'FRED/UNRATENSA',
                   'ISM/MAN_PMI',
                   'CHRIS/ICE_DX1.4',
                   'CHRIS/CME_ES1.4',
                   'USTREASURY/YIELD.10'
                   ]

    macro_columns = ['BCOM_Index',
                     'US_Inflation_Rate',
                     'US_Unemployment_Rate',
                     'US_PMI',
                     'US_Dollar_Index',
                     'S&P_500_Emini',
                     'US_10Year_Nominal_Yield'
                     ]

    # Limit start date to 10/31/2011 when BCOM data began
    bcom_start = dt.datetime(2011, 10, 31)
    macro_start = end_date - dt.timedelta(days=10*365)
    macro_start = dt.datetime(
        macro_start.year, macro_start.month, macro_start.day)
    macro_start_date = macro_start if macro_start >= bcom_start else bcom_start

    # Pull data
    @st.cache(persist=True)
    def get_macro(start_date, end_date, symbols=macro_codes):
        df = quandl.get(symbols, start_date=start_date,
                        end_date=end_date, collapse='monthly')
        df = df.fillna(method='ffill').fillna(method='bfill')
        df.columns = macro_columns

        # Convert to monthly returns
        df_ret = df[['BCOM_Index', 'US_Unemployment_Rate', 'US_PMI',
                     'US_Dollar_Index', 'S&P_500_Emini']].pct_change()[1:]
        df_ret['US_Inflation_Rate'] = df['US_Inflation_Rate'][1:]
        df_ret['US_10Year_Nominal_Yield'] = df['US_10Year_Nominal_Yield'][1:]

        # Convert to 12m rolling
        df_roll = (1 + df_ret[['BCOM_Index', 'US_Unemployment_Rate', 'US_PMI',
                               'US_Dollar_Index', 'S&P_500_Emini']]).rolling(12).apply(np.prod, raw=True) - 1
        df_roll['US_Inflation_Rate'] = df['US_Inflation_Rate'][12:]
        df_roll['US_10Year_Nominal_Yield'] = df['US_10Year_Nominal_Yield'][12:]

        return df, df_ret, df_roll

    df = get_macro(macro_start_date, end_date)[0]
    df_ret = get_macro(macro_start_date, end_date)[1]
    df_roll = get_macro(macro_start_date, end_date)[2]

    if st.checkbox('Show Underlying Data?', value=False, key=22):
        st.dataframe(df)

    if st.checkbox('Show Descriptive Statistics?', value=False, key=23):
        st.dataframe(df.describe().T)

    # Plot macro subplots
    fig = make_subplots(rows=3, cols=2, shared_xaxes=True,
                        vertical_spacing=0.05, subplot_titles=df.columns[1:])

    fig.add_trace(go.Scatter(
        x=df.index, y=df.iloc[:, 1].values, name=df.iloc[:, 1].name), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=df.index, y=df.iloc[:, 2].values, name=df.iloc[:, 2].name), row=1, col=2)
    fig.add_trace(go.Scatter(
        x=df.index, y=df.iloc[:, 3].values, name=df.iloc[:, 3].name), row=2, col=1)
    fig.add_trace(go.Scatter(
        x=df.index, y=df.iloc[:, 4].values, name=df.iloc[:, 4].name), row=2, col=2)
    fig.add_trace(go.Scatter(
        x=df.index, y=df.iloc[:, 5].values, name=df.iloc[:, 5].name), row=3, col=1)
    fig.add_trace(go.Scatter(
        x=df.index, y=df.iloc[:, 6].values, name=df.iloc[:, 6].name), row=3, col=2)

    fig.update_layout(height=700, width=800, template='plotly_white', showlegend=False, margin=dict(
        l=0, r=0, t=20, b=0), font=dict(size=11), title_font=dict(size=8))
    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)

    for i in fig['layout']['annotations']:
        i['font'] = dict(size=14)

    st.plotly_chart(fig)

    # Correlation matrix
    st.write('')
    st.write('')
    st.header('» Correlation Matrix')
    st.write('The following correlation matrix can be used to identify whether or not '
             'the selected economic data points display signs of a linear relationship. Aside from '
             'the inflation rate and 10yr nominal yield, which are already reported as annual rates, all data '
             'has been standardized using 12 month rolling returns.')

    matrix = df_roll.corr()

    if st.checkbox('Show Underlying Data?', value=False, key=24):
        st.dataframe(matrix)

    # Plot matrix
    fig = px.imshow(matrix, width=800, height=500,
                    template='plotly_white', color_continuous_scale='blues')
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig)

    # Page Footer
    st.write('')
    st.write('')
    st.write('---')
    st.image('https://i.imgur.com/OoRGfxB.png', use_column_width=True)
