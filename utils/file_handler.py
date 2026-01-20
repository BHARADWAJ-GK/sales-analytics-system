def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    Returns: list of raw lines (strings)
    """
    encodings = ['utf-8', 'latin-1', 'cp1252']
    lines = []

    for enc in encodings:
        try:
            with open(filename, 'r', encoding=enc) as file:
                raw_lines = file.readlines()

            for i, line in enumerate(raw_lines):
                line = line.strip()
                if i == 0:
                    continue  # Skip header
                if line:
                    lines.append(line)

            print(f"File read successfully using encoding: {enc}")
            return lines

        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print("ERROR: File not found. Please check the file path.")
            return []

    print("ERROR: Unable to read file with supported encodings.")
    return []
