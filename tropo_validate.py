# Flask for the virtual environment
from flask import Flask
# subprocess to run CLI commands in Python
import subprocess
# re to use regex for locating valid IP Addresses in the string
import re
app = Flask(__name__)

# This Function allow me to run nslookup inside a Python Environment and access the IP Addresses from _netblocks.tropo.com
process = subprocess.Popen(["nslookup", "-q=TXT", "_netblocks.tropo.com", "8.8.8.8"], stdout=subprocess.PIPE)
# Here I split the information wherever there is a new line allowing me to access '_netblocks.tropo.com\ttext = "159.122.242.16/28"' as a single item in a list
data = process.communicate()[0].split('\n')

# Validation checks if the pattern discovered by the re.findall() function is a valid IP Address and not just a random coincidence.  We check that we have 5 groups of numbers as well as whether those numbers are within a valid range for an accurate IP Address.  It returns a boolean used in the if statement on line 28
def validate_ip(num):
    test = re.findall("\d{1,3}", str(num))
    if len(test) != 5:
        return False
    for d in test:
        if int(d) < 0 or int(d) > 255:
            return False
    return True

# I create a list and then use a regex to search for IP addresses that match the required format.  When one is found and it passes validation it is added to the ip_arr along with the tropo string
ip_arr = []
for info in data:
    ip_add = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2}", info)
    if ip_add and validate_ip(ip_add):
        ip_arr.append('tropo,' + ip_add[0])
print ip_arr

if __name__ == '__main__':
    app.run(debug=True)
