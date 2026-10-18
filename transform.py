import csv
import requests
from datetime import datetime, timezone

def parse_val(v):
  if v == "***":
    return None
  try:
    return float(v) if "." in v else int(v)
  except ValueError:
    return None

def run(input):
  timestamp = datetime.now(timezone.utc).isoformat()
  # url = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"
  url = "https://raw.githubusercontent.com/albert7617/trmnl-climate-spiral/refs/heads/master/GLB.Ts%2BdSST.csv"
  headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:157.0) Gecko/20100101 Firefox/157.0"}

  try:
    res = requests.get(url, headers=headers, timeout=4)
    status_code = res.status_code
    status_text = res.reason
    res.raise_for_status()
  except Exception as e:
    return {
      "timestamp": timestamp,
      "error": str(e),
      "status_code": getattr(e.response, "status_code", None) if hasattr(e, "response") else "FETCH_FAILED",
      "status_msg": getattr(e.response, "reason", "Fetch failed") if hasattr(e, "response") else "Fetch failed"
    }

  lines = res.text.splitlines()
  lines = lines[1:] # remove first line "Land-Ocean: Global Means"
  reader = csv.DictReader(lines)
  history = []

  for row in reader:
    year = row.get("Year")

    if not year or not year.isdigit():
      continue

    # history.append({
    #   "year": year,
    #   "jan": row.get("Jan"),
    #   "feb": row.get("Feb"),
    #   "mar": row.get("Mar"),
    #   "apr": row.get("Apr"),
    #   "may": row.get("May"),
    #   "jun": row.get("Jun"),
    #   "jul": row.get("Jul"),
    #   "aug": row.get("Aug"),
    #   "sep": row.get("Sep"),
    #   "oct": row.get("Oct"),
    #   "nov": row.get("Nov"),
    #   "dec": row.get("Dec"),
    # })
    history.append({
      "name": year,
      "data": [
        parse_val(row.get("Jan")),
        parse_val(row.get("Feb")),
        parse_val(row.get("Mar")),
        parse_val(row.get("Apr")),
        parse_val(row.get("May")),
        parse_val(row.get("Jun")),
        parse_val(row.get("Jul")),
        parse_val(row.get("Aug")),
        parse_val(row.get("Sep")),
        parse_val(row.get("Oct")),
        parse_val(row.get("Nov")),
        parse_val(row.get("Dec")),
      ]
    })

  latest = history[-1] if history else {}

  return {
    "timestamp": timestamp,
    "http_status": status_code,
    "http_reason": status_text,
    "latest": latest,
    "history": history
  }