import csv

import psycopg2

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


def get_property(conn, gis_pin: str) -> tuple:
    with conn.cursor() as cur:
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
        cur.execute(query, (gis_pin,))
        data = cur.fetchone()
        return data


def sanitize_data(s: str) -> str:
    if not s:
        return None

    return " ".join(s.split()).strip()


def null_is_zero(d):
    if d == 0:
        return None
    return d


with open("./assets/quick_facts.csv", "r") as fp:
    reader = csv.DictReader(fp)
    row: dict
    for row in reader:
        prop = get_property(conn, row["gis_pin"])
        if not prop:
            continue

        qf = njpr_db.PropertyQuickFacts()
        qf.gis_pin = row["gis_pin"]
        qf.property_location = sanitize_data(row["property_location"])
        qf.additional_lots = sanitize_data(row["additional_lots"])
        qf.deed_book = row["deed_book"]
        qf.deed_page = row["deed_page"]
        qf.owner_address = sanitize_data(row["owner_address"])
        qf.owner_name = sanitize_data(row["owner_name"])
        qf.owner_zip = row["owner_zip"]
        qf.owner_city = sanitize_data(row["owner_city"])
        qf.improvement_value = row["improvement_value"]
        qf.land_value = row["land_value"]
        qf.net_value = row["net_value"]

        if prop[5] and qf.owner_name:
            # redacted. create owner record?
            pass

        qf.property_id = prop[0]
        qf.sale_date = prop[7]
        qf.sale_price = null_is_zero(prop[25])
        qf.sq_ft = null_is_zero(prop[6])
        qf.acreage = null_is_zero(prop[19])
        qf.property_class = prop[20]
        qf.deed_book = prop[8]
        qf.deed_page = prop[9]
        qf.county_id = prop[16]
        qf.county_name = prop[14]
        qf.municipality_id = prop[15]
        qf.municipality_name = prop[13]
        qf.improvement_value = null_is_zero(prop[11])
        qf.land_value = null_is_zero(prop[10])
        qf.net_value = null_is_zero(prop[12])
        qf.lat = prop[23]
        qf.lng = prop[24]

        qf.save()
        print(row["gis_pin"])
