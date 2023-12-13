# this file contains the feature columns of each groups for 
# sorted the original data

# group 1
# organizations, organization_descriptions, org_parents
organization_columns_sorted = [
    'uuid', 'name_x', 'type_x', 'permalink_x', 'cb_url_x', 'legal_name', 
    'roles', 'domain','homepage_url', 'email', 'phone', 'facebook_url', 
    'linkedin_url', 'twitter_url', 'logo_url', 'country_code', 
    'state_code', 'region', 'city', 'address', 'postal_code', 'status', 
    'primary_role', 'category_list', 'category_groups_list', 
    'short_description', 'description', 'employee_count', 
    'num_funding_rounds', 'total_funding_usd', 'founded_on', 
    'last_funding_on', 'closed_on', 'num_exits', 'parent_uuid', 
    'parent_name', 'alias1', 'alias2', 'alias3'
]
# group 2
funding_rounds_columns_sorted = [
    'org_uuid', 'org_name', 
    'country_code', 'state_code', 'region', 'city', 
    'investment_type', 'announced_on', 'raised_amount_usd', 
    'post_money_valuation_usd', 'lead_investor_uuids', 
    'lead_investor_1st', 'investor_count', 'entity_uuid', 
    'entity_name', 'entity_type', 'raised_amount_usd_x', 'count'
]

funds_columns_sorted = [
    'entity_uuid', 'entity_name', 'entity_type', 
    'raised_amount_usd_x', 'count'
]
# group 3
group_3_columns_dropped = [
    'permalink', 'cb_url', 'rank', 'created_at', 'updated_at'
]

partners_investors_columns_sorted = [
    'uuid', 'name', 'type', 'funding_round_uuid_x', 'funding_round_name_x', 
    'investor_uuid_x', 'investor_name_x', 'investor_type', 'is_lead_investor', 
    'partner_uuid', 'partner_name', 'uuid_y', 'name_y', 'type_y', 'roles', 
    'country_code', 'state_code', 'region', 'city', 
    'investor_types', 'investment_count', 
    'facebook_url', 'linkedin_url', 'twitter_url', 'logo_url'
]

investors_investors_columns_sorted = [
    'uuid', 'name', 'type', 'funding_round_uuid_x', 'funding_round_name_x', 
    'investor_uuid_x', 'investor_name_x', 'investor_type', 'is_lead_investor', 
    'partner_uuid', 'partner_name', 'uuid_y', 'name_y', 'type_y', 'roles', 
    'domain', 'country_code', 'state_code', 'region', 'city', 
    'investor_types', 'investment_count', 
    'total_funding_usd', 'founded_on', 'closed_on', 
    'facebook_url', 'linkedin_url', 'twitter_url', 'logo_url'
]
# group 4
group_4_columns_dropped = [
    'permalink', 'cb_url', 'rank', 'created_at', 'updated_at'
]
people_descriptions_columns_sorted = [
    'uuid', 'type_x', 'name_x', 'gender', 'description', 'country_code', 
    'state_code', 'region', 'city', 'featured_job_organization_uuid', 
    'featured_job_organization_name', 'featured_job_title', 
    'facebook_url', 'linkedin_url', 'twitter_url', 'logo_url'
]
people_descriptions_degrees_columns_sorted = [
    'uuid_x', 'type_x', 'name_x', 'gender', 'description', 
    'country_code', 'state_code', 'region', 'city', 
    'featured_job_organization_uuid', 'featured_job_organization_name', 
    'featured_job_title', 'facebook_url', 'linkedin_url', 'twitter_url', 
    'logo_url', 'institution_uuid', 'institution_name', 'degree_type', 
    'subject', 'started_on', 'completed_on', 'is_completed'
]
# group 5
group_5_columns_dropped = [
    'permalink', 'cb_url', 'rank', 'created_at', 'updated_at'
]
events_appearances_columns_sorted = [
    'uuid_x', 'name_x', 'type_x', 'event_uuid', 'event_name',
    'participant_uuid', 'participant_name', 'participant_type',
    'appearance_type', 'short_description_y', 'description', 
    'started_on', 'ended_on', 
    'venue_name',  'country_code', 'state_code', 'region', 'city', 
    'logo_url', 'event_roles'
]

# group 6
acquisitions_columns_sorted = [
    'uuid', 'name', 'type','acquiree_uuid', 'acquiree_name', 
    'acquiree_country_code', 'acquiree_state_code', 'acquiree_region', 
    'acquiree_city', 'acquirer_uuid', 'acquirer_name', 
    'acquirer_country_code', 'acquirer_state_code', 'acquirer_region', 
    'acquirer_city', 'acquisition_type', 'acquired_on', 'price_usd'
]

# group 7
category_groups_columns_sorted = [
    'uuid', 'name', 'type', 'category_groups_list'
]

# group 8
group_8_columns_dropped = [
    'uuid', 'name', 'type', 'permalink', 'cb_url', 'rank', 
    'created_at', 'updated_at', 'org_cb_url', 'share_price', 
    'share_price_currency_code', 'valuation_price', 
    'valuation_price_currency_code', 'money_raised', 
    'money_raised_currency_code'
]

