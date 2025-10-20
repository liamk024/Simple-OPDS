import os

for (root,dirs,files) in os.walk('./content', topdown=True):
    print (root)
    print (dirs)
    print (files)
    print ('--------------------------------')
