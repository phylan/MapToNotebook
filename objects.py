from csv import DictReader, DictWriter
import os

class Case(object):
	
	def __init__(baseFolder):
	
		self.baseFolder = baseFolder
		self.expFolder = baseFolder + '\\cm_export\\'
		self.impFolder = baseFolder + '\\cn_import\\'
		self.people = (self.expFolder + 'people.csv', self.impFolder + 'chars.csv')
		self.documents = (self.expFolder + 'documents.csv', self.impFolder + 'documents.csv')
		self.issues = (self.expFolder + 'issues.csv', self.impFolder + 'issues.csv')
		self.facts = (self.expFolder + 'facts.csv', self.impFolder + 'facts.csv')
		self.organizations = (self.expFolder + 'orgs.csv', self.impFolder + 'orgs.csv')
	
class Table(object):
	
	def __init__(tableFile, exportFile, mappings):
		
		with open(tableFile) as rawIn:
			reader = DictReader(rawIn)
			self.contents = [dict(a) for a in list(reader)]
		
		self.rawOut = exportFile
		self.writer = DictWriter(open(self.rawOut, 'w'))
