#!/opt/homebrew/bin/python3

import os
from urllib.parse import parse_qs

print( 'Content-Type: text/html\n\n' )
print( "QUERY_STRING: " )
print( os.environ['QUERY_STRING'] )
print( "<br />\n" )

qs_d = parse_qs( os.environ['QUERY_STRING'] )
print( "qs_d:" )
print( qs_d )
print( "\n" )
