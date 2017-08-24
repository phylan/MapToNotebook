from csv import DictReader, DictWriter
import os, mappings, re

class Case(object):
	
	def __init__(self, baseFolder):
	
		self.baseFolder = baseFolder
		self.expFolder = baseFolder + '\\cm_export\\'
		self.impFolder = baseFolder + '\\cn_import\\'
		self.people = (self.expFolder + 'people.csv', self.impFolder + 'chars.csv')
		self.documents = (self.expFolder + 'documents.csv', self.impFolder + 'documents.csv')
		self.issues = (self.expFolder + 'issues.csv', self.impFolder + 'issues.csv')
		self.facts = (self.expFolder + 'facts.csv', self.impFolder + 'facts.csv')
		self.organizations = (self.expFolder + 'orgs.csv', self.impFolder + 'orgs.csv')

	def convertIssues(self):

		namesWriter = DictWriter(open(self.expFolder + 'issue_names.csv', 'w'), lineterminator='\n', fieldnames = ['Short Name', 'Full Name'])
		namesWriter.writeheader()
		
		with open(self.issues[0]) as rawIn:
			reader = DictReader(rawIn)
			contents = [dict(a) for a in list(reader)]
			
		defaultColor = "#FFFF00"
		counter = 1
		
		convertedTable = []
		
		for row in contents:
		
			number = row['Full Name'].split()[0]
			
			if '.' not in number:
				number += '.0'
			
			name = ' '.join(row['Full Name'].split()[1:])
			color = defaultColor
			order = counter
			
			convertedTable.append({'Number' : number, 'Order' : order, 'Color' : color, 'Name' : name})
			counter += 1
			
			namesWriter.writerow({'Short Name' : row['Short Name'], 'Full Name' : name})
			
		issuesWriter = DictWriter(open(self.issues[1], 'w'), lineterminator='\n', fieldnames = ['Number', 'Order', 'Color', 'Name'])

		for row in convertedTable:
			issuesWriter.writerow(row)
			
	def convertDocs(self):
		
		shortMap, issueMap = {}, {}
		issueLists = []
		issuePrefix = "DLI_"
		
		with open(self.expFolder + 'people_names.csv','r') as namesIn:
			reader = DictReader(namesIn)
			[shortMap.update({a['Short Name']:a['Full Name']}) for a in list(reader)]
			
		with open(self.expFolder + 'issue_names.csv','r') as issuesIn:
			reader = DictReader(issuesIn)
			[issueMap.update({a['Short Name']:a['Full Name']}) for a in list(reader)]
		
		with open(self.documents[0]) as rawIn:
			reader = DictReader(rawIn)
			contents = [dict(a) for a in list(reader)]
			
		for entry in contents:
			for field in mappings.DOC_DISCARD_FIELDS:
				entry.pop(field)
				
			issueLists.append([a.strip() for a in entry['Linked Issues'].split(',')])
			
		issueMax = len(max(issueLists, key=len))
			
		allFields = list(contents[0].keys())
		
		for field in allFields:
			if not any(entry[field] for entry in contents):
				for row in contents:
					row.pop(field)
					
		for entry in contents:
			for suffix in mappings.DOC_SUFFIXES:
				entry['Linked File'] = entry['Linked File'].replace(suffix, '')
			
			for short, full in shortMap.items():
				for key, value in entry.items():
					entry[key] = value.replace(short,full)
		
		for field in list(contents[0].keys()):
			if field not in mappings.DOC_BUILT_INS:
				fieldOut = open(self.impFolder + 'doc_custom_props.txt', 'a')
				fieldOut.write("{0}".format(field))
				fieldOut.close()
		
		finalFields = list(contents[0].keys())
		finalFields.remove('Linked Issues')
		
		for i in range(0, issueMax):
			finalFields.append("{0}{1}".format(issuePrefix, i))
		
		for row in contents:
			
			if not row['Linked Issues'] == '':
				for index, issue in enumerate(row['Linked Issues'].split(',')):
					row.update({'{0}{1}'.format(issuePrefix, index) : issueMap[issue.strip()]})
		
			row.pop('Linked Issues')
		
			for key, value in row.items():
				row[key] = value.replace(',',';')
		
		writer = DictWriter(open(self.documents[1], 'w'), lineterminator = '\n', fieldnames = finalFields)
		
		writer.writeheader()
		
		for row in contents:
			writer.writerow(row)
		
	def convertPeople(self):
	
		people = Table(self.people[0], self.people[1], mappings.PEOPLE_EXPORT_FIELDS)
		includeExtras = []
		converted = []
		
		for extra in mappings.PEOPLE_EXTRAS:
			if any(entry[extra] for entry in people.contents):
				includeExtras.append(extra)
		
		namesWriter = DictWriter(open(self.expFolder + 'people_names.csv','w'), lineterminator='\n', fieldnames = ['Short Name', 'Full Name'])
		namesWriter.writeheader()
		
		for row in people.contents:
			convertedRow = {}
			
			for item in mappings.PEOPLE_MAPPINGS:
				convertedRow.update( { item[1] : row.get(item[0],'') } )
				
			if includeExtras:
				convertedRow['Notes'] += "\r\n\r\n===Casemap Data===\r\n"
				for extra in includeExtras:
					convertedRow['Notes'] += "{0}: {1}\r\n".format(extra, row.get(extra, ''))
			
			convName = fixName(row.get('Short Name', ''), row.get('Full Name', ''))
			
			convertedRow['Last Name'] = convName[0]
			convertedRow['First Name'] = convName[1]
			
			namesWriter.writerow({'Short Name' : row.get('Short Name'), 'Full Name' : "{0} {1}".format(convName[1], convName[0])})
			
			del convertedRow['Discard']
		
			converted.append(convertedRow)
			
		for row in converted:
			people.writer.writerow(row)
		
class Table(object):
	
	def __init__(self, tableFile, exportFile, fieldNames):
		
		with open(tableFile) as rawIn:
			reader = DictReader(rawIn)
			self.contents = [dict(a) for a in list(reader)]
		
		self.rawOut = exportFile
		self.writer = DictWriter(open(self.rawOut, 'w'), lineterminator='\n', fieldnames = fieldNames)

def fixName(shortName, fullName):
	
	splitShort = re.findall(r'[A-Z][a-z]*(?:[^A-Z])', shortName)
	
	try:
		if splitShort[0] in ['Mc', 'Mac', 'Von', 'Van', "O'"]:
			lastName = splitShort[0] + splitShort[1]
		
		else:
			lastName = splitShort[0]
	
	except IndexError:
		lastName = shortName[:-1]
	
	fullName = fullName.replace(lastName, '')
	
	for item in mappings.NAME_JUNK:
		fullName = fullName.replace(item, '')
		
	nameElements = fullName.split()
	
	if re.match(r'[A-Z]\.', nameElements[0]):
		firstName = "{0} {1}".format(nameElements[0], nameElements[1])
		
	else:
		firstName = nameElements[0]
	
	return (lastName, firstName)