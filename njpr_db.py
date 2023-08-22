from peewee import *

database = PostgresqlDatabase("njpr")


class BaseModel(Model):
    class Meta:
        database = database


class GeometryField(Field):
    field_type = "geometry"

    def db_value(self, value):
        return fn.ST_GeomFromGeoJSON(value)

    def python_value(self, value):
        return fn.ST_AsGeoJSON(value)


class Property(BaseModel):
    absentee = IntegerField(null=True)
    account = CharField(null=True)
    acreage = DoubleField(null=True)
    additional_lots = CharField(null=True)
    additional_lots_parsed = CharField(null=True)
    apn = CharField(null=True)
    assessed = IntegerField(null=True)
    bank_code = CharField(null=True)
    block_id = IntegerField(index=True)
    building_assmnt = IntegerField(null=True)
    building_class_id = IntegerField(null=True)
    building_desc = CharField(null=True)
    calculated_taxes = DoubleField(null=True)
    calculated_taxes_year = SmallIntegerField(null=True)
    census_code = CharField(null=True)
    class_4_code = CharField(null=True)
    corporate_owned = BooleanField()
    county_id = IntegerField(index=True)
    created_at = DateTimeField()
    deduction_amount = IntegerField(null=True)
    deed_book = CharField(null=True)
    deed_page = CharField(null=True)
    direct_parties = CharField(null=True)
    disabled_cnt = IntegerField(null=True)
    electric_provider_id = IntegerField(null=True)
    epl_desc = CharField(null=True)
    epl_facility_name = CharField(null=True)
    epl_further = DateField(null=True)
    epl_init = DateField(null=True)
    epl_own = CharField(null=True)
    epl_statute = CharField(null=True)
    epl_use = CharField(null=True)
    exempt = IntegerField(null=True)
    fips_census_code_id = IntegerField(index=True, null=True)
    gas_provider_id = IntegerField(null=True)
    geo_location = GeometryField(index=True, null=True)
    gis_pin = CharField(unique=True)
    is_redacted = BooleanField()
    is_rental = BooleanField()
    land_assmnt = IntegerField(null=True)
    land_desc = CharField(null=True)
    last_year_tax = DoubleField(null=True)
    map_img = CharField(null=True)
    map_page = CharField(null=True)
    market_value_estimate = IntegerField(null=True)
    market_value_estimate_range_max = IntegerField(null=True)
    market_value_estimate_range_min = IntegerField(null=True)
    market_value_estimate_updated = DateTimeField(null=True)
    matching_method_id = IntegerField(null=True)
    mortgage_account = CharField(null=True)
    mun_updated = DateField(null=True)
    municipality_id = IntegerField(index=True)
    nu_code = CharField(null=True)
    owner_city_location_id = IntegerField(null=True)
    owner_mail_address_id = IntegerField(null=True)
    # parcel_centroid = UnknownField(index=True, null=True)  # USER-DEFINED
    partial_record = BooleanField()
    prior_block = CharField(null=True)
    prior_gis_pin = CharField(null=True)
    prior_lot = CharField(null=True)
    prior_qual = CharField(null=True)
    property_city_location_id = IntegerField(null=True)
    property_city_state_zip = CharField(null=True)
    property_class = CharField(null=True)
    property_img = CharField(null=True)
    property_location = CharField(null=True)
    property_location_normalized = CharField(index=True, null=True)
    property_mail_address_id = IntegerField(null=True)
    property_owner_id = IntegerField(index=True, null=True)
    rate_year = SmallIntegerField(null=True)
    ratio = DoubleField(null=True)
    ratio_year = SmallIntegerField(null=True)
    rental_estimate = DoubleField(null=True)
    rental_estimate_range_max = DoubleField(null=True)
    rental_estimate_range_min = DoubleField(null=True)
    rental_estimate_updated = DateTimeField(null=True)
    reverse_parties = CharField(null=True)
    # rooftop = UnknownField(index=True, null=True)  # USER-DEFINED
    sale_date = DateField(null=True)
    sale_price = IntegerField(null=True)
    senior_citizens_cnt = IntegerField(null=True)
    sewer_service_area_id = IntegerField(null=True)
    shard_num = IntegerField()
    sq_ft = IntegerField(null=True)
    street_address = CharField(null=True)
    surv_spouse_cnt = IntegerField(null=True)
    tax_rate = DoubleField(null=True)
    tax_ratio = DoubleField(null=True)
    taxes_1 = DoubleField(null=True)
    taxes_2 = DoubleField(null=True)
    total_assmnt = DoubleField(null=True)
    total_units = IntegerField(null=True)
    type_use = CharField(null=True)
    updated = DateField(null=True)
    updated_at = DateTimeField(null=True)
    valuation_source = CharField(null=True)
    veterans_cnt = IntegerField(null=True)
    water_provider_id = IntegerField(null=True)
    widows_cnt = IntegerField(null=True)
    yr_built = SmallIntegerField(null=True)
    yr_built_raw = CharField(null=True)
    zillow_pid = CharField(null=True)
    zone_id = IntegerField(null=True)

    class Meta:
        table_name = "properties"
        indexes = ((("gis_pin", "partial_record"), False),)
        schema = "parcels"


class PropertyQuickFacts(BaseModel):
    acreage = DoubleField(null=True)
    additional_lots = CharField(null=True)
    county_id = IntegerField(null=True)
    county_name = CharField(null=True)
    deed_book = CharField(null=True)
    deed_page = CharField(null=True)
    gis_pin = CharField(unique=True)
    improvement_value = IntegerField(null=True)
    land_value = IntegerField(null=True)
    lat = DoubleField(null=True)
    lng = DoubleField(null=True)
    municipality_id = IntegerField(null=True)
    municipality_name = CharField(null=True)
    net_value = IntegerField(null=True)
    owner_address = CharField(null=True)
    owner_city = CharField(null=True)
    owner_id = IntegerField(null=True)
    owner_name = CharField(null=True)
    owner_zip = CharField(null=True)
    property_class = CharField(null=True)
    property_id = IntegerField(unique=True)
    property_location = CharField(null=True)
    sale_date = DateField(null=True)
    sale_price = IntegerField(null=True)
    sq_ft = IntegerField(null=True)

    class Meta:
        table_name = "property_quick_facts"
        schema = "parcels"


def find_property(gis_pin: str) -> Property | None:
    return Property.get_or_none(Property.gis_pin == gis_pin)
