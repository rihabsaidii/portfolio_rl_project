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
    file_path = output_dir + "/market_data.csv"
    print(f"Chemin du fichier : {file_path}")

    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print(f"Données sauvegardées dans {file_path}")

    # Versionner avec DVC
    os.system(f"dvc add {file_path}")
    os.system(f"git add {file_path}.dvc")
    os.system('git commit -m "Update market data"')

    # Pousser les fichiers vers le remote DVC
    os.system("dvc push")

    # Pousser les fichiers .dvc vers GitHub
    os.system("git push origin main")
