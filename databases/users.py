from google.cloud import bigquery

client = bigquery.Client()

query = """
SELECT *
FROM `bigquery-public-data.thelook_ecommerce.users`
"""

df = client.query(query).to_dataframe()

print(df.shape)

df.to_csv("users.csv", index=False)