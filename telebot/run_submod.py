import subprocess 
print "GO" 
a= subprocess.call(["read_wts_num", "2"]) 
print a 
if a==0:
	print "OK" 
else:
	print "FAIL"
