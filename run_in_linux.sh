pid=`ps -ef|grep "python3 runserver.py runserver --host 0.0.0.0 --port 5100"| grep -v "grep"|awk '{print $2}'`
if [ "$pid" != "" ]
then
        echo "runserver.py already run, stop it first"
        kill -9 ${pid}
fi
echo "starting now.."
nohup python3 runserver.py runserver --host 0.0.0.0 --port 5100 > myout.out 2>&1 &
pid=`ps -ef|grep "python3 runserver.py runserver --host 0.0.0.0 --port 5100"| grep -v "grep"|awk '{print $2}'`
echo ${pid} > pid.out
echo "runserver.py started at pid: "${pid}

