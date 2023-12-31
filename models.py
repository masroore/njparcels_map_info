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
    avg_residential_tax = DoubleField(null=True)
    avg_tax_assessment = DoubleField(null=True)
    clerk_address = CharField(null=True)
    clerk_city_state_zip = CharField(null=True)
    clerk_fax = CharField(null=True)
    clerk_name = CharField(null=True)
    clerk_phone = CharField(null=True)
    clerk_website = CharField(null=True)
    code = CharField(unique=True)
    created_at = DateTimeField()
    effective_tax_rate = DoubleField(null=True)
    median_home_value = IntegerField(null=True)
    median_income = IntegerField(null=True)
    median_real_estate_taxes_paid = IntegerField(null=True)
    name = CharField()
    normalized_name = CharField(unique=True)
    num_properties_tax_assess = IntegerField(null=True)
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

class CitizensPropertyTaxSummaries(BaseModel):
    avg_county_taxes = DoubleField(null=True)
    avg_municipal_taxes = DoubleField(null=True)
    avg_residential_property_value = DoubleField(null=True)
    avg_school_taxes = DoubleField(null=True)
    avg_total_taxes = DoubleField(null=True)
    county_id = IntegerField(index=True)
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
    municipality_code = CharField()
    municipality_id = IntegerField(unique=True)
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
    municipality_id = IntegerField(index=True)

    class Meta:
        table_name = 'municipality_blocks'
        indexes = (
            (('municipality_id', 'block'), False),
            (('municipality_id', 'block'), True),
        )
        schema = 'parcels'

class ContaminatedSites(BaseModel):
    address = CharField(null=True)
    category = CharField(null=True)
    comu_code = CharField(null=True)
    county_id = IntegerField(index=True)
    fingerprint = BigIntegerField(unique=True)
    geo_location = UnknownField(index=True, null=True)  # USER-DEFINED
    municipality_id = IntegerField(index=True)
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
    county_id = IntegerField()
    created_at = DateTimeField()
    property_class = CharField()
    tax_rate = DoubleField()
    tax_year = IntegerField()
    updated_at = DateTimeField(null=True)

    class Meta:
        table_name = 'county_annual_property_tax_rates'
        indexes = (
            (('county_id', 'tax_year'), True),
        )
        schema = 'parcels'

