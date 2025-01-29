import yfinance as yf
import os


def download_data():
    # 📂 Chemin absolu basé sur le chemin du script actuel
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
    base_dir = os.path.abspath(base_dir)  # Convertir en chemin absolu final

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        print(f"✅ Dossier créé : {base_dir}", flush=True)
    else:
        print(f"📂 Dossier existant : {base_dir}", flush=True)

    # 📊 Sélection des tickers
    # tickers = ['AAPL', 'MSFT', 'GOOGL']
    tickers = ["AAPL", "PG", "XOM"]

    print(f"📊 Téléchargement des données pour : {tickers}", flush=True)

    try:
        # ⏳ Télécharger les données
        data = yf.download(tickers, start="2020-01-01")
        print("✅ Téléchargement terminé.", flush=True)

        # 📈 Extraire les prix ajustés et calculer les rendements
        prices = data.xs('Adj Close', level='Price', axis=1)
        returns = prices.pct_change().dropna()
        print("✅ Extraction des prix et calcul des rendements terminés.", flush=True)

        # 💾 Sauvegarder les rendements
        returns_file_path = os.path.join(base_dir, 'returns.csv')
        returns.to_csv(returns_file_path)
        print(f"✅ Rendements sauvegardés : {returns_file_path}", flush=True)

        # 💾 Sauvegarder les prix ajustés
        prices_file_path = os.path.join(base_dir, 'prices.csv')
        prices.to_csv(prices_file_path)
        print(f"✅ Prix sauvegardés : {prices_file_path}", flush=True)

    except Exception as e:
        print(f"❌ Erreur lors du téléchargement ou de la sauvegarde : {e}", flush=True)

    print("🏁 Fin du script.", flush=True)
    return returns, prices


if __name__ == "__main__":
    download_data()
