from csv import DictReader, DictWriter
from dateutil.parser import parse
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
		
		shortMap, issueMap, orgMap = {}, {}, {}
		issueLists = []
		issuePrefix = "DLI_"
		
		with open(self.expFolder + 'org_names.csv', 'r') as namesIn:
			reader = DictReader(namesIn)
			[orgMap.update({a['Short Name']:a['Full Name']}) for a in list(reader)]
		
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
		
			if entry['Date'] in ['TBD','']:
				entry['Date'] = ''
			else:
				entry['Date'] = fixDate(entry['Date'])
				
			for suffix in mappings.DOC_SUFFIXES:
				entry['Linked File'] = entry['Linked File'].replace(suffix, '')
			
			for short, full in shortMap.items():
				for key, value in entry.items():
					if key == 'Linked File':
						continue
					else:
						entry[key] = value.replace(short,full)
					
			for short, full in orgMap.items():
				for key, value in entry.items():
					if key == 'Linked File':
						continue
					else:
						entry[key] = value.replace(short,full)
		
		for field in list(contents[0].keys()):
			if field not in mappings.DOC_BUILT_INS:
				fieldOut = open(self.impFolder + 'doc_custom_props.txt', 'a')
				fieldOut.write("{0}\n".format(field))
				fieldOut.close()
		
		finalFields = list(contents[0].keys())
		finalFields.remove('Linked Issues')
		
		for i in range(0, issueMax):
			finalFields.append("{0}{1}".format(issuePrefix, i))
		
		for row in contents:
			
			if not row['Linked Issues'] == '':
				for index, issue in enumerate(row['Linked Issues'].split(',')):
					try:
						row.update({'{0}{1}'.format(issuePrefix, index) : issueMap[issue.strip()]})
					except KeyError: # in case there are dupe issues(replaced above) and org names
						row.update({'{0}{1}'.format(issuePrefix, index) : issue.strip()})
						
			row.pop('Linked Issues')
		
			for key, value in row.items():
				if key == 'Linked File':
					continue
				else:
					row[key] = value.replace(',',';')
		
		writer = DictWriter(open(self.documents[1], 'w'), lineterminator = '\n', fieldnames = finalFields)
		docShortWriter = DictWriter(open(self.expFolder + 'doc_shorts.csv', 'w'), lineterminator = '\n', fieldnames = ['Short Name'])
	
		writer.writeheader()
		docShortWriter.writeheader()
		
		for row in contents:
			writer.writerow(row)
			docShortWriter.writerow({'Short Name' : row['Short Name']})
			
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
			
	def convertOrgs(self):
	
		namesWriter = DictWriter(open(self.expFolder + 'org_names.csv','w'), lineterminator='\n', fieldnames = ['Short Name', 'Full Name'])
		namesWriter.writeheader()
		
		with open(self.organizations[0]) as rawIn:
			reader = DictReader(rawIn)
			contents = [dict(a) for a in list(reader)]
			
		exportFields = mappings.ORG_EXPORT_FIELDS
		
		orgsWriter = DictWriter(open(self.organizations[1], 'w'), lineterminator='\n', fieldnames=exportFields, extrasaction='ignore')
		orgsWriter.writeheader()
		
		for row in contents:
			newRow = {
						'Title' : '',
						'First Name' : '',
						'Last Name' : '',
						'Company' : row.get('Full Name'),
						'Department' : 'Organization',
						'Business Street' : row.get('Address: Business',''),
						'E-mail Address' : row.get('Address: E-mail',''),
						'Notes' : row.get('Role In Case')
					}
			
			newRow['Notes'] += '\r\n Key: {0}'.format(row.get('Key',''))
			newRow['Notes'] += '\r\n Linked Issues: {0}'.format(row.get('Linked Issues',''))
			
			orgsWriter.writerow(newRow)
			namesWriter.writerow({'Short Name' : row.get('Short Name'), 'Full Name' : row.get('Full Name')})
	
	def convertFacts(self):
	
		finalFields = mappings.FACT_EXPORT_FIELDS
		
		shortMap, issueMap, orgMap = {}, {}, {}
		
		with open(self.expFolder + 'org_names.csv', 'r') as namesIn:
			reader = DictReader(namesIn)
			[orgMap.update({a['Short Name']:a['Full Name']}) for a in list(reader)]
		
		with open(self.expFolder + 'people_names.csv','r') as namesIn:
			reader = DictReader(namesIn)
			[shortMap.update({a['Short Name']:a['Full Name']}) for a in list(reader)]
			
		with open(self.expFolder + 'issue_names.csv','r') as issuesIn:
			reader = DictReader(issuesIn)
			[issueMap.update({a['Short Name']:a['Full Name']}) for a in list(reader)]
			
		with open(self.facts[0], 'r') as factsIn:
			reader = DictReader(factsIn)
			contents = [dict(a) for a in list(reader)]
		
		with open(self.expFolder + 'doc_shorts.csv','r') as docShortsIn:
			reader = DictReader(docShortsIn)
			docShorts = []
			[docShorts.append(a['Short Name']) for a in list(reader)]
		
		for row in contents:
			
			for field in mappings.FACT_DISCARD_FIELDS:
				row.pop(field,'')
		
		allFields = list(contents[0].keys())
		
		for field in allFields:
			if not any(entry[field] for entry in contents):
				for row in contents:
					row.pop(field)
		
		for field in list(contents[0].keys()):
			if field not in mappings.FACT_BUILT_INS:
				fieldOut = open(self.impFolder + 'fact_custom_props.txt', 'a')
				fieldOut.write("{0}\n".format(field))
				fieldOut.close()
		
		for row in contents:
			
			charList = []

			for short, full in orgMap.items():
				if short in row['Fact Text']:
					row['Fact Text'] = row['Fact Text'].replace(short, full)
					charList.append(full)
					
			for short, full in shortMap.items():
				if short in row['Fact Text']:
					row['Fact Text'] = row['Fact Text'].replace(short, full)
					charList.append(full)
								
			for short, full in issueMap.items():
				row['Linked Issues'] = row['Linked Issues'].replace(short, full)
				
			row['Issues'] = row.pop('Linked Issues').replace(',',';')
			row['Characters'] = '; '.join(charList)
			row['Description'] = row.pop('Fact Text')
			row['Title'] = ' '.join(row['Description'].split()[:8])
			row['Undisputed'] = 'No'
			
			if row['Date & Time'] == 'TBD':
				row['Start Date'] = ''
				row['End Date'] = ''
			
			else:
				row['Start Date'] = fixDate(row['Date & Time'])
				
			row.pop('Date & Time')
			
			row['Author'] = ''
			row['Annotation Sources'] = ''
			
			sourceList = []
			
			for doc in docShorts:
				if doc in row['Source(s)']:
					sourceList.append(doc)
					row['Source(s)'] = row['Source(s)'].replace(doc,'')
			
			row['Source(s)'] = re.sub(r'\[.*\]', '', row['Source(s)'])
			
			row['Full-Text Sources'] = '; '.join(sourceList)
			row['Full-Text Sources'] += '; {0}'.format(row['Source(s)'].strip())
			
			row.pop('Source(s)')
			
		finalFields = list(contents[0].keys())
		
		factWriter = DictWriter(open(self.facts[1], 'w'), lineterminator='\n', fieldnames=finalFields)
		factWriter.writeheader()
		
		for row in contents:
			factWriter.writerow(row)
		
class Table(object):
	
	def __init__(self, tableFile, exportFile, fieldNames):
		
		with open(tableFile) as rawIn:
			reader = DictReader(rawIn)
			self.contents = [dict(a) for a in list(reader)]
		
		self.rawOut = exportFile
		self.writer = DictWriter(open(self.rawOut, 'w'), lineterminator='\n', fieldnames = fieldNames)

class CMAnnotation(object):

	def __init__(self, annotationString):
	
		for pattern, props in mappings.annotationPatterns.items():
		
			if pattern.search(annotationString):
				
				self.raw = pattern.search(annotationString).group(0)
				self.parser = props['func']
				self.type = props['type']
				
		try:
			for key, value in self.parser(self.raw).items():
				setattr(self, key, value)
				
		except AttributeError:
			raise ValueError("Invalid annotation string")
		
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
	
def fixDate(dateString):
	
	dateString = dateString.replace('??','01')
	
	try:
		dateObj = parse(dateString)
		
	except ValueError:
		return dateString
		
	outFormat = "%m/%d/%Y %I:%M%p"
	
	return dateObj.strftime(outFormat)