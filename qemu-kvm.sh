#!/bin/sh

exec /usr/bin/qemu-system-x86 -machine accel=kvm "$@"
