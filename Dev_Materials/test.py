from bs4 import BeautifulSoup

with open("test.html") as fp:
    soup = BeautifulSoup(fp, "html.parser");

# tags
tag = soup.strong
ptag = soup.p
# You find the other ones with .find_all(element type)
print(tag)

# tag accesses name
print(tag.name)

# tag has attributes
print(ptag['id'])
# attrs prints as dictionary
print(ptag.attrs)

tag["another-attr"] = 3
ptag["plus"] = "haha"

# multi-valued attributes - class, rel, rev, accept-charset, headers, accesskey
# stored as a list, added as a list.
# multi_valued_attributes=None as a argument into the BeautifulSoup constructor

# NavigableString class is just like a unicode string, but contains tree searching properties.
# It contains the actual stuff between the element headlines.
# Please convert to unicode with static method unicode() if using solely as string.

print("Hmm: " + tag.string)

# They can't be replaced, but you can use .replace_with()

# BeautifulSoup object has name [document].

# Comments <!-- --!> are just a special type of NavigableString.

# Navigating the Tree!!!

print(soup.head)
print(soup.title)
# The above two lines return the raw HTML

# .contents/.children
# The "html" tag is the child of the BeautifulSoup Object. .contents
# refers down to the next child, stored as a list. Can be iterated over.
# /descendants lets us iterate over all of the children recursively
# iterates down the left (upper) branch first, inorder

# for child in soup.descendants:
    # print(child)

# repr() is just like str() but shows deeper representation

#.strings and .stripped_strings, just look at strings. Allows you to strip the
# \n escapes with stripped.

for string in soup.stripped_strings:
    print(repr(string))

# .parent : .children, .parents :: .descendants
# .next_sibling and .previous_sibling

