graph = {}
no_use_words = ['"',',']
link_predicates = ['father', 'mother', 'siblings', 'spouse', 'children', 'killer', 'predecessor', 'successor', 'lovers']

# If subject not given, use from history
# This variable will hold subject(last used) for successive queries
SUB = ""
