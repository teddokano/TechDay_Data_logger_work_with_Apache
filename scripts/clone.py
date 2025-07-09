#!/usr/bin/env python3

import	os
import	subprocess
import	argparse
import	datetime

clone_source		= "/Library/WebServer"
clone_target		= f"~/Desktop/techday_clone_{ datetime.datetime.today().strftime( '%Y-%m-%d_%H-%M-%S-%f' ) }"

def main():
	commands	 = []
	commands	+= [ f"cp -p -r {clone_source}/ {clone_target}/" ]

	if args.zipfile:
		commands	+= [ f"zip -r {clone_target}.zip {clone_target}/ > /dev/null" ]
		commands	+= [ f"rm -rf {clone_target}/" ]

	comm_exec( commands, not args.no_exec )


def comm_exec( commands, exe_flag ):
	for c in commands:
		print( "    executing command: " + c )

		if exe_flag:
			subprocess.run( c, shell = True )

def command_line_handling():
	parser	= argparse.ArgumentParser( description = "r01lib MCUXpresso project generator" )
	qv_grp	= parser.add_mutually_exclusive_group()
	
	parser.add_argument( "-z", "--zipfile",	help = "output in zip file", 	action = "store_true" )
	qv_grp.add_argument( "-d", "--delete", 	help = "delete session data",	action = "store_true" )
	qv_grp.add_argument( "-k", "--keep", 	help = "keep session data",		action = "store_true" )
	qv_grp.add_argument( "-N", "--no_exec", help = "no execution",			action = "store_true" )
	
	return	parser.parse_args()

if __name__ == "__main__":
	args	= command_line_handling()
	
	if args.no_exec:
		exec	= False
	main()

