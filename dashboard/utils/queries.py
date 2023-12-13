#!/usr/bin/env phthon3

# group list
group_dict = {
    'group_1': ['organizations', 'organization_descriptions', 'org_parents'],
    'group_2': ['funding', 'funding_rounds'],
    'group_3': ['investment', 'investors', 'investment_partners'],
    'group_4': ['people', 'people_description', 'degrees'],
    'group_5': ['events', 'event_appearances'],
    'group_6': ['acquistions'],
    'group_7': ['category_groups'],
    'group_8': ['ipos']
}

# group_dict = {
#     'group_1': sort_org(),
#     'group_2': ['funding', 'funding_rounds'],
#     'group_3': ['investment', 'investors', 'investment_partners'],
#     'group_4': ['people', 'people_description', 'degrees'],
#     'group_5': ['events', 'event_appearances'],
#     'group_6': ['acquistions'],
#     'group_7': ['category_groups'],
#     'group_8': ['ipos']
# }

acqusisitions_num_query = '''
    SELECT o.uuid, count(o.uuid) num_acquisitions
    FROM (
        SELECT uuid, name
        FROM organization_merged_final
    ) AS o
    LEFT JOIN acquisitions_final a
    ON o.uuid = a.acquirer_uuid
    GROUP BY o.uuid;
'''
acquired_num_query = '''
    SELECT o.uuid, count(o.uuid) num_acquisitions
    FROM (
        SELECT uuid, name
        FROM organization_merged_final
    ) AS o
    LEFT JOIN acquisitions_final a
    ON o.uuid = a.acquiree_uuid
    GROUP BY o.uuid;
'''

graduate_freq_by_org = '''
    SELECT al.featured_job_organization_uuid, sum(al.num) / count(al.featured_job_organization_uuid) AS graduate_freq_by_org
    FROM (
        SELECT pdd.institution_uuid AS institution_uuid_backup, pdd.featured_job_organization_uuid, ic.num 
        FROM people_descriptions_degrees_final AS pdd 
        LEFT JOIN (
            SELECT institution_uuid, count(institution_uuid) AS num 
            FROM people_descriptions_degrees_final 
            GROUP BY institution_uuid
        ) AS ic 
        ON pdd.institution_uuid = ic.institution_uuid
    ) AS al 
    GROUP BY al.featured_job_organization_uuid;
'''

funding_by_types = '''
    SELECT org_uuid,  investment_type, SUM(raised_amount_usd) AS total_by_type
    FROM funding_rounds_final 
    GROUP BY org_uuid, investment_type
'''
funds_raised_by_average = '''
    SELECT entity_uuid, raised_amount_usd_x / count AS raised_usd_average 
    FROM funds_final
'''

ipos_query = '''
    SELECT org_uuid, stock_exchange_symbol, stock_symbol, went_public_on, share_price_usd, valuation_price_usd, money_raised_usd 
    FROM ipos_final
'''

# sql code doesnt work now
funding_by_types_pivot = '''
    SELECT * 
    FROM (
        SELECT org_uuid,  investment_type, raised_amount_usd 
        FROM funding_rounds_final
    ) t 
    PIVOT (
        SUM(raised_amount_usd) 
        FOR investment_type IN (
            [angel], 
            [series_a], 
            [series_b], 
            [series_c])
    ) AS pivot_table;
'''