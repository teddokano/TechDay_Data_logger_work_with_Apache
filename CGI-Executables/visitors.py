#!/Library/WebServer/CGI-Executables/venv/bin/python3

import	os
import	sys
import	pandas as pd
import	openpyxl
import	pickle
from	urllib.parse import parse_qs
from	http.cookies import SimpleCookie

page_template_path	= "page_template/log_page.html"
visitors_data_file	= "data/visitors.pkl"
access_log_folder	= "access_log/"
image_folder_access	= "../Documents/img/"
excel_output_file	= "../Documents/visitors.xlsx"


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

try:
	with open( visitors_data_file, "rb" ) as f:
		visitors	= pickle.load( f )
except:
	visitors	= {}

total_log	= pd.DataFrame()

for k, v in visitors.items():
	d	= { "tag_id": k, "job_type": v.job_type, "product": v.product }
	total_log	= pd.concat( [total_log, pd.DataFrame( d, index = [ k ] ) ] )

total_log.fillna( "", inplace = True )
total_log.sort_values( "tag_id", ascending = False, inplace = True )

total_log.to_excel( excel_output_file, sheet_name='new_sheet_name')
demo_id	= ""

print( "Content-Type: text/html\n" )
h	= html_source.replace( "===DEBUG_INFO===", demo_id )
h	= h.replace( "===LOG_TABLE===",  scripts + total_log.to_html( classes = "my-table", index = False ) )
h	= h.replace( "===DOWNLOAD_LINK===", '<p><a href = "/visitors.xlsx">Download log file</a></p>' )

print( h )

