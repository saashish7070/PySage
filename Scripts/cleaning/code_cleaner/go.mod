module code_cleaner

go 1.23.3

replace code_cleaner/reindent => ./reindent

require (
	code_cleaner/NormalizeStrings v0.0.0-00010101000000-000000000000
	code_cleaner/WhiteSpaceCleanUp v0.0.0-00010101000000-000000000000
	code_cleaner/repos_reader v0.0.0-00010101000000-000000000000
)

replace code_cleaner/repos_reader => ./repos_reader

replace code_cleaner/NormalizeStrings => ./NormalizeStrings

replace code_cleaner/WhiteSpaceCleanUp => ./WhiteSpaceCleanUp
