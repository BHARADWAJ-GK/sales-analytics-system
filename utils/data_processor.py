from collections import defaultdict
from datetime import datetime

# -------------------------------
# Task 1.2: Parse and Clean Data
# -------------------------------
def parse_transactions(raw_lines):
    transactions = []

    for line in raw_lines:
        parts = line.split('|')

        if len(parts) != 8:
            continue

        try:
            transaction_id = parts[0].strip()
            date = parts[1].strip()
            product_id = parts[2].strip()
            product_name = parts[3].replace(',', '').strip()
            quantity = int(parts[4].replace(',', '').strip())
            unit_price = float(parts[5].replace(',', '').strip())
            customer_id = parts[6].strip()
            region = parts[7].strip()

            transaction = {
                'TransactionID': transaction_id,
                'Date': date,
                'ProductID': product_id,
                'ProductName': product_name,
                'Quantity': quantity,
                'UnitPrice': unit_price,
                'CustomerID': customer_id,
                'Region': region
            }

            transactions.append(transaction)
        except:
            continue

    return transactions


# -------------------------------
# Task 1.3: Validation & Filter
# -------------------------------
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid = []
    invalid_count = 0

    regions_available = set()
    min_tx_amount = float('inf')
    max_tx_amount = 0

    for tx in transactions:
        try:
            amount = tx['Quantity'] * tx['UnitPrice']

            regions_available.add(tx['Region'])
            min_tx_amount = min(min_tx_amount, amount)
            max_tx_amount = max(max_tx_amount, amount)

            if (
                tx['Quantity'] <= 0 or
                tx['UnitPrice'] <= 0 or
                not tx['TransactionID'].startswith('T') or
                not tx['ProductID'].startswith('P') or
                not tx['CustomerID'].startswith('C') or
                not tx['Region']
            ):
                invalid_count += 1
                continue

            valid.append(tx)
        except:
            invalid_count += 1

    print("\nAvailable Regions:", regions_available)
    print(f"Transaction Amount Range: {round(min_tx_amount,2)} - {round(max_tx_amount,2)}")

    filtered = []
    filtered_by_region = 0
    filtered_by_amount = 0

    for tx in valid:
        amount = tx['Quantity'] * tx['UnitPrice']

        if region and tx['Region'] != region:
            filtered_by_region += 1
            continue

        if min_amount and amount < min_amount:
            filtered_by_amount += 1
            continue

        if max_amount and amount > max_amount:
            filtered_by_amount += 1
            continue

        filtered.append(tx)

    summary = {
        'total_input': len(transactions),
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'final_count': len(filtered)
    }

    return filtered, invalid_count, summary


# -------------------------------
# Task 2.1: Revenue & Regions
# -------------------------------
def calculate_total_revenue(transactions):
    return sum(tx['Quantity'] * tx['UnitPrice'] for tx in transactions)


def region_wise_sales(transactions):
    region_data = defaultdict(lambda: {'total_sales': 0, 'transaction_count': 0})
    total_sales_all = 0

    for tx in transactions:
        revenue = tx['Quantity'] * tx['UnitPrice']
        region = tx['Region']

        region_data[region]['total_sales'] += revenue
        region_data[region]['transaction_count'] += 1
        total_sales_all += revenue

    result = {}
    for region, data in sorted(region_data.items(),
                               key=lambda x: x[1]['total_sales'],
                               reverse=True):
        result[region] = {
            'total_sales': round(data['total_sales'], 2),
            'transaction_count': data['transaction_count'],
            'percentage': round((data['total_sales'] / total_sales_all) * 100, 2)
        }

    return result


def top_selling_products(transactions, n=5):
    product_data = defaultdict(lambda: {'qty': 0, 'revenue': 0})

    for tx in transactions:
        name = tx['ProductName']
        product_data[name]['qty'] += tx['Quantity']
        product_data[name]['revenue'] += tx['Quantity'] * tx['UnitPrice']

    sorted_products = sorted(product_data.items(),
                             key=lambda x: x[1]['qty'],
                             reverse=True)

    return [
        (name, data['qty'], round(data['revenue'], 2))
        for name, data in sorted_products[:n]
    ]


def customer_analysis(transactions):
    customer_data = defaultdict(lambda: {
        'total_spent': 0,
        'purchase_count': 0,
        'products': set()
    })

    for tx in transactions:
        cid = tx['CustomerID']
        amount = tx['Quantity'] * tx['UnitPrice']

        customer_data[cid]['total_spent'] += amount
        customer_data[cid]['purchase_count'] += 1
        customer_data[cid]['products'].add(tx['ProductName'])

    result = {}
    for cid, data in sorted(customer_data.items(),
                            key=lambda x: x[1]['total_spent'],
                            reverse=True):
        result[cid] = {
            'total_spent': round(data['total_spent'], 2),
            'purchase_count': data['purchase_count'],
            'avg_order_value': round(data['total_spent'] / data['purchase_count'], 2),
            'products_bought': list(data['products'])
        }

    return result


# -------------------------------
# Task 2.2: Date Analysis
# -------------------------------
def daily_sales_trend(transactions):
    daily = defaultdict(lambda: {
        'revenue': 0,
        'transaction_count': 0,
        'unique_customers': set()
    })

    for tx in transactions:
        date = tx['Date']
        amount = tx['Quantity'] * tx['UnitPrice']

        daily[date]['revenue'] += amount
        daily[date]['transaction_count'] += 1
        daily[date]['unique_customers'].add(tx['CustomerID'])

    result = {}
    for date in sorted(daily.keys(),
                       key=lambda d: datetime.strptime(d, "%Y-%m-%d")):
        result[date] = {
            'revenue': round(daily[date]['revenue'], 2),
            'transaction_count': daily[date]['transaction_count'],
            'unique_customers': len(daily[date]['unique_customers'])
        }

    return result


