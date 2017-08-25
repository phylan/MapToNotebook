import re

PEOPLE_MAPPINGS = [
			('','Title'),
			('Works For','Company'),
			('','Department'),
			('Title','Job Title'),
			('Addresses','Business Street'),
			('','Business City'),
			('','Business State'),
			('','Business Postal Code'),
			('','Business Country/Region'),
			('','Business Fax'),
			('','Business Phone'),
			('','Home Street'),
			('','Home City'),
			('','Home State'),
			('','Home Postal Code'),
			('','Home Country/Region'),
			('','Home Fax'),
			('','Home Phone'),
			('','Home Phone 2'),
			('Phone Numbers','Mobile Phone'),
			('Address: E-mail','E-mail Address'),
			('','E-mail 2 Address'),
			('Role In Case','Notes'),
			('Short Name', 'Discard'), #Discard key will be deleted
			('Creation Author', 'Discard'),
			('Creation Scribe', 'Discard'),
			('Creation Time Stamp', 'Discard'),
			('Key', 'Discard'),
			('Last Update Author', 'Discard'),
			('Last Update Scribe', 'Discard'),
			('Last Update Time Stamp', 'Discard'),
			('Linked File', 'Discard'),
			('Object Type', 'Discard'),
			('Related Files', 'Discard'),
			('# Docs Authored', 'Discard'),
			('# Docs Not Privileged', 'Discard'),
			('# Docs Not Reviewed', 'Discard'),
			('# Docs Privileged', 'Discard'),
			('# Docs Received', 'Discard'),
			('# Docs Reviewed', 'Discard'),
			('# Emails', 'Discard'),
			('# Emails Authored', 'Discard'),
			('# Emails Received', 'Discard'),
			('# Fact Text', 'Discard'),
			('# Key Facts', 'Discard'),
			('# Objects', 'Discard'),
			('# Open Questions', 'Discard'),
			('# Prospective Facts', 'Discard'),
			('# Questions', 'Discard'),
			('# Sourced Facts', 'Discard'),
			('# Undisputed Facts', 'Discard')
]

#Extraneous Casemap fields that will get mapped to Notes with notation:

PEOPLE_EXTRAS = ['At Trial +', 'Calling Party +', 'Counsel', 'Deposition Date', 'Deposition Status +', 'Description', 'Gender', 'Type +', '# Facts', '# Documents', '# Issues', 'Linked Issues']

#Final field order of CN import file (matches Outlook fields per CN documentation):

PEOPLE_EXPORT_FIELDS = ["Title","First Name","Last Name","Company","Department","Job Title","Business Street","Business City","Business State","Business Postal Code","Business Country/Region","Business Fax","Business Phone","Home Street","Home City","Home State","Home Postal Code","Home Country/Region","Home Fax","Home Phone","Home Phone 2","Mobile Phone","E-mail Address","E-mail 2 Address","Notes"]

#Same but for Orgs

ORG_EXTRAS = ["Linked Issues"]
ORG_EXPORT_FIELDS = ["Title","First Name","Last Name","Company","Department","Job Title","Business Street","Business City","Business State","Business Postal Code","Business Country/Region","Business Fax","Business Phone","Home Street","Home City","Home State","Home Postal Code","Home Country/Region","Home Fax","Home Phone","Home Phone 2","Mobile Phone","E-mail Address","E-mail 2 Address","Notes"]

#Suffixes and prefixes to be removed from people Full Names during people import
NAME_JUNK = ["Dr. ", "Mr. ", " CPA", ", CPA", ", Esq", ", Esq.", " Esq.", " Esq", " M.D.", ", M.D.", "Mrs. ", "Ms. ", "Miss ", "Father ", "Monsignor ", "Msgr. ", ", PsyD", " PsyD"]

#Final field order of fact import:

FACT_EXPORT_FIELDS = ["Title", "Description", "Characters", "Start Date", "End Date", "Issues", "Full-Text Sources", "Annotation Sources", "Undisputed", "Author"]

