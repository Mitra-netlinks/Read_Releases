from github import Github
import getpass
import xlsxwriter
from github import BadCredentialsException


username = input("Github username: ")
password = getpass.getpass(prompt='Github password: ')
repo_name = input("Repository name: ")
release_name = input('Release name: ')

url = str(username+'/'+repo_name)

if username !='' and password !='':

	workbook = xlsxwriter.Workbook('release.xlsx')
	worksheet = workbook.add_worksheet()

	for i in range(1, 4):
		worksheet.set_column(i, i, 30)

	try:

		g = Github(username, password)

		repo = g.get_repo(url)
		worksheet.write(0, 0, 'Client Version')
		worksheet.write(0, 1, 'Version reference for Internal purposes')
		worksheet.write(0, 2, 'Proposed Change (Excepted Functional Behavior)')
		
		row = 1
		for release in repo.get_releases():
			
			worksheet.write(row, 0, release.tag_name)
			worksheet.write(row, 1, release.title)
			line = (release.body.splitlines)
			line_to_read = line()
			for l in line_to_read:
				worksheet.write(row,2,l)
				row += 1

		 
		print ('Excel file created successfully.')
	except BadCredentialsException:
		print ('Bad credentials. Try again!')
	finally:

		workbook.close()

else:
	print ('Github credentials are required!')

		
