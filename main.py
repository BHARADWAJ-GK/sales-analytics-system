from utils.file_handler import read_sales_data
from utils.data_processor import *
from utils.api_handler import *

DATA_FILE = "data/sales_data.txt"

def main():
    try:
        print("\n" + "=" * 35)
        print("  SALES ANALYTICS SYSTEM")
        print("=" * 35 + "\n")

        print("[1/10] Reading sales data...")
        raw_data = read_sales_data(DATA_FILE)
        print(f"✓ Successfully read {len(raw_data)} transactions\n")

        print("[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_data)
        print(f"✓ Parsed {len(transactions)} records\n")

        print("[3/10] Filter Options Available:")
        filtered, invalid_count, summary = validate_and_filter(transactions)
        print("\nDo you want to filter data? (y/n): ", end="")
        choice = input().lower()

        if choice == "y":
            print("Enter region (or press Enter to skip): ", end="")
            region = input().strip() or None

            print("Enter minimum amount (or press Enter to skip): ", end="")
            min_amt = input().strip()
            min_amt = float(min_amt) if min_amt else None

            print("Enter maximum amount (or press Enter to skip): ", end="")
            max_amt = input().strip()
            max_amt = float(max_amt) if max_amt else None

            filtered, invalid_count, summary = validate_and_filter(
                transactions, region, min_amt, max_amt
            )

        print("\n[4/10] Validating transactions...")
        print(f"✓ Valid: {summary['final_count']} | Invalid: {invalid_count}\n")

        print("[5/10] Analyzing sales data...")
        calculate_total_revenue(filtered)
        region_wise_sales(filtered)
        top_selling_products(filtered)
        customer_analysis(filtered)
        daily_sales_trend(filtered)
        find_peak_sales_day(filtered)
        low_performing_products(filtered)
        print("✓ Analysis complete\n")

        print("[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        mapping = create_product_mapping(api_products)

        print("[7/10] Enriching sales data...")
        enriched_data = enrich_sales_data(filtered, mapping)

        print("[8/10] Saving enriched data...")
        save_enriched_data(enriched_data)

        print("[9/10] Generating comprehensive report...")
        generate_sales_report(filtered, enriched_data)

        print("\n[10/10] PROCESS COMPLETED SUCCESSFULLY 🎉")
        print("Files generated:")
        print(" - data/enriched_sales_data.txt")
        print(" - output/sales_report.txt\n")

    except Exception as e:
        print("System Error:", e)

if __name__ == "__main__":
    main()