def find_peak_sales_day(transactions):
    daily = daily_sales_trend(transactions)
    peak_date = max(daily.items(), key=lambda x: x[1]['revenue'])
    return (peak_date[0], peak_date[1]['revenue'], peak_date[1]['transaction_count'])


# -------------------------------
# Task 2.3: Low Products
# -------------------------------
def low_performing_products(transactions, threshold=10):
    product_data = defaultdict(lambda: {'qty': 0, 'revenue': 0})

    for tx in transactions:
        name = tx['ProductName']
        product_data[name]['qty'] += tx['Quantity']
        product_data[name]['revenue'] += tx['Quantity'] * tx['UnitPrice']

    low_products = [
        (name, data['qty'], round(data['revenue'], 2))
        for name, data in product_data.items()
        if data['qty'] < threshold
    ]

    return sorted(low_products, key=lambda x: x[1])


# -------------------------------
# PART 4: REPORT
# -------------------------------
def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    try:
        with open(output_file, "w", encoding="utf-8") as file:

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            total_revenue = calculate_total_revenue(transactions)
            total_transactions = len(transactions)
            avg_order = round(total_revenue / total_transactions, 2) if total_transactions else 0

            dates = sorted(tx["Date"] for tx in transactions)
            date_range = f"{dates[0]} to {dates[-1]}" if dates else "N/A"

            file.write("=" * 40 + "\n")
            file.write("SALES ANALYTICS REPORT\n")
            file.write(f"Generated: {now}\n")
            file.write(f"Records Processed: {total_transactions}\n")
            file.write("=" * 40 + "\n\n")

            file.write("OVERALL SUMMARY\n")
            file.write("-" * 40 + "\n")
            file.write(f"Total Revenue: ₹{total_revenue:,.2f}\n")
            file.write(f"Total Transactions: {total_transactions}\n")
            file.write(f"Average Order Value: ₹{avg_order:,.2f}\n")
            file.write(f"Date Range: {date_range}\n\n")

            file.write("REGION-WISE PERFORMANCE\n")
            file.write("-" * 40 + "\n")
            region_stats = region_wise_sales(transactions)

            file.write(f"{'Region':<10}{'Sales':<15}{'% of Total':<15}{'Transactions':<15}\n")
            for region, data in region_stats.items():
                file.write(
                    f"{region:<10}"
                    f"₹{data['total_sales']:<14,.2f}"
                    f"{data['percentage']:<15}%"
                    f"{data['transaction_count']:<15}\n"
                )
            file.write("\n")

            file.write("TOP 5 PRODUCTS\n")
            file.write("-" * 40 + "\n")
            top_products = top_selling_products(transactions)

            file.write(f"{'Rank':<6}{'Product':<20}{'Qty':<10}{'Revenue':<10}\n")
            for i, (name, qty, rev) in enumerate(top_products, start=1):
                file.write(f"{i:<6}{name:<20}{qty:<10}{rev:<10,.2f}\n")
            file.write("\n")

            file.write("TOP 5 CUSTOMERS\n")
            file.write("-" * 40 + "\n")
            customers = list(customer_analysis(transactions).items())[:5]

            file.write(f"{'Rank':<6}{'Customer':<15}{'Spent':<15}{'Orders':<10}\n")
            for i, (cid, data) in enumerate(customers, start=1):
                file.write(
                    f"{i:<6}{cid:<15}"
                    f"₹{data['total_spent']:<14,.2f}"
                    f"{data['purchase_count']:<10}\n"
                )
            file.write("\n")

            file.write("DAILY SALES TREND\n")
            file.write("-" * 40 + "\n")
            daily = daily_sales_trend(transactions)

            file.write(f"{'Date':<15}{'Revenue':<15}{'Transactions':<15}{'Customers':<10}\n")
            for date, data in daily.items():
                file.write(
                    f"{date:<15}"
                    f"₹{data['revenue']:<14,.2f}"
                    f"{data['transaction_count']:<15}"
                    f"{data['unique_customers']:<10}\n"
                )
            file.write("\n")

            peak = find_peak_sales_day(transactions)
            low_products = low_performing_products(transactions)

            file.write("PRODUCT PERFORMANCE ANALYSIS\n")
            file.write("-" * 40 + "\n")
            file.write(f"Best Selling Day: {peak[0]} | Revenue: ₹{peak[1]:,.2f} | Transactions: {peak[2]}\n\n")

            file.write("Low Performing Products:\n")
            if low_products:
                for name, qty, rev in low_products:
                    file.write(f"- {name} | Qty: {qty} | Revenue: ₹{rev:,.2f}\n")
            else:
                file.write("None\n")

            enriched_count = sum(1 for tx in enriched_transactions if tx.get("API_Match"))
            failed = len(enriched_transactions) - enriched_count
            success_rate = round((enriched_count / len(enriched_transactions)) * 100, 2) if enriched_transactions else 0

            file.write("\nAPI ENRICHMENT SUMMARY\n")
            file.write("-" * 40 + "\n")
            file.write(f"Total Products Enriched: {enriched_count}\n")
            file.write(f"Success Rate: {success_rate}%\n")
            file.write(f"Failed Enrichments: {failed}\n")

        print(f"Sales report generated at {output_file}")
    except Exception as e:
        print("Failed to generate report:", e)
