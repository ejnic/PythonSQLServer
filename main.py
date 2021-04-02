import pyodbc
import sqlalchemy as sal
import datetime
from sqlalchemy import create_engine
import pandas as pd
import connection as con
import sqlstrings as sql
import numpy as np

# engine = sal.create_engine('mssql+pyodbc://ads//ejnic' + ':' + con.strpassword + '@dev1.whedb.iu.edu/UAGrad_eDocs?driver=SQL+Server&authentication=ActiveDirectoryIntegrated')

enginemssql = sal.create_engine('mssql+pyodbc://@SQLServerPRD32')
engineora = sal.create_engine(con.strengineoracle)

dfenroute = pd.read_sql_query(sql.sqledocs, engineora)
dfenroute['prncpl_nm'] = dfenroute['prncpl_nm'].fillna('-')
dfenroute['grp_nm'] = dfenroute['grp_nm'].fillna('-')
dfenroute['qual_role_nm'] = dfenroute['qual_role_nm'].fillna('-')
dfpivot = pd.pivot_table(dfenroute, index=['doc_hdr_id', 'doc_typ_nm', 'doc_crte_dt', 'crte_dt', 'doc_mdfn_dt', 'actn_rqst_cd', 'prncpl_nm', 'grp_nm','qual_role_nm'], values=['fld_val'], columns='fld_nm', aggfunc='last')



dfpivot = dfpivot.reset_index()
dfpivot.index.rename('pyindex', inplace=True)
print(list(dfpivot.columns))

dfpivot.columns = ['doc_hdr_id', 'doc_typ_nm', 'doc_crte_dt', 'crte_dt', 'doc_mdfn_dt', 'actn_rqst_cd', 'prncpl_nm', 'grp_nm','qual_role_nm', 'campus', 'campusTitle', 'concentration1', 'concentration2', 'concentrationTrack', 'department', 'department1', 'department2', 'major', 'major1', 'major2', 'minor1', 'minor2']

dfpivot['department1'] = dfpivot['department1'].astype(str) + dfpivot['department'].astype(str)
dfpivot['major1'] = dfpivot['major1'].astype(str) + dfpivot['major'].astype(str)
dfpivot['department1'] = dfpivot['department1'].str.replace('nan', '')
dfpivot['major1'] = dfpivot['major1'].str.replace('nan', '')

dfpivot['dayscreated'] = ((datetime.datetime.now() - dfpivot['doc_crte_dt']).dt.days)
dfpivot['daysnotif'] = ((datetime.datetime.now() - dfpivot['crte_dt']).dt.days)
dfpivot['daysmod'] = ((datetime.datetime.now() - dfpivot['doc_mdfn_dt']).dt.days)

print(dfpivot.dtypes)


strdate = '{date:%Y%m%d}'.format( date=datetime.datetime.now())
dfenroute.to_excel(con.homepath + 'enrouteedocs_'+ strdate + '.xlsx')
dfpivot.to_excel(con.homepath + 'pivotenrouteedocs_'+ strdate + '.xlsx')

dfedocoutput = dfpivot[['doc_hdr_id', 'doc_typ_nm', 'doc_crte_dt', 'crte_dt', 'doc_mdfn_dt', 'actn_rqst_cd','prncpl_nm', 'grp_nm','qual_role_nm', 'campus', 'campusTitle', 'concentration1', 'concentration2', 'concentrationTrack', 'department1', 'department2', 'major1', 'major2', 'minor1', 'minor2', 'dayscreated', 'daysnotif', 'daysmod']]

dfedocoutput.to_sql("enrouteedocs", enginemssql, if_exists="replace", schema="dbo")


print(list(dfpivot.columns))