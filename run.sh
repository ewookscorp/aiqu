#/bin/bash
echo "0" > /tmp/aiqumotionpipe
echo "{}" > /tmp/aigupipe
dd if=/dev/zero of=/dev/fb0
dd if=/dev/zero of=/dev/fb1
sudo python aiqu_sdl.py
