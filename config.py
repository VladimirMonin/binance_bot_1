API_KEY = 'YOUR_API_KEY'  # ключ API, который используется для авторизации в Binance API
API_SECRET = 'YOUR_API_SECRET'  # секретный ключ API, который используется для авторизации в Binance API
SYMBOL = 'ETHUSDT'  # символ, для которого нужно получить данные о цене. В данном случае это "ETHUSDT", то есть пара ETH/USDT
FUTURE_SYMBOL = 'ETHUSDT_220325'  # символ фьючерса, для которого нужно получить текущую цену. В данном случае это "ETHUSDT_220325", то есть фьючерс на пару ETH/USDT с датой истечения 25 марта 2022 года
INTERVAL = '1m'  # интервал свечей для получения исторических данных о цене. В данном случае это "1m", то есть свечи по 1 минуте
WINDOW_SIZE = 60  # размер окна (количество свечей), для которого нужно получить исторические данные о цене
PRICE_CHANGE_THRESHOLD = 1.0  # пороговое значение процентного изменения цены, при котором должно выводиться сообщение о смене цены
API_FREQ = 0.5  # Частота обращения к API (в секундах), т.е. время задержки между запросами к API.
