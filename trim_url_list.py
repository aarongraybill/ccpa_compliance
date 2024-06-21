import pandas as pd

# Downloaded from https://majestic.com/reports/majestic-million
# 2024-June-18th 5pm (links will change in the future)
df = pd.read_csv('input_data/majestic_million.csv')

# Here we're essentially converting the global rank into a percentile by
# asking how many rows there are, dividing that by 100 to get group size
# and then splitting by row into groups of the size previously determined
df['GlobalRank_percentile'] = (df['GlobalRank']-1) // (df.shape[0] // 100)

df.groupby(['TLD']).agg({'GlobalRank':'mean'}).sort_values(['GlobalRank'])

# Only TLDs from common US sites
# https://www.onlydomains.com/blog/10-most-popular-domain-hacks/
tld_whitelist = [
    '.co',
    '.me',
    '.it',
    '.gg',
    '.io',
    '.ai',
    '.vc',
    '.ly',
    '.in',
    '.tv',
    '.to',
    '.is',
    '.am',
    '.fm'
]

# Get all of TLDs primarily associated with a specific country
tld_url = 'https://en.wikipedia.org/w/index.php?title=Country_code_top-level_domain&oldid=1227340805#Unconventional_usage'
country_tlds = pd.read_html(tld_url,match = 'Commonly used for academic websites')[0]

# Any TLD country-specific that's not white listed will be blacklisted
tld_blacklist = {s for s in country_tlds['Name[3]'].values}.difference(tld_whitelist)
# remove the "." in ".ru" leaving just "ru" 
tld_blacklist = {s[1:] for s in tld_blacklist}

# remove any rows with country-specific TLDs
df_us_tlds = df[~df.TLD.isin(tld_blacklist)]

# Get 10 rows from each group
df_sample = df_us_tlds.groupby(['GlobalRank_percentile']).sample(n=10, random_state=314159)

# 
df_sample.to_csv('input_data/1k_trim_majestic_million.csv')