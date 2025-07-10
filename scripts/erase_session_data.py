#!/usr/bin/env python3

import	os
import	subprocess
import	argparse
import	datetime

def main():
	commands	 = [ "./scripts/clone.py -z" ]
	commands	+= [ f"rm -f ./CGI-Executables/data/visitors.pkl" ]
	commands	+= [ f"rm -f ./CGI-Executables/access_log/*" ]
	commands	+= [ f"rm -f ./Documents/img/*" ]
	commands	+= [ f"cp ./Documents/default_img/default.png ./Documents/img/default.png" ]
	commands	+= [ f"cp ./Documents/default_img/test000.jpg ./Documents/img/test000.jpg" ]

	comm_exec( commands, not args.no_exec )


def comm_exec( commands, exe_flag ):
	for c in commands:
		print( "    executing command: " + c )

		if exe_flag:
			subprocess.run( c, shell = True )


def command_line_handling():
	parser	= argparse.ArgumentParser( description = "r01lib MCUXpresso project generator" )
	qv_grp	= parser.add_mutually_exclusive_group()
	
	qv_grp.add_argument( "-N", "--no_exec", help = "no execution",			action = "store_true" )
	
	return	parser.parse_args()

if __name__ == "__main__":
	args	= command_line_handling()
	
	if args.no_exec:
		exec	= False
	main()

