#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright (c) 2015, Matthew Brennan Jones <matthew.brennan.jones@gmail.com>
# A module for identifying Sony Playstation 2 games with Python 2 & 3
# It uses a MIT style license
# It is hosted at: https://github.com/workhorsy/identify_gamecube_games
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import sys, os
import json

# Load the databases
with open('db_gamecube_official_us.json', 'rb') as f:
	db_gamecube_official_us = json.loads(f.read())

with open('db_gamecube_official_au.json', 'rb') as f:
	db_gamecube_official_au = json.loads(f.read())

with open('db_gamecube_official_eu.json', 'rb') as f:
	db_gamecube_official_eu = json.loads(f.read())

with open('db_gamecube_official_jp.json', 'rb') as f:
	db_gamecube_official_jp = json.loads(f.read())

with open('db_gamecube_official_ko.json', 'rb') as f:
	db_gamecube_official_ko = json.loads(f.read())


def get_gamecube_game_info(file_name):
	# Skip if not an ISO
	if not os.path.splitext(file_name)[1].lower() in ['.iso', '.gcm']:
		raise Exception("Not an ISO file.")

	with open(entry, 'rb') as f:
		'''
		f.seek(0x1c)
		if not f.read(4) == 0xC2339F3D:
			raise Exception("Not a GameCube disk file.")
		'''
		f.seek(0)
		serial_number = f.read(4)
		#print(serial_number)

		f.seek(32)
		sloppy_title = f.read(32).strip(chr(0))

	# Get the region from the game code
	region = serial_number[3]
	if region == 'D':
		region = 'EUR'
	elif region == 'E':
		region = 'USA'
	elif region == 'F':
		region = 'EUR'
	elif region == 'I':
		region = 'EUR'
	elif region == 'J':
		region = 'JPN'
	elif region == 'K':
		region = 'KOR'
	elif region == 'P':
		region = 'EUR'
	elif region == 'R':
		region = 'EUR'
	elif region == 'S':
		region = 'EUR'
	elif region == 'T':
		region = 'TAI'
	elif region == 'U':
		region = 'AUS'

	serial_number = 'DOL-{0}-{1}'.format(serial_number, region)

	# Look up the proper name and vague region
	title, vague_region = None, None
	if serial_number in db_gamecube_official_au:
		vague_region = "AUS"
		title = db_gamecube_official_au[serial_number]
	elif serial_number in db_gamecube_official_eu:
		vague_region = "EUR"
		title = db_gamecube_official_eu[serial_number]
	elif serial_number in db_gamecube_official_jp:
		vague_region = "JPN"
		title = db_gamecube_official_jp[serial_number]
	elif serial_number in db_gamecube_official_ko:
		vague_region = "KOR"
		title = db_gamecube_official_ko[serial_number]
	elif serial_number in db_gamecube_official_us:
		vague_region = "USA"
		title = db_gamecube_official_us[serial_number]

	# Skip if unknown serial number
	if not title or not vague_region:
		raise Exception("Failed to find game in database.")

	return {
		'serial_number' : serial_number,
		'region' : vague_region,
		'title' : title
	}

#'''
games = "E:/Nintendo/GameCube"
for root, dirs, files in os.walk(games):
	for file in files:
		# Get the full path
		entry = root + '/' + file

		if not os.path.splitext(entry)[1].lower() in ['.iso', '.gcm']:
			continue

		#print(entry)
		try:
			info = get_gamecube_game_info(entry)
			print(info)
		except:
			print("Failed on \"{0}\"".format(entry))
#'''


		