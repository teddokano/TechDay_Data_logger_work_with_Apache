#!/usr/bin/env python3

import os
import cgi
from urllib.parse import parse_qs


page_template_path		= "page_template/upload_page.html"
upload_path				= "../Documents/img/"

MEGA		= 1048576

try:
	query	= parse_qs( os.environ[ "QUERY_STRING" ] )
except:
	pass

try:
	tag_id	= query[ "tag_id" ][ 0 ]
except:
	tag_id	= "Unknown_image"

with open( page_template_path, "r" ) as f:
	html_source 	= f.read()					

cgi.maxlen	= 400_000_000
form_data	= cgi.FieldStorage()
file_name	= f"{tag_id}.jpg"
full_path	= upload_path + file_name

with open( full_path, "wb" ) as uploaded_file:
	item = form_data[ "image" ]

	while True:
		chunk = item.file.read( MEGA )
		
		if not chunk:
			break
		
		uploaded_file.write( chunk )

h	= html_source.replace( '===TAG_ID===', str( tag_id ) )

print( "Content-Type: text/html\n" )
print( h )
