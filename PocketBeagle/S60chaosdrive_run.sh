#!/bin/sh -e
### BEGIN INIT INFO
# Provides:          chaosdrive
# Required-Start:    $local_fs
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Enables the chaosDrive
# Description:       Enables the chaosDrive
#
### END INIT INFO


# Start chaosdrive
#exec /etc/chaos/chaosDrive.py run

case "$1" in
  start) exec /etc/chaos/chaosDrive_pb.py -d run;;
  stop) exec /etc/chaos/chaosDrive_pb.py stop ;;
  restart|force-reload) exit 0 ;;
  *) echo "Usage: $0 {start|stop|restart|force-reload}" >&2; exit 1 ;;
esac

exit 0
