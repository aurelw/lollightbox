#!/bin/bash

### BEGIN INIT INFO
# Provides:          craftui
# Required-Start:    $local_fs $network
# Required-Stop:     $local_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: start script for devlock locksyste.
# Description:       start script for devlock locksyste.
### END INIT INFO

USER="pi"
MQTT_BROKER="test.mosquitto.org"
LIGHTBOX_CMD="/home/pi/lollightbox/lollightbox_mqtt.py"

case "$1" in

    start)
        su $USER <<EOF
        screen -S lollightbox -d -m bash -c "sudo $LIGHTBOX_CMD --host $MQTT_BROKER"
EOF
    ;;

    stop)
        if [ "`pgrep lollightbox`" ]
        then
            echo "Stop lollightbox"
            sudo kill -9 `pgrep lollightbox`
        fi

    ;;

esac

exit 0

