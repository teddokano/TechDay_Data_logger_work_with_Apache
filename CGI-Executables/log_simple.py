#!/Library/WebServer/CGI-Executables/venv/bin/python3

import	os
import	sys
import	pandas as pd
import	openpyxl
import	pickle
from	urllib.parse import parse_qs
from	http.cookies import SimpleCookie

page_template_path	= "page_template/log_page.html"
access_log_folder	= "access_log/"
excel_output_file	= "../Documents/log.xlsx"

with open( page_template_path, "r" ) as f:
	html_source 	= f.read()					

class Access:
	def __init__( self, query, time, user_name, demo_id, ip_addr ):
		self.query		= query
		self.time		= time
		self.user_name	= user_name
		self.demo_id	= demo_id
		self.ip_addr	= ip_addr

files		= os.listdir( access_log_folder )
log_files	= [ f for f in files if f.endswith( ".log" ) == True ]

logs		= []

for f in log_files:
	try:
		print( f"loading: {f}  ", end = "" )
		with open( access_log_folder + f, "rb" ) as file:
			logs.append( pickle.load( file ) )

	except:
		pass


total_log	= pd.DataFrame()

for i in logs:	
	d	= { "time": i.time, "user_name": i.user_name, "demo_id": i.demo_id, "ip_addr": i.ip_addr }
	d.update( i.query )
	
	total_log	= pd.concat( [total_log, pd.DataFrame( d ) ] )

total_log.fillna( "", inplace = True )
total_log.sort_values( "time", ascending = False, inplace = True )

demo_id	= None
	
cookies	= SimpleCookie()
try:
	cookies.load( os.environ[ "HTTP_COOKIE" ] )
	demo_id	= cookies[ "demo_id" ].value
except:
	pass

try:
	query	= parse_qs( os.environ[ "QUERY_STRING" ] )
	demo_id	= query[ "demo_id" ][0]
	if demo_id == "all":
		demo_id	= None
except:
	pass

if demo_id is not None:
	total_log	= total_log[ total_log[ "demo_id" ] == demo_id ]
	demo_id	= f"filtered for {demo_id}"
else:
	total_log.to_excel( excel_output_file, sheet_name='new_sheet_name')
	demo_id = "all demo_id"
	
print( "Content-Type: text/html\n" )
h	= html_source.replace( "===DEBUG_INFO===", demo_id )
h	= h.replace( "===LOG_TABLE===",  total_log.to_html() )

if demo_id == "all demo_id":
	h	= h.replace( "===DOWNLOAD_LINK===", '<p><a href = "/log.xlsx">Download log file</a></p>' )
else:
	h	= h.replace( "===DOWNLOAD_LINK===", "" )

print( h )

