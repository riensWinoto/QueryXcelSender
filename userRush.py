import psycopg2
import pandas as pd
from slack import WebClient
import hvac
import os
import sys

# fetch credential from hashicorp vault
client = hvac.Client(
    url=os.environ['VAULT_ADDR'],
    token=os.environ['VAULT_TOKEN']
)

vault_psql = client.secrets.kv.v2.read_secret_version(
    mount_point='kv',
    path='postgres',
)

vault_slack = client.secrets.kv.v2.read_secret_version(
    mount_point='kv',
    path='slack',
)

psql_pass = vault_psql['data']['data']['production']
slack_creds = vault_slack['data']['data']['kueri_sender']

# open connection to db
connection = psycopg2.connect(
    user="youruser",
    password=psql_pass,
    host="100.100.100.100",
    port="5432",
    database="yourdb"
)

# get input from command line
in_cmdl = sys.argv
print(f"Argument given: {in_cmdl}")

# variables
start_date = in_cmdl[1]
end_date = in_cmdl[2]
excel_title = "userStrike.xlsx"
csv_locs = "/home/rienswinoto/Documents/pythonCollection/queryDB/sql.csv"
excel_locs = f"/home/rienswinoto/Documents/pythonCollection/queryDB/{excel_title}"
slack_token = slack_creds
slack_receiver_id = "slack receiver id"
slack_comment = "your comment to receiver"

# start query
cursor = connection.cursor()
select_query = f"""COPY(SELECT created_at
FROM anything
WHERE created_at between '{start_date}' and '{end_date}'
ORDER by company.name Asc)
TO STDOUT WITH CSV HEADER DELIMITER ','"""

# convert to csv
with open (f"{csv_locs}","w") as file:
    cursor.copy_expert(select_query, file)
print("Query converted to CSV")
cursor.close()
connection.close()

# convert to excel
pgsql_csv = pd.read_csv(csv_locs, delimiter=',')
pgsql_csv.to_excel(excel_locs, index=None)
print("CSV converted to Excel")

# send to slack
print("Try send to slack")
client = WebClient(token=slack_token)
response = client.files_upload(
    channels=slack_fadel_id,
    title=excel_title,
    file=excel_locs,
    filetype='xlsx',
    initial_comment=slack_comment
)
slack_retcode = response.status_code

if slack_retcode is 200:
    print("Success upload to slack")
else:
    print("Failed upload to slack")
