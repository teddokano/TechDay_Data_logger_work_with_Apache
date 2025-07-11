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

scripts_net = """
    <link href="https://cdnjs.cloudflare.com/ajax/libs/foundation/6.4.3/css/foundation.min.css" rel="stylesheet"/>
    <link href="https://cdn.datatables.net/v/zf/jq-3.6.0/dt-1.13.4/b-2.3.6/b-html5-2.3.6/date-1.4.1/fh-3.3.2/sb-1.4.2/datatables.min.css" rel="stylesheet"/>
 
    <script src="https://cdn.datatables.net/v/zf/jq-3.6.0/dt-1.13.4/b-2.3.6/b-html5-2.3.6/date-1.4.1/fh-3.3.2/sb-1.4.2/datatables.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/foundation/6.4.3/js/foundation.min.js"></script>

    <script>
        $(document).ready(function() {$('.my-table').DataTable({
            select: true,
            displayLength: 25,
            buttons: ['copy'],
            fixedHeader: true,
            dom: 'iQrtBlp',
        });})
    </script>
"""
# https://qiita.com/TKfumi/items/05fc0208014a83fb8079
scripts = """
    <link href="/styles/foundation.min.css" rel="stylesheet"/>
    <link href="/styles/datatables.min.css" rel="stylesheet"/>
 
    <script src="/styles/datatables.min.js"></script>
    <script src="/styles/foundation.min.js"></script>

    <script>
        $(document).ready(function() {$('.my-table').DataTable({
            select: true,
            displayLength: 25,
            buttons: ['copy'],
            fixedHeader: true,
            dom: 'iQrtBlp',
        });})
    </script>
"""


class Access:
    def __init__( self, query, time, user_name, demo_id, ip_addr, serial ):
        self.query		= query
        self.time		= time
        self.user_name	= user_name
        self.demo_id	= demo_id
        self.ip_addr	= ip_addr
        self.serial		= serial

def get_log_data( path = access_log_folder ):
	files		= os.listdir( path )
	log_files	= [ access_log_folder + f for f in files if f.endswith( ".log" ) == True ]

	logs		= []
	
	for f in log_files:
		with open( f, "rb" ) as file:
			logs.append( pickle.load( file ) )

	total_log	= pd.DataFrame()

	for i in logs:	
		d	= { "time": i.time, "user_name": i.user_name, "demo_id": i.demo_id, "ip_addr": i.ip_addr, "serial": i.serial }
		d.update( i.query )
		
		total_log	= pd.concat( [total_log, pd.DataFrame( d, index = [ 0 ] ) ] )

	total_log.fillna( "", inplace = True )

	return total_log
	

def get_log():

	###
	### page preparation
	###
	
	with open( page_template_path, "r" ) as f:
		html_source 	= f.read()					

	
	###
	### get log data
	###
	
	total_log	= get_log_data()
	
	if ( any( total_log ) ):
		total_log.sort_values( "time", ascending = False, inplace = True )


	###
	### check own demo_id and filter log if needed
	###
	
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
#		total_log.to_excel( excel_output_file, sheet_name='new_sheet_name', index = False )
		total_log.to_excel( excel_output_file, index = False )
		demo_id = "all demo_id"
	
	
	###
	### html generation
	###
		
	print( "Content-Type: text/html\n" )
	h	= html_source.replace( "===DEBUG_INFO===", demo_id )
	h	= h.replace( "===LOG_TABLE===",  scripts + total_log.to_html( classes = "my-table", index = False ) )

	if demo_id == "all demo_id":
		h	= h.replace( "===DOWNLOAD_LINK===", '<p><a href = "/log.xlsx">Download log file</a></p>' )
	else:
		h	= h.replace( "===DOWNLOAD_LINK===", "" )

	###
	### html output
	###
		
	print( h )


def main():
	get_log()
	
if __name__ == "__main__":
	main()
