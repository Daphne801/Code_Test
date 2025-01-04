import sys
import csv

# The following function is written in Python 3.9

def main():
    # Read in input_file and output_file paths from command inputs
    if len(sys.argv) != 3:
        print("Please follow the input format: ./Exercise.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    
    stats = {}

    # Read input CSV line-by-line (streaming)
    with open(input_file, "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            
            # Convert to integers           
            timestamp = int(row[0])
            symbol = row[1]
            quantity = int(row[2])
            price = int(row[3])

            if symbol not in stats:
                # Initialize if first time seeing this symbol
                stats[symbol] = {
                    "last_timestamp": None,
                    "max_time_gap": 0,
                    "total_volume": 0,
                    "total_cost": 0,
                    "max_price": 0
                }

            # Update max_time_gap
            if stats[symbol]["last_timestamp"] is not None:
                gap = timestamp - stats[symbol]["last_timestamp"]
                if gap > stats[symbol]["max_time_gap"]:
                    stats[symbol]["max_time_gap"] = gap

            # Update last_timestamp
            stats[symbol]["last_timestamp"] = timestamp

            # Update total_volume
            stats[symbol]["total_volume"] += quantity

            # Update total_cost (for Weighted Average Price)
            stats[symbol]["total_cost"] += quantity * price

            # Update max_price
            if price > stats[symbol]["max_price"]:
                stats[symbol]["max_price"] = price

    # Now write results to output
    # Sorted by symbol ascending
    with open(output_file, "w", newline="") as out:
        writer = csv.writer(out)
        for symbol in sorted(stats.keys()):
            info = stats[symbol]
            # WeightedAveragePrice is truncated integer division
            # total_cost // total_volume
            weighted_avg_price = info["total_cost"] // info["total_volume"]

            writer.writerow([
                symbol,
                info["max_time_gap"],
                info["total_volume"],
                weighted_avg_price,
                info["max_price"]
            ])

if __name__ == "__main__":
    main()
