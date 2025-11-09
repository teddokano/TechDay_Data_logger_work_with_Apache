#!/Library/WebServer/CGI-Executables/venv/bin/python3

series_label	= "mm"
demo_name_list	= "./page_template/demo_list.txt"

id_valid_duration		= 3600 * 10
name_valid_duration		= 3600 * 24 * 365

import urllib.request
import json
import os
from urllib.parse import urlparse
from urllib.parse import parse_qs, quote_plus, unquote_plus
from http.cookies import SimpleCookie

import	pickle
import	datetime

from log import	*

page_template_path		= "page_template/main_page.html"
error404_template_path	= "page_template/404.html"
image_folder			= "/img/"
image_folder_access		= "../Documents/img/"
default_image			= f"{image_folder}default.png"
visitors_data_file		= "data/visitors.pkl"
access_log_folder		= "access_log/"
test_page_tag_id		= "test000"

class Access:
    def __init__( self, query, time, user_name, demo_id, ip_addr, serial ):
        self.query		= query
        self.time		= time
        self.user_name	= user_name
        self.demo_id	= demo_id
        self.ip_addr	= ip_addr
        self.serial		= serial

class Visitor:
	def __init__( self, visitor_count, job = "未設定", prod = "未設定" ):
		self.job_type	= job
		self.product	= prod
		self.serial		= 0
		
try:
	with open( visitors_data_file, "rb" ) as f:
		visitors	= pickle.load( f )
except:
	visitors	= {}

with open( page_template_path, "r" ) as f:
	html_source 	= f.read()					

def action():
	cookies	= SimpleCookie()
	
	try:
		cookies.load( os.environ[ "HTTP_COOKIE" ] )
	except:
		pass
			
	try:
		query	= parse_qs( os.environ[ "QUERY_STRING" ] )
	except:
		pass
		
	remote_addr	= os.environ[ "REMOTE_ADDR" ]
	
	tag_id		= cookie_and_query( "tag_id", "test000", query, cookies )
	serial		= cookie_and_query( "serial",    "none", query, cookies )
	demo_id		= cookie_and_query( "demo_id",   "none", query, cookies )
	user_name	= cookie_and_query( "user_name", "none", query, cookies )
	
	new_tag	= False
	
	if tag_id not in visitors.keys():
		visitors[ tag_id ]			= Visitor( tag_id )
		visitors[ tag_id ].serial	= series_label + str( len( visitors ) - 1 )	#	count start from 0, expecting to handle an ID for test
		new_tag						= True

	visitor	= visitors[ tag_id ]
	v_count	= len( visitors ) - 1	#	"-1" to exclude ID for test
	
	visitor_update	= False

	try:
		visitor.job_type	= query[ "job_type" ][0]
		visitor_update		= True
	except:
		pass
		
	try:
		visitor.product		= query[ "product"  ][0]
		visitor_update		= True
	except:
		pass
		
	if 	new_tag or visitor_update:
		try:
			with open( visitors_data_file, "wb" ) as f:
				pickle.dump( visitors, f )
		except:
			raise Exception( "########## vistors data saving error" )
		
	cookies[ "tag_id"    ][ "max-age" ] = id_valid_duration
	cookies[ "serial"    ][ "max-age" ] = id_valid_duration
	cookies[ "demo_id"   ][ "max-age" ] = id_valid_duration
	cookies[ "user_name" ][ "max-age" ] = name_valid_duration

	demo_visit_count	= demo_access_count( tag_id )

	print( cookies.output() )
	print( "Content-Type: text/html\n" )
	
	h	= html_source.replace( '===TAG_ID===', str( tag_id ) )
#	h	= h.replace( '===DEMO_LIST===',  demo_list( demo_id, 30 ) )
	h	= h.replace( '===DEMO_LIST===',  demo_list_from_file( demo_id, demo_name_list ) )
	h	= h.replace( '===USER_NAME===',  user_name )
	h	= h.replace( '===DEMO_ID===',    demo_id )
	h	= h.replace( '===JOB_TYPE===',   visitor.job_type )
	h	= h.replace( '===PRODUCT===',    visitor.product )
	h	= h.replace( '===SERIAL===',     visitor.serial )
	h	= h.replace( '===DEMO_COUNT===', demo_visit_count )
	h	= h.replace( '===VSTR_COUNT===', str( v_count ) )

	image_file	= f"{image_folder_access}{tag_id}.jpg"
	
	if os.path.isfile( image_file ):
		image_file	= f"{image_folder}{tag_id}.jpg"
	else:
		image_file	= default_image
		
	h	= h.replace( '===IMAGE_FILE===', image_file )
	
	if new_tag:
		h	= h.replace( '===DISPLAY_CONTROL===', "newTag" )
	else:
		h	= h.replace( '===DISPLAY_CONTROL===', "isFirstAccess" )
	
	h	= h.replace( '===DEBUG_INFO===', cookies.output() + "<br />" + f"{query}" + "<br />" + f"{os.environ}" + "<br />" +  f"{remote_addr}"  + "<br />" +  f"{image_file}" + "<br />" +  f"{default_image}" + "<br />" +  f"{tag_id}" + "<br />" + f"visitor_update={visitor_update}" )
	
	print( h )
	
	try:
		with open( access_log_folder + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f") + "_" + user_name + "_" + demo_id + ".log", "wb" ) as f:
			pickle.dump( Access( query, datetime.datetime.now(), user_name, demo_id, remote_addr, visitor.serial ), f )			
	except:
		raise Exception( "########## access loggging error" )

def cookie_and_query( key, default_value, q, c ):
	try:
		rv	= c[ key ].value
		rv	= unquote_plus( rv )	#	to handle multibyte-characters
	except:
		rv	= None
	
	try:
		rv	= q[ key ][0]
	except:
		rv	= rv if rv else default_value
	
	c[ key ]	= quote_plus( rv )	#	to handle multibyte-characters

	return rv

def demo_list( selected, length ):
	str_list    = []
	
	for i in range( 1, length ):
		id	= f"demo{i}"
		if selected == id:
			sel	= "selected"
		else:
			sel	= ""
    		
		str_list   += [ f'<option value= "{id}" {sel}>Demo {i}</option>' ]

	return "\n".join( str_list )

def demo_list_from_file( selected, file ):
	with open( file, encoding='utf-8' ) as f:
		demo_names	= [ f"demo{i}: {line.strip()}" for i, line in enumerate( f, start = 1 ) ]

	str_list    = []
	
	for i in range( 0, len( demo_names ) ):
		id	= f"demo{i + 1}"
		if selected == id:
			sel	= "selected"
		else:
			sel	= ""
    		
		str_list   += [ f'<option value= "{id}" {sel}>{demo_names[ i ]}</option>' ]

	return "\n".join( str_list )

def demo_access_count( tag_id ):

	log_data	= get_log_data()

	try:
		log_data[ "tag_id" ].map( lambda x: int( x ) if type( x ) is float else x )
	except:
		return "0"
		
	pv	= pd.pivot_table( log_data, index = "tag_id", columns = "demo_id", values = "time", aggfunc = "count" )
	pv	= pv.apply( lambda col: col.map( lambda x: 1 if (x != float( "NaN" )) and (x > 0) else 0 ) )
	pv.insert( 0, "total", pv.sum( axis = 1) )

	try:
		demo_visit_count	= pv[ "total" ][ tag_id ]
	except KeyError:
		return "0"

	return	demo_visit_count.astype( str )

def main():
	action()
	
if __name__ == "__main__":
	main()
