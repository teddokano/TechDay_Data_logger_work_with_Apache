#!/Library/WebServer/CGI-Executables/venv/bin/python3

import	os
import	sys
import	pandas as pd
import	openpyxl
import	pickle
from	urllib.parse import parse_qs
from	http.cookies import SimpleCookie

from log import	*

page_template_path	= "page_template/log_page.html"
visitors_data_file	= "data/visitors.pkl"
access_log_folder	= "access_log/"
image_folder_access	= "../Documents/img/"
image_folder_web	= "/img/"
excel_output_file	= "../Documents/visitors.xlsx"


def link_to_image( tag_id ):
	if os.path.isfile( f"{image_folder_access}{tag_id}.jpg" ):
		return f"<td><a href = '{image_folder_web}{tag_id}.jpg'>{k}<img src='{image_folder_web}{tag_id}.jpg' width='200' alt='{tag_id}'></td></a>"
	else:	
		return f"<td><a href = '{image_folder_web}{tag_id}.jpg'>{k}</td></a>"

scripts = """
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

with open( page_template_path, "r" ) as f:
	html_source 	= f.read()					

class Visitor:
	def __init__( self, id, job = "未設定", prod = "未設定" ):
		self.job_type	= job
		self.product	= prod
		self.serial		= 0

###
###	find visited demo
###

log_data	= get_log_data()

if ( any( log_data ) ):
	log_data[ "tag_id" ].map( lambda x: int( x ) if type( x ) is float else x )

	pv	= pd.pivot_table( log_data, index = "tag_id", columns = "demo_id", values = "time", aggfunc = "count" )
	pv	= pv.apply( lambda col: col.map( lambda x: 1 if (x != float( "NaN" )) and (x > 0) else 0 ) )
	pv.insert( 0, "total", pv.sum( axis = 1) )

###
### load visitor info
###

try:
	with open( visitors_data_file, "rb" ) as f:
		visitors	= pickle.load( f )
except:
	visitors	= {}

total_log	= pd.DataFrame()

if ( any( visitors ) ):
	for k, v in visitors.items():
		d	= { "tag_id": k, "serial": v.serial, "job_type": v.job_type, "product": v.product }
		total_log	= pd.concat( [total_log, pd.DataFrame( d, index = [ k ] ) ] )

	tags	= [ k for k in visitors.keys() ]

	total_log	= total_log.join( pv )
	total_log.fillna( "", inplace = True )
	total_log = total_log.apply( lambda col: col.map( lambda x: int( x ) if type( x ) is float else x ) )


	total_log.sort_values( "tag_id", ascending = False, inplace = True )
else:
	tags	= []

total_log.to_excel( excel_output_file, sheet_name='new_sheet_name')
demo_id	= ""

print( "Content-Type: text/html\n" )
h	= html_source.replace( "===DEBUG_INFO===", demo_id )
h	= h.replace( "===LOG_TABLE===",  scripts + total_log.to_html( classes = "my-table", index = False ) )
#h	= h.replace( "===LOG_TABLE===",  scripts + total_log.to_html( classes = "my-table", index = True ) )
h	= h.replace( "===DOWNLOAD_LINK===", '<p><a href = "/visitors.xlsx">Download log file</a></p>' )

for k in tags:
	h	= h.replace( f"<td>{k}</td>", link_to_image( k ) )

print( h )

