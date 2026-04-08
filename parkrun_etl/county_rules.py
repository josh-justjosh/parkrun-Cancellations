"""UK and Ireland county name normalisation for regional aggregates."""


def normalise_uk_ie_county(properties):
    """Mutate properties['County'] in place (England / Wales legacy groupings)."""
    if properties['County'] in [
            'Bedford', 'Central Bedfordshire', 'Luton']:
        properties['County'] = 'Bedfordshire'
    elif properties['County'] in ['Bracknell Forest', 'Reading', 'Slough', 'West Berkshire', 'Windsor and Maidenhead', 'Wokingham']:
        properties['County'] = 'Berkshire'
    elif properties['County'] in ['Buckinghamshire', 'Milton Keynes']:
        properties['County'] = 'Buckinghamshire'
    elif properties['County'] in ['Cambridgeshire', 'Peterborough']:
        properties['County'] = 'Cambridgeshire'
    elif properties['County'] in ['Cheshire East', 'Cheshire', 'Halton', 'Warrington']:
        properties['County'] = 'Cheshire'
    elif properties['County'] in ['Derbyshire', 'Derby']:
        properties['County'] = 'Derbyshire'
    elif properties['County'] in ['Devon', 'Plymouth', 'Torbay']:
        properties['County'] = 'Devon'
    elif properties['County'] in ['Dorset', 'Bournemouth, Christchurch and Poole Council']:
        properties['County'] = 'Dorset'
    elif properties['County'] in ['Durham', 'Darlington', 'Hartlepool', 'Stockton-on-Tees']:
        properties['County'] = 'Durham'
    elif properties['EventLongName'] in ['Tees Barrage parkrun', 'Billingham junior parkrun']:
        properties['County'] = 'Durham'
    elif properties['County'] in ['East Yorkshire', 'Kingston upon Hull']:
        properties['County'] = 'East Yorkshire'
    elif properties['County'] in ['East Sussex', 'Brighton and Hove']:
        properties['County'] = 'East Sussex'
    elif properties['County'] in ['Essex', 'Southend-on-Sea', 'Thurrock']:
        properties['County'] = 'Essex'
    elif properties['County'] in ['Gloucestershire', 'South Gloucestershire']:
        properties['County'] = 'Gloucestershire'
    # elif properties['County'] in ['City of Westminster', 'Kensington and Chelsea', 'Hammersmith and Fulham', 'Wandsworth', 'Lambeth', 'Southwark', 'Tower Hamlets', 'Hackney', 'Islington', 'Camden', 'Brent', 'Ealing', 'Hounslow', 'Richmond upon Thames', 'Kingston upon Thames', 'Merton', 'Sutton', 'Croydon', 'Bromley', 'Lewisham', 'Greenwich', 'Bexley', 'Havering', 'Barking and Dagenham', 'Redbridge', 'Newham', 'Waltham Forest', 'Haringey', 'Enfield', 'Barnet', 'Harrow', 'Hillingdon']:
        # properties['County'] = 'Greater London'
        # pass
    elif properties['County'] in ['Manchester', 'Bolton', 'Stockport', 'Tameside', 'Oldham', 'Rochdale', 'Bury', 'Bolton', 'Wigan', 'Salford', 'Trafford']:
        properties['County'] = 'Greater Manchester'
    elif properties['County'] in ['Liverpool', 'Wirral', 'Knowsley', 'Sefton', 'St. Helens']:
        properties['County'] = 'Merseyside'
    elif properties['County'] in ['Hampshire', 'Portsmouth', 'Southampton']:
        properties['County'] = 'Hampshire'
    elif properties['County'] in ['Kent', 'Medway']:
        properties['County'] = 'Kent'
    elif properties['County'] in ['Blackburn with Darwen', 'Blackpool', 'Lancashire']:
        properties['County'] = 'Lancashire'
    elif properties['County'] in ['Leicestershire', 'Leicester']:
        properties['County'] = 'Leicestershire'
    elif properties['County'] in ['Lincolnshire', 'North Lincolnshire', 'North East Lincolnshire']:
        properties['County'] = 'Lincolnshire'
    elif properties['County'] in ['Middlesbrough', 'North Yorkshire', 'Redcar and Cleveland', 'York']:
        properties['County'] = 'North Yorkshire'
    elif properties['County'] in ['Nottinghamshire', 'Nottingham']:
        properties['County'] = 'Nottinghamshire'
    elif properties['County'] in ['Shropshire', 'Telford and Wrekin']:
        properties['County'] = 'Shropshire'
    elif properties['County'] in ['Bath and North East Somerset', 'North Somerset', 'Somerset']:
        properties['County'] = 'Somerset'
    elif properties['County'] in ['Barnsley', 'Doncaster', 'Rotherham', 'Sheffield']:
        properties['County'] = 'South Yorkshire'
    elif properties['County'] in ['Staffordshire', 'Stoke-on-Trent']:
        properties['County'] = 'Staffordshire'
    elif properties['County'] in ['Gateshead', 'Newcastle upon Tyne', 'North Tyneside', 'South Tyneside', 'Sunderland']:
        properties['County'] = 'Tyne and Wear'
    elif properties['County'] in ['Birmingham', 'Wolverhampton', 'Dudley', 'Walsall', 'Sandwell', 'Solihull', 'Coventry']:
        properties['County'] = 'West Midlands'
    elif properties['County'] in ['Leeds', 'Wakefield', 'Kirklees', 'Calderdale', 'Bradford']:
        properties['County'] = 'West Yorkshire'
    elif properties['County'] in ['Swindon', 'Wiltshire']:
        properties['County'] = 'Wiltshire'
    # Wales
    elif properties['County'] in ['Conwy', 'Denbighshire', 'Flintshire', 'Wrexham']:
        properties['County'] = 'Clwyd'
    elif properties['County'] in ['Carmarthenshire', 'Ceredigion', 'Pembrokeshire']:
        properties['County'] = 'Dyfed'
    elif properties['County'] in ['Blaenau Gwent', 'Caerphilly', 'Monmouthshire', 'Newport', 'Torfaen County Borough']:
        properties['County'] = 'Gwent'
    elif properties['County'] in ['Gwynedd', 'Anglesey']:
        properties['County'] = 'Gwynedd'
    elif properties['County'] in ['County Borough of Bridgend', 'Merthyr Tydfil', 'Rhondda Cynon Taf']:
        properties['County'] = 'Mid Glamorgan'
    elif properties['County'] in ['Cardiff', 'Vale of Glamorgan']:
        properties['County'] = 'South Glamorgan'
    elif properties['County'] in ['Neath Port Talbot', 'City and County of Swansea']:
        properties['County'] = 'West Glamorgan'
