import itertools
import os
import sys
import time

# If you want to use the Facebook friend functionality, you have to provide your own API KEY and SECRET
# You also need the python Facebook library


API     = ''
SECRET  = ''



# Returns a set of friend's name that can be made from 'jumble'
def friendSolve(facebook,jumble):

    gen = substrings(jumble)
    res = set()
    for g in gen:
        res.add(g)    
    return (first_names & res)
    


# Returns the friend list
def getFriends(facebook): 
    friends = facebook.friends.get()
    friends = facebook.users.getInfo(friends[0:], ['name'])
    first_names = set()
    for friend in friends:
        f = friend['name'].split(' ')[0]
        first_names.add(f.lower())
    
    return first_names


# Login to facebook, and return the fb object
def fbLogin():
    from facebook import Facebook
    facebook = Facebook(API,SECRET)
    facebook.auth.createToken()
    facebook.login()
    facebook.auth.getSession()
    return facebook


# Simple brute force generator
def substrings(s):
    for i in range(3, len(s)+1):
        for p in itertools.permutations(s, i):
            yield ''.join(p)


# Note: this is only for Mac OS X
def sendText(text):
    cmd     = """osascript -e 'tell application "System Events" to keystroke "%s"' """ % text
    cmd2    = """osascript -e 'tell application "System Events" to keystroke return' """
    os.system(cmd)
    os.system(cmd2)



#  Sends the elements of s, with a 2 second delay
def outputSet(s):
    
    print s
    
    # Some delay
    print "Key sending commencing in 2 seconds"
    time.sleep(2) 
    
    for a in s:
        sendText(a)



# Load dictionary into memory
def loadDict():
    f = open('dict.txt','r')
    dic = set()
    for line in f:
        dic.add(line[:-1])
    return dic



# Solves the jumble using list

def solve(jumble,list):
    answer = set()
    generator = substrings(jumble)
    for word in generator:
        if(word in list):
            answer.add(word)
    return answer



# Main Function
def main():
    print "pyWordChallengeBot v0.1"
    print ''
    print "Usage: At the prompt, type in the mode of the application (1 for normal solving, 2 for friend solving), followed by the word jumble! To use the friend solving ability, you will need to provide an API KEY and a SECRET to this script."
    print 'eg: --> 1 telret'
    print "type 'quit' to quit"
    print ''
    
    dic = loadDict()    # Load the dictionary
    
    
    
    # Comment this out if you don't want the Facebook friend functionality.
    # fb = fbLogin()      
    # names = getFriends(fb)
    # # # # # # # # # # # # # # # # # # #
    
    
    
    # Event loop here
    
    modes = ['1','2']
    running = 1
    
    while running:
        i = raw_input('-->').split(' ')
        
        if i[0] == 'quit':
            print "Exiting the bot..."
            quit()
        
        if not(len(i) == 2) or not(i[0] in modes):
            print "Improper Usage, try again!"
            continue
        
        mode    = i[0]
        jumble  = i[1]
        
        if mode == '1': # Dictionary Lookup
            answer = solve(jumble,dic)
            outputSet(answer)
        
        elif mode == '2': # Facebook friend lookup
            answer = solve(jumble,names)
            outputSet(answer)
        

if __name__ == '__main__':
    main()
