import requests

BASE_URL = "https://dummyjson.com/products"

def fetch_all_products(limit=100):
    try:
        print("Fetching products from API...")
        response = requests.get(f"{BASE_URL}?limit={limit}")
        response.raise_for_status()
        data = response.json()
        print("API fetch successful")
        return data.get("products", [])
    except Exception as e:
        print("API fetch failed:", e)
        return []


def create_product_mapping(api_products):
    mapping = {}
    for product in api_products:
        try:
            pid = int(product["id"])
            mapping[pid] = {
                "title": product.get("title"),
                "category": product.get("category"),
                "brand": product.get("brand"),
                "rating": product.get("rating")
            }
        except:
            continue
    return mapping


def enrich_sales_data(transactions, product_mapping):
    enriched = []
    for tx in transactions:
        new_tx = tx.copy()
        try:
            numeric_id = int(''.join(filter(str.isdigit, tx["ProductID"])))
            if numeric_id in product_mapping:
                product = product_mapping[numeric_id]
                new_tx["API_Category"] = product["category"]
                new_tx["API_Brand"] = product["brand"]
                new_tx["API_Rating"] = product["rating"]
                new_tx["API_Match"] = True
            else:
                new_tx["API_Category"] = None
                new_tx["API_Brand"] = None
                new_tx["API_Rating"] = None
                new_tx["API_Match"] = False
        except:
            new_tx["API_Category"] = None
            new_tx["API_Brand"] = None
            new_tx["API_Rating"] = None
            new_tx["API_Match"] = False
        enriched.append(new_tx)
    return enriched


def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            header = "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n"
            file.write(header)

            for tx in enriched_transactions:
                line = (
                    f"{tx['TransactionID']}|"
                    f"{tx['Date']}|"
                    f"{tx['ProductID']}|"
                    f"{tx['ProductName']}|"
                    f"{tx['Quantity']}|"
                    f"{tx['UnitPrice']}|"
                    f"{tx['CustomerID']}|"
                    f"{tx['Region']}|"
                    f"{tx.get('API_Category', '')}|"
                    f"{tx.get('API_Brand', '')}|"
                    f"{tx.get('API_Rating', '')}|"
                    f"{tx.get('API_Match', False)}\n"
                )
                file.write(line)

        print(f"Enriched data saved to {filename}")
    except Exception as e:
        print("Failed to save enriched data:", e)
