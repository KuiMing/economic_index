import pandas as pd

index_archive = pd.read_csv('economic_index.csv')
index_archive.loc[(index_archive.base_year == 2010) & (index_archive.economic == 'leading'), 'economic_index'] *= (107*(1-0.006) / 130.9)
index_archive.loc[(index_archive.base_year == 2004) & (index_archive.economic == 'leading'), 'economic_index'] *= (98.3954 * (1 - 0.005) / 105.5)
index_archive.loc[(index_archive.base_year == 2004) & (index_archive.economic == 'leading') & 
                  (index_archive.year_month < 201112), 
                  'economic_index'] *= (87.50988 * (1 - 0.004) / 109.5034)
index_archive.loc[(index_archive.base_year == 1996) & (index_archive.economic == 'leading'), 
                  'economic_index'] *= (75.34153 * (1 - 0.001) / 135)
index_archive.loc[(index_archive.base_year == 1996) & (index_archive.economic == 'leading') & 
                  (index_archive.year_month < 200506), 
                  'economic_index'] *= (76.77151 / 63.61387)

index_archive.loc[(index_archive.base_year == 2010) & (index_archive.economic == 'coincident'), 'economic_index'] *= 102.8 * (1 - 0.003) / 116.5
index_archive.loc[(index_archive.base_year == 2004) & (index_archive.economic == 'coincident'), 'economic_index'] *= 98.0048 * (1 - 0.002) / 110.7
index_archive.loc[(index_archive.base_year == 1996) & (index_archive.economic == 'coincident'), 'economic_index'] *= 94.62802 * (1 - 0) / 124.9

index_archive.loc[(index_archive.base_year == 2010) & (index_archive.economic == 'lagging'), 'economic_index'] *= 104 * (1 - 0.007) / 125.6
index_archive.loc[(index_archive.base_year == 2004) & (index_archive.economic == 'lagging'), 'economic_index'] *= 94.55637 * (1 - 0.003) / 125.4
index_archive.loc[(index_archive.base_year == 1996) & (index_archive.economic == 'lagging'), 'economic_index'] *= 83.89819 * (1 - 0.004) / 131.2
index_archive.loc[(index_archive.base_year == 1996) & (index_archive.economic == 'lagging') & 
                  (index_archive.year_month < 200506), 
                  'ecnomic_index'] *= (76.23813 * (1 - 0.003) / 63.56362)