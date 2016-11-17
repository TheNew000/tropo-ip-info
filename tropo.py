from flask import Flask
import subprocess
import re
app = Flask(__name__)

process = subprocess.Popen(["nslookup", "-q=TXT", "_netblocks.tropo.com", "8.8.8.8"], stdout=subprocess.PIPE)
data = process.communicate()[0].split('\n')

ip_arr = []
for info in data:
    ip_add = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2}", info)
    if ip_add:
        ip_arr.append('tropo,' + ip_add[0])
print ip_arr

if __name__ == '__main__':
    app.run(debug=True)