FACT_DISCARD_FIELDS = ["Creation Author", "Creation Scribe", "Creation Time Stamp", "Last Update Author", "Last Update Scribe", "Last Update Time Stamp", "# Issues",
						"# Objects", "# Open Questions", "# Questions", "# Sources"]

FACT_BUILT_INS = ["Date & Time","Creation Author","Creation Scribe","Creation Time Stamp","Description","Key","Last Update Author","Last Update Scribe","Last Update Time Stamp","Potential Source(s)","Related Files","Source Quote","Status Description","# Issues","# Objects","# Open Questions","# Questions","# Sources","Fact Text","Source(s)","Material +","Status +","Linked Issues"]
#Extraneous fields in documents from CM to discard

DOC_DISCARD_FIELDS = ["Creation Author", "Creation Scribe", "Last Update Author", "Last Update Scribe", "Pages", "Attach Count", "Last Update Time Stamp", "Object Type", "Related Files",
						"Reviewed By +", "Sent Via +", "# Docs Not Privileged","# Docs Not Reviewed","# Docs Privileged","# Docs Reviewed","# Documents","# Emails","# Fact Text","# Facts","# Issues","# Key Facts",
						"# Objects","# Open Questions","# Prospective Facts","# Questions","# Undisputed Facts", "# Sourced Facts", "Creation Time Stamp"]

DOC_SUFFIXES = [" - (Power PDF)", " - (Acrobat)", " - (Windows Files)"]

DOC_BUILT_INS = ["Bates - Begin", "Bates - End", "Date", "Short Name", "Type +", "Author(s)", "Recipient(s)", "Copied To", "Linked Issues", "Linked File", "Full Name"]

DOC_MULTI_FIELDS = ["Linked Issues", "Author(s)", "Recipient(s)", "CC", "BCC"]

# Patterns for matching Casemap annotations (note: page number is zero based)

multipageTranscript = re.compile(r'\[%LF% pg=\d*? ln=\d*? - pg=\d*? ln=\d*?\]')
singlepageTranscript = re.compile(r'\[%LF% pg=\d*? ln=\d*? - ln=\d*?\]')
docPageOnly = re.compile(r'\[%LF%\|\d*?\]')
docCoords = re.compile(r'\[%LF%(\|\d*?)*?\]')

def processMultiPageTrx(annotationString):

	pages = re.findall(r'pg=\d*', annotationString)
	lines = re.findall(r'ln=\d*', annotationString)
	
	return {
				'beginPage' : int(pages[0].replace('pg=','')),
				'beginLine' : int(lines[0].replace('ln=','')),
				'endPage' : int(pages[1].replace('pg=','')),
				'endLine' : int(lines[1].replace('ln=',''))
			}

def processSinglePageTrx(annotationString):

	pages = re.findall(r'pg=\d*', annotationString)
	lines = re.findall(r'ln=\d*', annotationString)
	
	return {
				'beginPage' : int(pages[0].replace('pg=','')),
				'beginLine' : int(lines[0].replace('ln=','')),
				'endPage' : int(pages[0].replace('pg=','')),
				'endLine' : int(lines[1].replace('ln=',''))
			}
			
def processDocPageOnly(annotationString):

	page = re.findall(r'\d+', annotationString)[0]
	
	return {
				'page' : int(page)
			}
			
def processDocCoords(annotationString):

	parsed = annotationString.replace(']','').split('|')
	page = int(parsed[1])
	coords = [int(a) for a in parsed[2:]]
	
	return {
				'page' : page,
				'coords' : coords
			}
	
annotationPatterns = {
						multipageTranscript : {'func' : processMultiPageTrx, 'type' : 'MultiplePageTranscriptAnnotation'}, 
						singlepageTranscript : {'func' : processSinglePageTrx, 'type' : 'SinglePageTranscriptAnnotation'},
						docPageOnly : {'func' : processDocPageOnly, 'type' : 'DocumentPageOnlyAnnotation'},
						docCoords : {'func' : processDocCoords, 'type' : 'DocumentCoordinatesAnnotation'}
						}			