# data for ml
df_columns_dropped = [
    'alias1', 'alias2', 'alias3', 'featured_job_organization_uuid'
]
# query columns
acquisition_num_columns = ['uuid', 'acquisition_num']
acquired_num_columns = ['uuid', 'acquired_num']
graduate_freq_columns = [
    'featured_job_organization_uuid', 'graduate_freq_by_org'
]
ipos_columns = [
    'org_uuid', 'stock_exchange_symbol', 'stock_symbol', 
    'went_public_on', 'share_price_usd', 'valuation_price_usd', 
    'money_raised_usd'
]
funding_by_type_columns = [
    'org_uuid', 'investment_type', 'total_by_type'
]
ml_columns = [
    'uuid', 'name', 'roles', 
    'country_code', 'state_code', 'region', 'city', 'address', 'status', 
    'primary_role',
    'category_list', 'category_groups_list', 'employee_count', 
    'num_funding_rounds', 'total_funding_usd', 
    'founded_on', 'last_funding_on', 'closed_on', 'went_public_on', 'num_exits', 
    'acquisition_num', 'acquired_num', 
    'graduate_freq_by_org', 
    'angel','convertible_note', 'corporate_round', 'debt_financing',
    'equity_crowdfunding', 'grant', 'initial_coin_offering',
    'non_equity_assistance', 'post_ipo_debt', 'post_ipo_equity',
    'post_ipo_secondary', 'pre_seed', 'private_equity',
    'product_crowdfunding', 'secondary_market', 'seed', 'series_a',
    'series_b', 'series_c', 'series_d', 'series_e', 'series_f', 'series_g',
    'series_h', 'series_i', 'series_j', 'series_unknown', 'undisclosed',
    'stock_exchange_symbol', 'stock_symbol', 
    'share_price_usd', 'valuation_price_usd', 'money_raised_usd'
]
# df_all columns
columns_string = [
    'uuid', 'name', 'type', 'permalink', 'cb_url', 'legal_name', 
    'roles', 'domain', 'homepage_url', 'email', 'phone', 
    'facebook_url', 'linkedin_url', 'twitter_url', 'logo_url', 
    'country_code', 'state_code', 'region', 'city', 'address', 
    'status', 'primary_role', 'category_list', 
    'category_groups_list', 'short_description','description',
    'parent_uuid', 'parent_name','org_uuid_x','org_uuid_y', 
    'stock_exchange_symbol', 'stock_symbol', 'employee_count',
    'postal_code'
]
columns_numeric = [
    'num_funding_rounds', 'total_funding_usd', 
    'num_exits', 'acquisition_num', 'acquired_num', 
    'graduate_freq_by_org', 'angel','convertible_note', 
    'corporate_round', 'debt_financing', 'equity_crowdfunding', 
    'grant', 'initial_coin_offering', 'non_equity_assistance', 
    'post_ipo_debt', 'post_ipo_equity', 'post_ipo_secondary', 
    'pre_seed', 'private_equity', 'product_crowdfunding', 
    'secondary_market', 'seed', 'series_a', 'series_b', 
    'series_c', 'series_d', 'series_e', 
    'series_f', 'series_g', 'series_h', 'series_i', 'series_j', 
    'series_unknown', 'undisclosed','share_price_usd', 
    'valuation_price_usd', 'money_raised_usd'
]
columns_date = [
    'founded_on', 'last_funding_on', 'closed_on','went_public_on'
]


# ml training
numerical_features = [
    'num_funding_rounds', 'total_funding_usd', 'num_exits', 
    'acquisition_num', 'acquired_num', 'graduate_freq_by_org', 
    'share_price_usd', 'valuation_price_usd', 'money_raised_usd'
]

freqs_features = [
    'country_code', 'state_code', 'region', 'city', 
    'employee_count'
]

funding_features = [
    'angel', 'convertible_note', 'corporate_round',
    'debt_financing', 'equity_crowdfunding', 'grant',
    'initial_coin_offering', 'non_equity_assistance', 'post_ipo_debt',
    'post_ipo_equity', 'post_ipo_secondary', 'pre_seed', 
    'private_equity','product_crowdfunding', 'secondary_market', 
    'seed', 'series_a', 'series_b', 'series_c', 'series_d', 'series_e', 
    'series_f', 'series_g','series_h', 'series_i', 'series_j', 
    'series_unknown', 'undisclosed'
]

time_features = [
    'founded_on', 'last_funding_on', 'closed_on', 'went_public_on'
]

all_features_ml = numerical_features \
    + freqs_features \
    + funding_features \
    + time_features

# ml focused categories
focus_categories = [
    'agriculture', 'biotechnology', 'health care', 'food', 'beverage',
    'science', 'engineering'
]

# statistic features
options_funding_features = [
    'num_funding_rounds', 'total_funding_usd', 'share_price_usd', 
    'valuation_price_usd', 'money_raised_usd', 'angel', 
    'convertible_note', 'corporate_round',
    'debt_financing', 'equity_crowdfunding', 'grant',
    'initial_coin_offering', 'non_equity_assistance', 'post_ipo_debt',
    'post_ipo_equity', 'post_ipo_secondary', 'pre_seed', 
    'private_equity','product_crowdfunding', 'secondary_market', 
    'seed', 'series_a', 'series_b', 'series_c', 'series_d', 'series_e', 
    'series_f', 'series_g','series_h', 'series_i', 'series_j', 
    'series_unknown', 'undisclosed'
]
options_categorical_features = [
    'country_code', 'state_code', 'region', 'city', 'status'
]
options_time_features = time_features
