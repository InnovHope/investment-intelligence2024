#from download_preprocess import get_path

# daily download api
bulk_download_link = 'https://api.crunchbase.com/bulk/v4/bulk_export.tar.gz?user_key='

# crunchbase automcomplete api link
api_ac_part_1 = 'https://api.crunchbase.com/api/v4/autocompletes?query='
api_ac_part_2 = '&collection_ids=organization.companies&user_key='

# entity lookup
card_ids = 'founders,raised_funding_rounds'
field_ids = 'categories,description,founded_on,website,facebook'
api_lookup_part_1 = 'https://api.crunchbase.com/api/v4/entities/organizations/'
api_lookup_part_2 = '?card_ids=' \
    + card_ids\
    + '&field_ids='\
    + field_ids \
    + '&user_key='

lookup_link = api_lookup_part_1 \
    + '416361c1-aa7c-8fce-1ab1-5d03b0f433bc'\
    + api_lookup_part_2
