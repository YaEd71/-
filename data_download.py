import yfinance as yf
import numpy as np


def fetch_stock_data(ticker, period='1mo'):
    """Получает данные об акциях для указанного тикера из Yahoo Finance"""
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)
        return data
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        return None


def add_moving_average(data, window_size=5):
    """Добавляет скользящее среднее к данным"""
    if data is None:
        return None
    try:
        data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
        return data
    except Exception as e:
        print(f"Ошибка при расчете скользящего среднего: {e}")
        return data


def calculate_average_price(data):
    """Вычисляет и выводит среднюю цену закрытия за период"""
    if data is None:
        print("Нет данных для расчета средней цены.")
        return None

    try:
        average_price = np.mean(data['Close'])
        print(f"Средняя цена закрытия за период: ${average_price:.2f}")
        return average_price
    except Exception as e:
        print(f"Ошибка при расчете средней цены: {e}")
        return None

def notify_if_strong_fluctuations(data, ticker, threshold=5):
    """
    Анализирует колебания цен акций и уведомляет о значительных изменениях.

    :param data: DataFrame с данными о акциях
    :param ticker: Тикер акции
    :param threshold: Порог колебаний в процентах (по умолчанию 5%)
    :return: Словарь с информацией о колебаниях или None
    """
    if data is None:
        print("Нет данных для анализа колебаний.")
        return None

    try:
        # Получаем цены закрытия
        close_prices = data['Close']

        # Вычисляем минимальную и максимальную цены
        min_price = close_prices.min()
        max_price = close_prices.max()

        # Вычисляем процент колебаний
        price_range_percent = ((max_price - min_price) / min_price) * 100

        # Уведомление о колебаниях
        if price_range_percent > threshold:
            fluctuation_info = {
                'ticker': ticker,
                'min_price': min_price,
                'max_price': max_price,
                'fluctuation_percent': round(price_range_percent, 2)
            }

            print(f"⚠️ ВНИМАНИЕ: Значительные колебания для акций {ticker}!")
            print(f"Диапазон цен: ${min_price:.2f} - ${max_price:.2f}")
            print(f"Процент колебаний: {price_range_percent:.2f}%")

            return fluctuation_info

        return None

    except Exception as e:
        print(f"Ошибка при анализе колебаний: {e}")
        return None