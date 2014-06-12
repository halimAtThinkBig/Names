import re


#####################################################
#
#   N A M E    M A N A G E R      M O D U L E
#
#   Halim Abbas (halim.abbas@thinkbiganalytics.com)
#
#   
#
#	Parsing Names:
#
#		>>> from names import *
#		>>> m = NameManager()
#		>>> matt = m.parseName("matt b DAMON")
#		>>> matt.toString()
#		'Mathiew B. Damon'
#		>>> matt.toString(NAME_FORMAT_LAST_COMMA_FIRST)
#		'Damon, Mathiew'
#		>>> matt.toString(NAME_FORMAT_LAST_COMMA_FIRST_MIDDLES)
#		'Damon, Mathiew B.'
#
#		>>>z = m.parseName("abu-shaer, dr Zeinab muhammad a")
#		>>>z.title
#		'doctor'
#		>>>z.last
#		'Abu-shaer'
#
#		>>> x = m.parseName("prof ben pasik")
#		>>> x.toString(NAME_FORMAT_LAST_COMMA_FIRST)
#		'Pasik, Benjamin'
#		>>>x.title
#		'professor'
#
#		>>>y = m.parseName("smith, Mr. will a")
#		>>> y.gender
#		'male'
#		>>> y.toString()
#		'William A. Smith'
#
#
#		>>> m.allowedNamePunctuation = ["\-",  "'" ] 
#		>>> m.parseName("rob o o'dowell").toString(NAME_FORMAT_LAST_COMMA_FIRST_MIDDLES)
#		"O'dowell, Robert O."
#
#
#
#	Comparing Names:
#
#		>>> from names import *
#		>>> m = NameManager()
#
#		>>> m.areNamesEqual( m.parseName("matt damon"), m.parseName( "damon, mathiew"))
#		True
#
#		>>> m.middleNameMatchingScheme = MIDDLE_NAME_MATCHING_SCHEME_ALL_INITIALS
#		>>> m.areNamesEqual( m.parseName("matt a damon"), m.parseName( "damon, mathiew"))
#		False
#		>>> m.areNamesEqual( m.parseName("matt a damon"), m.parseName( "damon, mathiew andrew"))
#		True
#		>>> m.areNamesEqual( m.parseName("matt a damon"), m.parseName( "damon, mathiew a"))
#		True
#		
#		>>> m.middleNameMatchingScheme = MIDDLE_NAME_MATCHING_SCHEME_IGNORE_TRAILING_INITIALS
#		>>> m.areNamesEqual( m.parseName("matt a damon"), m.parseName( "damon, mathiew b"))
#		False
#		>>> m.areNamesEqual( m.parseName("matt a damon"), m.parseName( "damon, mathiew "))
#		True
#		>>> m.areNamesEqual( m.parseName("matt a damon"), m.parseName( "damon, mathiew andrew"))
#		True
#		>>> m.areNamesEqual( m.parseName("matt a damon"), m.parseName( "damon, mathiew andrew bernard"))
#		True
#		
#		>>> m.areNamesEqual( m.parseName("bill O'dowell"), m.parseName( "odowell, william"))
#		False
#		>>> m.forgiveMissingPunctuation = True
#		>>> m.areNamesEqual( m.parseName("bill O'dowell"), m.parseName( "odowell, william"))
#		True
#
######################################################





#####################################################
#
#   C O N S T A N T S
#
#####################################################


NAME_FORMAT_LAST_COMMA_FIRST = 0
NAME_FORMAT_FIRST_LAST = 1
NAME_FORMAT_LAST_COMMA_FIRST_MIDDLES = 2
NAME_FORMAT_FIRST_MIDDLES_LAST = 3


MIDDLE_NAME_MATCHING_SCHEME_IGNORE_MIDDLE_NAMES = 0
MIDDLE_NAME_MATCHING_SCHEME_ALL_INITIALS = 1
MIDDLE_NAME_MATCHING_SCHEME_IGNORE_TRAILING_INITIALS = 2
MIDDLE_NAME_MATCHING_SCHEME_ALL_MIDDLE_NAMES = 3
MIDDLE_NAME_MATCHING_SCHEME_IGNORE_TRAILING_MIDDLE_NAMES = 4

GENDER_MALE = "male"
GENDER_FEMALE = "female"
GENDER_UNSPECIFIED = "unspecified"

#####################################################
#
#   C H E A T    S H E E T S
#
#####################################################


COMMON_NAME_ALIASES = {
	"bill": "william",
	"will": "william", 
	"willie": "william",
	"ed": "edward",
	"christopher": "chris",
	"christine": "chris",
	"alex": "alexander",
	"al": "albert",
	"dan": "daniel",
	"danny": "daniel",
	"matt": "mathiew",
	"ben":"benjamin",
	"rob": "robert",
	"tom": "thomas"
}


