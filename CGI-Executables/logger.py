#!/usr/bin/env python3

import http.server
import socketserver
import urllib.request
import json
import	os
from urllib.parse import urlparse
from urllib.parse import parse_qs
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler

import	pickle
import	datetime

page_template_path		= "page_template/main_page.html"
error404_template_path	= "page_template/404.html"
image_folder			= "img"
default_image			= f"{image_folder}/default.png"
verbose					= True

visitors_data_file		= "data/visitors.pkl"

PORT = 8000

access_log_folder	= "access_log/"
access_log			= []

class Access:
    def __init__( self, query, time, ip_addr ):
        self.query		= query
        self.time		= time
        self.ip_addr	= ip_addr

class Visitor:
	def __init__( self, id, job = "未設定", prod = "未設定" ):
		self.tag_id		= id
		self.job_type	= job
		self.product	= prod
		
try:
	with open( visitors_data_file, "rb" ) as f:
		visitors	= pickle.load( f )
		print( f"previous '{visitors_data_file}' has been loaded" )
except:
	visitors	= {}

print( visitors )

with open( page_template_path, "r" ) as f:
	html_source 	= f.read()					

with open( error404_template_path, "r" ) as f:
	html404_source 	= f.read()					

class ActionHandler( BaseHTTPRequestHandler ):
	def do_GET( self ):
	
		cookies = SimpleCookie( self.headers.get( "Cookie" ) )
		parsed	= urlparse( self.path )
		query	= parse_qs( parsed.query )

		if ( verbose ):
			print( f"========== verbose print ==========" )
			print( f"parsed = {parsed}" )
			print( f"parsed.path = {parsed.path}" )
			print( f"query = {query}" )
		
		if parsed.path != "/action":
			file_path	= parsed.path[ 1: ]
			
			if not os.path.isfile( file_path ):
				self.send_response( 404 )
				self.send_header( "Content-Type", "text/html" )
				self.end_headers()
				self.wfile.write( html404_source.encode("utf-8") )
			else:
				try:
					content_type = {ext_content[ os.path.splitext( parsed.path )[ 1 ][ 1: ] ]}
				except KeyError:
					content_type  = "text/html"

				with open( file_path, "rb" ) as f:
					data 	= f.read()					

				print( f"ext_content = {ext_content[ os.path.splitext( parsed.path )[ 1 ][ 1: ] ]}" )
		
				self.send_response( 200 )
				self.send_header( "Content-Type", content_type )
				self.end_headers()
			
				self.wfile.write( data )

		else:
		
			print( "********** got access **********" )
			
			print( any( query ) )
			
			try:
#				filename    = f"{access_log_folder}{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f.log')}"
				print( access_log_folder + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f.log") )
				with open( access_log_folder + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f.log"), "wb" ) as f:
					pickle.dump( Access( query, datetime.datetime.now(), self.client_address[0] ), f )
					
			except:
			    print( "########## access loggging error" )

			tag_id		= cookie_and_query( "tag_id",         9999,      query, cookies )
			demo_id		= cookie_and_query( "demo_id",    "demo10",      query, cookies )
			user_name	= cookie_and_query( "user_name",     "none",     query, cookies )
			
			if tag_id not in visitors.keys():
				visitors[ tag_id ]	= Visitor( tag_id )

			visitor	= visitors[ tag_id ]

			try:
				visitor.job_type	= query[ "job_type" ][0]
				visitor.product		= query[ "product"  ][0]
				
				with open( visitors_data_file, "wb" ) as f:
					pickle.dump( visitors, f )
    				
			except:
				pass

			cookie_expire_seconds	= 3600 * 24 * 3
			cookies[ "tag_id"    ][ "max-age" ] = cookie_expire_seconds
			cookies[ "demo_id"   ][ "max-age" ] = cookie_expire_seconds
			cookies[ "user_name" ][ "max-age" ] = cookie_expire_seconds * 365

			self.send_response( 200 )
			self.send_header( "Set-Cookie", f"tag_id={tag_id};   path=/" )
			self.send_header( "Set-Cookie", f"demo_id={demo_id}; path=/" )
			self.send_header( "Set-Cookie", f"user_name={user_name}; path=/" )
			self.send_header( "Content-Type", "text/html" )
			self.end_headers()
			
			h	= html_source.replace( '===TAG_ID===', str( tag_id ) )
			h	= h.replace( '===DEMO_LIST===', demo_list( demo_id, 18 ) )
			h	= h.replace( '===USER_NAME===', user_name )
			h	= h.replace( '===JOB_TYPE===', visitor.job_type )
			h	= h.replace( '===PRODUCT===', visitor.product )

			image_file	= f"{image_folder}/{tag_id}.jpg"
			if not os.path.isfile( image_file ):
				image_file	= default_image
				
			h	= h.replace( '===IMAGE_FILE===', image_file )
			self.wfile.write( h.encode("utf-8") )

def cookie_and_query( key, default_value, q, c ):
	try:
		rv	= c[ key ].value
	except:
		rv	= None
	
	try:
		rv	= q[ key ][0]
	except:
		rv	= rv if rv else default_value
	
	c[ key ]	= rv
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

def main():
	with socketserver.TCPServer( ( "", PORT ), ActionHandler ) as httpd:		
		print("serving at port", PORT)
		httpd.serve_forever()

ext_content	= {	"css" : "text/css",
				"html": "text/html",
				"js"  : "text/javascript",
				"png" : "image/png",
				"jpg" : "image/jpg",
				"ico" : "image/ico",
				}	

if __name__ == "__main__":
	main()
