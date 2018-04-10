#/bin/bash
dd if=/dev/zero of=/dev/fb0
dd if=/dev/zero of=/dev/fb1
sudo python aiqu.py
