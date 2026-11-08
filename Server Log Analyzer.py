
def analyze_log(file_name):
    status_counts = {}
    ip_counts = {}
    slow_requests = []

    total_requests = 0

    try:
        with open(file_name, "r", encoding="utf-8") as file:

            for line_number, line in enumerate(file, start=1):

                if not line.strip():
                    continue

                parts = [item.strip() for item in line.split("|")]

                if len(parts) != 6:
                    print(f"Invalid log format at line {line_number}")
                    continue

                timestamp, ip, method, path, status, response_time = parts

                try:
                    status = int(status)
                    response_time = float(response_time)

                except ValueError:
                    print(f"Invalid data at line {line_number}")
                    continue

                total_requests += 1

                status_counts[status] = status_counts.get(status, 0) + 1

                ip_counts[ip] = ip_counts.get(ip, 0) + 1

                if response_time > 1:
                    slow_requests.append({
                        "ip": ip,
                        "path": path,
                        "response_time": response_time
                    })

    except FileNotFoundError:
        print("Log file was not found.")
        return

    display_report(
        total_requests,
        status_counts,
        ip_counts,
        slow_requests
    )


def display_report(total, status_counts, ip_counts, slow_requests):

    print("\nSERVER LOG ANALYSIS REPORT")
    print("=" * 45)

    print(f"Total Requests: {total}")

    print("\nHTTP Status Summary")
    print("-" * 45)

    for status, count in sorted(status_counts.items()):
        print(f"Status {status}: {count} requests")

    print("\nTop IP Addresses")
    print("-" * 45)

    sorted_ips = sorted(
        ip_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )

    for ip, count in sorted_ips[:5]:
        print(f"{ip}: {count} requests")

    print("\nSlow Requests (Over 1 Second)")
    print("-" * 45)

    if slow_requests:
        for request in slow_requests:
            print(
                f"{request['ip']} | "
                f"{request['path']} | "
                f"{request['response_time']} seconds"
            )
    else:
        print("No slow requests found.")

    print("\nAnalysis Completed.")


def main():
    print("Server Log Analyzer")
    print("-" * 30)

    file_name = input("Enter log file name: ").strip()

    if not file_name:
        print("File name cannot be empty.")
        return

    analyze_log(file_name)


if __name__ == "__main__":
    main()
