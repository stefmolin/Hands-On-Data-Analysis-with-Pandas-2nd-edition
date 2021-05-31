if __name__ == '__main__':

    #===== DP STATE data ========================
    # DP because this program loads only the "Data Profile" var's, not the DT's
    # States, not metros and not counties

    import requests
    import pandas as pd

    response = requests.get(
        'https://api.census.gov/data/2019/acs/acs5/profile?get=GEO_ID,NAME,DP02_0087E,DP02_0070PE,DP02_0067PE,DP02_0068PE,DP03_0003E,DP03_0004E,DP03_0088E,DP03_0025E,DP03_0062E,DP03_0009PE,DP03_0128PE,DP04_0089E,DP04_0134E&for=state:*')
    DPStates_list = response.json()
    # Get PR data that is missing from the above
    response = requests.get(
        'https://api.census.gov/data/2019/acs/acs5/profile?get=GEO_ID,NAME,DP02PR_0087E,DP02PR_0070PE,DP02PR_0067PE,DP02PR_0068PE&for=state:72')  # noqa
    DPPRState_list = response.json()
    # Strip the column titles off the top
    DPStates_list = DPStates_list[1:]
    # Now correct the PR data in the initial response
    DPStates_list.sort() #sorts by first field, which is geo_id, which puts PR last
    DPStates_list[-1][1:6] = DPPRState_list[1][1:6]  # replaces values in the last record

    DP_column_names_17 = (
        'geo_id', 'areaname_unused', 'population', 'vets', 'hs', 'bach', 'lf', 'employed', 'pcincome', 'travel', 'mincome',
        'unemp', 'poverty', 'housevalue', 'grossrent', 'stfips')

    DPStates_df = pd.DataFrame(DPStates_list, columns=DP_column_names_17)

    #so it matches final product, fill it out
    #  assign stfips value to new column acs_geo_id2.
    DPStates_df.insert(1, "acs_geo_id2", DPStates_df['stfips'].str.zfill(2))
    # assign constant state type id. Future improvement:  force this to be string, len 2.
    DPStates_df.insert(3,"areatype","01")
    # assign stfips value to new column area
    DPStates_df.insert(4, "areacode", DPStates_df['stfips'].str.zfill(6))

    #DPStates_df.to_csv("DPStates3.csv")

    # ===== DP COUNTY data ========================
    response = requests.get(
        'https://api.census.gov/data/2019/acs/acs5/profile?get=GEO_ID,NAME,DP02_0087E,DP02_0070PE,DP02_0067PE,DP02_0068PE,DP03_0003E,DP03_0004E,DP03_0088E,DP03_0025E,DP03_0062E,DP03_0009PE,DP03_0128PE,DP04_0089E,DP04_0134E&for=county:*')
    DPC_l = response.json()  # Data Profiles, Counties, List

    DP_cols_16 = (
        'geo_id', 'areaname_unused', 'population', 'vets', 'hs', 'bach', 'lf', 'employed', 'pcincome', 'travel', 'mincome',
        'unemp', 'poverty', 'housevalue', 'grossrent', 'stfips', 'areacode')
    DPC_l = DPC_l[1:]
    DPC_df = pd.DataFrame(DPC_l, columns=DP_cols_16)  # Data Profiles Counties Dataframe

    response = requests.get(
        'https://api.census.gov/data/2019/acs/acs5/profile?get=GEO_ID,NAME,DP02PR_0087E,DP02PR_0070PE,DP02PR_0067PE,DP02PR_0068PE&for=county:*&in=state:72')
    PRC_l = response.json()
    PR_cols = ('geo_id', 'areaname_unusedPR', 'population', 'vets', 'hs', 'bach', 'stfipsPR', 'areacodePR')
    PRC_l = PRC_l[1:]
    PRC_df = pd.DataFrame(PRC_l, columns=PR_cols)

    # Now we have 2 df's, merge them into one
    mergecounties = pd.merge(DPC_df, PRC_df, how='outer', on='geo_id')
    # create a new column that merges the way I want
    mergecounties['population'] = mergecounties['population_x'].where(mergecounties['population_y'].isnull(),
                                                                     mergecounties['population_y'])
    mergecounties['vets'] = mergecounties['vets_x'].where(mergecounties['vets_y'].isnull(),
                                                                mergecounties['vets_y'])
    mergecounties['hs'] = mergecounties['hs_x'].where(mergecounties['hs_y'].isnull(), mergecounties['hs_y'])
    mergecounties['bach'] = mergecounties['bach_x'].where(mergecounties['bach_y'].isnull(),
                                                                mergecounties['bach_y'])
    mergecounties.drop(
        ['population_x', 'population_y', 'vets_x', 'vets_y', 'hs_x', 'hs_y', 'bach_x', 'bach_y', 'stfipsPR',
         'areacodePR', 'areaname_unusedPR'], axis=1, inplace=True)
    # GREAT! I have 3220 rows (all counties), all the right columns, with PR data replacing the null PR values from broader API calls.
    # columns are not in the same order as the spreadsheet i should give to Othman.
    # don't yet have ID's composed.

    DPCounties_df = mergecounties
    # so it matches final product, fill it out
    #  assign stfips value to new column acs_geo_id2.
    DPCounties_df.insert(1, "acs_geo_id2", DPCounties_df['stfips'].str.zfill(2))
    # assign constant state type id. Future improvement:  force this to be string, len 2.
    DPCounties_df.insert(3, "areatype", "04")

    #DPCounties_df.to_csv("DPCounties2.csv")

    #===== DP METRO data ========================
    # Get metro data; must assign partial PR data to the right records

    response = requests.get(
        'https://api.census.gov/data/2019/acs/acs5/profile?get=GEO_ID,NAME,DP02_0087E,DP02_0070PE,DP02_0067PE,DP02_0068PE,DP03_0003E,DP03_0004E,DP03_0088E,DP03_0025E,DP03_0062E,DP03_0009PE,DP03_0128PE,DP04_0089E,DP04_0134E&for=metropolitan%20statistical%20area/micropolitan%20statistical%20area:*')
    DPMM_list = response.json()
    DPM_column_names = ['geo_id', 'areaname_unused', 'population', 'vets', 'hs', 'bach', 'lf', 'employed', 'pcincome',
                       'travel', 'mincome', 'unemp', 'poverty', 'housevalue', 'grossrent', 'areacode']
    DPMM_list = DPMM_list[1:]

    # now to pick up only Metro Areas, drop Micro Areas.
    DPMetro_list = []
    for i in range(len(DPMM_list)):
        if (DPMM_list[i][1].endswith('Metro Area')):
            DPMetro_list.append(DPMM_list[i])

    DPMetro_df = pd.DataFrame(DPMetro_list, columns=DPM_column_names)  # All Metros; PR have no data for 4 var's
    # 388 rows x 16 columns, with geo_id
    # The PR metros are missing 4 variables
    #DPMetro_df.to_csv("DPMetrospartial.csv")

    # ----------------Now for PR
    response = requests.get(
        'https://api.census.gov/data/2019/acs/acs5/profile?get=GEO_ID,NAME,DP02PR_0087E,DP02PR_0070PE,DP02PR_0067PE,DP02PR_0068PE&for=metropolitan%20statistical%20area/micropolitan%20statistical%20area:*')
    DPPRMM_list = response.json()
    DPPR_column_names = ['geo_idPR', 'areaname_unusedPR', 'population', 'vets', 'hs', 'bach', 'areacode']
    DPPRMM_list = DPPRMM_list[1:]  # ALL STATES, not just PR; but non-PR are null

    # now to pick up only Metro Areas, drop Micro Areas.
    DPPRMetro_list = []
    for PRi in range(len(DPPRMM_list)):
        if (DPPRMM_list[PRi][1].endswith('Metro Area')):
            DPPRMetro_list.append(DPPRMM_list[PRi])

    DPPRMetro_df = pd.DataFrame(DPPRMetro_list, columns=DPPR_column_names)  # All Metros; only PR have data

    # ----Merge PR data into the main table
    mergemetros = pd.merge(DPMetro_df, DPPRMetro_df, how='outer', on='areacode')
    # create a new column that merges the way I want
    mergemetros['population'] = mergemetros['population_x'].where(mergemetros['population_y'].isnull(),mergemetros['population_y'])
    mergemetros['vets'] = mergemetros['vets_x'].where(mergemetros['vets_y'].isnull(),mergemetros['vets_y'])
    mergemetros['hs'] = mergemetros['hs_x'].where(mergemetros['hs_y'].isnull(), mergemetros['hs_y'])
    mergemetros['bach'] = mergemetros['bach_x'].where(mergemetros['bach_y'].isnull(),mergemetros['bach_y'])
    mergemetros.drop(
        ['population_x', 'population_y', 'vets_x', 'vets_y', 'hs_x', 'hs_y', 'bach_x', 'bach_y',
         'geo_idPR','areaname_unusedPR'], axis=1, inplace=True)

    # so it matches final product, fill it out
    #  assign stfips value to new column acs_geo_id2.
    #  This will be complicated. It's not in the data from census. Have to do some string manipulation to find 2-char state, then lookup STFIPS
    #mergemetros.insert(1, "acs_geo_id2", "needed")
    mergemetros.insert(1, "acs_geo_id2", mergemetros['areacode'])
    #mergemetros.insert(17, "stfips", "needed")
    Rside = mergemetros['areaname_unused'].str.split(', ').str[1]
    mergemetros.insert(17, "ABBREV", Rside.str[:2])
    stfipstb = pd.read_csv('stfipstb.csv')
    mergedf = pd.merge(stfipstb, mergemetros, how='inner', on='ABBREV')
    mergedf.drop(['STNAME', 'ABBREV'], axis=1, inplace=True)
    mergedf.rename(columns={"STFIPS": "stfips"}, inplace=True)
    mergemetros = mergedf
    # assign constant state type id. Future improvement:  force this to be string, len 2.
    mergemetros.insert(3, "areatype", "21")

    #mergemetros.to_csv("DPMetros.csv")

    #==== DP ALL data ========================
    DPall = DPStates_df
    DPall = DPall.append(DPCounties_df, ignore_index=True)
    DPall = DPall.append(mergemetros, ignore_index=True)
    #DPall.to_csv("DPall.csv")

    #==== DT STATE Data =======================
    #def get_DT_state_data():

    response = requests.get(
        'https://api.census.gov/data/2019/acs/acs5?get=GEO_ID,NAME,B25071_001E,B25092_001E&for=state:*')
    DTStates_list = response.json()

    # DP_column_names = DPStates_list[0]
    DT_column_names = ['geo_id', 'areaname_unused', 'rentpct', 'ownerpct', 'stfips']
    DTStates_list = DTStates_list[1:]
    # print(DTStates_list[1])
    DTStates_df = pd.DataFrame(DTStates_list, columns=DT_column_names)

    # assign stfips value to new column area
    DTStates_df.insert(4, "areacode", DTStates_df['stfips'].str.zfill(6))

    #DTStates_df.to_csv("DTStates.csv")

    #==== DT COUNTY Data =======================
    response = requests.get(
        'https://api.census.gov/data/2019/acs/acs5?get=GEO_ID,NAME,B25071_001E,B25092_001E&for=county:*')
    DTCounties_list = response.json()

    DT_column_names = ['geo_id', 'areaname_unused', 'rentpct', 'ownerpct', 'stfips', 'areacode']
    DTCounties_list = DTCounties_list[1:]
    DTCounties_df = pd.DataFrame(DTCounties_list, columns=DT_column_names)
    #DTCounties_df.to_csv("DTCounties.csv")

    #==== DT METRO Data =======================
    # Get metro data; PR data is a non-issue
    response = requests.get(
        'https://api.census.gov/data/2019/acs/acs5?get=GEO_ID,NAME,B25071_001E,B25092_001E&for=metropolitan%20statistical%20area/micropolitan%20statistical%20area:*')
    DTMM_list = response.json()
    DTMM_list = DTMM_list[1:]

    # now to pick up only Metro Areas, drop Micro Areas.
    DTMetro_list = []
    for i in range(len(DTMM_list)):
        if (DTMM_list[i][1].endswith('Metro Area')):
            DTMetro_list.append(DTMM_list[i])

    DT_column_names = ['geo_id', 'areaname_unused', 'rentpct', 'ownerpct', 'areacode']
    DTMetro_df = pd.DataFrame(DTMetro_list, columns=DT_column_names)
    #DTMetro_df.to_csv("DTMetro.csv")

    DTall = DTStates_df
    DTall = DTall.append(DTCounties_df, ignore_index=True)
    DTall = DTall.append(DTMetro_df, ignore_index=True)
    #DTall.to_csv("DTall.csv")

    # Now we have ALL data combined into 2 df's; merge them into one
    acs = pd.merge(DTall, DPall, how='outer', on='geo_id')
    #stfips for DP metros needs to be preserved
    acs['stfips'] = acs['stfips_x'].where(acs['stfips_y'].isnull(), acs['stfips_y'])
    acs.drop(['stfips_x'], axis=1, inplace=True)
    acs.drop(['areaname_unused_y', 'stfips_y', 'areacode_y'], axis=1, inplace=True)

    #order columns according to prior years deliveries to DBA/Othman
    acs = acs[['geo_id', 'acs_geo_id2','stfips','areatype','areacode_x',
               'population','lf','employed','unemp','mincome','pcincome','poverty','hs',
               'bach','grossrent','rentpct','housevalue','ownerpct','travel','vets','areaname_unused_x']]
    acs.rename(columns={"geo_id": "ACS_GEO_ID"
                        , "acs_geo_id2": "ACS_GEO_ID2"
                        , "stfips":     "STFIPS"
                        , "areatype":   "AREATYPE"
                        , "areacode_x": "AREA"
                        , "population": "TOTAL_POPULATION"
                        , "lf":         "CIVILIAN_LABOR_FORCE"
                        , "employed":   "NUMBER_EMPLOYED"
                        , "unemp":      "UNEMPLOYMENT_RATE"
                        , "mincome":    "MEDIAN_HOUSEHOLD_INCOME"
                        , "pcincome":   "PER_CAPITA_INCOME"
                        , "poverty":    "POVERTY_RATE"
                        , "hs":         "HIGH_SCHOOL_GRADUATE"
                        , "bach":       "BACHELOR_DEGREE_GRADUATE"
                        , "grossrent":  "MEDIAN_GROSS_RENT"
                        , "rentpct":    "RENT_PERCENT_INCOME"
                        , "housevalue": "MEDIAN_HOUSING_VALUE"
                        , "ownerpct":   "OWNER_COST_PERCENT_INCOME"
                        , "travel":     "MEAN_TRAVEL_TIME_TO_WORK"
                        , "vets":       "CIVILIAN_VETERANS"
                        , "areaname_unused_x":   "AREANAME_UNUSED"
                        }, inplace=True)
    acs.to_csv("census_acs1519.Mar22 cvbnm.csv")
    #acs.to_excel("acs1519.xlsx")