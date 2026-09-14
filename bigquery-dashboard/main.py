import os
from flask import Flask, render_template, request
from google.cloud import bigquery

app = Flask(__name__)

# --- BigQuery SQL (your B3 queries) ---

QUERY_COUNTRY_REVENUE = """
SELECT
  u.country AS country,
  ROUND(SUM(oi.sale_price), 2) AS total_revenue,
  COUNT(DISTINCT oi.order_id) AS total_orders
FROM `bigquery-public-data.thelook_ecommerce.order_items` oi
JOIN `bigquery-public-data.thelook_ecommerce.users` u
  ON oi.user_id = u.id
WHERE oi.status = 'Complete'
GROUP BY country
ORDER BY total_revenue DESC
LIMIT 10
"""

QUERY_MONTHLY_REVENUE = """
SELECT
  FORMAT_DATE('%Y-%m', DATE(created_at)) AS month,
  ROUND(SUM(sale_price), 2) AS revenue
FROM `bigquery-public-data.thelook_ecommerce.order_items`
WHERE status = 'Complete'
GROUP BY month
ORDER BY month
"""

def run_bq_query(sql: str):
    client = bigquery.Client()
    job = client.query(sql)
    rows = job.result()
    return [dict(r) for r in rows]


@app.get("/")
def home():
    # default view
    selected = request.args.get("q", "country")
    data = None
    title = None

    if selected == "country":
        title = "Top Revenue by Country (Completed Orders)"
        data = run_bq_query(QUERY_COUNTRY_REVENUE)

    elif selected == "monthly":
        title = "Monthly Revenue Trend (Completed Orders)"
        data = run_bq_query(QUERY_MONTHLY_REVENUE)

    else:
        title = "Choose a query"
        data = []

    return render_template("index.html", selected=selected, title=title, data=data)


if __name__ == "__main__":
    # local run
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
