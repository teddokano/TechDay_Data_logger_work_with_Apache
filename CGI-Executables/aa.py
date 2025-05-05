#!/usr/bin/env python3

import urllib.request
import json
import	os
from urllib.parse import urlparse
from urllib.parse import parse_qs
from http.cookies import SimpleCookie

import	pickle
import	datetime

#page_template_path		= "page_template/main_page.html"
page_template_path		= "main_page.html"
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
except:
	visitors	= {}

try:
	with open( page_template_path, "r" ) as f:
		html_source 	= f.read()					
except:
	html_source	= "AAA"
	



def action():

	print( "Content-Type: text/html\n\n" )

	"""
	print( "Set-Cookie: test0=0;       path=/" )
	print( "Set-Cookie: test1=1;       path=/" )
	print( "Set-Cookie: test2=2;       path=/" )
	"""
	"""
	print( "Set-Cookie: tag_id={tag_id};       path=/" )
	print( "Set-Cookie: demo_id={demo_id};     path=/" )
	print( "Set-Cookie: user_name={user_name}; path=/" )
	"""
#	print()
	
	h	= html_source.replace( '===TAG_ID===', 'TEST' )

#	print( h.encode("utf-8") )
	print( h )

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
	action()
	
if __name__ == "__main__":
	main()
