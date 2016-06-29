from __future__ import unicode_literals

def  is_unicode( word ):
    if isinstance(word, str):
        print("str here ", word )
        return True
    elif isinstance(word, unicode):
        print("unicode here ", word)
        return True
    else:
        print("big error ", word)
        return False

# Replace ascii characters with "-"
def to_unicode(word):
    for letter in word:
        if (ord(letter) > 128):
            word=word.encode("utf-8")
    return word
    #return all(ord(letter) > 128 for letter in word)
        
# Check if it still contains ascii charaters
def is_ascii(word):
    for letter in word:
        if (ord(letter) > 128):
            print("big error ", word)
            return False
    return True
    

    