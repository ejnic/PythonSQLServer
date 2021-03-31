import pyodbc
server = 'dev1.whedb.iu.edu'
database = 'UAGrad_eDocs'
cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes')
#cursor = cnxn.cursor()
#cursor.execute('SELECT top 1 * FROM [DBNAME].[SchemaNAME].[YourTable]')
#for row in cursor:
#    print(row)