class CountyTaxBreakdowns(BaseModel):
    county_id = IntegerField()
    created_at = DateTimeField()
    tax_heading = CharField()
    tax_rate = DoubleField()
    updated_at = DateTimeField(null=True)

    class Meta:
        table_name = 'county_tax_breakdowns'
        indexes = (
            (('county_id', 'tax_heading'), True),
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
    mail_error_code_id = IntegerField(null=True)
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

class DemographicStatistics(BaseModel):
    demographics_id = IntegerField(index=True)
    name = CharField()
    stats_type = CharField()
    value = DoubleField()

    class Meta:
        table_name = 'demographic_statistics'
        schema = 'parcels'

class Demographics(BaseModel):
    average_age = DoubleField(null=True)
    average_household_income = IntegerField(null=True)
    average_household_size = DoubleField(null=True)
    children_percentage = DoubleField(null=True)
    education_percentage = DoubleField(null=True)
    employment_percentage = DoubleField(null=True)
    municipality_id = IntegerField(unique=True)

    class Meta:
        table_name = 'demographics'
        schema = 'parcels'

class Elections(BaseModel):
    name = CharField()
    slug = CharField(unique=True)

    class Meta:
        table_name = 'elections'
        schema = 'parcels'

class FipsCensusCodes(BaseModel):
    block = CharField()
    block_code = CharField(unique=True)
    county_code = CharField()
    county_id = IntegerField(index=True, null=True)
    county_name = CharField()
    municipality_id = IntegerField(index=True, null=True)
    state_code = CharField()
    tract = CharField()
    tract_code = CharField()
    tract_name = CharField()

    class Meta:
        table_name = 'fips_census_codes'
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

class MailingAddresses(BaseModel):
    address = CharField(null=True)
    address_carrier_route = CharField(null=True)
    city = CharField(null=True)
    cmra = CharField(null=True)
    company = CharField(null=True)
    corrections = CharField(null=True)
    crrt = CharField(null=True)
    deliverable = CharField(null=True)
    discriminator = CharField()
    dpv = CharField(null=True)
    dpv_notes = CharField(null=True)
    error_code_id = IntegerField(null=True)
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
    city = CharField(null=True)
    fingerprint = BigIntegerField(unique=True)
    fname_mname = CharField(null=True)
    full_name = CharField()
    lname_or_corpname = CharField(null=True)
    mail_unit_number = CharField(null=True)
    state = CharField(null=True)
    street_address = CharField(null=True)
    zip = CharField(null=True)
    zip4 = CharField(null=True)

    class Meta:
        table_name = 'mortgage_borrowers'
        schema = 'parcels'

class MortgageLenders(BaseModel):
    dba_name = CharField(null=True)
    fingerprint = BigIntegerField(unique=True)
    lender_type = CharField(null=True)
    lender_type_description = CharField(null=True)
    mailing_address_id = IntegerField(null=True)
    name = CharField(index=True)
    zip = CharField(null=True)
    zip4 = CharField(null=True)

    class Meta:
        table_name = 'mortgage_lenders'
        schema = 'parcels'

class Municipalities(BaseModel):
    agg_assessed_value = DoubleField(null=True)
    agg_true_value = DoubleField(null=True)
    appeal_avg_ratio = DoubleField(null=True)
    appeal_lower_limit = DoubleField(null=True)
    appeal_upper_limit = DoubleField(null=True)
    assessed_value_personal = DoubleField(null=True)
    assessor_email = CharField(null=True)
    assessor_name = CharField(null=True)
    assessor_phone = CharField(null=True)
    assessor_website = CharField(null=True)
    avg_ratio_assessed_true_val = DoubleField(null=True)
    avg_residential_tax = DoubleField(null=True)
    avg_sales_price = DoubleField(null=True)
    avg_tax_assessment = DoubleField(null=True)
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
    num_properties_tax_assess = IntegerField(null=True)
    num_sales = IntegerField(null=True)
    opra_method = CharField(null=True)
    opra_url = CharField(null=True)
    shard_num = IntegerField()
    total_sales_price = DoubleField(null=True)
    updated_at = DateTimeField(null=True)
    website = CharField(null=True)
    zip_code = CharField(null=True)
    zone_map_date = CharField(null=True)
    zone_map_url = CharField(null=True)

    class Meta:
        table_name = 'municipalities'
        schema = 'parcels'

class MunicipalityBlockAvgSalesPrices(BaseModel):
    block_id = IntegerField()
    data_quarter = SmallIntegerField(null=True)
    data_year = SmallIntegerField(null=True)
    sales_price = DoubleField()

    class Meta:
        table_name = 'municipality_block_avg_sales_prices'
        indexes = (
            (('block_id', 'data_year', 'data_quarter'), True),
        )
        schema = 'parcels'

class MunicipalityPropertyTaxSummaries(BaseModel):
    avg_residential_property_value = DoubleField(null=True)
    avg_total_property_taxes = DoubleField(null=True)
    county_health_services_taxes = DoubleField(null=True)
    county_id = IntegerField(index=True)
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
    municipality_id = IntegerField(unique=True)
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
    municipality_id = IntegerField(index=True)
    sheet = CharField()
    status = IntegerField(null=True)
    top_left = UnknownField(index=True, null=True)  # USER-DEFINED
    top_right = UnknownField(index=True, null=True)  # USER-DEFINED
    width = IntegerField(null=True)
    year = IntegerField()

    class Meta:
        table_name = 'municipality_tax_maps'
        indexes = (
            (('municipality_id', 'year', 'sheet'), False),
            (('municipality_id', 'year', 'sheet'), True),
        )
        schema = 'parcels'

class MunicipalityTaxRates(BaseModel):
    created_at = DateTimeField()
    effective_tax_rate = DoubleField(null=True)
    general_tax_rate = DoubleField(null=True)
    municipality_id = IntegerField(index=True)
    ratio = DoubleField(null=True)
    tax_year = IntegerField()
    updated_at = DateTimeField(null=True)

    class Meta:
        table_name = 'municipality_tax_rates'
        indexes = (
            (('municipality_id', 'tax_year'), False),
            (('municipality_id', 'tax_year'), True),
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
    municipality_id = IntegerField(index=True)
    sheet = CharField()
    status = IntegerField(null=True)
    top_left = UnknownField(index=True, null=True)  # USER-DEFINED
    top_right = UnknownField(index=True, null=True)  # USER-DEFINED
    width = IntegerField(null=True)

    class Meta:
        table_name = 'municipality_zoning_maps'
        indexes = (
            (('municipality_id', 'sheet'), False),
            (('municipality_id', 'sheet'), True),
        )
        schema = 'parcels'

class NearbyProperties(BaseModel):
    main_property_id = IntegerField(index=True)
    nearby_property_id = IntegerField()

    class Meta:
        table_name = 'nearby_properties'
        indexes = (
            (('main_property_id', 'nearby_property_id'), True),
        )
        schema = 'parcels'

class NonusableDeedCategories(BaseModel):
    code = CharField(unique=True)
    description = CharField()

    class Meta:
        table_name = 'nonusable_deed_categories'
        schema = 'parcels'

class Properties(BaseModel):
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
    geo_location = UnknownField(index=True, null=True)  # USER-DEFINED
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
    parcel_centroid = UnknownField(index=True, null=True)  # USER-DEFINED
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
    rooftop = UnknownField(index=True, null=True)  # USER-DEFINED
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
        table_name = 'properties'
        indexes = (
            (('gis_pin', 'partial_record'), False),
        )
        schema = 'parcels'

class PropertyAreas(BaseModel):
    area = IntegerField(null=True)
    attic = IntegerField(null=True)
    bsmnt = IntegerField(null=True)
    discriminator = CharField()
    first_floor = IntegerField(null=True)
    half_story = IntegerField(null=True)
    name = CharField()
    property_id = IntegerField(index=True)
    segment = CharField(null=True)
    uppr_floor = IntegerField(null=True)

    class Meta:
        table_name = 'property_areas'
        schema = 'parcels'

class PropertyAssociatedPartyLinks(BaseModel):
    associated_party_id = IntegerField()
    property_id = IntegerField()

    class Meta:
        table_name = 'property_associated_party_links'
        indexes = (
            (('property_id', 'associated_party_id'), True),
        )
        schema = 'parcels'
        primary_key = CompositeKey('associated_party_id', 'property_id')

class PropertyBroadbandProviderLinks(BaseModel):
    block_code = CharField(null=True)
    broadband_provider_id = IntegerField()
    log_rec_no = CharField(null=True)
    max_ad_down = DoubleField(null=True)
    max_ad_up = DoubleField(null=True)
    property_id = IntegerField()
    tech_code = CharField(null=True)

    class Meta:
        table_name = 'property_broadband_provider_links'
        indexes = (
            (('property_id', 'broadband_provider_id'), True),
        )
        schema = 'parcels'
        primary_key = CompositeKey('broadband_provider_id', 'property_id')

class PropertyConstructionPermits(BaseModel):
    block = CharField(null=True)
    build_fee = IntegerField(null=True)
    census_desc = CharField(null=True)
    census_number = CharField(null=True)
    cert_count = IntegerField(null=True)
    cert_date = DateField(null=True)
    cert_fee = IntegerField(null=True)
    cert_type = CharField(null=True)
    cert_type_desc = CharField(null=True)
    const_cost = IntegerField(null=True)
    county = CharField(null=True)
    county_id = IntegerField(index=True)
    created_at = DateTimeField()
    cubic = IntegerField(null=True)
    dca_fee = IntegerField(null=True)
    elect_fee = IntegerField(null=True)
    elev_fee = IntegerField(null=True)
    fire_fee = IntegerField(null=True)
    hud_seal = BooleanField(null=True)
    lot = CharField(null=True)
    manufactured = BooleanField(null=True)
    muni_name = CharField(null=True)
    muni_type = CharField(null=True)
    municipality_id = IntegerField(index=True)
    other_fee = IntegerField(null=True)
    permit_date = DateField(null=True)
    permit_no = CharField(null=True)
    permit_status_desc = CharField(null=True)
    permit_type = CharField(null=True)
    permit_type_desc = CharField(null=True)
    plumb_fee = IntegerField(null=True)
    process_date = DateField(null=True)
    property_id = IntegerField(index=True)
    public = BooleanField(null=True)
    record_id = CharField(null=True)
    rent_gained = IntegerField(null=True)
    sale_gained = IntegerField(null=True)
    source = CharField(null=True)
    source_desc = CharField(null=True)
    squarefeet = IntegerField(null=True)
    status = CharField(null=True)
    storage = BooleanField(null=True)
    total_fee = IntegerField(null=True)
    treasury_code = CharField(null=True)
    update = BooleanField(null=True)
    updated_at = DateTimeField(null=True)
    use_group = CharField(null=True)
    use_group_desc = CharField(null=True)
    version = CharField(null=True)

    class Meta:
        table_name = 'property_construction_permits'
        indexes = (
            (('county_id', 'permit_date'), False),
            (('municipality_id', 'permit_date'), False),
        )
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
    county_id = IntegerField(null=True)
    created_at = DateTimeField()
    critical_error_flag = CharField(null=True)
    date_recorded = DateField(null=True)
    date_typed = DateField(null=True)
    deed_book = CharField(null=True)
    deed_book_num = IntegerField(null=True)
    deed_date = DateField(null=True)
    deed_id_num = CharField(null=True)
    deed_page = CharField(null=True)
    deed_page_num = IntegerField(null=True)
    dln = CharField(null=True)
    document_path = CharField(null=True)
    etc = CharField(null=True)
    field_date = DateField(null=True)
    field_status_code = CharField(null=True)
    grantee_id = IntegerField(null=True)
    grantor_id = IntegerField(null=True)
    is_redacted = BooleanField(null=True)
    last_update_date = DateField(null=True)
    living_space = IntegerField(null=True)
    match_method_id = IntegerField(null=True)
    municipality_id = IntegerField()
    property_class = CharField(null=True)
    property_id = IntegerField()
    property_location_id = IntegerField(null=True)
    questionnaire_date = DateField(null=True)
    questionnaire_status_code = CharField(null=True)
    questionnaire_who_code = CharField(null=True)
    realty_transfer_fee = IntegerField(null=True)
    reported_sales_price = IntegerField(null=True)
    rtf_error_flag = CharField(null=True)
    rtf_exempt_code = CharField(null=True)
    sales_ratio = DoubleField(null=True)
    serial_number = CharField(null=True)
    sr_nu_code = CharField(null=True)
    u_n_type = CharField(null=True)
    updated_at = DateTimeField(null=True)
    verified_sales_price = IntegerField(null=True)
    year = IntegerField(null=True)
    year_built = IntegerField(null=True)

    class Meta:
        table_name = 'property_deeds'
        indexes = (
            (('county_id', 'deed_date'), False),
            (('deed_book_num', 'deed_page_num'), False),
            (('deed_book_num', 'deed_page_num', 'municipality_id'), False),
            (('municipality_id', 'deed_date'), False),
            (('property_id', 'deed_date'), False),
        )
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
    case_number = CharField(null=True)
    county_id = IntegerField(null=True)
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
    municipality_id = IntegerField(null=True)
    original_loan_amount = DoubleField(null=True)
    original_loan_book_page = CharField(null=True)
    original_loan_instrument_number = CharField(null=True)
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
    property_id = IntegerField(index=True)
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
        indexes = (
            (('county_id', 'foreclosure_instrument_date'), False),
            (('municipality_id', 'foreclosure_instrument_date'), False),
            (('property_id', 'foreclosure_instrument_date'), False),
        )
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
    building_desc = CharField(null=True)
    calculated_taxes = DoubleField(null=True)
    calculated_taxes_year = SmallIntegerField(null=True)
    corporate_owned = BooleanField()
    data_year = SmallIntegerField(null=True)
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
    municipality_id = IntegerField()
    no_of_commercial_dw = IntegerField(null=True)
    no_of_dwellings = IntegerField(null=True)
    nu_code = CharField(null=True)
    number_of_owners = IntegerField(null=True)
    old_property_id = CharField(null=True)
    owner_mail_address_id = IntegerField(null=True)
    percent_owned_code = CharField(null=True)
    prior_gis_pin = CharField(null=True)
    property_class = CharField(null=True)
    property_flags = CharField(null=True)
    property_id = IntegerField()
    property_location_id = IntegerField(null=True)
    property_owner_id = IntegerField(null=True)
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
    building_desc = CharField(null=True)
    calculated_taxes = DoubleField(null=True)
    calculated_taxes_year = SmallIntegerField(null=True)
    corporate_owned = BooleanField()
    data_year = SmallIntegerField(null=True)
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
    municipality_id = IntegerField()
    no_of_commercial_dw = IntegerField(null=True)
    no_of_dwellings = IntegerField(null=True)
    nu_code = CharField(null=True)
    number_of_owners = IntegerField(null=True)
    old_property_id = CharField(null=True)
    owner_mail_address_id = IntegerField(null=True)
    percent_owned_code = CharField(null=True)
    prior_gis_pin = CharField(null=True)
    property_class = CharField(null=True)
    property_flags = CharField(null=True)
    property_id = IntegerField()
    property_location_id = IntegerField(null=True)
    property_owner_id = IntegerField(null=True)
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
            (('shard_num', 'property_id'), False),
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
    building_desc = CharField(null=True)
    calculated_taxes = DoubleField(null=True)
    calculated_taxes_year = SmallIntegerField(null=True)
    corporate_owned = BooleanField()
    data_year = SmallIntegerField(null=True)
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
    municipality_id = IntegerField()
    no_of_commercial_dw = IntegerField(null=True)
    no_of_dwellings = IntegerField(null=True)
    nu_code = CharField(null=True)
    number_of_owners = IntegerField(null=True)
    old_property_id = CharField(null=True)
    owner_mail_address_id = IntegerField(null=True)
    percent_owned_code = CharField(null=True)
    prior_gis_pin = CharField(null=True)
    property_class = CharField(null=True)
    property_flags = CharField(null=True)
    property_id = IntegerField()
    property_location_id = IntegerField(null=True)
    property_owner_id = IntegerField(null=True)
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
            (('shard_num', 'property_id'), False),
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
    building_desc = CharField(null=True)
    calculated_taxes = DoubleField(null=True)
    calculated_taxes_year = SmallIntegerField(null=True)
    corporate_owned = BooleanField()
    data_year = SmallIntegerField(null=True)
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
    municipality_id = IntegerField()
    no_of_commercial_dw = IntegerField(null=True)
    no_of_dwellings = IntegerField(null=True)
    nu_code = CharField(null=True)
    number_of_owners = IntegerField(null=True)
    old_property_id = CharField(null=True)
    owner_mail_address_id = IntegerField(null=True)
    percent_owned_code = CharField(null=True)
    prior_gis_pin = CharField(null=True)
    property_class = CharField(null=True)
    property_flags = CharField(null=True)
    property_id = IntegerField()
    property_location_id = IntegerField(null=True)
    property_owner_id = IntegerField(null=True)
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
            (('shard_num', 'property_id'), False),
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
    building_desc = CharField(null=True)
    calculated_taxes = DoubleField(null=True)
    calculated_taxes_year = SmallIntegerField(null=True)
    corporate_owned = BooleanField()
    data_year = SmallIntegerField(null=True)
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
    municipality_id = IntegerField()
    no_of_commercial_dw = IntegerField(null=True)
    no_of_dwellings = IntegerField(null=True)
    nu_code = CharField(null=True)
    number_of_owners = IntegerField(null=True)
    old_property_id = CharField(null=True)
    owner_mail_address_id = IntegerField(null=True)
    percent_owned_code = CharField(null=True)
    prior_gis_pin = CharField(null=True)
    property_class = CharField(null=True)
    property_flags = CharField(null=True)
    property_id = IntegerField()
    property_location_id = IntegerField(null=True)
    property_owner_id = IntegerField(null=True)
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
            (('shard_num', 'property_id'), False),
        )
        schema = 'parcels'
        primary_key = CompositeKey('id', 'shard_num')

class PropertyHistories5(BaseModel):
    absentee = SmallIntegerField(null=True)
    acreage = DoubleField(null=True)
    addition_lots_2 = CharField(null=True)
    additional_lots = CharField(null=True)
    assessed = IntegerField(null=True)
    bank_code = CharField(null=True)
    building_assmnt = IntegerField(null=True)
    building_class = ForeignKeyField(column_name='building_class_id', field='id', model=LookupTable, null=True)
    building_desc = CharField(null=True)
    calculated_taxes = DoubleField(null=True)
    calculated_taxes_year = SmallIntegerField(null=True)
    corporate_owned = BooleanField()
    data_year = SmallIntegerField(null=True)
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
    municipality_id = IntegerField()
    no_of_commercial_dw = IntegerField(null=True)
    no_of_dwellings = IntegerField(null=True)
    nu_code = CharField(null=True)
    number_of_owners = IntegerField(null=True)
    old_property_id = CharField(null=True)
    owner_mail_address_id = IntegerField(null=True)
    percent_owned_code = CharField(null=True)
    prior_gis_pin = CharField(null=True)
    property_class = CharField(null=True)
    property_flags = CharField(null=True)
    property_id = IntegerField()
    property_location_id = IntegerField(null=True)
    property_owner_id = IntegerField(null=True)
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
        table_name = 'property_histories_5'
        indexes = (
            (('id', 'shard_num'), True),
            (('shard_num', 'property_id'), False),
        )
        schema = 'parcels'
        primary_key = CompositeKey('id', 'shard_num')

class PropertyHistories6(BaseModel):
    absentee = SmallIntegerField(null=True)
    acreage = DoubleField(null=True)
    addition_lots_2 = CharField(null=True)
    additional_lots = CharField(null=True)
    assessed = IntegerField(null=True)
    bank_code = CharField(null=True)
    building_assmnt = IntegerField(null=True)
    building_class = ForeignKeyField(column_name='building_class_id', field='id', model=LookupTable, null=True)
    building_desc = CharField(null=True)
    calculated_taxes = DoubleField(null=True)
    calculated_taxes_year = SmallIntegerField(null=True)
    corporate_owned = BooleanField()
    data_year = SmallIntegerField(null=True)
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
    municipality_id = IntegerField()
    no_of_commercial_dw = IntegerField(null=True)
    no_of_dwellings = IntegerField(null=True)
    nu_code = CharField(null=True)
    number_of_owners = IntegerField(null=True)
    old_property_id = CharField(null=True)
    owner_mail_address_id = IntegerField(null=True)
    percent_owned_code = CharField(null=True)
    prior_gis_pin = CharField(null=True)
    property_class = CharField(null=True)
    property_flags = CharField(null=True)
    property_id = IntegerField()
    property_location_id = IntegerField(null=True)
    property_owner_id = IntegerField(null=True)
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
        table_name = 'property_histories_6'
        indexes = (
            (('id', 'shard_num'), True),
            (('shard_num', 'property_id'), False),
        )
        schema = 'parcels'
        primary_key = CompositeKey('id', 'shard_num')

class PropertyHistories7(BaseModel):
    absentee = SmallIntegerField(null=True)
    acreage = DoubleField(null=True)
    addition_lots_2 = CharField(null=True)
    additional_lots = CharField(null=True)
    assessed = IntegerField(null=True)
    bank_code = CharField(null=True)
    building_assmnt = IntegerField(null=True)
    building_class = ForeignKeyField(column_name='building_class_id', field='id', model=LookupTable, null=True)
    building_desc = CharField(null=True)
    calculated_taxes = DoubleField(null=True)
    calculated_taxes_year = SmallIntegerField(null=True)
    corporate_owned = BooleanField()
    data_year = SmallIntegerField(null=True)
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
    municipality_id = IntegerField()
    no_of_commercial_dw = IntegerField(null=True)
    no_of_dwellings = IntegerField(null=True)
    nu_code = CharField(null=True)
    number_of_owners = IntegerField(null=True)
    old_property_id = CharField(null=True)
    owner_mail_address_id = IntegerField(null=True)
    percent_owned_code = CharField(null=True)
    prior_gis_pin = CharField(null=True)
    property_class = CharField(null=True)
    property_flags = CharField(null=True)
    property_id = IntegerField()
    property_location_id = IntegerField(null=True)
    property_owner_id = IntegerField(null=True)
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
        table_name = 'property_histories_7'
        indexes = (
            (('id', 'shard_num'), True),
            (('shard_num', 'property_id'), False),
        )
        schema = 'parcels'
        primary_key = CompositeKey('id', 'shard_num')

class PropertyHistories8(BaseModel):
    absentee = SmallIntegerField(null=True)
    acreage = DoubleField(null=True)
    addition_lots_2 = CharField(null=True)
    additional_lots = CharField(null=True)
    assessed = IntegerField(null=True)
    bank_code = CharField(null=True)
    building_assmnt = IntegerField(null=True)
    building_class = ForeignKeyField(column_name='building_class_id', field='id', model=LookupTable, null=True)
    building_desc = CharField(null=True)
    calculated_taxes = DoubleField(null=True)
    calculated_taxes_year = SmallIntegerField(null=True)
    corporate_owned = BooleanField()
    data_year = SmallIntegerField(null=True)
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
    municipality_id = IntegerField()
    no_of_commercial_dw = IntegerField(null=True)
    no_of_dwellings = IntegerField(null=True)
    nu_code = CharField(null=True)
    number_of_owners = IntegerField(null=True)
    old_property_id = CharField(null=True)
    owner_mail_address_id = IntegerField(null=True)
    percent_owned_code = CharField(null=True)
    prior_gis_pin = CharField(null=True)
    property_class = CharField(null=True)
    property_flags = CharField(null=True)
    property_id = IntegerField()
    property_location_id = IntegerField(null=True)
    property_owner_id = IntegerField(null=True)
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
        table_name = 'property_histories_8'
        indexes = (
            (('id', 'shard_num'), True),
            (('shard_num', 'property_id'), False),
        )
        schema = 'parcels'
        primary_key = CompositeKey('id', 'shard_num')

class PropertyLocations(BaseModel):
    location = CharField(unique=True)
    street_address = CharField(null=True)

    class Meta:
        table_name = 'property_locations'
        schema = 'parcels'

class PropertyMortgages(BaseModel):
    adjustable_rate_index = CharField(null=True)
    adjustable_rate_rider = BooleanField(null=True)
    assessors_land_use = CharField(null=True)
    assessors_parcel_number = CharField(null=True)
    borrower1_code_id = IntegerField(null=True)
    borrower1_id = IntegerField(index=True, null=True)
    borrower2_code_id = IntegerField(null=True)
    borrower2_id = IntegerField(index=True, null=True)
    borrower_vesting_code_id = IntegerField(null=True)
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
    lender_id = IntegerField(index=True, null=True)
    loan_amount = IntegerField(null=True)
    loan_financing_type_id = IntegerField(null=True)
    loan_term_months = IntegerField(null=True)
    loan_term_years = IntegerField(null=True)
    loan_type = ForeignKeyField(column_name='loan_type_id', field='id', model=LookupTable, null=True)
    maximum_interest_rate = DoubleField(null=True)
    original_date_of_contract = DateField(null=True)
    prepayment_rider = CharField(null=True)
    prepayment_term_penalty_rider = CharField(null=True)
    property_address = ForeignKeyField(column_name='property_address_id', field='id', model=MailingAddresses, null=True)
    property_id = IntegerField(index=True)
    property_identifier = CharField(null=True)
    property_unit_type = CharField(null=True)
    purchase_money_mortgage = BooleanField(null=True)
    rate_change_frequency = CharField(null=True)
    record_type_id = IntegerField(null=True)
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

class PropertyOwners(BaseModel):
    city_state_zip = CharField(null=True)
    fingerprint = BigIntegerField(unique=True)
    is_redacted = BooleanField()
    name = CharField()
    normalized_location = CharField(index=True, null=True)
    normalized_name = CharField(index=True)
    street_address = CharField(null=True)

    class Meta:
        table_name = 'property_owners'
        schema = 'parcels'

class PropertyParcelNumbers(BaseModel):
    parcel_number = CharField(index=True)
    property_id = IntegerField()

    class Meta:
        table_name = 'property_parcel_numbers'
        indexes = (
            (('property_id', 'parcel_number'), True),
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
        table_name = 'property_quick_facts'
        schema = 'parcels'

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
    property_id = IntegerField(index=True)
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
    property_id = IntegerField(index=True)

    class Meta:
        table_name = 'property_residents'
        schema = 'parcels'

class PropertyTaxClassifications(BaseModel):
    category = CharField(null=True)
    description = CharField(null=True)
    name = CharField()
    property_class = CharField(unique=True)
    short_name = CharField()

    class Meta:
        table_name = 'property_tax_classifications'
        schema = 'parcels'

class PropertyVoterLinks(BaseModel):
    property_id = IntegerField()
    voter_id = IntegerField()

    class Meta:
        table_name = 'property_voter_links'
        indexes = (
            (('property_id', 'voter_id'), True),
        )
        schema = 'parcels'
        primary_key = CompositeKey('property_id', 'voter_id')

class PublicUtilities(BaseModel):
    created_at = DateTimeField()
    description = CharField(null=True)
    name = CharField()
    price_url = CharField(null=True)
    type = CharField()
    updated_at = DateTimeField(null=True)
    web = CharField(null=True)

    class Meta:
        table_name = 'public_utilities'
        indexes = (
            (('name', 'type'), True),
        )
        schema = 'parcels'

class UtilitySuppliers(BaseModel):
    city_state_zip = CharField(null=True)
    commercial = BooleanField()
    description = CharField(null=True)
    fingerprint = BigIntegerField(unique=True)
    industrial = BooleanField()
    name = CharField()
    phones = CharField(null=True)
    price_url = CharField(null=True)
    residential = BooleanField()
    street = CharField(null=True)
    type = CharField()
    web = CharField(null=True)

    class Meta:
        table_name = 'utility_suppliers'
        schema = 'parcels'

class PublicUtilitySupplierLinks(BaseModel):
    supplier = ForeignKeyField(column_name='supplier_id', field='id', model=UtilitySuppliers)
    utility = ForeignKeyField(column_name='utility_id', field='id', model=PublicUtilities)

    class Meta:
        table_name = 'public_utility_supplier_links'
        indexes = (
            (('utility', 'supplier'), True),
        )
        schema = 'parcels'
        primary_key = CompositeKey('supplier', 'utility')

class RegisteredVoters(BaseModel):
    city = CharField(null=True)
    congressional = IntegerField(null=True)
    county_id = IntegerField(index=True)
    district = CharField(null=True)
    dob = DateField(null=True)
    fire = IntegerField(null=True)
    first_name = CharField(index=True)
    freeholder = IntegerField(null=True)
    last_name = CharField(index=True)
    leg_id = CharField(null=True)
    legislative = IntegerField(null=True)
    location = CharField(null=True)
    municipality_id = IntegerField(index=True)
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

class RelatedProperties(BaseModel):
    main_property_id = IntegerField(index=True)
    related_property_id = IntegerField()

    class Meta:
        table_name = 'related_properties'
        indexes = (
            (('main_property_id', 'related_property_id'), True),
        )
        schema = 'parcels'

class Schools(BaseModel):
    city = CharField(null=True)
    county = CharField(null=True)
    county_id = IntegerField(index=True, null=True)
    district_id = IntegerField(null=True)
    district_name = CharField(null=True)
    fax = CharField(null=True)
    fipscounty = CharField(null=True)
    geo_location = UnknownField(index=True, null=True)  # USER-DEFINED
    level = CharField(null=True)
    level_codes = CharField(null=True)
    municipality_id = IntegerField(index=True, null=True)
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
    city_id = IntegerField(index=True)
    county_id = IntegerField(index=True)
    municipality_id = IntegerField(index=True, null=True)
    name = CharField()
    normalized_name = CharField()
    num_properties = IntegerField(null=True)

    class Meta:
        table_name = 'streets'
        indexes = (
            (('city_id', 'normalized_name'), False),
            (('city_id', 'normalized_name'), True),
        )
        schema = 'parcels'

class TaxationBoards(BaseModel):
    address = CharField(null=True)
    county_id = IntegerField(index=True)
    county_name = CharField()
    created_at = DateTimeField()
    email = CharField(null=True)
    entity_type = CharField(index=True)
    fax = CharField(null=True)
    municipality_id = IntegerField(index=True, null=True)
    municipality_name = CharField(null=True)
    name = CharField(null=True)
    phone = CharField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        table_name = 'taxation_boards'
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

class VotingHistories(BaseModel):
    did_vote = BooleanField()
    election_date = DateField(null=True)
    election_id = IntegerField()
    voter_id = IntegerField(index=True)

    class Meta:
        table_name = 'voting_histories'
        indexes = (
            (('voter_id', 'election_date'), False),
        )
        schema = 'parcels'

class VwBorrowerMortgagesList(BaseModel):
    acreage = DoubleField(null=True)
    borrower1_id = IntegerField(null=True)
    borrower2_id = IntegerField(null=True)
    county_id = IntegerField(null=True)
    county_name = CharField(null=True)
    gis_pin = CharField(null=True)
    instrument_date = DateField(null=True)
    instrument_number = CharField(null=True)
    interest_rate = DoubleField(null=True)
    lat = DoubleField(null=True)
    lender_id = IntegerField(null=True)
    lender_name = CharField(null=True)
    lng = DoubleField(null=True)
    loan_amount = IntegerField(null=True)
    loan_term_months = IntegerField(null=True)
    loan_term_years = IntegerField(null=True)
    mortgage_id = IntegerField(null=True)
    municipality_id = IntegerField(null=True)
    municipality_name = CharField(null=True)
    property_class = CharField(null=True)
    property_id = IntegerField(null=True)
    property_location = CharField(null=True)
    sale_date = DateField(null=True)
    sale_price = IntegerField(null=True)
    sq_ft = IntegerField(null=True)

    class Meta:
        table_name = 'vw_borrower_mortgages_list'
        schema = 'parcels'
        primary_key = False

class VwDeedPartiesSummary(BaseModel):
    buyer_city_state = CharField(null=True)
    buyer_id = IntegerField(null=True)
    buyer_name = CharField(null=True)
    buyer_street = CharField(null=True)
    buyer_zip = CharField(null=True)
    county_id = IntegerField(null=True)
    deed_book = CharField(null=True)
    deed_book_num = IntegerField(null=True)
    deed_date = DateField(null=True)
    deed_id = IntegerField(null=True)
    deed_page = CharField(null=True)
    deed_page_num = IntegerField(null=True)
    municipality_id = IntegerField(null=True)
    property_id = IntegerField(null=True)
    realty_transfer_fee = IntegerField(null=True)
    reported_sales_price = IntegerField(null=True)
    seller_city_state = CharField(null=True)
    seller_id = IntegerField(null=True)
    seller_name = CharField(null=True)
    seller_street = CharField(null=True)
    seller_zip = CharField(null=True)
    serial_number = CharField(null=True)
    verified_sales_price = IntegerField(null=True)

    class Meta:
        table_name = 'vw_deed_parties_summary'
        schema = 'parcels'
        primary_key = False

class VwLenderMortgageBorrowersList(BaseModel):
    borrower1_description = CharField(null=True)
    borrower1_fname_mname = CharField(null=True)
    borrower1_full_name = CharField(null=True)
    borrower1_id = IntegerField(null=True)
    borrower1_lname_or_corpname = CharField(null=True)
    borrower2_description = CharField(null=True)
    borrower2_fname_mname = CharField(null=True)
    borrower2_full_name = CharField(null=True)
    borrower2_id = IntegerField(null=True)
    borrower2_lname_or_corpname = CharField(null=True)
    city = CharField(null=True)
    lender_id = IntegerField(null=True)
    state = CharField(null=True)
    street_address = CharField(null=True)
    zip = CharField(null=True)

    class Meta:
        table_name = 'vw_lender_mortgage_borrowers_list'
        schema = 'parcels'
        primary_key = False

class VwLenderMortgagePropertiesList(BaseModel):
    county_name = CharField(null=True)
    gis_pin = CharField(null=True)
    lender_id = IntegerField(null=True)
    municipality_name = CharField(null=True)
    property_city_state_zip = CharField(null=True)
    property_class_code = CharField(null=True)
    property_class_short_name = CharField(null=True)
    property_id = IntegerField(null=True)
    property_location = CharField(null=True)
    sale_date = DateField(null=True)
    sale_price = IntegerField(null=True)
    sq_ft = IntegerField(null=True)

    class Meta:
        table_name = 'vw_lender_mortgage_properties_list'
        schema = 'parcels'
        primary_key = False

class VwLenderMortgagesList(BaseModel):
    due_date = DateField(null=True)
    gis_pin = CharField(null=True)
    instrument_date = DateField(null=True)
    instrument_number = CharField(null=True)
    interest_rate = DoubleField(null=True)
    lender_id = IntegerField(null=True)
    loan_amount = IntegerField(null=True)
    loan_term_months = IntegerField(null=True)
    loan_term_years = IntegerField(null=True)
    loan_type = CharField(null=True)
    loan_type_code = CharField(null=True)
    mortgage_id = IntegerField(null=True)
    property_city_state_zip = CharField(null=True)
    property_id = IntegerField(null=True)
    property_location = CharField(null=True)

    class Meta:
        table_name = 'vw_lender_mortgages_list'
        schema = 'parcels'
        primary_key = False

class VwMortgageDetails(BaseModel):
    adjustable_rate_index = CharField(null=True)
    adjustable_rate_rider = BooleanField(null=True)
    assessors_land_use = CharField(null=True)
    assessors_parcel_number = CharField(null=True)
    borrower1_code = CharField(null=True)
    borrower1_code_description = CharField(null=True)
    borrower1_id = IntegerField(null=True)
    borrower1_name = CharField(null=True)
    borrower2_code = CharField(null=True)
    borrower2_code_description = CharField(null=True)
    borrower2_id = IntegerField(null=True)
    borrower2_name = CharField(null=True)
    borrower_address = CharField(null=True)
    borrower_city = CharField(null=True)
    borrower_mail_unit_number = CharField(null=True)
    borrower_state = CharField(null=True)
    borrower_vesting_code = CharField(null=True)
    borrower_vesting_description = CharField(null=True)
    borrower_zip = CharField(null=True)
    borrower_zip4 = CharField(null=True)
    cash_purchase = BooleanField(null=True)
    change_index = CharField(null=True)
    construction_loan = BooleanField(null=True)
    display_id = IntegerField(null=True)
    document_path = CharField(null=True)
    due_date = DateField(null=True)
    equity_credit_line = BooleanField(null=True)
    fips_code = CharField(null=True)
    first_change_date_month_day_conversion_rider = CharField(null=True)
    first_change_date_year_conversion_rider = CharField(null=True)
    fixedstep_conversion_rate_rider = CharField(null=True)
    gis_pin = CharField(null=True)
    id = IntegerField(null=True)
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
    lender_dba_name = CharField(null=True)
    lender_id = IntegerField(null=True)
    lender_mailing_address_city = CharField(null=True)
    lender_mailing_address_state = CharField(null=True)
    lender_mailing_address_street = CharField(null=True)
    lender_mailing_address_zip = CharField(null=True)
    lender_name = CharField(null=True)
    lender_type = CharField(null=True)
    lender_type_description = CharField(null=True)
    loan_amount = IntegerField(null=True)
    loan_financing_type = CharField(null=True)
    loan_financing_type_description = CharField(null=True)
    loan_term_months = IntegerField(null=True)
    loan_term_years = IntegerField(null=True)
    loan_type = CharField(null=True)
    loan_type_description = CharField(null=True)
    maximum_interest_rate = DoubleField(null=True)
    original_date_of_contract = DateField(null=True)
    prepayment_rider = CharField(null=True)
    prepayment_term_penalty_rider = CharField(null=True)
    property_address_id = IntegerField(null=True)
    property_id = IntegerField(null=True)
    property_identifier = CharField(null=True)
    property_mailing_address_city = CharField(null=True)
    property_mailing_address_state = CharField(null=True)
    property_mailing_address_street = CharField(null=True)
    property_mailing_address_zip = CharField(null=True)
    property_unit_type = CharField(null=True)
    purchase_money_mortgage = BooleanField(null=True)
    rate_change_frequency = CharField(null=True)
    record_type = CharField(null=True)
    record_type_description = CharField(null=True)
    record_type_id = IntegerField(null=True)
    recorders_book_number = CharField(null=True)
    recorders_document_number = CharField(null=True)
    recorders_page_number = CharField(null=True)
    recording_date = DateField(null=True)
    residential_indicator = BooleanField(null=True)
    source = CharField(null=True)
    standalone_refi = BooleanField(null=True)
    title_company_name = CharField(null=True)
    transaction_id = CharField(null=True)
    unique_link_id = CharField(null=True)

    class Meta:
        table_name = 'vw_mortgage_details'
        schema = 'parcels'
        primary_key = False

class VwMortgageLenderDetails(BaseModel):
    address = CharField(null=True)
    city = CharField(null=True)
    dba_name = CharField(null=True)
    id = IntegerField(null=True)
    lender_type = CharField(null=True)
    lender_type_description = CharField(null=True)
    name = CharField(null=True)
    state = CharField(null=True)
    zip = CharField(null=True)
    zip4 = CharField(null=True)

    class Meta:
        table_name = 'vw_mortgage_lender_details'
        schema = 'parcels'
        primary_key = False

class VwMortgageSummary(BaseModel):
    borrower1_code = CharField(null=True)
    borrower1_code_description = CharField(null=True)
    borrower1_id = IntegerField(null=True)
    borrower1_name = CharField(null=True)
    borrower2_code = CharField(null=True)
    borrower2_code_description = CharField(null=True)
    borrower2_id = IntegerField(null=True)
    borrower2_name = CharField(null=True)
    borrower_address = CharField(null=True)
    borrower_city = CharField(null=True)
    borrower_state = CharField(null=True)
    borrower_vesting_code = CharField(null=True)
    borrower_vesting_description = CharField(null=True)
    borrower_zip = CharField(null=True)
    cash_purchase = BooleanField(null=True)
    construction_loan = BooleanField(null=True)
    data_year = DecimalField(null=True)
    display_id = IntegerField(null=True)
    equity_credit_line = BooleanField(null=True)
    id = IntegerField(null=True)
    instrument_book = CharField(null=True)
    instrument_date = DateField(null=True)
    instrument_number = CharField(null=True)
    instrument_page = CharField(null=True)
    interest_rate = DoubleField(null=True)
    lender_dba_name = CharField(null=True)
    lender_id = IntegerField(null=True)
    lender_name = CharField(null=True)
    lender_type = CharField(null=True)
    lender_type_description = CharField(null=True)
    loan_amount = IntegerField(null=True)
    loan_financing_type = CharField(null=True)
    loan_financing_type_description = CharField(null=True)
    loan_term_months = IntegerField(null=True)
    loan_term_years = IntegerField(null=True)
    loan_type = CharField(null=True)
    loan_type_description = CharField(null=True)
    original_date_of_contract = DateField(null=True)
    property_id = IntegerField(null=True)
    record_type = CharField(null=True)
    record_type_description = CharField(null=True)
    recording_date = DateField(null=True)
    residential_indicator = BooleanField(null=True)
    source = CharField(null=True)
    standalone_refi = BooleanField(null=True)
    title_company_name = CharField(null=True)

    class Meta:
        table_name = 'vw_mortgage_summary'
        schema = 'parcels'
        primary_key = False

class VwMunicipalityBlocksList(BaseModel):
    block = CharField(null=True)
    block_id = IntegerField(null=True)
    county_id = IntegerField(null=True)
    county_name = CharField(null=True)
    municipality_code = CharField(null=True)
    municipality_id = IntegerField(null=True)
    municipality_name = CharField(null=True)

    class Meta:
        table_name = 'vw_municipality_blocks_list'
        schema = 'parcels'
        primary_key = False

class VwPropertyDeeds(BaseModel):
    assess_year = IntegerField(null=True)
    buyer_city_state = CharField(null=True)
    buyer_id = IntegerField(null=True)
    buyer_name = CharField(null=True)
    buyer_street = CharField(null=True)
    buyer_zip = CharField(null=True)
    county_id = IntegerField(null=True)
    county_name = CharField(null=True)
    date_recorded = DateField(null=True)
    deed_book = CharField(null=True)
    deed_date = DateField(null=True)
    deed_id_num = CharField(null=True)
    deed_page = CharField(null=True)
    id = IntegerField(null=True)
    municipality_id = IntegerField(null=True)
    municipality_name = CharField(null=True)
    property_class_code = CharField(null=True)
    property_class_name = CharField(null=True)
    property_class_short_name = CharField(null=True)
    property_id = IntegerField(null=True)
    realty_transfer_fee = IntegerField(null=True)
    reported_sales_price = IntegerField(null=True)
    seller_city_state = CharField(null=True)
    seller_id = IntegerField(null=True)
    seller_name = CharField(null=True)
    seller_street = CharField(null=True)
    seller_zip = CharField(null=True)
    serial_number = CharField(null=True)
    verified_sales_price = IntegerField(null=True)

    class Meta:
        table_name = 'vw_property_deeds'
        schema = 'parcels'
        primary_key = False

class VwPropertyHistory(BaseModel):
    absentee = SmallIntegerField(null=True)
    acreage = DoubleField(null=True)
    addition_lots_2 = CharField(null=True)
    additional_lots = CharField(null=True)
    assessed = IntegerField(null=True)
    bank_code = CharField(null=True)
    building_assmnt = IntegerField(null=True)
    building_desc = CharField(null=True)
    calculated_taxes = DoubleField(null=True)
    calculated_taxes_year = SmallIntegerField(null=True)
    code = CharField(null=True)
    corporate_owned = BooleanField(null=True)
    data_year = SmallIntegerField(null=True)
    deduction_amount = IntegerField(null=True)
    deed_book = CharField(null=True)
    deed_page = CharField(null=True)
    delinquent_code = CharField(null=True)
    description = CharField(null=True)
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
    land_assmnt = IntegerField(null=True)
    land_desc = CharField(null=True)
    last_year_tax = DoubleField(null=True)
    map_page = CharField(null=True)
    multiple_occupancy = CharField(null=True)
    municipality_effective_tax_rate = DoubleField(null=True)
    municipality_general_tax_rate = DoubleField(null=True)
    municipality_id = IntegerField(null=True)
    municipality_tax_ratio = DoubleField(null=True)
    no_of_commercial_dw = IntegerField(null=True)
    no_of_dwellings = IntegerField(null=True)
    nu_code = CharField(null=True)
    number_of_owners = IntegerField(null=True)
    old_property_id = CharField(null=True)
    owner_city_state_zip = CharField(null=True)
    owner_is_redacted = BooleanField(null=True)
    owner_name = CharField(null=True)
    owner_street_address = CharField(null=True)
    percent_owned_code = CharField(null=True)
    prior_gis_pin = CharField(null=True)
    property_class = CharField(null=True)
    property_flags = CharField(null=True)
    property_id = IntegerField(null=True)
    property_owner_id = IntegerField(null=True)
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
    shard_num = SmallIntegerField(null=True)
    sp_tax_cd = CharField(null=True)
    sq_ft = IntegerField(null=True)
    surv_spouse_cnt = IntegerField(null=True)
    taxes = DoubleField(null=True)
    total_assmnt = IntegerField(null=True)
    veterans_cnt = IntegerField(null=True)
    widows_cnt = IntegerField(null=True)
    yr_built = SmallIntegerField(null=True)

    class Meta:
        table_name = 'vw_property_history'
        schema = 'parcels'
        primary_key = False

class VwPropertyMasterDetails(BaseModel):
    absentee = IntegerField(null=True)
    account = CharField(null=True)
    acreage = DoubleField(null=True)
    additional_lots = CharField(null=True)
    additional_lots_parsed = CharField(null=True)
    apn = CharField(null=True)
    assessed = IntegerField(null=True)
    bank_code = CharField(null=True)
    block_id = IntegerField(null=True)
    building_assmnt = IntegerField(null=True)
    building_class_code = CharField(null=True)
    building_class_description = CharField(null=True)
    building_class_id = IntegerField(null=True)
    building_desc = CharField(null=True)
    calculated_taxes = DoubleField(null=True)
    calculated_taxes_year = SmallIntegerField(null=True)
    census_code = CharField(null=True)
    class_4_code = CharField(null=True)
    corporate_owned = BooleanField(null=True)
    county_code = CharField(null=True)
    county_id = IntegerField(null=True)
    county_name = CharField(null=True)
    created_at = DateTimeField(null=True)
    deduction_amount = IntegerField(null=True)
    deed_book = CharField(null=True)
    deed_page = CharField(null=True)
    direct_parties = CharField(null=True)
    disabled_cnt = IntegerField(null=True)
    electric_provider_id = IntegerField(null=True)
    electric_provider_name = CharField(null=True)
    epl_desc = CharField(null=True)
    epl_facility_name = CharField(null=True)
    epl_further = DateField(null=True)
    epl_init = DateField(null=True)
    epl_own = CharField(null=True)
    epl_statute = CharField(null=True)
    epl_use = CharField(null=True)
    exempt = IntegerField(null=True)
    gas_provider_id = IntegerField(null=True)
    gas_provider_name = CharField(null=True)
    gis_pin = CharField(null=True)
    id = IntegerField(null=True)
    is_redacted = BooleanField(null=True)
    is_rental = BooleanField(null=True)
    land_assmnt = IntegerField(null=True)
    land_desc = CharField(null=True)
    last_year_tax = DoubleField(null=True)
    lat = DoubleField(null=True)
    lng = DoubleField(null=True)
    map_img = CharField(null=True)
    map_page = CharField(null=True)
    market_value_estimate = IntegerField(null=True)
    market_value_estimate_range_max = IntegerField(null=True)
    market_value_estimate_range_min = IntegerField(null=True)
    market_value_estimate_updated = DateTimeField(null=True)
    mortgage_account = CharField(null=True)
    mun_updated = DateField(null=True)
    municipality_code = CharField(null=True)
    municipality_id = IntegerField(null=True)
    municipality_name = CharField(null=True)
    nu_code = CharField(null=True)
    owner_city = CharField(null=True)
    owner_city_state_zip = CharField(null=True)
    owner_is_redacted = BooleanField(null=True)
    owner_name = CharField(null=True)
    owner_state = CharField(null=True)
    owner_street_address = CharField(null=True)
    owner_zip_code = CharField(null=True)
    parcel_acres = DoubleField(null=True)
    parcel_centroid_lat = DoubleField(null=True)
    parcel_centroid_lng = DoubleField(null=True)
    parcel_perimeter = DoubleField(null=True)
    parcel_sqft = DoubleField(null=True)
    prior_block = CharField(null=True)
    prior_gis_pin = CharField(null=True)
    prior_lot = CharField(null=True)
    prior_qual = CharField(null=True)
    property_city = CharField(null=True)
    property_city_location_id = IntegerField(null=True)
    property_city_state_zip = CharField(null=True)
    property_class = CharField(null=True)
    property_class_category = CharField(null=True)
    property_class_description = CharField(null=True)
    property_class_name = CharField(null=True)
    property_class_short_name = CharField(null=True)
    property_img = CharField(null=True)
    property_location = CharField(null=True)
    property_location_normalized = CharField(null=True)
    property_mail_address = CharField(null=True)
    property_mail_address_id = IntegerField(null=True)
    property_mail_city = CharField(null=True)
    property_mail_cmra = CharField(null=True)
    property_mail_crrt = CharField(null=True)
    property_mail_deliverable = CharField(null=True)
    property_mail_dpv = CharField(null=True)
    property_mail_dpv_notes = CharField(null=True)
    property_mail_pbsa = CharField(null=True)
    property_mail_rdi = CharField(null=True)
    property_mail_state = CharField(null=True)
    property_mail_street = CharField(null=True)
    property_mail_vacant_status = CharField(null=True)
    property_mail_zip = CharField(null=True)
    property_owner_id = IntegerField(null=True)
    property_state = CharField(null=True)
    property_zip_code = CharField(null=True)
    rate_year = SmallIntegerField(null=True)
    ratio = DoubleField(null=True)
    ratio_year = SmallIntegerField(null=True)
    rental_estimate = DoubleField(null=True)
    rental_estimate_range_max = DoubleField(null=True)
    rental_estimate_range_min = DoubleField(null=True)
    rental_estimate_updated = DateTimeField(null=True)
    reverse_parties = CharField(null=True)
    rooftop_lat = DoubleField(null=True)
    rooftop_lng = DoubleField(null=True)
    sale_date = DateField(null=True)
    sale_price = IntegerField(null=True)
    senior_citizens_cnt = IntegerField(null=True)
    sewer_service_area_id = IntegerField(null=True)
    sewer_service_area_name = CharField(null=True)
    shard_num = IntegerField(null=True)
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
    water_provider_name = CharField(null=True)
    widows_cnt = IntegerField(null=True)
    yr_built = SmallIntegerField(null=True)
    yr_built_raw = CharField(null=True)
    zillow_pid = CharField(null=True)
    zone_id = IntegerField(null=True)
    zoning_code = CharField(null=True)
    zoning_description = CharField(null=True)

    class Meta:
        table_name = 'vw_property_master_details'
        schema = 'parcels'
        primary_key = False

class VwPropertyParcelNumbers(BaseModel):
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

class VwPropertySummary(BaseModel):
    acreage = DoubleField(null=True)
    block_id = IntegerField(null=True)
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
    property_city = CharField(null=True)
    property_class_code = CharField(null=True)
    property_class_name = CharField(null=True)
    property_class_short_name = CharField(null=True)
    property_id = IntegerField(null=True)
    property_location = CharField(null=True)
    property_location_normalized = CharField(null=True)
    property_state = CharField(null=True)
    property_zip = CharField(null=True)
    sale_date = DateField(null=True)
    sale_price = IntegerField(null=True)
    sq_ft = IntegerField(null=True)
    yr_built = SmallIntegerField(null=True)

    class Meta:
        table_name = 'vw_property_summary'
        schema = 'parcels'
        primary_key = False

class Walkabilities(BaseModel):
    bike_score = SmallIntegerField(null=True)
    block_id = IntegerField(unique=True)
    transit_score = SmallIntegerField(null=True)
    walk_score = SmallIntegerField(null=True)

    class Meta:
        table_name = 'walkabilities'
        schema = 'parcels'

