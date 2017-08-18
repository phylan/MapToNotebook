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

#Suffixes and prefixes to be removed from people Full Names during people import
NAME_JUNK = ["Dr. ", "Mr. ", " CPA", ", CPA", ", Esq", ", Esq.", " Esq.", " Esq", " M.D.", ", M.D.", "Mrs. ", "Ms. ", "Miss ", "Father ", "Monsignor ", "Msgr. ", ", PsyD", " PsyD"]

#Final field order of fact import:

FACT_EXPORT_FIELDS = ["Title", "Description", "Characters", "Start Date", "End Date", "Issues", "Full-Text Sources", "Annotation Sources", "Undisputed", "Author"]

#Extraneous fields in documents from CM to discard

DOC_DISCARD_FIELDS = ["Creation Author", "Creation Scribe", "Last Update Author", "Last Update Scribe", "Pages", "Attach Count", "Last Update Time Stamp", "Object Type", "Related Files",
						"Reviewed By +", "Sent Via +", "# Docs Not Privileged","# Docs Not Reviewed","# Docs Privileged","# Docs Reviewed","# Documents","# Emails","# Fact Text","# Facts","# Issues","# Key Facts",
						"# Objects","# Open Questions","# Prospective Facts","# Questions","# Undisputed Facts", "# Sourced Facts", "Creation Time Stamp"]

DOC_SUFFIXES = [" - (Power PDF)", " - (Acrobat)", " - (Windows Files)"]

DOC_BUILT_INS = ["Bates - Begin", "Bates - End", "Date", "Short Name", "Type +", "Author(s)", "Recipient(s)", "Copied To", "Linked Issues", "Linked File"]

DOC_MULTI_FIELDS = ["Linked Issues", "Author(s)", "Recipient(s)", "CC", "BCC"]