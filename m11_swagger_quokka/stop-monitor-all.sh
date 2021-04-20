ps -ef | grep _monitor.py | grep python | grep -v grep | awk '{print $2}' | xargs sudo kill
ps -ef | grep _portscan.py | grep python | grep -v grep | awk '{print $2}' | xargs sudo kill
