from peewee import *

database = PostgresqlDatabase('njpr')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class AssociatedParties(BaseModel):
    full_name = CharField()
    normalized_name = CharField(unique=True)

    class Meta:
        table_name = 'associated_parties'
        schema = 'parcels'

class BroadbandProviders(BaseModel):
    business = BooleanField(null=True)
    consumer = BooleanField(null=True)
    dba_name = CharField(null=True)
    frn = CharField(unique=True)
    hoco_final = CharField(null=True)
    hoco_num = CharField(index=True, null=True)
    holding_company_name = CharField(null=True)
    provider_id = CharField(null=True, unique=True)
    provider_name = CharField(null=True)
    state_abbr = CharField(null=True)

    class Meta:
        table_name = 'broadband_providers'
        schema = 'parcels'

class Counties(BaseModel):
    code = CharField(unique=True)
    created_at = DateTimeField()
    effective_tax_rate = DoubleField(null=True)
    median_home_value = IntegerField(null=True)
    median_income = IntegerField(null=True)
    median_real_estate_taxes_paid = IntegerField(null=True)
    name = CharField()
    normalized_name = CharField(unique=True)
    owner_occupied_housing_pct = DoubleField(null=True)
    renter_occupied_housing_pct = DoubleField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        table_name = 'counties'
        schema = 'parcels'

class Cities(BaseModel):
    county = ForeignKeyField(column_name='county_id', field='id', model=Counties)
    name = CharField()
    normalized_name = CharField(unique=True)

    class Meta:
        table_name = 'cities'
        indexes = (
            (('county', 'normalized_name'), False),
            (('county', 'normalized_name'), True),
        )
        schema = 'parcels'

class Municipalities(BaseModel):
    agg_assessed_value = DoubleField(null=True)
    agg_true_value = DoubleField(null=True)
    assessed_value_personal = DoubleField(null=True)
    assessor_email = CharField(null=True)
    assessor_name = CharField(null=True)
    assessor_phone = CharField(null=True)
    assessor_website = CharField(null=True)
    avg_ratio_assessed_true_val = DoubleField(null=True)
    avg_sales_price = DoubleField(null=True)
    clerk_email = CharField(null=True)
    clerk_fax = CharField(null=True)
    clerk_name = CharField(null=True)
    clerk_phone = CharField(null=True)
    clerk_website = CharField(null=True)
    codebook_homepage = CharField(null=True)
    codebook_zoning = CharField(null=True)
    county = CharField(index=True)
    county_id = ForeignKeyField(column_name='county_id', field='id', model=Counties)
    created_at = DateTimeField()
    d_clerk_email = CharField(null=True)
    d_clerk_name = CharField(null=True)
    d_clerk_phone = CharField(null=True)
    eng_email = CharField(null=True)
    eng_name = CharField(null=True)
    eng_phone = CharField(null=True)
    eng_website = CharField(null=True)
    equalized_valuation = DoubleField(null=True)
    munic_code = CharField(unique=True)
    name = CharField(index=True)
    normalized_name = CharField(index=True)
    num_sales = IntegerField(null=True)
    opra_url = CharField(null=True)
    shard_num = IntegerField()
    total_sales_price = DoubleField(null=True)
    updated_at = DateTimeField(null=True)
    website = CharField(null=True)

    class Meta:
        table_name = 'municipalities'
        schema = 'parcels'

class CitizensPropertyTaxSummaries(BaseModel):
    avg_county_taxes = DoubleField(null=True)
    avg_municipal_taxes = DoubleField(null=True)
    avg_residential_property_value = DoubleField(null=True)
    avg_school_taxes = DoubleField(null=True)
    avg_total_taxes = DoubleField(null=True)
    county = ForeignKeyField(column_name='county_id', field='id', model=Counties)
    county_name = CharField()
    county_property_tax_rate_eq = DoubleField(null=True)
    county_rate = DoubleField(null=True)
    county_share = DoubleField(null=True)
    county_taxes = DoubleField(null=True)
    created_at = DateTimeField()
    municipal_property_tax_rate_eq = DoubleField(null=True)
    municipal_rate = DoubleField(null=True)
    municipal_share = DoubleField(null=True)
    municipal_taxes = DoubleField(null=True)
    municipality_code = CharField(unique=True)
    municipality = ForeignKeyField(column_name='municipality_id', field='id', model=Municipalities, unique=True)
    municipality_name = CharField()
    school_property_tax_rate_eq = DoubleField(null=True)
    school_rate = DoubleField(null=True)
    school_share = DoubleField(null=True)
    school_taxes = DoubleField(null=True)
    taxable_property_value = DoubleField(null=True)
    total_property_tax_rate_eq = DoubleField(null=True)
    total_rate = DoubleField(null=True)
    total_taxes = DoubleField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        table_name = 'citizens_property_tax_summaries'
        schema = 'parcels'

class CityLocations(BaseModel):
    city = CharField(null=True)
    fingerprint = BigIntegerField(unique=True)
    state = CharField(null=True)
    zip = CharField(null=True)

    class Meta:
        table_name = 'city_locations'
        schema = 'parcels'

class MunicipalityBlocks(BaseModel):
    block = CharField()
    municipality = ForeignKeyField(column_name='municipality_id', field='id', model=Municipalities)

    class Meta:
        table_name = 'municipality_blocks'
        indexes = (
            (('municipality', 'block'), False),
            (('municipality', 'block'), True),
        )
        schema = 'parcels'

class ContaminatedSites(BaseModel):
    address = CharField(null=True)
    category = CharField(null=True)
    comu_code = CharField(null=True)
    county = ForeignKeyField(column_name='county_id', field='id', model=Counties)
    fingerprint = BigIntegerField(unique=True)
    geo_location = UnknownField(index=True, null=True)  # USER-DEFINED
    municipality = ForeignKeyField(column_name='municipality_id', field='id', model=Municipalities)
    pi_name = CharField(null=True)
    rem_level = CharField(null=True)
    status = CharField(null=True)
    zip_code = CharField(null=True)

    class Meta:
        table_name = 'contaminated_sites'
        schema = 'parcels'

class ContaminatedSiteBlockLinks(BaseModel):
    block = ForeignKeyField(column_name='block_id', field='id', model=MunicipalityBlocks)
    contaminated_site = ForeignKeyField(column_name='contaminated_site_id', field='id', model=ContaminatedSites)

    class Meta:
        table_name = 'contaminated_site_block_links'
        indexes = (
            (('contaminated_site', 'block'), True),
        )
        schema = 'parcels'
        primary_key = CompositeKey('block', 'contaminated_site')

