import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "2pT0OiBxG0x_ErBAPnlyWTGWls9SWRh8qgsUVCcRfwvdU9YjHZwEQkWCmVMRMP-ieEjoCOrgOl5MIp6l_hOubQ=="
org = "Papagei"
url = "http://localhost:8086"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket = "Hatred"

write_api = client.write_api(write_options=SYNCHRONOUS)

for value in range(5):
    point = (
        Point("measurement1")
        .tag("tagname1", "tagvalue1")
        .field("field1", value)
    )
    write_api.write(bucket=bucket, org="Papagei", record=point)
    time.sleep(1)

query_api = client.query_api()

query = """from(bucket: "Hatred")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "measurement1")"""
tables = query_api.query(query, org="Papagei")

for table in tables:
  for record in table.records:
    print(record)