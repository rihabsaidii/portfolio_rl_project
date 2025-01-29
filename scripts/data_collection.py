# import yfinance as yf
# import os
# import csv
#
#
# def fetch_data(symbols, start_date, end_date, interval='1d'):
#     """
#     Collecte les données ajustées de clôture depuis Yahoo Finance.
#     """
#     data = {}
#     for symbol in symbols:
#         ticker = yf.Ticker(symbol)
#         # Récupérer les données dans un format brut
#         raw_data = ticker.history(start=start_date, end=end_date, interval=interval)
#
#         # Convertir les données brutes en dictionnaire de dates et de prix ajustés
#         adjusted_close = {}
#         for date, row in raw_data.iterrows():
#             adjusted_close[date.strftime('%Y-%m-%d')] = row['Adj Close']
#
#         data[symbol] = adjusted_close
#     return data
#
#
# def save_data(data, output_dir):
#     """
#     Sauvegarder les données dans des fichiers CSV.
#     """
#     os.makedirs(output_dir, exist_ok=True)
#     for symbol, symbol_data in data.items():
#         file_path = os.path.join(output_dir, f'{symbol}_adjusted_close.csv')
#         with open(file_path, mode='w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(["Date", "Adjusted Close"])
#             for date, adj_close in symbol_data.items():
#                 writer.writerow([date, adj_close])
#         print(f'Données sauvegardées pour {symbol} dans {file_path}')
import yfinance as yf
import os
import csv

def fetch_data(assets, start_date, end_date, interval):
    """Télécharge les prix de clôture ajustés des actifs sous forme de liste de dictionnaires."""
    data = []
    headers = ["Date"] + assets
    all_dates = set()

    # Télécharger les données pour chaque actif
    asset_prices = {}
    for asset in assets:
        ticker = yf.Ticker(asset)
        history = ticker.history(start=start_date, end=end_date, interval=interval)
        asset_prices[asset] = {}

        for date, row in history.iterrows():
            date_str = date.strftime("%Y-%m-%d")
            asset_prices[asset][date_str] = row["Close"]
            all_dates.add(date_str)

    # Trier les dates
    sorted_dates = sorted(all_dates)

    # Construire la structure des données
    for date in sorted_dates:
        row = [date] + [asset_prices[asset].get(date, "N/A") for asset in assets]
        data.append(row)

    return [headers] + data

def save_data(data, output_dir):
    """Sauvegarde les données sous format CSV et versionne avec DVC."""
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "market_data.csv")

    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print(f"Données sauvegardées dans {file_path}")

    # Versionner avec DVC
    os.system(f"dvc add {file_path}")
    os.system("git add data/raw.dvc")
    os.system("git commit -m 'Mise à jour des données'")

assets = ["AAPL", "PG", "XOM"]
start_date = "2022-01-01"
end_date = "2025-01-01"
interval = "1d"
data = fetch_data(assets, start_date, end_date, interval)
print(data)