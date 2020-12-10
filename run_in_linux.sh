pid=`ps -ef|grep "gunicorn -w 10 -b 127.0.0.1:5101 run:app"| grep -v "grep"|awk '{print $2}'`
if [ "$pid" != "" ]
then
        echo "runserver.py already run, stop it first"
        kill -9 ${pid}
fi
echo "starting now.."
nohup gunicorn -w 10 -b 127.0.0.1:5101 run:app > ./log/myout.log 2>&1 &
pid=`ps -ef|grep "gunicorn -w 10 -b 127.0.0.1:5101 run:app"| grep -v "grep"|awk '{print $2}'`
echo ${pid} >> ./log/pid.log
date >> ./log/pid.log
echo "runserver.py started at pid: "${pid}
