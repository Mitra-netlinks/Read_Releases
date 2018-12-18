from github import Github
import getpass
import xlsxwriter
from github import BadCredentialsException


username = raw_input("Github username: ")
password = getpass.getpass(prompt='Github password: ')

if username !='' and password !='':

	workbook = xlsxwriter.Workbook('release.xlsx')
	worksheet = workbook.add_worksheet()

	for i in range(1, 4):
		worksheet.set_column(i, i, 30)


	g = Github(username, password)

	repo = g.get_repo('Mitra-netlinks/test_repo')
	worksheet.write(0, 0, 'Client Version')
	worksheet.write(0, 1, 'Version reference for Internal purposes')
	worksheet.write(0, 2, 'Proposed Change (Excepted Functional Behavior)')
	# worksheet.write(0, 3, 'BUG FIX?')
	
	row = 1
	k = 0
	for release in repo.get_releases():
		
		worksheet.write(row, 0, release.tag_name)
		worksheet.write(row, 1, release.title)
		worksheet.write(row, 2, release.body.splitlines)
		# worksheet.write(row, 3, release.body)

		line = (body.splitlines)
		line_to_read = line(0)
		for l in line_to_read:
			worksheet.write_row(row,k, [tag_name, title, l])

	 
		row += 1

	print 'Excel file created successfully.'

	workbook.close()

else:
	print 'Github credentials are required!'

		