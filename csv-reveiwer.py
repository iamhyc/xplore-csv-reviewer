
import csv
import sys
from os import path, system
from termcolor import colored, cprint
from optparse import OptionParser
from pynput import keyboard
'''
0x0 Get CSV Parsed
0x1 Get Rows and Columns
0x2 First Row is title; Column Number selected for display
0x3 in-time parse the remaining list, and keep record
0x4 item view/list view
'''
global f, r, titles, num_arr, curr_pos
COLRS_NUM = 6
COLRS = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']

def toBitArray(n):
	return [1 if x=='1' else 0 for x in bin(n)[2:]]

def fromNumArray(num_arr):
	n = 0
	for x in num_arr:
		n |= (1<<x)
	return n

def m_cls(hlp=''):
	t = system('clear')
	print(hlp)
	pass

def list_view(key):
	global curr_pos
	#less-like list view
	pass

def item_view(key):
	global prev_pos, curr_pos, f, r, num_arr, jumped_list
	prev_pos = curr_pos
	jumps_len = len(jumped_list)

	if key==keyboard.Key.left:
		curr_pos = (curr_pos-1) if curr_pos>0 else 0
		pass
	elif key==keyboard.Key.right:
		curr_pos = (curr_pos+1) if curr_pos<jumps_len-2 else jumps_len-1
		pass
	elif key==keyboard.Key.page_up:
		curr_pos = (curr_pos-10) if curr_pos>10 else 0
		pass
	elif key==keyboard.Key.page_down:
		curr_pos = (curr_pos+10) if curr_pos<jumps_len-11 else jumps_len-1
		pass
	
	if prev_pos!=curr_pos:
		m_cls('(LeftArrow and RightArrow for navigation; PageUp and PageDown for 10 items)')
		f.seek(jumped_list[curr_pos])
		t = r.next()
		txt = ['\t\t\t\t[Item-%d/%d]'%(curr_pos, jumps_len)]
		for i,x in enumerate(num_arr):
			txt.append(colored(t[x], COLRS[i%COLRS_NUM]))
			pass
		txt.append('> ')
		sys.stdout.write('\n'.join(txt))
		sys.stdout.flush()
		pass
	pass

def main(options, args):
	global f, r, prev_pos, curr_pos, num_arr
	curr_pos = options.curr_pos + 1
	## setup csv file
	csvfile = './export.csv'
	if len(args) and path.isfile(args[0]) and ('csv' in path.basename(args[0])):
		csvfile = args[0]
		pass

	f = open(csvfile, 'rb')
	r = csv.reader(iter(f.readline, ''), dialect='excel')
	
	titles = r.next()

	## set display columns
	if options.numbers>0:
		num_arr = toBitArray(options.numbers)
		num_arr = [i for (i,x) in enumerate(reversed(num_arr)) if x==1]
		pass
	else:
		title = ['%d %s'%(i, x) for (i,x) in enumerate(titles)]
		cprint('\t'.join(title), 'magenta')
		num_arr = raw_input('Please select columns (split by SPACE):').split(' ')
		num_arr = [int(x) for x in num_arr]
		print('Your long number: %r'%fromNumArray(num_arr))
		raw_input('press ENTER to continue...')
		pass

	## setup event monitor
	if options.list_view:
		list_view()
		with keyboard.Listener(on_press=list_view) as listener:
			listener.join()
			pass
		pass
	else:
		global jumped_list
		jumped_list = []
		try:
			print('preloading...')
			jumped_list.append(f.tell())
			while r.next()[0]!='': jumped_list.append(f.tell())
		except Exception as e: pass
		finally:
			r = csv.reader(iter(f.readline, ''), dialect='excel')
			f.seek(jumped_list[0])

		item_view(keyboard.Key.left)
		with keyboard.Listener(on_press=item_view) as listener:
			listener.join()
			pass
		pass
	pass

def m_exit():
	global f
	try:
		f.close()
	except Exception as e: pass
	exit()
	pass

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option("-l", "--list-view",
		dest="list_view", action="store_true", 
		default=False,
		help="change to list view, not item view")
	parser.add_option("-b", "--numbers",
		type="int",
		dest="numbers",
		default=-1,
		help="the long number for column display")
	parser.add_option("-p", "--position",
		type="int",
		dest="curr_pos",
		default=0,
		help="the long number for column display")

	try:
		(options, args) = parser.parse_args()
		main(options, args)
	except Exception as e:
		cprint(e, 'red')
	finally:
		m_exit()
	