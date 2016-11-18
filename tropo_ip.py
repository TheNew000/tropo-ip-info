# Flask for the virtual environment
from flask import Flask
# subprocess to run CLI commands in Python
import subprocess
# re to use regex for locating valid IP Addresses in the string
import re
app = Flask(__name__)

def tropo_ip_extraction(name, server):
    # Empty list to populate with 'tropo,' + ip_address
    ip_arr = []
    # This Function allow me to run nslookup inside a Python Environment and access the IP Addresses from _netblocks.tropo.com
    process = subprocess.Popen(["nslookup", "-q=TXT", name, server], stdout=subprocess.PIPE)
    # Here I split the information wherever there is a new line allowing me to access '_netblocks.tropo.com\ttext = "159.122.242.16/28"' as a single item in a list
    data = process.communicate()[0].split('\n')

    # Validation checks if the pattern discovered by the re.findall() function is a valid IP Address and not just a random coincidence.  We check that we have 5 groups of numbers as well as whether those numbers are within a valid range for an accurate IP Address.  It returns a boolean used in the if statement on line 33
    def validate_ip(num):
        test = re.findall("\d{1,3}", str(num))
        if len(test) != 5:
            return False
        for d in test:
            if int(d) < 0 or int(d) > 255:
                return False
        return True

    for info in data:
        # If there is an error with the server address a message will appear as an item in the list that begins with '"** server can't find'.  If that's not present we can continue with the function, otherwise, we print an error message
        if "** server can't find" not in info:
            # I use a regex to search for IP addresses that match the required format.  When one is found and it passes validation it is added to the ip_arr along with the tropo string
            ip_add = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2}", info)
            if ip_add and validate_ip(ip_add):
                ip_arr.append('tropo,' + ip_add[0])
        else:
            print "Invalid address server cannot connect"
            return
    # If the array is empty we return an error explaining that no valid IP Addresses were found
    if len(ip_arr) > 0:
        print ip_arr
        return ip_arr
    else:
        print "No valid IP Addresses were found"
        return

    if __name__ == '__main__':
        app.run(debug=True)

tropo_ip_extraction("_netblocks.tropo.com", "8.8.8.8")
