from datetime import datetime, timezone
import requests

def main():
    timestamp = datetime.now(timezone.utc).isoformat()
    url = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:157.0) Gecko/20100101 Firefox/157.0"}

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()

        output_file = "GLB.Ts+dSST.csv"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(res.text)

        print(f"Successfully fetched and saved to {output_file} at {timestamp}")
    except Exception as e:
        print(f"Error fetching data: {e}")
        exit(1)

if __name__ == "__main__":
    main()