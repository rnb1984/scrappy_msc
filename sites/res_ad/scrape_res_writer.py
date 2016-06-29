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
def to_unicode(word):

    for letter in word:
        if (ord(letter) > 128):
            word=word.replace(letter,"-")
    return word
    #return all(ord(letter) > 128 for letter in word)
        

def is_ascii(word):
    for letter in word:
        if (ord(letter) > 128):
            print("big error ", word)
            return False
    return True
    

    