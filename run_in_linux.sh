
service=/home/kismanager/KIS/Fetch_Agent_Service
log=/home/kismanager/KIS/Fetch_Agent_Service/log
time=$(date "+%Y%m%d")

cd $service
pid=`ps -ef|grep "gunicorn -c gunicorn_fetch_agent.conf run:app"| grep -v "grep"|awk '{print $2}'`
if [ "$pid" != "" ]
then
        echo "runserver.py already run, stop it first"
        kill -9 ${pid}
fi
echo "starting now.."
nohup /usr/local/bin/gunicorn -c gunicorn_fetch_agent.conf run:app >> $log/Fetch_Agent_Service_$time.log 2>&1 &
pid=`ps -ef|grep "gunicorn -c gunicorn_fetch_agent.conf run:app"| grep -v "grep"|awk '{print $2}'`
echo "runserver.py started at pid: "${pid}

#删除3天前的日志
find $log -mtime +3 -name "*.log" -exec rm -rf {} \;