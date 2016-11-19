# Flask for the virtual environment
from flask import Flask
# subprocess to run CLI commands in Python
import subprocess
# re to use regex for locating valid IP Addresses in the string
import re
app = Flask(__name__)

def tropo_ip_extraction(name, server):
    # Empty list to populate with 'tropo,' + ip_address
    ip_list = []
    # This Function allow me to run nslookup inside a Python Environment and access the IP Addresses from _netblocks.tropo.com
    process = subprocess.Popen(["nslookup", "-q=TXT", name, server], stdout=subprocess.PIPE)
    # Here I split the information wherever there is a new line allowing me to access '_netblocks.tropo.com\ttext = "159.122.242.16/28"' as a single item in a list
    data_list = process.communicate()[0].split('\n')

    # Validation checks if the pattern discovered by the re.findall() function is a valid IP Address and not just a random coincidence.  We check that we have 5 groups of numbers as well as whether those numbers are within a valid range for an accurate IP Address.  It returns a boolean used in the if statement on line 34
    def validate_ip(num):
        test = re.findall("\d{1,3}", str(num))
        if len(test) != 5:
            return False
        for d in test:
            if int(d) < 0 or int(d) > 255:
                return False
        return True

    for info in data_list:
        # If there is an error with the server name a string will appear as an item in the list that includes "connection timed out" and the function will immediately return an error message.  Otherwise the function continues
        if "connection timed out" not in info:
            # If there is an error with the address a string will appear as an item in the list that includes '"** server can't find'.  The function will immediately return an error message.  Otherwise the function continues
            if "** server can't find" not in info:
                # I use a regex to search for IP addresses that match the required format.  When one is found and it passes validation it is added to the ip_list along with the tropo string
                ip_add = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2}", info)
                if ip_add and validate_ip(ip_add):
                    ip_list.append('tropo,' + ip_add[0])
            else:
                print name + " is an invalid server name"
                return
        else:
            print server + " is an invalid address"
            return
    # If the list is empty we return an error explaining that no valid IP Addresses were found
    if len(ip_list) > 0:
        print ip_list
        return ip_list
    else:
        print "Returned empty list.  No valid IP Addresses were found"
        return

tropo_ip_extraction("_netblocks.tropo.com", "8.8.8.8")

if __name__ == '__main__':
    app.run(debug=True)
