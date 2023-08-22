import psycopg2
import csv
from scrape_kit.src import utils
import njpr_db

conn = psycopg2.connect("dbname=njpr user=postgres")

FIELDS = [
    "gis_pin",
    "property_location",
    "additional_lots",
    "deed_book",
    "deed_page",
    "owner_address",
    "owner_city",
    "owner_name",
    "owner_zip",
    "improvement_value",
    "land_value",
    "net_value",
]

with open("./assets/quick_facts.csv", "r") as fp:
    reader = csv.DictReader(fp)
    for row in reader:
        print(row)
        row["gis_pin"]
        break

cur = conn.cursor()
query = """
SELECT
	properties."id" AS property_id,
	properties.property_location,
	property_owners."name" AS owner_name,
	property_owners.street_address AS owner_address,
	property_owners.city_state_zip AS owner_city,
	property_owners.is_redacted AS owner_is_redacted,
	properties.sq_ft,
	properties.sale_date,
	properties.deed_book, 
	properties.deed_page,	
	properties.land_assmnt,
	properties.building_assmnt,
	properties.total_assmnt, 	
	municipalities."name" AS municipality_name,
	municipalities.county AS county_name,
	properties.municipality_id,
	properties.county_id,
	properties.block_id,
	properties.additional_lots,
	properties.acreage,
	properties.property_class,
	properties.property_owner_id,
	properties.geo_location,
	ST_X ( properties.geo_location :: geometry ) AS lat,
	ST_Y ( properties.geo_location :: geometry ) AS lng,
	properties.sale_price 
FROM
	parcels.properties
	INNER JOIN parcels.property_owners ON properties.property_owner_id = property_owners."id"
	INNER JOIN parcels.municipalities ON properties.municipality_id = municipalities."id" 
WHERE
	properties.gis_pin = %s
"""
cur.execute(query, ("0906_15203_19",))
data = cur.fetchone()
print(data)

prop = njpr_db.find_property("0906_15203_19")
print(prop.property_location)