COMMON_TITLES = {
	"doctor": {"label":"doctor", "gender":GENDER_UNSPECIFIED},
	"dr": {"label":"doctor", "gender":GENDER_UNSPECIFIED},

	"professor": {"label":"professor", "gender":GENDER_UNSPECIFIED},
	"prof": {"label":"professor", "gender":GENDER_UNSPECIFIED},
	
	"mister": {"label":"mister", "gender":GENDER_MALE},
	"mr": {"label":"mister", "gender":GENDER_MALE},
	
	"missus": {"label":"missus", "gender":GENDER_FEMALE},
	"mrs": {"label":"missus", "gender":GENDER_FEMALE},

	"miss": {"label":"miss", "gender":GENDER_FEMALE},
	"mz": {"label":"mz", "gender":GENDER_FEMALE},

}


#####################################################
#
#   D E F A U L T S
#
#####################################################

NAME_FORMAT_DEFAULT = NAME_FORMAT_FIRST_MIDDLES_LAST
MIDDLE_NAME_MATCHING_SCHEME_DEFAULT = MIDDLE_NAME_MATCHING_SCHEME_IGNORE_TRAILING_INITIALS
ALIASES_MAP_DEFAULT = COMMON_NAME_ALIASES
TITLES_MAP_DEFAULT = COMMON_TITLES
ALLOWED_NAME_PUNCTUATION_DEFAULT = ["\-",  "'" ] #'
FORGIVE_MISSING_PUNCTUATION_DEFAULT = True

#####################################################
#
#   N A M E    C L A S S 
#
#####################################################


class Name:
			
	def __init__(self, manager, first, middles, last, title=None, gender=GENDER_UNSPECIFIED):
		self.manager = manager
		self.first = first
		self.middles = middles[:]
		self.last = last
		self.title = title
		self.gender = gender

	
	def __eq__(self, other):
		return self.manager.areNamesEqual(self, other)
	
	def toString(self, nameFormat=NAME_FORMAT_DEFAULT):
	
		nameString = None	
		
		firstString = self.first.capitalize()
		lastString = self.last.capitalize()
		middlesStrings = []
		for middle in self.middles:
			if middle and len(middle)>0:
				if len(middle)==1:
					middlesStrings.append("%s." % middle.capitalize())
				else:
					middlesStrings.append("%s" % middle.capitalize())

		tokens = []
				
		if nameFormat==NAME_FORMAT_LAST_COMMA_FIRST:
			tokens.append("%s," % lastString)
			tokens.append("%s" % firstString)
		elif nameFormat== NAME_FORMAT_FIRST_LAST:
			tokens.append("%s" % firstString)
			tokens.append("%s" % lastString)
		elif nameFormat== NAME_FORMAT_LAST_COMMA_FIRST_MIDDLES:
			tokens.append("%s," % lastString)
			tokens.append("%s" % firstString)
			tokens.extend(middlesStrings)
		elif nameFormat== NAME_FORMAT_FIRST_MIDDLES_LAST:
			tokens.append("%s" % firstString)
			tokens.extend(middlesStrings)
			tokens.append("%s" % lastString)
		
		if len(tokens)>1:
			nameString = " ".join(tokens).strip()
			
		return nameString

#####################################################
#
#   N A M E    M A N A G E R    C L A S S 
#
#####################################################



