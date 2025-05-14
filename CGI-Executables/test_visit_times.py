#!/Library/WebServer/CGI-Executables/venv/bin/python3

import	pandas as pd

df	= pd.read_excel( "../Documents/log.xlsx" )
df.fillna( "", inplace = True )

df[ "tag_id" ] = df[ "tag_id" ].map( lambda x: int( x ) if type( x ) is float else x )

print( df[ "tag_id" ].astype( str ) )

pv	= pd.pivot_table( df, index = "tag_id", columns = "demo_id", values = "time", aggfunc = "count" )
pv.fillna( 0, inplace = True )

print( pv )

pv.replace( 0, "", inplace = True )
pv = pv.apply( lambda col: col.map( lambda x: 1 if x != "" else 0 ) )

pv[ "total" ] = pv.sum(axis=1)
print( pv )
