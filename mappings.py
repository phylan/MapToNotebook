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

#Final field order of fact import:

FACT_EXPORT_FIELDS = ["Title", "Description", "Characters", "Start Date", "End Date", "Issues", "Full-Text Sources", "Annotation Sources", "Undisputed", "Author"]