class NameManager:

	def __init__(
		self, 
		aliasesMap = ALIASES_MAP_DEFAULT, 
		titlesMap = TITLES_MAP_DEFAULT,
		middleNameMatchingScheme = MIDDLE_NAME_MATCHING_SCHEME_DEFAULT,
		allowedNamePunctuation = ALLOWED_NAME_PUNCTUATION_DEFAULT,
		forgiveMissingPunctuation = FORGIVE_MISSING_PUNCTUATION_DEFAULT
		):
		
		self.aliasesMap = aliasesMap
		self.titlesMap = titlesMap
		self.middleNameMatchingScheme = middleNameMatchingScheme
		self.allowedNamePunctuation = allowedNamePunctuation
		self.forgiveMissingPunctuation = forgiveMissingPunctuation
		
			

	def parseName(self, nameString):
		name = None
		
		#attempt to determine the format of the name in the given string
		nameFormat = NAME_FORMAT_FIRST_MIDDLES_LAST
		if ',' in nameString:
			nameFormat = NAME_FORMAT_LAST_COMMA_FIRST_MIDDLES
		
			
		
		#expecting to parse at least 2 chars
		if nameString and len(nameString)>1:
		
			#strip left or right whitespace
			nameString = nameString.strip()
			
			#take to lower case
			nameString = nameString.lower()
						
			#tokenize by splitting on whitespace and any punctuation except what's allowed
			regex = "[\w%s]+" % "".join(self.allowedNamePunctuation)
			tokens = re.findall(regex, nameString)
						
			#remove invalid tokens
			tokensCopy = []
			for token in tokens:
				#only numerical tokens are invalid
				if not isNumber(token):
					tokensCopy.append(token)
			tokens = tokensCopy[:]
			
			#expecting at least 2 tokens in the name (first & last)
			if len(tokens)>1:

				#take lastname token aside
				if nameFormat == NAME_FORMAT_FIRST_MIDDLES_LAST:
					last = tokens[-1]
					firstAndMiddlesTokens = tokens[0:-1]
				elif nameFormat == NAME_FORMAT_LAST_COMMA_FIRST_MIDDLES:
					last = tokens[0]
					firstAndMiddlesTokens = tokens[1:]
				else:
					return name
				
				
				#then keep processing first and middle name tokens
				
				
				#expecting at least 1 token in the firstAndMiddlesTokens (i.e. the first name) 
				if len(firstAndMiddlesTokens)>0:
				
					#look for titles
					if firstAndMiddlesTokens[0] in self.titlesMap:
						titleToken = firstAndMiddlesTokens.pop(0)
						titleTokenValue = self.titlesMap[titleToken]
						title = titleTokenValue["label"] if "label" in titleTokenValue else None
						gender = titleTokenValue["gender"] if "gender" in titleTokenValue else GENDER_UNSPECIFIED
						
					else:
						title = None
						gender = GENDER_UNSPECIFIED
						
					#expecting at least 1 token left after removing titles if any (i.e. the first name) 
					if len(firstAndMiddlesTokens)>0:
				
					
						#apply aliases
						tokensCopy = []
						for token in firstAndMiddlesTokens:
							if token in self.aliasesMap:
								tokensCopy.append(self.aliasesMap[token])
							else:
								tokensCopy.append(token)
						firstAndMiddlesTokens = tokensCopy[:]
						
						first = firstAndMiddlesTokens[0]
						middles = firstAndMiddlesTokens[1:]
						name = Name(self, first, middles, last, title, gender)			
					
		return name

	def areNamesEqual(self, nameA, nameB):
	
		if not self.areTokensEqual(nameA.first,nameB.first):
			return False
			
		if not self.areTokensEqual(nameA.last, nameB.last):
			return False
			
		if self.middleNameMatchingScheme  == MIDDLE_NAME_MATCHING_SCHEME_IGNORE_MIDDLE_NAMES:
			return True
			
		elif self.middleNameMatchingScheme == MIDDLE_NAME_MATCHING_SCHEME_ALL_INITIALS:
			initialsA = [x[0] for x in nameA.middles]
			initialsB = [x[0] for x in nameB.middles]
			return initialsA == initialsB
			
		elif self.middleNameMatchingScheme == MIDDLE_NAME_MATCHING_SCHEME_IGNORE_TRAILING_INITIALS:
			initialsA = [x[0] for x in nameA.middles]
			initialsB = [x[0] for x in nameB.middles]
			while len(initialsA)>0 and len(initialsB)>0:
				if initialsA[0] != initialsB[0]:
					return False
				del initialsA[0]
				del initialsB[0]
			return True
		
		elif self.middleNameMatchingScheme == MIDDLE_NAME_MATCHING_SCHEME_ALL_MIDDLE_NAMES:
			return self.areTokensEqual(nameA.middles, nameB.middles)
			
		elif self.middleNameMatchingScheme == MIDDLE_NAME_MATCHING_SCHEME_IGNORE_TRAILING_MIDDLE_NAMES:
			middlesA = nameA.middles[:]
			middlesB = nameB.middles[:]
			while len(middlesA)>0 and len(middlesB)>0:
				if not self.areTokensEqual(middlesA[0], middlesB[0]):
					return False
				del middlesA[0]
				del middlesB[0]
			return True
			
		
		
		return False
	
	def areTokensEqual(self, tokenA, tokenB):
		a = tokenA
		b = tokenB
		
		if self.forgiveMissingPunctuation:
			regex = "[%s]" % "".join(self. allowedNamePunctuation)
			a = re.sub(regex,'', a)
			b = re.sub(regex,'', b)
			
		return a==b
		
#####################################################
#
# H E L P E R    F U N C T I O N S 
#
#####################################################

def isNumber(token):
	try:
		float(token)
		return True
	except ValueError:
		return False
