# -*- coding: utf-8 -*-
#! /user/bin/python

# Import packages and libraries
from github import Github
import getpass
from github import BadCredentialsException
import gspread
import oauth2client
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials

# Define and get User Github credentials
username = raw_input("Github username: ")
password = getpass.getpass(prompt='Github password: ')
repo_name = raw_input("Repository name: ")
release_name = raw_input('Release name: ')

# Prepare Github user and repository name
url = str(username+'/'+repo_name)

# Check if username and repository name exist
if username !='' and password !='':

    try:
		# Authunticate with given username and password
		g = Github(username, password)
		# Fetches passed repository releases
		repo = g.get_repo(url)

		# Uses gspread package to read and write to Google Sheet 
		# Declare scope
		scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

		# Set credentials for Google API
		credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

		# Authunticate for right username and password
		file = gspread.authorize(credentials)

		# Open Google Sheet
		sheet = file.open('Releases').sheet1

		# Set format for cells
		fmt = cellFormat(
			backgroundColor = color(0.9,0.9,0.9),
			textFormat = textFormat(bold = True),
			horizontalAlignment='CENTER'
			)
		format_cell_ranges(sheet, [('A1:D1', fmt)])

		# Add headers to the sheet
		sheet.update_acell('A1', 'Client Version')
		sheet.update_acell('B1', 'Version Reference for Internal Purposes')
		sheet.update_acell('C1', 'Proposed Change (Expected Functional Behavior)')
		sheet.update_acell('D1', 'Bug Fix?')

		# Define counter
		row = 2
		# Loop and fetch all releases from Github
		for release in repo.get_releases():
			tag_name = (release.tag_name).encode('utf-8')
			name = (release.title).encode('utf-8')
			# Filter releases name with give release name
			if name == release_name:
				body = (release.body)
				line_to_read = (body.splitlines)
				final_line = line_to_read(0)
				for l in final_line:
					linee =  (l[:1]).encode('utf-8')
					# Check if the release body starts with bullet ('•') or not
					if linee == '•':
						sheet.insert_row([tag_name, name, l[1:].encode('utf-8')], row)
						row += 1
						
		print "Releases inserted to the Google sheet."

    except BadCredentialsException:
    	print ('Bad credentials. Try again!')
   
else:
	print ('Github credentials are required!')