class CountyAnnualPropertyTaxRates(BaseModel):
    county = ForeignKeyField(column_name='county_id', field='id', model=Counties)
    created_at = DateTimeField()
    property_class = CharField()
    tax_rate = DoubleField()
    tax_year = IntegerField(index=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        table_name = 'county_annual_property_tax_rates'
        indexes = (
            (('county', 'tax_year'), False),
            (('county', 'tax_year'), True),
        )
        schema = 'parcels'

class CountyTaxBreakdowns(BaseModel):
    county = ForeignKeyField(column_name='county_id', field='id', model=Counties)
    created_at = DateTimeField()
    tax_heading = CharField(index=True)
    tax_rate = DoubleField()
    updated_at = DateTimeField(null=True)

    class Meta:
        table_name = 'county_tax_breakdowns'
        indexes = (
            (('county', 'tax_heading'), False),
            (('county', 'tax_heading'), True),
        )
        schema = 'parcels'

class LookupTable(BaseModel):
    code = CharField()
    description = CharField(null=True)
    discriminator = CharField()

    class Meta:
        table_name = 'lookup_table'
        indexes = (
            (('discriminator', 'code'), False),
            (('discriminator', 'code'), True),
        )
        schema = 'parcels'

class DeedParties(BaseModel):
    city_state = CharField(null=True)
    fingerprint = BigIntegerField(unique=True)
    is_grantee = BooleanField()
    mail_city = CharField(null=True)
    mail_company = CharField(null=True)
    mail_corrections = CharField(null=True)
    mail_crrt = CharField(null=True)
    mail_dpv = CharField(null=True)
    mail_error_code = ForeignKeyField(column_name='mail_error_code_id', field='id', model=LookupTable, null=True)
    mail_house_num = CharField(null=True)
    mail_left_overs = CharField(null=True)
    mail_post_dir = CharField(null=True)
    mail_pre_dir = CharField(null=True)
    mail_rdi = CharField(null=True)
    mail_result_code = CharField(null=True)
    mail_state = CharField(null=True)
    mail_street = CharField(null=True)
    mail_street2 = CharField(null=True)
    mail_street_name = CharField(null=True)
    mail_sud = CharField(null=True)
    mail_suffix = CharField(null=True)
    mail_suite = CharField(null=True)
    mail_unit_num = CharField(null=True)
    mail_zip = CharField(null=True)
    mail_zip4 = CharField(null=True)
    name = CharField(null=True)
    nctl = CharField(null=True)
    street = CharField(null=True)
    zip = CharField(null=True)

    class Meta:
        table_name = 'deed_parties'
        schema = 'parcels'

class Demographics(BaseModel):
    average_age = DoubleField(null=True)
    average_household_income = IntegerField(null=True)
    average_household_size = DoubleField(null=True)
    children_percentage = DoubleField(null=True)
    education_percentage = DoubleField(null=True)
    employment_percentage = DoubleField(null=True)
    municipality = ForeignKeyField(column_name='municipality_id', field='id', model=Municipalities, unique=True)

    class Meta:
        table_name = 'demographics'
        schema = 'parcels'

class DemographicStatistics(BaseModel):
    demographics = ForeignKeyField(column_name='demographics_id', field='id', model=Demographics)
    name = CharField()
    stats_type = CharField()
    value = DoubleField()

    class Meta:
        table_name = 'demographic_statistics'
        indexes = (
            (('demographics', 'stats_type'), False),
        )
        schema = 'parcels'

class Elections(BaseModel):
    name = CharField()
    slug = CharField(unique=True)

    class Meta:
        table_name = 'elections'
        schema = 'parcels'

class FloodZones(BaseModel):
    area = DoubleField(null=True)
    dfirm_id = CharField(null=True)
    eff_date = DateField(null=True)
    firm_pan = CharField(null=True)
    fld_ar_id = CharField(null=True)
    fld_zone = CharField(null=True)
    gid = CharField(index=True, null=True)
    intersection_area = DoubleField(null=True)
    intersection_percent = DoubleField(null=True)
    parcel_area = DoubleField(null=True)
    sfha_tf = CharField(null=True)
    static_bfe = CharField(null=True)
    version_id = CharField(null=True)
    zone_subty = CharField(null=True)

    class Meta:
        table_name = 'flood_zones'
        indexes = (
            (('dfirm_id', 'firm_pan', 'fld_ar_id', 'fld_zone', 'gid'), False),
        )
        schema = 'parcels'

class MailingAddresses(BaseModel):
    address = CharField(null=True)
    address_carrier_route = CharField(null=True)
    city = CharField(null=True)
    cmra = CharField(null=True)
    company = CharField(null=True)
    corrections = CharField(null=True)
    crrt = CharField(null=True)
    deliverable = CharField(null=True)
    discriminator = CharField(index=True)
    dpv = CharField(null=True)
    dpv_notes = CharField(null=True)
    error_code = ForeignKeyField(column_name='error_code_id', field='id', model=LookupTable, null=True)
    fingerprint = BigIntegerField(unique=True)
    house_number = CharField(null=True)
    left_overs = CharField(null=True)
    line_of_travel = CharField(null=True)
    no_stats = CharField(null=True)
    pbsa = CharField(null=True)
    post_direction = CharField(null=True)
    pre_direction = CharField(null=True)
    rdi = CharField(null=True)
    result_code = CharField(null=True)
    state = CharField(null=True)
    street = CharField(null=True)
    street2 = CharField(null=True)
    street_direction = CharField(null=True)
    street_direction_left = CharField(null=True)
    street_direction_right = CharField(null=True)
    street_name = CharField(null=True)
    sud = CharField(null=True)
    suffix = CharField(null=True)
    suite = CharField(null=True)
    unit_number = CharField(null=True)
    usps_bar_code = CharField(null=True)
    vacant_status = CharField(null=True)
    zip = CharField(null=True)
    zip4 = CharField(null=True)

    class Meta:
        table_name = 'mailing_addresses'
        schema = 'parcels'

class MortgageBorrowers(BaseModel):
    full_name = CharField(unique=True)

    class Meta:
        table_name = 'mortgage_borrowers'
        schema = 'parcels'

class MortgageLenders(BaseModel):
    dba_name = CharField(null=True)
    fingerprint = BigIntegerField(unique=True)
    lender_type = CharField(null=True)
    lender_type_description = CharField(null=True)
    mailing_address = ForeignKeyField(column_name='mailing_address_id', field='id', model=MailingAddresses, null=True)
    name = CharField(index=True)
    zip = CharField(null=True)
    zip4 = CharField(null=True)

    class Meta:
        table_name = 'mortgage_lenders'
        indexes = (
            (('name', 'zip'), False),
        )
        schema = 'parcels'

class MunicipalityBlockAvgSalesPrices(BaseModel):
    block = ForeignKeyField(column_name='block_id', field='id', model=MunicipalityBlocks)
    data_quarter = SmallIntegerField(null=True)
    data_year = SmallIntegerField(null=True)
    sales_price = DoubleField()

    class Meta:
        table_name = 'municipality_block_avg_sales_prices'
        indexes = (
            (('block', 'data_year', 'data_quarter'), False),
            (('block', 'data_year', 'data_quarter'), True),
        )
        schema = 'parcels'

class MunicipalityPropertyTaxSummaries(BaseModel):
    avg_residential_property_value = DoubleField(null=True)
    avg_total_property_taxes = DoubleField(null=True)
    county_health_services_taxes = DoubleField(null=True)
    county = ForeignKeyField(column_name='county_id', field='id', model=Counties)
    county_library_taxes = DoubleField(null=True)
    county_name = CharField()
    county_net_taxes_apportioned = DoubleField(null=True)
    county_open_space_preservation_trust_fund = DoubleField(null=True)
    county_tax_levy_total = DoubleField(null=True)
    created_at = DateTimeField()
    cy_county_eq_tax_rate = DoubleField(null=True)
    cy_county_rate = DoubleField(null=True)
    cy_equalized_property_value_pre_appeal = DoubleField(null=True)
    cy_local_purpose_municipal_eq_tax_rate = DoubleField(null=True)
    cy_municipal_library_rate = DoubleField(null=True)
    cy_municipal_open_space_rate = DoubleField(null=True)
    cy_municipal_rate = DoubleField(null=True)
    cy_school_eq_tax_rate = DoubleField(null=True)
    cy_school_rate = DoubleField(null=True)
    cy_total_eq_rate_excl_reap = DoubleField(null=True)
    cy_total_municipal_eq_rate = DoubleField(null=True)
    cy_total_municipal_rate = DoubleField(null=True)
    cy_total_rate = DoubleField(null=True)
    exemptions_disabled_veterans_widow_avg = DoubleField(null=True)
    exemptions_disabled_veterans_widow_num = IntegerField(null=True)
    municipal_local_open_space = DoubleField(null=True)
    municipal_local_purposes = DoubleField(null=True)
    municipal_minimum_library_tax = DoubleField(null=True)
    municipal_tax_levy_total = DoubleField(null=True)
    municipality_code = CharField(unique=True)
    municipality = ForeignKeyField(column_name='municipality_id', field='id', model=Municipalities, unique=True)
    municipality_name = CharField()
    net_valuation_taxable = DoubleField(null=True)
    property_tax_deduction_disabled_avg = DoubleField(null=True)
    property_tax_deductions_disabled_num = IntegerField(null=True)
    property_tax_deductions_senior_avg = DoubleField(null=True)
    property_tax_deductions_senior_num = IntegerField(null=True)
    property_tax_deductions_veterans_avg = DoubleField(null=True)
    property_tax_deductions_veterans_num = IntegerField(null=True)
    property_tax_deductions_veterans_surviving_spouse_avg = DoubleField(null=True)
    property_tax_deductions_veterans_surviving_spouse_num = IntegerField(null=True)
    property_tax_deductions_veterans_widow_avg = DoubleField(null=True)
    property_tax_deductions_veterans_widow_num = IntegerField(null=True)
    reap_credit_rate = DoubleField(null=True)
    school_district_budget = DoubleField(null=True)
    school_local_municipal_budget = DoubleField(null=True)
    school_regional_consolidated_joint_budget = DoubleField(null=True)
    school_tax_levy_total = DoubleField(null=True)
    state_equalization_table_avg_ratio = DoubleField(null=True)
    total_levy_county_pct = DoubleField(null=True)
    total_levy_municipal_pct = DoubleField(null=True)
    total_levy_school_pct = DoubleField(null=True)
    total_levy_tax_rate_computed = DoubleField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        table_name = 'municipality_property_tax_summaries'
        schema = 'parcels'

class MunicipalityTaxMaps(BaseModel):
    bottom_left = UnknownField(index=True, null=True)  # USER-DEFINED
    bottom_right = UnknownField(index=True, null=True)  # USER-DEFINED
    display_id = IntegerField(null=True)
    geo_pnt1 = UnknownField(index=True, null=True)  # USER-DEFINED
    geo_pnt2 = UnknownField(index=True, null=True)  # USER-DEFINED
    geo_pnt3 = UnknownField(index=True, null=True)  # USER-DEFINED
    height = IntegerField(null=True)
    img_pnt1_x = DoubleField(null=True)
    img_pnt1_y = DoubleField(null=True)
    img_pnt2_x = DoubleField(null=True)
    img_pnt2_y = DoubleField(null=True)
    img_pnt3_x = DoubleField(null=True)
    img_pnt3_y = DoubleField(null=True)
    municipality = ForeignKeyField(column_name='municipality_id', field='id', model=Municipalities)
    sheet = CharField()
    status = IntegerField(null=True)
    top_left = UnknownField(index=True, null=True)  # USER-DEFINED
    top_right = UnknownField(index=True, null=True)  # USER-DEFINED
    width = IntegerField(null=True)
    year = IntegerField()

    class Meta:
        table_name = 'municipality_tax_maps'
        indexes = (
            (('municipality', 'year', 'sheet'), False),
            (('municipality', 'year', 'sheet'), True),
        )
        schema = 'parcels'

class MunicipalityTaxRates(BaseModel):
    created_at = DateTimeField()
    effective_tax_rate = DoubleField(null=True)
    general_tax_rate = DoubleField(null=True)
    municipality = ForeignKeyField(column_name='municipality_id', field='id', model=Municipalities)
    ratio = DoubleField(null=True)
    tax_year = IntegerField()
    updated_at = DateTimeField(null=True)

    class Meta:
        table_name = 'municipality_tax_rates'
        indexes = (
            (('municipality', 'tax_year'), False),
            (('municipality', 'tax_year'), True),
        )
        schema = 'parcels'

class MunicipalityZoningMaps(BaseModel):
    bottom_left = UnknownField(index=True, null=True)  # USER-DEFINED
    bottom_right = UnknownField(index=True, null=True)  # USER-DEFINED
    display_id = IntegerField(null=True)
    geo_pnt1 = UnknownField(index=True, null=True)  # USER-DEFINED
    geo_pnt2 = UnknownField(index=True, null=True)  # USER-DEFINED
    geo_pnt3 = UnknownField(index=True, null=True)  # USER-DEFINED
    height = IntegerField(null=True)
    img_pnt1_x = DoubleField(null=True)
    img_pnt1_y = DoubleField(null=True)
    img_pnt2_x = DoubleField(null=True)
    img_pnt2_y = DoubleField(null=True)
    img_pnt3_x = DoubleField(null=True)
    img_pnt3_y = DoubleField(null=True)
    municipality = ForeignKeyField(column_name='municipality_id', field='id', model=Municipalities)
    sheet = CharField()
    status = IntegerField(null=True)
    top_left = UnknownField(index=True, null=True)  # USER-DEFINED
    top_right = UnknownField(index=True, null=True)  # USER-DEFINED
    width = IntegerField(null=True)

    class Meta:
        table_name = 'municipality_zoning_maps'
        indexes = (
            (('municipality', 'sheet'), False),
            (('municipality', 'sheet'), True),
        )
        schema = 'parcels'

class UtilityProviders(BaseModel):
    city_state_zip = CharField(null=True)
    fingerprint = BigIntegerField(unique=True)
    location = CharField(null=True)
    name = CharField()
    outage_check_url = CharField(null=True)
    outage_report_url = CharField(null=True)
    phone = CharField(null=True)
    service_type = CharField()
    website = CharField(null=True)

    class Meta:
        table_name = 'utility_providers'
        schema = 'parcels'

class PropertyOwners(BaseModel):
    city_state_zip = CharField(null=True)
    fingerprint = BigIntegerField(unique=True)
    is_redacted = BooleanField(index=True)
    name = CharField()
    normalized_location = CharField(index=True)
    normalized_name = CharField(index=True)
    street_address = CharField(null=True)

    class Meta:
        table_name = 'property_owners'
        indexes = (
            (('is_redacted', 'normalized_name'), False),
        )
        schema = 'parcels'

class Properties(BaseModel):
    absentee = IntegerField(null=True)
    account = CharField(null=True)
    acreage = DoubleField(null=True)
    additional_lots = CharField(null=True)
    additional_lots_parsed = CharField(null=True)
    apn = CharField(null=True)
    bank_code = CharField(null=True)
    block = ForeignKeyField(column_name='block_id', field='id', model=MunicipalityBlocks)
    building_class = ForeignKeyField(column_name='building_class_id', field='id', model=LookupTable, null=True)
    calculated_taxes = DoubleField(null=True)
    calculated_taxes_year = SmallIntegerField(null=True)
    census_code = CharField(null=True)
    city_state_zip = CharField(null=True)
    class_4_code = CharField(null=True)
    corporate_owned = BooleanField()
    county = ForeignKeyField(column_name='county_id', field='id', model=Counties)
    created_at = DateTimeField()
    deduction_amount = IntegerField(null=True)
    deed_book = CharField(null=True)
    deed_page = CharField(null=True)
    direct_parties = CharField(null=True)
    disabled_cnt = IntegerField(null=True)
    electric_provider = ForeignKeyField(column_name='electric_provider_id', field='id', model=UtilityProviders, null=True)
    epl_desc = CharField(null=True)
    epl_facility_name = CharField(null=True)
    epl_further = DateField(null=True)
    epl_init = DateField(null=True)
    epl_own = CharField(null=True)
    epl_statute = CharField(null=True)
    epl_use = CharField(null=True)
    gas_provider = ForeignKeyField(backref='utility_providers_gas_provider_set', column_name='gas_provider_id', field='id', model=UtilityProviders, null=True)
    geo_location = UnknownField(index=True, null=True)  # USER-DEFINED
    gis_pin = CharField(unique=True)
    is_redacted = BooleanField()
    is_rental = BooleanField()
    land_desc = CharField(null=True)
    last_year_tax = DoubleField(null=True)
    map_img = CharField(null=True)
    map_page = CharField(null=True)
    market_value_estimate = IntegerField(null=True)
    market_value_estimate_range_max = IntegerField(null=True)
    market_value_estimate_range_min = IntegerField(null=True)
    market_value_estimate_updated = DateTimeField(null=True)
    matching_method = ForeignKeyField(backref='lookup_table_matching_method_set', column_name='matching_method_id', field='id', model=LookupTable, null=True)
    mortgage_account = CharField(null=True)
    mun_updated = DateField(null=True)
    municipality = ForeignKeyField(column_name='municipality_id', field='id', model=Municipalities)
    nu_code = CharField(null=True)
    owner_city_location = ForeignKeyField(column_name='owner_city_location_id', field='id', model=CityLocations, null=True)
    owner_mail_address = ForeignKeyField(column_name='owner_mail_address_id', field='id', model=MailingAddresses, null=True)
    parcel_centroid = UnknownField(index=True, null=True)  # USER-DEFINED
    partial_record = BooleanField(index=True)
    prior_block = CharField(null=True)
    prior_gis_pin = CharField(null=True)
    prior_lot = CharField(null=True)
    prior_qual = CharField(null=True)
    property_city_location = ForeignKeyField(backref='city_locations_property_city_location_set', column_name='property_city_location_id', field='id', model=CityLocations, null=True)
    property_class = CharField(null=True)
    property_img = CharField(null=True)
    property_location = CharField(null=True)
    property_location_normalized = CharField(index=True, null=True)
    property_mail_address = ForeignKeyField(backref='mailing_addresses_property_mail_address_set', column_name='property_mail_address_id', field='id', model=MailingAddresses, null=True)
    property_owner = ForeignKeyField(column_name='property_owner_id', field='id', model=PropertyOwners, null=True)
    rate_year = SmallIntegerField(null=True)
    ratio = DoubleField(null=True)
    ratio_year = SmallIntegerField(null=True)
    rental_estimate = DoubleField(null=True)
    rental_estimate_range_max = DoubleField(null=True)
    rental_estimate_range_min = DoubleField(null=True)
    rental_estimate_updated = DateTimeField(null=True)
    reverse_parties = CharField(null=True)
    rooftop = UnknownField(index=True, null=True)  # USER-DEFINED
    sale_date = DateField(null=True)
    sale_price = IntegerField(null=True)
    senior_citizens_cnt = IntegerField(null=True)
    sewer_service_area = ForeignKeyField(backref='utility_providers_sewer_service_area_set', column_name='sewer_service_area_id', field='id', model=UtilityProviders, null=True)
    shard_num = IntegerField()
    sq_ft = IntegerField(null=True)
    street_address = CharField(null=True)
    surv_spouse_cnt = IntegerField(null=True)
    tax_rate = DoubleField(null=True)
    tax_ratio = DoubleField(null=True)
    total_units = IntegerField(null=True)
    type_use = CharField(null=True)
    updated = DateField(null=True)
    updated_at = DateTimeField(null=True)
    valuation_source = CharField(null=True)
    veterans_cnt = IntegerField(null=True)
    water_provider = ForeignKeyField(backref='utility_providers_water_provider_set', column_name='water_provider_id', field='id', model=UtilityProviders, null=True)
    widows_cnt = IntegerField(null=True)
    yr_built = SmallIntegerField(null=True)
    yr_built_raw = CharField(null=True)
    zillow_pid = CharField(null=True)
    zone = ForeignKeyField(backref='lookup_table_zone_set', column_name='zone_id', field='id', model=LookupTable, null=True)

    class Meta:
        table_name = 'properties'
        schema = 'parcels'

class NearbyProperties(BaseModel):
    main_property = ForeignKeyField(column_name='main_property_id', field='id', model=Properties)
    nearby_property = ForeignKeyField(backref='properties_nearby_property_set', column_name='nearby_property_id', field='id', model=Properties)

    class Meta:
        table_name = 'nearby_properties'
        schema = 'parcels'

class NonusableDeedCategories(BaseModel):
    code = CharField(unique=True)
    description = CharField()

    class Meta:
        table_name = 'nonusable_deed_categories'
        schema = 'parcels'

class PropertyAreas(BaseModel):
    area = IntegerField(null=True)
    attic = IntegerField(null=True)
    bsmnt = IntegerField(null=True)
    discriminator = CharField()
    first_floor = IntegerField(null=True)
    half_story = IntegerField(null=True)
    name = CharField()
    property = ForeignKeyField(column_name='property_id', field='id', model=Properties)
    segment = CharField(null=True)
    uppr_floor = IntegerField(null=True)

    class Meta:
        table_name = 'property_areas'
        indexes = (
            (('property', 'discriminator', 'name'), False),
        )
        schema = 'parcels'

class PropertyAssociatedPartyLinks(BaseModel):
    associated_party = ForeignKeyField(column_name='associated_party_id', field='id', model=AssociatedParties)
    property = ForeignKeyField(column_name='property_id', field='id', model=Properties)

    class Meta:
        table_name = 'property_associated_party_links'
        indexes = (
            (('property', 'associated_party'), True),
        )
        schema = 'parcels'
        primary_key = CompositeKey('associated_party', 'property')

class PropertyBroadbandProviderLinks(BaseModel):
    block_code = CharField(null=True)
    broadband_provider = ForeignKeyField(column_name='broadband_provider_id', field='id', model=BroadbandProviders)
    log_rec_no = CharField(null=True)
    max_ad_down = DoubleField(null=True)
    max_ad_up = DoubleField(null=True)
    property = ForeignKeyField(column_name='property_id', field='id', model=Properties)
    tech_code = CharField(null=True)

    class Meta:
        table_name = 'property_broadband_provider_links'
        indexes = (
            (('property', 'broadband_provider'), True),
        )
        schema = 'parcels'
        primary_key = CompositeKey('broadband_provider', 'property')

class PropertyLocations(BaseModel):
    location = CharField(unique=True)
    street_address = CharField(null=True)

    class Meta:
        table_name = 'property_locations'
        schema = 'parcels'

class PropertyDeeds(BaseModel):
    addl_block_1 = CharField(null=True)
    addl_block_2 = CharField(null=True)
    addl_block_3 = CharField(null=True)
    addl_block_4 = CharField(null=True)
    addl_block_5 = CharField(null=True)
    addl_lot_1 = CharField(null=True)
    addl_lot_2 = CharField(null=True)
    addl_lot_3 = CharField(null=True)
    addl_lot_4 = CharField(null=True)
    addl_lot_5 = CharField(null=True)
    addl_qualifier_1 = CharField(null=True)
    addl_qualifier_2 = CharField(null=True)
    addl_qualifier_3 = CharField(null=True)
    addl_qualifier_4 = CharField(null=True)
    addl_qualifier_5 = CharField(null=True)
    addl_value_bldg_1 = IntegerField(null=True)
    addl_value_bldg_2 = IntegerField(null=True)
    addl_value_bldg_3 = IntegerField(null=True)
    addl_value_bldg_4 = IntegerField(null=True)
    addl_value_bldg_5 = IntegerField(null=True)
    addl_value_land_1 = IntegerField(null=True)
    addl_value_land_2 = IntegerField(null=True)
    addl_value_land_3 = IntegerField(null=True)
    addl_value_land_4 = IntegerField(null=True)
    addl_value_land_5 = IntegerField(null=True)
    addl_value_total_1 = IntegerField(null=True)
    addl_value_total_2 = IntegerField(null=True)
    addl_value_total_3 = IntegerField(null=True)
    addl_value_total_4 = IntegerField(null=True)
    addl_value_total_5 = IntegerField(null=True)
    aging_date = DateField(null=True)
    appeal_status = CharField(null=True)
    assess_year = IntegerField(null=True)
    assessed_value_bldg = IntegerField(null=True)
    assessed_value_land = IntegerField(null=True)
    assessed_value_total = IntegerField(null=True)
    assessor_nu_code = CharField(null=True)
    assessor_written_cd = CharField(null=True)
    class_4_type = CharField(null=True)
    condo = CharField(null=True)
    county = ForeignKeyField(column_name='county_id', field='id', model=Counties, null=True)
    created_at = DateTimeField()
    critical_error_flag = CharField(null=True)
    date_recorded = DateField(null=True)
    date_typed = DateField(null=True)
    deed_book = CharField(null=True)
    deed_date = DateField(null=True)
    deed_id_num = CharField(index=True, null=True)
    deed_page = CharField(null=True)
    dln = CharField(null=True)
    document_path = CharField(null=True)
    etc = CharField(null=True)
    field_date = DateField(null=True)
    field_status_code = CharField(null=True)
    grantee = ForeignKeyField(column_name='grantee_id', field='id', model=DeedParties, null=True)
    grantor = ForeignKeyField(backref='deed_parties_grantor_set', column_name='grantor_id', field='id', model=DeedParties, null=True)
    is_redacted = BooleanField(null=True)
    last_update_date = DateField(null=True)
    living_space = IntegerField(null=True)
    match_method = ForeignKeyField(column_name='match_method_id', field='id', model=LookupTable, null=True)
    municipality = ForeignKeyField(column_name='municipality_id', field='id', model=Municipalities)
    property_class = CharField(null=True)
    property = ForeignKeyField(column_name='property_id', field='id', model=Properties)
    property_location = ForeignKeyField(column_name='property_location_id', field='id', model=PropertyLocations, null=True)
    questionnaire_date = DateField(null=True)
    questionnaire_status_code = CharField(null=True)
    questionnaire_who_code = CharField(null=True)
    realty_transfer_fee = IntegerField(null=True)
    reported_sales_price = IntegerField(null=True)
    rtf_error_flag = CharField(index=True, null=True)
    rtf_exempt_code = CharField(index=True, null=True)
    sales_ratio = DoubleField(null=True)
    serial_number = CharField(index=True, null=True)
    sr_nu_code = CharField(null=True)
    u_n_type = CharField(null=True)
    updated_at = DateTimeField(null=True)
    verified_sales_price = IntegerField(null=True)
    year = IntegerField(null=True)
    year_built = IntegerField(null=True)

    class Meta:
        table_name = 'property_deeds'
        schema = 'parcels'

class PropertyFloodZoneLinks(BaseModel):
    flood_zone = ForeignKeyField(column_name='flood_zone_id', field='id', model=FloodZones)
    property = ForeignKeyField(column_name='property_id', field='id', model=Properties)

    class Meta:
        table_name = 'property_flood_zone_links'
        indexes = (
            (('property', 'flood_zone'), True),
        )
        schema = 'parcels'
        primary_key = CompositeKey('flood_zone', 'property')

class PropertyForeclosures(BaseModel):
    area_building = IntegerField(null=True)
    area_building_definition_code = CharField(null=True)
    area_lot_acres = DoubleField(null=True)
    area_lot_sf = DoubleField(null=True)
    attom_id = CharField(index=True, null=True)
    auction_address = CharField(null=True)
    auction_city = CharField(null=True)
    auction_date = DateField(null=True)
    auction_direction = CharField(null=True)
    auction_house_number = CharField(null=True)
    auction_street_name = CharField(null=True)
    auction_suffix = CharField(null=True)
    auction_time = CharField(null=True)
    auction_unit = CharField(null=True)
    bath_count = IntegerField(null=True)
    bedrooms_count = IntegerField(null=True)
    borrower_name_owner = CharField(null=True)
    case_number = CharField(index=True, null=True)
    create_date = DateField(null=True)
    created_at = DateTimeField()
    default_amount = DoubleField(null=True)
    estimated_value = DoubleField(null=True)
    foreclosure_book_page = CharField(null=True)
    foreclosure_instrument_date = DateField(null=True)
    foreclosure_instrument_number = CharField(index=True, null=True)
    foreclosure_recording_date = DateField(null=True)
    geo_location = UnknownField(index=True, null=True)  # USER-DEFINED
    geo_quality = IntegerField(null=True)
    judgment_amount = DoubleField(null=True)
    judgment_date = DateField(null=True)
    lender_address = CharField(null=True)
    lender_address_city = CharField(null=True)
    lender_address_state = CharField(null=True)
    lender_address_zip = CharField(null=True)
    lender_name_full_standardized = CharField(null=True)
    lender_phone = CharField(null=True)
    loan_balance = DoubleField(null=True)
    loan_maturity_date = DateField(null=True)
    original_loan_amount = DoubleField(null=True)
    original_loan_book_page = CharField(null=True)
    original_loan_instrument_number = CharField(index=True, null=True)
    original_loan_interest_rate = DoubleField(null=True)
    original_loan_loan_number = CharField(null=True)
    original_loan_recording_date = DateField(null=True)
    parcel_number_formatted = CharField(null=True)
    penalty_interest = DoubleField(null=True)
    property_address_city = CharField(null=True)
    property_address_crrt = CharField(null=True)
    property_address_full = CharField(null=True)
    property_address_house_number = CharField(null=True)
    property_address_state = CharField(null=True)
    property_address_street_direction = CharField(null=True)
    property_address_street_name = CharField(null=True)
    property_address_street_post_direction = CharField(null=True)
    property_address_street_suffix = CharField(null=True)
    property_address_unit_prefix = CharField(null=True)
    property_address_unit_value = CharField(null=True)
    property_address_zip = CharField(null=True)
    property_address_zip4 = CharField(null=True)
    property = ForeignKeyField(column_name='property_id', field='id', model=Properties)
    property_jurisdiction_name = CharField(null=True)
    property_use_group = CharField(null=True)
    property_use_muni = CharField(null=True)
    property_use_standardized = CharField(null=True)
    publication_date = DateField(null=True)
    record_last_updated = DateField(null=True)
    record_type = CharField(null=True)
    recorded_auction_opening_bid = DoubleField(null=True)
    servicer_address = CharField(null=True)
    servicer_city = CharField(null=True)
    servicer_name = CharField(null=True)
    servicer_phone = CharField(null=True)
    servicer_state = CharField(null=True)
    servicer_zip = CharField(null=True)
    situs_county = CharField(null=True)
    situs_state_code = CharField(null=True)
    situs_state_county_fips = CharField(null=True)
    transaction_id = CharField(null=True)
    trustee_address = CharField(null=True)
    trustee_address_city = CharField(null=True)
    trustee_address_house_number = CharField(null=True)
    trustee_address_state = CharField(null=True)
    trustee_address_street_direction = CharField(null=True)
    trustee_address_street_name = CharField(null=True)
    trustee_address_street_post_direction = CharField(null=True)
    trustee_address_street_suffix = CharField(null=True)
    trustee_address_unit_value = CharField(null=True)
    trustee_address_zip = CharField(null=True)
    trustee_name = CharField(null=True)
    trustee_phone = CharField(null=True)
    trustee_reference_number = CharField(null=True)
    updated_at = DateTimeField(null=True)
    year_built = IntegerField(null=True)
    year_built_effective = IntegerField(null=True)

    class Meta:
        table_name = 'property_foreclosures'
        schema = 'parcels'

class PropertyHistories(BaseModel):
    absentee = SmallIntegerField(null=True)
    acreage = DoubleField(null=True)
    addition_lots_2 = CharField(null=True)
    additional_lots = CharField(null=True)
    assessed = IntegerField(null=True)
    bank_code = CharField(null=True)
    building_assmnt = IntegerField(null=True)
    building_class = ForeignKeyField(column_name='building_class_id', field='id', model=LookupTable, null=True)
    calculated_taxes = DoubleField(null=True)
    calculated_taxes_year = SmallIntegerField(null=True)
    corporate_owned = BooleanField()
    data_year = SmallIntegerField()
    deduction_amount = IntegerField(null=True)
    deed_book = CharField(null=True)
    deed_page = CharField(null=True)
    delinquent_code = CharField(null=True)
    disabled_cnt = IntegerField(null=True)
    epl_desc = CharField(null=True)
    epl_facility_name = CharField(null=True)
    epl_further = DateField(null=True)
    epl_init = DateField(null=True)
    epl_own = CharField(null=True)
    epl_statute = CharField(null=True)
    epl_use = CharField(null=True)
    exempt = DoubleField(null=True)
    exemption_amt = IntegerField(null=True)
    exemption_code = CharField(null=True)
    id = UUIDField()
    is_redacted = BooleanField()
    land_assmnt = IntegerField(null=True)
    land_desc = CharField(null=True)
    last_year_tax = DoubleField(null=True)
    map_page = CharField(null=True)
    matching_method = ForeignKeyField(backref='lookup_table_matching_method_set', column_name='matching_method_id', field='id', model=LookupTable, null=True)
    multiple_occupancy = CharField(null=True)
    municipality = ForeignKeyField(column_name='municipality_id', field='id', model=Municipalities)
    no_of_commercial_dw = IntegerField(null=True)
    no_of_dwellings = IntegerField(null=True)
    nu_code = CharField(null=True)
    number_of_owners = IntegerField(null=True)
    old_property_id = CharField(null=True)
    owner_mail_address = ForeignKeyField(column_name='owner_mail_address_id', field='id', model=MailingAddresses, null=True)
    percent_owned_code = CharField(null=True)
    prior_gis_pin = CharField(null=True)
    property_class = CharField(null=True)
    property_flags = CharField(null=True)
    property = ForeignKeyField(column_name='property_id', field='id', model=Properties)
    property_location = ForeignKeyField(column_name='property_location_id', field='id', model=PropertyLocations, null=True)
    property_owner = ForeignKeyField(column_name='property_owner_id', field='id', model=PropertyOwners, null=True)
    property_use_code = CharField(null=True)
    rate_year = SmallIntegerField(null=True)
    ratio = DoubleField(null=True)
    ratio_year = SmallIntegerField(null=True)
    rebate_base_year = SmallIntegerField(null=True)
    rebate_base_year_net_val = IntegerField(null=True)
    rebate_base_year_tax = DoubleField(null=True)
    rebate_code = CharField(null=True)
    rebate_response_flg = CharField(null=True)
    record_id = CharField(null=True)
    sale_assessment = IntegerField(null=True)
    sale_date = DateField(null=True)
    sale_price = IntegerField(null=True)
    sale_sr1a_un_code = CharField(null=True)
    sales_price_code = CharField(null=True)
    senior_citizens_cnt = IntegerField(null=True)
    shard_num = SmallIntegerField()
    sp_tax_cd = CharField(null=True)
    sq_ft = IntegerField(null=True)
    surv_spouse_cnt = IntegerField(null=True)
    taxes = DoubleField(null=True)
    total_assmnt = IntegerField(null=True)
    updated = DateField(null=True)
    user_field_1 = CharField(null=True)
    user_field_2 = CharField(null=True)
    veterans_cnt = IntegerField(null=True)
    widows_cnt = IntegerField(null=True)
    yr_built = SmallIntegerField(null=True)

    class Meta:
        table_name = 'property_histories'
        schema = 'parcels'
        primary_key = CompositeKey('id', 'shard_num')

class PropertyHistories1(BaseModel):
    absentee = SmallIntegerField(null=True)
    acreage = DoubleField(null=True)
    addition_lots_2 = CharField(null=True)
    additional_lots = CharField(null=True)
    assessed = IntegerField(null=True)
    bank_code = CharField(null=True)
    building_assmnt = IntegerField(null=True)
    building_class = ForeignKeyField(column_name='building_class_id', field='id', model=LookupTable, null=True)
    calculated_taxes = DoubleField(null=True)
    calculated_taxes_year = SmallIntegerField(null=True)
    corporate_owned = BooleanField()
    data_year = SmallIntegerField()
    deduction_amount = IntegerField(null=True)
    deed_book = CharField(null=True)
    deed_page = CharField(null=True)
    delinquent_code = CharField(null=True)
    disabled_cnt = IntegerField(null=True)
    epl_desc = CharField(null=True)
    epl_facility_name = CharField(null=True)
    epl_further = DateField(null=True)
    epl_init = DateField(null=True)
    epl_own = CharField(null=True)
    epl_statute = CharField(null=True)
    epl_use = CharField(null=True)
    exempt = DoubleField(null=True)
    exemption_amt = IntegerField(null=True)
    exemption_code = CharField(null=True)
    id = UUIDField()
    is_redacted = BooleanField()
    land_assmnt = IntegerField(null=True)
    land_desc = CharField(null=True)
    last_year_tax = DoubleField(null=True)
    map_page = CharField(null=True)
    matching_method = ForeignKeyField(backref='lookup_table_matching_method_set', column_name='matching_method_id', field='id', model=LookupTable, null=True)
    multiple_occupancy = CharField(null=True)
    municipality = ForeignKeyField(column_name='municipality_id', field='id', model=Municipalities)
    no_of_commercial_dw = IntegerField(null=True)
    no_of_dwellings = IntegerField(null=True)
    nu_code = CharField(null=True)
    number_of_owners = IntegerField(null=True)
    old_property_id = CharField(null=True)
    owner_mail_address = ForeignKeyField(column_name='owner_mail_address_id', field='id', model=MailingAddresses, null=True)
    percent_owned_code = CharField(null=True)
    prior_gis_pin = CharField(null=True)
    property_class = CharField(null=True)
    property_flags = CharField(null=True)
    property = ForeignKeyField(column_name='property_id', field='id', model=Properties)
    property_location = ForeignKeyField(column_name='property_location_id', field='id', model=PropertyLocations, null=True)
    property_owner = ForeignKeyField(column_name='property_owner_id', field='id', model=PropertyOwners, null=True)
    property_use_code = CharField(null=True)
    rate_year = SmallIntegerField(null=True)
    ratio = DoubleField(null=True)
    ratio_year = SmallIntegerField(null=True)
    rebate_base_year = SmallIntegerField(null=True)
    rebate_base_year_net_val = IntegerField(null=True)
    rebate_base_year_tax = DoubleField(null=True)
    rebate_code = CharField(null=True)
    rebate_response_flg = CharField(null=True)
    record_id = CharField(null=True)
    sale_assessment = IntegerField(null=True)
    sale_date = DateField(null=True)
    sale_price = IntegerField(null=True)
    sale_sr1a_un_code = CharField(null=True)
    sales_price_code = CharField(null=True)
    senior_citizens_cnt = IntegerField(null=True)
    shard_num = SmallIntegerField()
    sp_tax_cd = CharField(null=True)
    sq_ft = IntegerField(null=True)
    surv_spouse_cnt = IntegerField(null=True)
    taxes = DoubleField(null=True)
    total_assmnt = IntegerField(null=True)
    updated = DateField(null=True)
    user_field_1 = CharField(null=True)
    user_field_2 = CharField(null=True)
    veterans_cnt = IntegerField(null=True)
    widows_cnt = IntegerField(null=True)
    yr_built = SmallIntegerField(null=True)

    class Meta:
        table_name = 'property_histories_1'
        indexes = (
            (('id', 'shard_num'), True),
            (('property', 'shard_num', 'data_year', 'deed_book', 'deed_page'), False),
        )
        schema = 'parcels'
        primary_key = CompositeKey('id', 'shard_num')

class PropertyHistories2(BaseModel):
    absentee = SmallIntegerField(null=True)
    acreage = DoubleField(null=True)
    addition_lots_2 = CharField(null=True)
    additional_lots = CharField(null=True)
    assessed = IntegerField(null=True)
    bank_code = CharField(null=True)
    building_assmnt = IntegerField(null=True)
    building_class = ForeignKeyField(column_name='building_class_id', field='id', model=LookupTable, null=True)
    calculated_taxes = DoubleField(null=True)
    calculated_taxes_year = SmallIntegerField(null=True)
    corporate_owned = BooleanField()
    data_year = SmallIntegerField()
    deduction_amount = IntegerField(null=True)
    deed_book = CharField(null=True)
    deed_page = CharField(null=True)
    delinquent_code = CharField(null=True)
    disabled_cnt = IntegerField(null=True)
    epl_desc = CharField(null=True)
    epl_facility_name = CharField(null=True)
    epl_further = DateField(null=True)
    epl_init = DateField(null=True)
    epl_own = CharField(null=True)
    epl_statute = CharField(null=True)
    epl_use = CharField(null=True)
    exempt = DoubleField(null=True)
    exemption_amt = IntegerField(null=True)
    exemption_code = CharField(null=True)
    id = UUIDField()
    is_redacted = BooleanField()
    land_assmnt = IntegerField(null=True)
    land_desc = CharField(null=True)
    last_year_tax = DoubleField(null=True)
    map_page = CharField(null=True)
    matching_method = ForeignKeyField(backref='lookup_table_matching_method_set', column_name='matching_method_id', field='id', model=LookupTable, null=True)
    multiple_occupancy = CharField(null=True)
    municipality = ForeignKeyField(column_name='municipality_id', field='id', model=Municipalities)
    no_of_commercial_dw = IntegerField(null=True)
    no_of_dwellings = IntegerField(null=True)
    nu_code = CharField(null=True)
    number_of_owners = IntegerField(null=True)
    old_property_id = CharField(null=True)
    owner_mail_address = ForeignKeyField(column_name='owner_mail_address_id', field='id', model=MailingAddresses, null=True)
    percent_owned_code = CharField(null=True)
    prior_gis_pin = CharField(null=True)
    property_class = CharField(null=True)
    property_flags = CharField(null=True)
    property = ForeignKeyField(column_name='property_id', field='id', model=Properties)
    property_location = ForeignKeyField(column_name='property_location_id', field='id', model=PropertyLocations, null=True)
    property_owner = ForeignKeyField(column_name='property_owner_id', field='id', model=PropertyOwners, null=True)
    property_use_code = CharField(null=True)
    rate_year = SmallIntegerField(null=True)
    ratio = DoubleField(null=True)
    ratio_year = SmallIntegerField(null=True)
    rebate_base_year = SmallIntegerField(null=True)
    rebate_base_year_net_val = IntegerField(null=True)
    rebate_base_year_tax = DoubleField(null=True)
    rebate_code = CharField(null=True)
    rebate_response_flg = CharField(null=True)
    record_id = CharField(null=True)
    sale_assessment = IntegerField(null=True)
    sale_date = DateField(null=True)
    sale_price = IntegerField(null=True)
    sale_sr1a_un_code = CharField(null=True)
    sales_price_code = CharField(null=True)
    senior_citizens_cnt = IntegerField(null=True)
    shard_num = SmallIntegerField()
    sp_tax_cd = CharField(null=True)
    sq_ft = IntegerField(null=True)
    surv_spouse_cnt = IntegerField(null=True)
    taxes = DoubleField(null=True)
    total_assmnt = IntegerField(null=True)
    updated = DateField(null=True)
    user_field_1 = CharField(null=True)
    user_field_2 = CharField(null=True)
    veterans_cnt = IntegerField(null=True)
    widows_cnt = IntegerField(null=True)
    yr_built = SmallIntegerField(null=True)

    class Meta:
        table_name = 'property_histories_2'
        indexes = (
            (('id', 'shard_num'), True),
            (('property', 'shard_num', 'data_year', 'deed_book', 'deed_page'), False),
        )
        schema = 'parcels'
        primary_key = CompositeKey('id', 'shard_num')

class PropertyHistories3(BaseModel):
    absentee = SmallIntegerField(null=True)
    acreage = DoubleField(null=True)
    addition_lots_2 = CharField(null=True)
    additional_lots = CharField(null=True)
    assessed = IntegerField(null=True)
    bank_code = CharField(null=True)
    building_assmnt = IntegerField(null=True)
    building_class = ForeignKeyField(column_name='building_class_id', field='id', model=LookupTable, null=True)
    calculated_taxes = DoubleField(null=True)
    calculated_taxes_year = SmallIntegerField(null=True)
    corporate_owned = BooleanField()
    data_year = SmallIntegerField()
    deduction_amount = IntegerField(null=True)
    deed_book = CharField(null=True)
    deed_page = CharField(null=True)
    delinquent_code = CharField(null=True)
    disabled_cnt = IntegerField(null=True)
    epl_desc = CharField(null=True)
    epl_facility_name = CharField(null=True)
    epl_further = DateField(null=True)
    epl_init = DateField(null=True)
    epl_own = CharField(null=True)
    epl_statute = CharField(null=True)
    epl_use = CharField(null=True)
    exempt = DoubleField(null=True)
    exemption_amt = IntegerField(null=True)
    exemption_code = CharField(null=True)
    id = UUIDField()
    is_redacted = BooleanField()
    land_assmnt = IntegerField(null=True)
    land_desc = CharField(null=True)
    last_year_tax = DoubleField(null=True)
    map_page = CharField(null=True)
    matching_method = ForeignKeyField(backref='lookup_table_matching_method_set', column_name='matching_method_id', field='id', model=LookupTable, null=True)
    multiple_occupancy = CharField(null=True)
    municipality = ForeignKeyField(column_name='municipality_id', field='id', model=Municipalities)
    no_of_commercial_dw = IntegerField(null=True)
    no_of_dwellings = IntegerField(null=True)
    nu_code = CharField(null=True)
    number_of_owners = IntegerField(null=True)
    old_property_id = CharField(null=True)
    owner_mail_address = ForeignKeyField(column_name='owner_mail_address_id', field='id', model=MailingAddresses, null=True)
    percent_owned_code = CharField(null=True)
    prior_gis_pin = CharField(null=True)
    property_class = CharField(null=True)
    property_flags = CharField(null=True)
    property = ForeignKeyField(column_name='property_id', field='id', model=Properties)
    property_location = ForeignKeyField(column_name='property_location_id', field='id', model=PropertyLocations, null=True)
    property_owner = ForeignKeyField(column_name='property_owner_id', field='id', model=PropertyOwners, null=True)
    property_use_code = CharField(null=True)
    rate_year = SmallIntegerField(null=True)
    ratio = DoubleField(null=True)
    ratio_year = SmallIntegerField(null=True)
    rebate_base_year = SmallIntegerField(null=True)
    rebate_base_year_net_val = IntegerField(null=True)
    rebate_base_year_tax = DoubleField(null=True)
    rebate_code = CharField(null=True)
    rebate_response_flg = CharField(null=True)
    record_id = CharField(null=True)
    sale_assessment = IntegerField(null=True)
    sale_date = DateField(null=True)
    sale_price = IntegerField(null=True)
    sale_sr1a_un_code = CharField(null=True)
    sales_price_code = CharField(null=True)
    senior_citizens_cnt = IntegerField(null=True)
    shard_num = SmallIntegerField()
    sp_tax_cd = CharField(null=True)
    sq_ft = IntegerField(null=True)
    surv_spouse_cnt = IntegerField(null=True)
    taxes = DoubleField(null=True)
    total_assmnt = IntegerField(null=True)
    updated = DateField(null=True)
    user_field_1 = CharField(null=True)
    user_field_2 = CharField(null=True)
    veterans_cnt = IntegerField(null=True)
    widows_cnt = IntegerField(null=True)
    yr_built = SmallIntegerField(null=True)

    class Meta:
        table_name = 'property_histories_3'
        indexes = (
            (('id', 'shard_num'), True),
            (('property', 'shard_num', 'data_year', 'deed_book', 'deed_page'), False),
        )
        schema = 'parcels'
        primary_key = CompositeKey('id', 'shard_num')

class PropertyHistories4(BaseModel):
    absentee = SmallIntegerField(null=True)
    acreage = DoubleField(null=True)
    addition_lots_2 = CharField(null=True)
    additional_lots = CharField(null=True)
    assessed = IntegerField(null=True)
    bank_code = CharField(null=True)
    building_assmnt = IntegerField(null=True)
    building_class = ForeignKeyField(column_name='building_class_id', field='id', model=LookupTable, null=True)
    calculated_taxes = DoubleField(null=True)
    calculated_taxes_year = SmallIntegerField(null=True)
    corporate_owned = BooleanField()
    data_year = SmallIntegerField()
    deduction_amount = IntegerField(null=True)
    deed_book = CharField(null=True)
    deed_page = CharField(null=True)
    delinquent_code = CharField(null=True)
    disabled_cnt = IntegerField(null=True)
    epl_desc = CharField(null=True)
    epl_facility_name = CharField(null=True)
    epl_further = DateField(null=True)
    epl_init = DateField(null=True)
    epl_own = CharField(null=True)
    epl_statute = CharField(null=True)
    epl_use = CharField(null=True)
    exempt = DoubleField(null=True)
    exemption_amt = IntegerField(null=True)
    exemption_code = CharField(null=True)
    id = UUIDField()
    is_redacted = BooleanField()
    land_assmnt = IntegerField(null=True)
    land_desc = CharField(null=True)
    last_year_tax = DoubleField(null=True)
    map_page = CharField(null=True)
    matching_method = ForeignKeyField(backref='lookup_table_matching_method_set', column_name='matching_method_id', field='id', model=LookupTable, null=True)
    multiple_occupancy = CharField(null=True)
    municipality = ForeignKeyField(column_name='municipality_id', field='id', model=Municipalities)
    no_of_commercial_dw = IntegerField(null=True)
    no_of_dwellings = IntegerField(null=True)
    nu_code = CharField(null=True)
    number_of_owners = IntegerField(null=True)
    old_property_id = CharField(null=True)
    owner_mail_address = ForeignKeyField(column_name='owner_mail_address_id', field='id', model=MailingAddresses, null=True)
    percent_owned_code = CharField(null=True)
    prior_gis_pin = CharField(null=True)
    property_class = CharField(null=True)
    property_flags = CharField(null=True)
    property = ForeignKeyField(column_name='property_id', field='id', model=Properties)
    property_location = ForeignKeyField(column_name='property_location_id', field='id', model=PropertyLocations, null=True)
    property_owner = ForeignKeyField(column_name='property_owner_id', field='id', model=PropertyOwners, null=True)
    property_use_code = CharField(null=True)
    rate_year = SmallIntegerField(null=True)
    ratio = DoubleField(null=True)
    ratio_year = SmallIntegerField(null=True)
    rebate_base_year = SmallIntegerField(null=True)
    rebate_base_year_net_val = IntegerField(null=True)
    rebate_base_year_tax = DoubleField(null=True)
    rebate_code = CharField(null=True)
    rebate_response_flg = CharField(null=True)
    record_id = CharField(null=True)
    sale_assessment = IntegerField(null=True)
    sale_date = DateField(null=True)
    sale_price = IntegerField(null=True)
    sale_sr1a_un_code = CharField(null=True)
    sales_price_code = CharField(null=True)
    senior_citizens_cnt = IntegerField(null=True)
    shard_num = SmallIntegerField()
    sp_tax_cd = CharField(null=True)
    sq_ft = IntegerField(null=True)
    surv_spouse_cnt = IntegerField(null=True)
    taxes = DoubleField(null=True)
    total_assmnt = IntegerField(null=True)
    updated = DateField(null=True)
    user_field_1 = CharField(null=True)
    user_field_2 = CharField(null=True)
    veterans_cnt = IntegerField(null=True)
    widows_cnt = IntegerField(null=True)
    yr_built = SmallIntegerField(null=True)

    class Meta:
        table_name = 'property_histories_4'
        indexes = (
            (('id', 'shard_num'), True),
            (('property', 'shard_num', 'data_year', 'deed_book', 'deed_page'), False),
        )
        schema = 'parcels'
        primary_key = CompositeKey('id', 'shard_num')

class PropertyMortgages(BaseModel):
    adjustable_rate_index = CharField(null=True)
    adjustable_rate_rider = BooleanField(null=True)
    assessors_land_use = CharField(null=True)
    assessors_parcel_number = CharField(null=True)
    borrower1_code = ForeignKeyField(column_name='borrower1_code_id', field='id', model=LookupTable, null=True)
    borrower1 = ForeignKeyField(column_name='borrower1_id', field='id', model=MortgageBorrowers, null=True)
    borrower2_code = ForeignKeyField(backref='lookup_table_borrower2_code_set', column_name='borrower2_code_id', field='id', model=LookupTable, null=True)
    borrower2 = ForeignKeyField(backref='mortgage_borrowers_borrower2_set', column_name='borrower2_id', field='id', model=MortgageBorrowers, null=True)
    borrower_address = CharField(null=True)
    borrower_city = CharField(null=True)
    borrower_mail_unit_number = CharField(null=True)
    borrower_state = CharField(null=True)
    borrower_vesting_code = ForeignKeyField(backref='lookup_table_borrower_vesting_code_set', column_name='borrower_vesting_code_id', field='id', model=LookupTable, null=True)
    borrower_zip = CharField(null=True)
    borrower_zip4 = CharField(null=True)
    buyer_mail_full_street_address = CharField(null=True)
    cash_purchase = BooleanField()
    change_index = CharField(null=True)
    construction_loan = BooleanField()
    created_at = DateTimeField()
    display_id = IntegerField(null=True)
    document_path = CharField(null=True)
    due_date = DateField(null=True)
    equity_credit_line = BooleanField()
    fips_code = CharField(null=True)
    first_change_date_month_day_conversion_rider = CharField(null=True)
    first_change_date_year_conversion_rider = CharField(null=True)
    fixedstep_conversion_rate_rider = CharField(null=True)
    gis_pin = CharField(null=True)
    instrument_book = CharField(null=True)
    instrument_date = DateField(null=True)
    instrument_number = CharField(null=True)
    instrument_page = CharField(null=True)
    interest_only_period = CharField(null=True)
    interest_rate = DoubleField(null=True)
    interest_rate_not_greater_than = DoubleField(null=True)
    interest_rate_not_less_than = DoubleField(null=True)
    legal_block = CharField(null=True)
    legal_brief_description = CharField(null=True)
    legal_city_township_municipality = CharField(null=True)
    legal_land_lot = CharField(null=True)
    legal_lot_number = CharField(null=True)
    legal_municipality = CharField(null=True)
    legal_phase_number = CharField(null=True)
    legal_section = CharField(null=True)
    legal_sectiontownship_rangemeridian = CharField(null=True)
    legal_subdivision = CharField(null=True)
    legal_tract_number = CharField(null=True)
    legal_unit = CharField(null=True)
    lender = ForeignKeyField(column_name='lender_id', field='id', model=MortgageLenders, null=True)
    loan_amount = IntegerField(null=True)
    loan_financing_type = ForeignKeyField(backref='lookup_table_loan_financing_type_set', column_name='loan_financing_type_id', field='id', model=LookupTable, null=True)
    loan_term_months = IntegerField(null=True)
    loan_term_years = IntegerField(null=True)
    loan_type = ForeignKeyField(backref='lookup_table_loan_type_set', column_name='loan_type_id', field='id', model=LookupTable, null=True)
    maximum_interest_rate = DoubleField(null=True)
    original_date_of_contract = DateField(null=True)
    prepayment_rider = CharField(null=True)
    prepayment_term_penalty_rider = CharField(null=True)
    property_address = ForeignKeyField(column_name='property_address_id', field='id', model=MailingAddresses, null=True)
    property = ForeignKeyField(column_name='property_id', field='id', model=Properties)
    property_identifier = CharField(null=True)
    property_unit_type = CharField(null=True)
    purchase_money_mortgage = CharField(null=True)
    rate_change_frequency = CharField(null=True)
    record_type = ForeignKeyField(backref='lookup_table_record_type_set', column_name='record_type_id', field='id', model=LookupTable, null=True)
    recorders_book_number = CharField(null=True)
    recorders_document_number = CharField(null=True)
    recorders_page_number = CharField(null=True)
    recording_date = DateField(null=True)
    residential_indicator = BooleanField()
    source = CharField(null=True)
    standalone_refi = BooleanField()
    title_company_name = CharField(null=True)
    transaction_id = CharField(null=True)
    unique_link_id = CharField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        table_name = 'property_mortgages'
        schema = 'parcels'

class PropertyParcelNumbers(BaseModel):
    parcel_number = CharField()
    property = ForeignKeyField(column_name='property_id', field='id', model=Properties)

    class Meta:
        table_name = 'property_parcel_numbers'
        indexes = (
            (('property', 'parcel_number'), False),
            (('property', 'parcel_number'), True),
        )
        schema = 'parcels'

class PropertyParcels(BaseModel):
    acres = DoubleField(null=True)
    geo_location = UnknownField(index=True, null=True)  # USER-DEFINED
    geoms = UnknownField(index=True, null=True)  # USER-DEFINED
    pams_pin = CharField(null=True)
    perimeter = DoubleField(null=True)
    property = ForeignKeyField(column_name='property_id', field='id', model=Properties, primary_key=True)
    sq_ft = DoubleField(null=True)

    class Meta:
        table_name = 'property_parcels'
        schema = 'parcels'

class PropertyQuickFacts(BaseModel):
    acreage = DoubleField(null=True)
    county_id = IntegerField()
    county_name = CharField()
    deed_book = CharField(null=True)
    deed_page = CharField(null=True)
    gis_pin = CharField()
    id = IntegerField(constraints=[SQL("DEFAULT nextval('parcels.property_quick_facts_id_seq'::regclass)")])
    improvement_value = IntegerField(null=True)
    land_value = IntegerField(null=True)
    lat = DoubleField(null=True)
    lng = DoubleField(null=True)
    municipality_id = IntegerField()
    municipality_name = CharField()
    net_value = IntegerField(null=True)
    owner_address = CharField(null=True)
    owner_city = CharField(null=True)
    owner_id = IntegerField(null=True)
    owner_name = CharField(null=True)
    owner_zip = CharField(null=True)
    property_class = CharField(null=True)
    property_id = IntegerField()
    property_location = CharField(null=True)
    sale_date = DateField(null=True)
    sale_price = IntegerField(null=True)
    sq_ft = IntegerField(null=True)

    class Meta:
        table_name = 'property_quick_facts'
        schema = 'parcels'
        primary_key = False

class PropertyRecordCards(BaseModel):
    account_number = CharField(null=True)
    acres = DoubleField(null=True)
    addtl_lots = CharField(null=True)
    air_cond = CharField(null=True)
    assesment_year = SmallIntegerField(null=True)
    attic_area_sqft = IntegerField(null=True)
    attic_finish_sqft = IntegerField(null=True)
    basement = CharField(null=True)
    basement_area_sqft = IntegerField(null=True)
    basement_finish_sqft = IntegerField(null=True)
    basement_unfinished_sqft = IntegerField(null=True)
    bath = DoubleField(null=True)
    bath_1 = SmallIntegerField(null=True)
    bath_2 = SmallIntegerField(null=True)
    bath_3 = SmallIntegerField(null=True)
    bath_4 = SmallIntegerField(null=True)
    bath_b = SmallIntegerField(null=True)
    bath_t = SmallIntegerField(null=True)
    bed = SmallIntegerField(null=True)
    bed_1 = SmallIntegerField(null=True)
    bed_2 = SmallIntegerField(null=True)
    bed_3 = SmallIntegerField(null=True)
    bed_4 = SmallIntegerField(null=True)
    bed_b = SmallIntegerField(null=True)
    bed_t = SmallIntegerField(null=True)
    bldg_desc = CharField(null=True)
    bldg_name = CharField(null=True)
    bldg_quality_class = CharField(null=True)
    builtin_sqft = IntegerField(null=True)
    den_1 = SmallIntegerField(null=True)
    den_2 = SmallIntegerField(null=True)
    den_3 = SmallIntegerField(null=True)
    den_4 = SmallIntegerField(null=True)
    den_b = SmallIntegerField(null=True)
    den_t = SmallIntegerField(null=True)
    dining_1 = SmallIntegerField(null=True)
    dining_2 = SmallIntegerField(null=True)
    dining_3 = SmallIntegerField(null=True)
    dining_4 = SmallIntegerField(null=True)
    dining_b = SmallIntegerField(null=True)
    dining_t = SmallIntegerField(null=True)
    eff_age = SmallIntegerField(null=True)
    exterior_condition = CharField(null=True)
    exterior_finish = CharField(null=True)
    fireplace = CharField(null=True)
    first_floor_sqft = IntegerField(null=True)
    floor = CharField(null=True)
    floor_finish = CharField(null=True)
    foundation = CharField(null=True)
    front_feet = IntegerField(null=True)
    gas = CharField(null=True)
    half_stories_sqft = IntegerField(null=True)
    heat_src = CharField(null=True)
    heat_sys = CharField(null=True)
    height = CharField(null=True)
    info_by = CharField(null=True)
    interior_condition = CharField(null=True)
    interior_finish = CharField(null=True)
    kitchen_1 = SmallIntegerField(null=True)
    kitchen_2 = SmallIntegerField(null=True)
    kitchen_3 = SmallIntegerField(null=True)
    kitchen_4 = SmallIntegerField(null=True)
    kitchen_b = SmallIntegerField(null=True)
    kitchen_t = SmallIntegerField(null=True)
    land_desc = CharField(null=True)
    layout_condition = CharField(null=True)
    living_1 = SmallIntegerField(null=True)
    living_2 = SmallIntegerField(null=True)
    living_3 = SmallIntegerField(null=True)
    living_4 = SmallIntegerField(null=True)
    living_b = SmallIntegerField(null=True)
    living_sqft = IntegerField(null=True)
    living_t = SmallIntegerField(null=True)
    map_page = SmallIntegerField(null=True)
    model = CharField(null=True)
    nbhd = CharField(null=True)
    occupancy = CharField(null=True)
    plumbing = CharField(null=True)
    processed = DateTimeField(null=True)
    prop_class = CharField(null=True)
    property = ForeignKeyField(column_name='property_id', field='id', model=Properties)
    rec_1 = SmallIntegerField(null=True)
    rec_2 = SmallIntegerField(null=True)
    rec_3 = SmallIntegerField(null=True)
    rec_4 = SmallIntegerField(null=True)
    rec_b = SmallIntegerField(null=True)
    rec_t = SmallIntegerField(null=True)
    road = CharField(null=True)
    roof_material = CharField(null=True)
    roof_type = CharField(null=True)
    sewer = CharField(null=True)
    sfla = IntegerField(null=True)
    site_value = IntegerField(null=True)
    source = CharField(null=True)
    style = CharField(null=True)
    topography = CharField(null=True)
    total_rooms = SmallIntegerField(null=True)
    total_rooms_1 = SmallIntegerField(null=True)
    total_rooms_2 = SmallIntegerField(null=True)
    total_rooms_3 = SmallIntegerField(null=True)
    total_rooms_4 = SmallIntegerField(null=True)
    total_rooms_b = SmallIntegerField(null=True)
    total_rooms_t = SmallIntegerField(null=True)
    type_use = CharField(null=True)
    units = SmallIntegerField(null=True)
    upper_stories_sqft = IntegerField(null=True)
    vcs = CharField(null=True)
    water = CharField(null=True)
    year_built = SmallIntegerField(null=True)
    zoning = CharField(null=True)

    class Meta:
        table_name = 'property_record_cards'
        schema = 'parcels'

class PropertyResidents(BaseModel):
    is_owner = BooleanField()
    name = CharField()
    normalized_name = CharField(index=True)
    property = ForeignKeyField(column_name='property_id', field='id', model=Properties)

    class Meta:
        table_name = 'property_residents'
        schema = 'parcels'

class PropertyTaxClassifications(BaseModel):
    category = CharField(null=True)
    description = CharField(null=True)
    name = CharField()
    property_class = CharField(unique=True)

    class Meta:
        table_name = 'property_tax_classifications'
        schema = 'parcels'

class PropertyTaxes(BaseModel):
    amount = DoubleField(null=True)
    created_at = DateTimeField()
    improved = IntegerField(null=True)
    land = IntegerField(null=True)
    municipality = ForeignKeyField(column_name='municipality_id', field='id', model=Municipalities)
    property = ForeignKeyField(column_name='property_id', field='id', model=Properties)
    total = IntegerField(null=True)
    updated_at = DateTimeField(null=True)
    year = SmallIntegerField()

    class Meta:
        table_name = 'property_taxes'
        indexes = (
            (('property', 'year'), False),
            (('property', 'year'), True),
        )
        schema = 'parcels'

class RegisteredVoters(BaseModel):
    block = ForeignKeyField(column_name='block_id', field='id', model=MunicipalityBlocks)
    city = CharField(null=True)
    congressional = IntegerField(null=True)
    county = ForeignKeyField(column_name='county_id', field='id', model=Counties)
    district = CharField(null=True)
    dob = DateField(null=True)
    fire = IntegerField(null=True)
    first_name = CharField(index=True)
    freeholder = IntegerField(null=True)
    last_name = CharField(index=True)
    leg_id = CharField(null=True)
    legislative = IntegerField(null=True)
    location = CharField(null=True)
    municipality = ForeignKeyField(column_name='municipality_id', field='id', model=Municipalities)
    party = CharField(null=True)
    reg_date = DateField(null=True)
    school = BooleanField(null=True)
    status = CharField(null=True)
    suffix = CharField(null=True)
    voter_registration_id = CharField(unique=True)
    ward = CharField(null=True)
    zip = CharField(null=True)

    class Meta:
        table_name = 'registered_voters'
        schema = 'parcels'

class PropertyVoterLinks(BaseModel):
    property = ForeignKeyField(column_name='property_id', field='id', model=Properties)
    voter = ForeignKeyField(column_name='voter_id', field='id', model=RegisteredVoters)

    class Meta:
        table_name = 'property_voter_links'
        indexes = (
            (('property', 'voter'), True),
        )
        schema = 'parcels'
        primary_key = CompositeKey('property', 'voter')

class RelatedProperties(BaseModel):
    main_property = ForeignKeyField(column_name='main_property_id', field='id', model=Properties)
    related_property = ForeignKeyField(backref='properties_related_property_set', column_name='related_property_id', field='id', model=Properties)

    class Meta:
        table_name = 'related_properties'
        schema = 'parcels'

class Schools(BaseModel):
    city = CharField(null=True)
    county = CharField(null=True)
    county_id = ForeignKeyField(column_name='county_id', field='id', model=Counties, null=True)
    district_id = IntegerField(null=True)
    district_name = CharField(null=True)
    fax = CharField(null=True)
    fipscounty = CharField(null=True)
    geo_location = UnknownField(index=True, null=True)  # USER-DEFINED
    level = CharField(null=True)
    level_codes = CharField(null=True)
    municipality = ForeignKeyField(column_name='municipality_id', field='id', model=Municipalities, null=True)
    name = CharField(null=True)
    nces_id = CharField(null=True)
    overview_url = CharField(null=True)
    phone = CharField(null=True)
    rating = CharField(null=True)
    school_summary = CharField(null=True)
    state = CharField(null=True)
    state_id = CharField(null=True)
    street = CharField(null=True)
    type = CharField(null=True)
    universal_id = CharField(unique=True)
    web_site = CharField(null=True)
    year = IntegerField(null=True)
    zip = CharField(null=True)

    class Meta:
        table_name = 'schools'
        schema = 'parcels'

class SchoolBlockLinks(BaseModel):
    block = ForeignKeyField(column_name='block_id', field='id', model=MunicipalityBlocks)
    school = ForeignKeyField(column_name='school_id', field='id', model=Schools)

    class Meta:
        table_name = 'school_block_links'
        indexes = (
            (('school', 'block'), True),
        )
        schema = 'parcels'
        primary_key = CompositeKey('block', 'school')

class Streets(BaseModel):
    avg_lot_size = IntegerField(null=True)
    avg_property_value = IntegerField(null=True)
    city = ForeignKeyField(column_name='city_id', field='id', model=Cities)
    county = ForeignKeyField(column_name='county_id', field='id', model=Counties)
    municipality = ForeignKeyField(column_name='municipality_id', field='id', model=Municipalities, null=True)
    name = CharField()
    normalized_name = CharField(unique=True)
    num_properties = IntegerField(null=True)

    class Meta:
        table_name = 'streets'
        indexes = (
            (('city', 'normalized_name'), False),
            (('city', 'normalized_name'), True),
        )
        schema = 'parcels'

class TaxationBoards(BaseModel):
    address = CharField(null=True)
    county = ForeignKeyField(column_name='county_id', field='id', model=Counties)
    county_name = CharField()
    created_at = DateTimeField()
    email = CharField(null=True)
    entity_type = CharField(index=True)
    fax = CharField(null=True)
    last_updated = DateTimeField()
    municipality = ForeignKeyField(column_name='municipality_id', field='id', model=Municipalities, null=True)
    municipality_name = CharField(null=True)
    name = CharField(null=True)
    phone = CharField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        table_name = 'taxation_boards'
        schema = 'parcels'

class VotingHistories(BaseModel):
    did_vote = BooleanField()
    election_date = DateField(null=True)
    election = ForeignKeyField(column_name='election_id', field='id', model=Elections)
    voter = ForeignKeyField(column_name='voter_id', field='id', model=RegisteredVoters)

    class Meta:
        table_name = 'voting_histories'
        indexes = (
            (('voter', 'election_date'), False),
        )
        schema = 'parcels'

class VwPropertyLocationOwners(BaseModel):
    acreage = DoubleField(null=True)
    county_id = IntegerField(null=True)
    county_name = CharField(null=True)
    gis_pin = CharField(null=True)
    lat = DoubleField(null=True)
    lng = DoubleField(null=True)
    municipality_id = IntegerField(null=True)
    municipality_name = CharField(null=True)
    owner_city_state_zip = CharField(null=True)
    owner_id = IntegerField(null=True)
    owner_name = CharField(null=True)
    owner_normalized_name = CharField(null=True)
    owner_redacted = BooleanField(null=True)
    owner_street_address = CharField(null=True)
    property_city_state_zip = CharField(null=True)
    property_class_code = CharField(null=True)
    property_class_name = CharField(null=True)
    property_id = IntegerField(null=True)
    property_location = CharField(null=True)
    property_location_normalized = CharField(null=True)
    sale_date = DateField(null=True)
    sale_price = IntegerField(null=True)
    sq_ft = IntegerField(null=True)

    class Meta:
        table_name = 'vw_property_location_owners'
        schema = 'parcels'
        primary_key = False

class VwPropertyParcelNumbers(BaseModel):
    acreage = DoubleField(null=True)
    county_id = IntegerField(null=True)
    county_name = CharField(null=True)
    gis_pin = CharField(null=True)
    lat = DoubleField(null=True)
    lng = DoubleField(null=True)
    municipality_id = IntegerField(null=True)
    municipality_name = CharField(null=True)
    parcel_number = CharField(null=True)
    property_id = IntegerField(null=True)
    property_location = CharField(null=True)
    sale_date = DateField(null=True)
    sale_price = IntegerField(null=True)
    sq_ft = IntegerField(null=True)

    class Meta:
        table_name = 'vw_property_parcel_numbers'
        schema = 'parcels'
        primary_key = False

class VwPropertyResidents(BaseModel):
    county_id = IntegerField(null=True)
    county_name = CharField(null=True)
    gis_pin = CharField(null=True)
    municipality_id = IntegerField(null=True)
    municipality_name = CharField(null=True)
    property_id = IntegerField(null=True)
    property_location = CharField(null=True)
    property_location_normalized = CharField(null=True)
    resident_is_owner = BooleanField(null=True)
    resident_name = CharField(null=True)
    resident_normalized_name = CharField(null=True)
    sale_date = DateField(null=True)
    sale_price = IntegerField(null=True)
    sq_ft = IntegerField(null=True)

    class Meta:
        table_name = 'vw_property_residents'
        schema = 'parcels'
        primary_key = False

class VwPropertyTaxHistory(BaseModel):
    amount = DoubleField(null=True)
    effective_tax_rate = DoubleField(null=True)
    general_tax_rate = DoubleField(null=True)
    improved = IntegerField(null=True)
    land = IntegerField(null=True)
    property_id = IntegerField(null=True)
    ratio = DoubleField(null=True)
    total = IntegerField(null=True)
    year = SmallIntegerField(null=True)

    class Meta:
        table_name = 'vw_property_tax_history'
        schema = 'parcels'
        primary_key = False

class Walkabilities(BaseModel):
    bike_score = SmallIntegerField(null=True)
    block = ForeignKeyField(column_name='block_id', field='id', model=MunicipalityBlocks, unique=True)
    transit_score = SmallIntegerField(null=True)
    walk_score = SmallIntegerField(null=True)

    class Meta:
        table_name = 'walkabilities'
        schema = 'parcels'

