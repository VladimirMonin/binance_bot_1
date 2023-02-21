import time
from binance.client import Client
import pandas as pd
from scipy import stats

from config import API_KEY, API_SECRET, FUTURE_SYMBOL, SYMBOL, WINDOW_SIZE, PRICE_CHANGE_THRESHOLD, API_FREQ, INTERVAL

client = Client(API_KEY, API_SECRET)


def get_historical_klines(symbol, interval, window_size):
    """
    Получает исторические данные цены для указанного символа с указанным интервалом свечей
    и размером окна (количество свечей), возвращает DataFrame с ценами закрытия за последние
    window_size свечей.

    """
    klines = client.futures_klines(symbol=symbol, interval=interval)
    data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                         'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                                         'taker_buy_quote_asset_volume', 'ignore'])
    data.drop(columns=['timestamp', 'high', 'low', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades',
                       'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'], inplace=True)
    data['open'] = data['open'].astype(float)
    data['close'] = data['close'].astype(float)
    return data.tail(window_size)


def get_future_price():
    """
    Получает текущую цену фьючерса ETHUSDT_220325 и возвращает ее в виде числа с плавающей точкой.
    """
    ticker = client.futures_symbol_ticker(symbol=FUTURE_SYMBOL)
    return float(ticker['lastPrice'])


def calculate_beta(price_data):
    """
    Вычисляет значение beta с помощью простой линейной регрессии на основе данных о цене
    ETHUSDT и BTCUSDT в price_data. Возвращает коэффициент наклона линии регрессии.
    """
    y = price_data['ETHUSDT'].pct_change().dropna()
    x = price_data['BTCUSDT'].pct_change().dropna()
    slope, _, rvalue, _, _ = stats.linregress(x, y)
    return slope


def get_clean_price(future_price, beta):
    """
    Вычисляет очищенную цену фьючерса ETHUSDT с помощью значения future_price (текущая цена фьючерса)
    и значения beta, полученного с помощью функции calculate_beta().
    """
    return (1 - beta) * client.get_symbol_ticker(symbol=SYMBOL)['price'] + beta * future_price


def monitor_price(price_data, beta):
    """
    в бесконечном цикле с задержкой в 1 секунду получает текущую цену фьючерса ETHUSDT,
    вычисляет очищенную цену с помощью функции get_clean_price, проверяет изменение цены
    за последний час с помощью функции check_price_change и выводит сообщение в консоль,
    если изменение превышает заданный порог.

    После этого функция ожидает 1 секунду и повторяет цикл.
    """
    while True:
        future_price = get_future_price()
        clean_price = get_clean_price(future_price, beta)
        print('Clean price:', clean_price)

        price_data = price_data.append({'BTCUSDT': client.get_symbol_ticker(symbol='BTCUSDT')['price'],
                                        'ETHUSDT': client.get_symbol_ticker(symbol='ETHUSDT')['price']},
                                       ignore_index=True)
        price_data = price_data.iloc[1:]

        beta = calculate_beta(price_data)
        print('Current beta:', beta)

        eth_price_pct_change = price_data['ETHUSDT'].pct_change(periods=WINDOW_SIZE - 1)[-1]
        if abs(eth_price_pct_change) >= PRICE_CHANGE_THRESHOLD / 100:
            print(f"ETH price has changed by {PRICE_CHANGE_THRESHOLD}% over the last {WINDOW_SIZE} minutes!")

        time.sleep(API_FREQ)


def main():
    """
    В бесконечном цикле получает очищенную цену фьючерса ETHUSDT,
    выводит ее в консоль, обновляет данные о цене ETHUSDT и BTCUSDT в price_data,
    вычисляет новое значение beta, проверяет, изменилась ли цена на 1% за последние 60 минут,
    и выводит соответствующее сообщение в консоль.
    """
    price_data = get_historical_klines(SYMBOL, INTERVAL, WINDOW_SIZE)
    beta = calculate_beta(price_data)
    print('Current beta:', beta)

    monitor_price(price_data, beta)


if __name__ == '__main__':
    main()
