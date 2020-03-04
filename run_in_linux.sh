pid=`ps -ef|grep "python3 runserver.py runserver"| grep -v "grep"|awk '{print $2}'`
if [ "$pid" != "" ]
then
        echo "runserver.py already run, stop it first"
        kill -9 ${pid}
fi
echo "starting now..."
sudo nginx -c /home/kismanager/KIS/Page_Agent_Service/nginx.conf
nohup python3 runserver.py runserver --host 0.0.0.0 --port 5001 > myout.out 2>&1 &
nohup python3 runserver.py runserver --host 0.0.0.0 --port 5002 > myout.out 2>&1 &
nohup python3 runserver.py runserver --host 0.0.0.0 --port 5003 > myout.out 2>&1 &
nohup python3 runserver.py runserver --host 0.0.0.0 --port 5004 > myout.out 2>&1 &
nohup python3 runserver.py runserver --host 0.0.0.0 --port 5005 > myout.out 2>&1 &
pid=`ps -ef|grep "python3 runserver.py runserver"| grep -v "grep"|awk '{print $2}'`
echo ${pid} > pid.out
echo "runserver.py started at pid: "${pid}

