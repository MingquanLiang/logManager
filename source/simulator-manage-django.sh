#!/bin/bash

#This is a script used for start uwsgi + nginx

baseDir="/opt/architecture/simulator"
logDir="${baseDir}/log"
cacheDir="${baseDir}/cache"
uwsgiIni="mysite_uwsgi.ini"
logFile="simulator.log"

case "$1" in
    start)
        echo "[ $(date '+%Y-%m-%d %H:%M:%S') ] Try To Startup Django + uwsgi + nginx ... " | tee -a ${logDir}/${logFile}
        chown -R nginx:root ${baseDir}
        cd ${baseDir}
        export PYTHON_EGG_CACHE=${cacheDir}
        nohup /usr/local/bin/uwsgi --ini ${uwsgiIni} >> ${logDir}/${logFile} 2>&1 &
        ret=$?
        [ "$?" != "0" ] && { echo "Failed To read uwsgi ini file" | tee -a ${logDir}/${logFile} ; exit 1 ; }
        sleep 3
        ps -elf | grep uwsgi | grep -v grep 2>&1 >/dev/null
        ret=$?
        if [ "${ret}" == "0" ]
        then
            echo "==> It is OK for uwsgi to Startup" | tee -a ${logDir}/${logFile}
            service nginx status | grep 'stop' 2>&1 >/dev/null
            ret=$?
            [ "$ret" == "0" ] && service nginx start || service nginx restart
        else
            echo "==> Failed To Startup uwsgi" | tee -a ${logDir}/${logFile}
        fi
        ;;
    stop)
        echo "[ $(date '+%Y-%m-%d %H:%M:%S') ] Try To Stop Django + uwsgi ... " | tee -a ${logDir}/${logFile}
        killall uwsgi
        sleep 2
        if [ "x$(ps -elf | grep uwsgi | grep -v grep)" != "x" ]
        then
            killall -9 uwsgi
            sleep 2
            if [ "x$(ps -elf | grep uwsgi | grep -v grep)" != "x" ]
            then
                echo "Failed to Stop uwsgi, please stop it manually or reboot your system" | tee -a ${logDir}/${logFile}
                exit 2
            fi
        fi
        ;;
    restart)
        $0 stop
        $0 start
        ;;
    *)
        echo "Usage: $0 {start|stop}"
        exit 1
        ;;
esac

