import data_download as dd
import data_plotting as dplt


def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print(
        "Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), "
        "MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print(
        "Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")

    try:
        # Запрос тикера акции
        ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ")

        # Запрос периода для данных
        period = input("Введите период для данных (например, '1mo' для одного месяца): ")

        # Получение данных о биржевой акции
        stock_data = dd.fetch_stock_data(ticker, period)

        if stock_data is None:
            print("Не удалось получить данные. Завершение программы.")
            return

        # Добавление скользящего среднего к данным
        stock_data = dd.add_moving_average(stock_data)

        # Проверка сильных колебаний
        dd.notify_if_strong_fluctuations(stock_data, ticker, threshold=3)

        # Расчет и вывод средней цены
        dd.calculate_average_price(stock_data)

        # Построение графика данных
        dplt.create_and_save_plot(stock_data, ticker, period)

    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


if __name__ == "__main__":
    main()