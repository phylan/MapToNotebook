from csv import DictReader, DictWriter
import os, mappings

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
		
	def convertPeople(self):
	
		people = Table(self.people[0], self.people[1], mappings.PEOPLE_EXPORT_FIELDS)
		includeExtras = []
		converted = []
		
		for extra in mappings.PEOPLE_EXTRAS:
			if any(entry[extra] for entry in people.contents):
				includeExtras.append(extra)
		
		for row in people.contents:
			convertedRow = {}
			
			for item in mappings.PEOPLE_MAPPINGS:
				convertedRow.update( { item[1] : row.get(item[0],'') } )
				
			if includeExtras:
				convertedRow['Notes'] += "\r\n\r\n===Casemap Data===\r\n"
				for extra in includeExtras:
					convertedRow['Notes'] += "{0}: {1}".format(extra, row.get(extra, ''))
			
			convName = fixName(row.get('Short Name', ''), row.get('Full Name', ''))
			
			convertedRow['Last Name'] = convName[0]
			convertedRow['First Name'] = convName[1]
			
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
	
	lastName = shortName[:-1]
	firstName = fullName[fullName.find(shortName[-1]):fullName.find(' ', fullName.find(shortName[-1]))]
	
	return (lastName, firstName)