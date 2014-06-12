Names
=====

Python module for smart parsing and matching of people's names

	Parsing Names:

		>>> from names import *
		>>> m = NameManager()
		>>> matt = m.parseName("matt b DAMON")
		>>> matt.toString()
		'Mathiew B. Damon'
		>>> matt.toString(NAME_FORMAT_LAST_COMMA_FIRST)
		'Damon, Mathiew'
		>>> matt.toString(NAME_FORMAT_LAST_COMMA_FIRST_MIDDLES)
		'Damon, Mathiew B.'

		>>>z = m.parseName("abu-shaer, dr Zeinab muhammad a")
		>>>z.title
		'doctor'
		>>>z.last
		'Abu-shaer'

		>>> x = m.parseName("prof ben pasik")
		>>> x.toString(NAME_FORMAT_LAST_COMMA_FIRST)
		'Pasik, Benjamin'
		>>>x.title
		'professor'

		>>>y = m.parseName("smith, Mr. will a")
		>>> y.gender
		'male'
		>>> y.toString()
		'William A. Smith'


		>>> m.allowedNamePunctuation = ["\-",  "'" ] 
		>>> m.parseName("rob o o'dowell").toString(NAME_FORMAT_LAST_COMMA_FIRST_MIDDLES)
		"O'dowell, Robert O."



	Comparing Names:

		>>> from names import *
		>>> m = NameManager()

		>>> m.areNamesEqual( m.parseName("matt damon"), m.parseName( "damon, mathiew"))
		True

		>>> m.middleNameMatchingScheme = MIDDLE_NAME_MATCHING_SCHEME_ALL_INITIALS
		>>> m.areNamesEqual( m.parseName("matt a damon"), m.parseName( "damon, mathiew"))
		False
		>>> m.areNamesEqual( m.parseName("matt a damon"), m.parseName( "damon, mathiew andrew"))
		True
		>>> m.areNamesEqual( m.parseName("matt a damon"), m.parseName( "damon, mathiew a"))
		True
		
		>>> m.middleNameMatchingScheme = MIDDLE_NAME_MATCHING_SCHEME_IGNORE_TRAILING_INITIALS
		>>> m.areNamesEqual( m.parseName("matt a damon"), m.parseName( "damon, mathiew b"))
		False
		>>> m.areNamesEqual( m.parseName("matt a damon"), m.parseName( "damon, mathiew "))
		True
		>>> m.areNamesEqual( m.parseName("matt a damon"), m.parseName( "damon, mathiew andrew"))
		True
		>>> m.areNamesEqual( m.parseName("matt a damon"), m.parseName( "damon, mathiew andrew bernard"))
		True
		
		>>> m.areNamesEqual( m.parseName("bill O'dowell"), m.parseName( "odowell, william"))
		False
		>>> m.forgiveMissingPunctuation = True
		>>> m.areNamesEqual( m.parseName("bill O'dowell"), m.parseName( "odowell, william"))
		True
