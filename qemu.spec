# build-time settings that support --with or --without:
#
# = x86only =
# Build only x86 Qemu targets.
#
# Disabled by default.
#
# = exclusive_x86_64 =
# ExclusiveArch: x86_64
#
# Disabled by default, except on RHEL.
#
# = rbd =
# Enable rbd support.
#
# Enable by default, except on RHEL.
#
# = fdt =
# Enable fdt support.
#
# Enabled by default, except on RHEL.

%if 0%{?rhel}
# RHEL-specific defaults:
%bcond_with    x86only          # disabled
%bcond_without exclusive_x86_64 # enabled
%bcond_with    rbd              # disabled
%bcond_with    fdt              # disabled
%else
# General defaults:
%bcond_with    x86only          # disabled
%bcond_with    exclusive_x86_64 # disabled
%bcond_without rbd              # enabled
%bcond_without fdt              # enabled
%endif


Summary: QEMU is a FAST! processor emulator
Name: qemu
Version: 1.0.1
Release: 6%{?dist}
# Epoch because we pushed a qemu-1.0 package. AIUI this can't ever be dropped
Epoch: 2
License: GPLv2+ and LGPLv2+ and BSD
Group: Development/Tools
URL: http://www.qemu.org/
# RHEL will build Qemu only on x86_64:
%if %{with exclusive_x86_64}
ExclusiveArch: x86_64
%endif

# OOM killer breaks builds with parallel make on s390(x)
%ifarch s390 s390x
%define _smp_mflags %{nil}
%endif

Source0: http://downloads.sourceforge.net/sourceforge/kvm/qemu-kvm-%{version}.tar.gz

Source1: qemu.binfmt

# Loads kvm kernel modules at boot
Source2: kvm.modules

# Creates /dev/kvm
Source3: 80-kvm.rules

# KSM control scripts
Source4: ksm.service
Source5: ksm.sysconfig
Source6: ksmctl.c
Source7: ksmtuned.service
Source8: ksmtuned
Source9: ksmtuned.conf

Source10: qemu-guest-agent.service
Source11: 99-qemu-guest-agent.rules

# Upstream USB bits and flow control series
Patch0001: 0001-usb-redir-Clear-iso-irq-error-when-stopping-the-stre.patch
Patch0002: 0002-usb-redir-Dynamically-adjust-iso-buffering-size-base.patch
Patch0003: 0003-usb-redir-Pre-fill-our-isoc-input-buffer-before-send.patch
Patch0004: 0004-usb-redir-Try-to-keep-our-buffer-size-near-the-targe.patch
Patch0005: 0005-usb-redir-Improve-some-debugging-messages.patch
Patch0006: 0006-char-Split-out-tcp-socket-close-code-in-a-separate-f.patch
Patch0007: 0007-char-Add-a-QemuChrHandlers-struct-to-initialise-char.patch
Patch0008: 0008-iohandlers-Add-enable-disable_write_fd_handler-funct.patch
Patch0009: 0009-char-Add-framework-for-a-write-unblocked-callback.patch
Patch0010: 0010-char-Update-send_all-to-handle-nonblocking-chardev-w.patch
Patch0011: 0011-char-Equip-the-unix-tcp-backend-to-handle-nonblockin.patch
Patch0012: 0012-char-Throttle-when-host-connection-is-down.patch
Patch0013: 0013-virtio-console-Enable-port-throttling-when-chardev-i.patch
Patch0014: 0014-spice-qemu-char.c-add-throttling.patch
Patch0015: 0015-spice-qemu-char.c-remove-intermediate-buffer.patch
Patch0016: 0016-usb-redir-Add-flow-control-support.patch
Patch0017: 0017-virtio-serial-bus-replay-guest_open-on-migration.patch
Patch0018: 0018-char-Disable-write-callback-if-throttled-chardev-is-.patch
Patch0019: 0019-usb-ehci-Clear-the-portstatus-powner-bit-on-device-d.patch
Patch0020: 0020-usb-redir-Add-the-posibility-to-filter-out-certain-d.patch
Patch0021: 0021-usb-redir-Fix-printing-of-device-version.patch
Patch0022: 0022-usb-redir-Always-clear-device-state-on-filter-reject.patch
Patch0023: 0023-usb-redir-Let-the-usb-host-know-about-our-device-fil.patch
Patch0024: 0024-usb-redir-Limit-return-values-returned-by-iso-packet.patch
Patch0025: 0025-usb-redir-Return-USB_RET_NAK-when-we-ve-no-data-for-.patch
Patch0026: 0026-usb-ehci-Handle-ISO-packets-failing-with-an-error-ot.patch
Patch0027: 0027-usb-ehci-Never-follow-table-entries-with-the-T-bit-s.patch
Patch0028: 0028-usb-ehci-split-our-qh-queue-into-async-and-periodic-.patch
Patch0029: 0029-usb-ehci-always-call-ehci_queues_rip_unused-for-peri.patch
Patch0030: 0030-usb-ehci-Drop-cached-qhs-when-the-doorbell-gets-rung.patch
Patch0031: 0031-usb-ehci-Rip-the-queues-when-the-async-or-period-sch.patch
Patch0032: 0032-usb-ehci-Any-packet-completion-except-for-NAK-should.patch
Patch0033: 0033-usb-ehci-Fix-cerr-tracking.patch
Patch0034: 0034-usb-ehci-Remove-dead-nakcnt-code.patch
Patch0035: 0035-usb-ehci-Fix-and-simplify-nakcnt-handling.patch
Patch0036: 0036-usb-ehci-Remove-dead-isoch_pause-code.patch
Patch0037: 0037-usb-return-BABBLE-rather-then-NAK-when-we-receive-to.patch
Patch0038: 0038-usb-add-USB_RET_IOERROR.patch
Patch0039: 0039-usb-ehci-fix-reset.patch
Patch0040: 0040-usb-ehci-sanity-check-iso-xfers.patch
Patch0041: 0041-usb-ehci-frindex-always-is-a-14-bits-counter.patch
Patch0042: 0042-usb-ehci-Drop-unused-sofv-value.patch
Patch0043: 0043-usb-redir-Notify-our-peer-when-we-reject-a-device-du.patch
Patch0044: 0044-usb-redir-An-interface-count-of-0-is-a-valid-value.patch
Patch0045: 0045-usb-redir-Reset-device-address-and-speed-on-disconne.patch
Patch0046: 0046-usb-redir-Not-finding-an-async-urb-id-is-not-an-erro.patch
Patch0047: 0047-usb-ehci-Ensure-frindex-writes-leave-a-valid-frindex.patch

# QXL backports from 1.1
Patch0101: 0101-qxl-Slot-sanity-check-in-qxl_phys2virt-is-off-by-one.patch
Patch0102: 0102-input-send-kbd-mouse-events-only-to-running-guests.patch
Patch0103: 0103-qxl-fix-warnings-on-32bit.patch
Patch0104: 0104-qxl-don-t-render-stuff-when-the-vm-is-stopped.patch
Patch0105: 0105-qxl-set-only-off-screen-surfaces-dirty-instead-of-th.patch
Patch0106: 0106-qxl-make-sure-primary-surface-is-saved-on-migration-.patch
Patch0107: 0107-Add-SPICE-support-to-add_client-monitor-command.patch
Patch0108: 0108-spice-support-ipv6-channel-address-in-monitor-events.patch
Patch0109: 0109-qxl-drop-vram-bar-minimum-size.patch
Patch0110: 0110-qxl-move-ram-size-init-to-new-function.patch
Patch0111: 0111-qxl-add-user-friendly-bar-size-properties.patch
Patch0112: 0112-qxl-fix-spice-sdl-no-cursor-regression.patch
Patch0113: 0113-sdl-remove-NULL-check-g_malloc0-can-t-fail.patch
Patch0114: 0114-qxl-drop-qxl_spice_update_area_async-definition.patch
Patch0115: 0115-qxl-require-spice-0.8.2.patch
Patch0116: 0116-qxl-remove-flipped.patch
Patch0117: 0117-qxl-introduce-QXLCookie.patch
Patch0118: 0118-qxl-make-qxl_render_update-async.patch
Patch0119: 0119-spice-use-error_report-to-report-errors.patch
Patch0120: 0120-Error-out-when-tls-channel-option-is-used-without-TL.patch
Patch0121: 0121-qxl-properly-handle-upright-and-non-shared-surfaces.patch
Patch0122: 0122-spice-set-spice-uuid-and-name.patch
Patch0123: 0123-monitor-fix-client_migrate_info-error-handling.patch
Patch0124: 0124-qxl-init_pipe_signaling-exit-on-failure.patch
Patch0125: 0125-qxl-switch-qxl.c-to-trace-events.patch
Patch0126: 0126-qxl-qxl_render.c-add-trace-events.patch
Patch0127: 0127-hw-qxl.c-Fix-compilation-failures-on-32-bit-hosts.patch
Patch0128: 0128-spice-fix-broken-initialization.patch
Patch0129: 0129-ui-spice-display.c-Fix-compilation-warnings-on-32-bi.patch
Patch0130: 0130-ui-spice-display-use-uintptr_t-when-casting-qxl-phys.patch
Patch0131: 0131-qxl-add-optinal-64bit-vram-bar.patch
Patch0132: 0132-qxl-set-default-values-of-vram-_size_mb-to-1.patch
Patch0133: 0133-qxl-render-fix-broken-vnc-spice-since-commit-f934493.patch
Patch0134: 0134-qxl-don-t-assert-on-guest-create_guest_primary.patch

# Spice volume control backports, all are upstream for 1.1
Patch0201: 0201-audio-add-VOICE_VOLUME-ctl.patch
Patch0202: 0202-audio-don-t-apply-volume-effect-if-backend-has-VOICE.patch
Patch0203: 0203-hw-ac97-remove-USE_MIXER-code.patch
Patch0204: 0204-hw-ac97-the-volume-mask-is-not-only-0x1f.patch
Patch0205: 0205-hw-ac97-add-support-for-volume-control.patch
Patch0206: 0206-audio-spice-add-support-for-volume-control.patch
Patch0207: 0207-Do-not-use-pa_simple-PulseAudio-API.patch
Patch0208: 0208-configure-pa_simple-is-not-needed-anymore.patch
Patch0209: 0209-Allow-controlling-volume-with-PulseAudio-backend.patch

# F17 feature backports
Patch0301: 0301-enable-architectural-PMU-cpuid-leaf-for-kvm.patch
Patch0302: 0302-virtio-scsi-backport.patch
# Remove O_NOATIME for 9p filesystems
Patch0303: 0303-hw-9pfs-Remove-O_NOATIME-flag-from-9pfs-open-calls-i.patch
# Fix booting NetBSD VM (bz #830261)
Patch0304: 0304-pci-fix-corrupted-pci-conf-index-register-by-unalign.patch
# Fix fedora guest hang with virtio console (bz #837925)
Patch0305: 0305-virtio-console-Fix-failure-on-unconnected-pty.patch
# Fix VNC audio tunnelling (bz #840653)
Patch0306: 0306-audio-Unbreak-capturing-in-mixemu-case.patch
# CVE-2012-2652: Possible symlink attacks with -snapshot (bz #825697, bz
# #824919)
Patch0307: 0307-block-prevent-snapshot-mode-TMPDIR-symlink-attack.patch
# Fix systemtap tapsets (bz #831763)
Patch0308: 0308-Fix-systemtap-keyword-collisions.patch
# Remove comma from 1.0.1 version number
Patch0309: 0309-qemu-1.0.1-VERSION.patch
# CVE-2012-3515 VT100 emulation vulnerability (bz #854600, bz #851252)
Patch0310: 0310-console-bounds-check-whenever-changing-the-cursor-du.patch
# Fix slirp crash (bz #845793)
Patch0311: 0311-slirp-Fix-requeuing-of-batchq-packets-in-if_start.patch
# CVE-2012-6075: Buffer overflow in e1000 nic (bz #889301, bz #889304)
Patch0312: 0312-e1000-Discard-packets-that-are-too-long-if-SBP-and-L.patch
Patch0313: 0313-e1000-Discard-oversized-packets-based-on-SBP-LPE.patch
# Fix -vga vmware crashes (bz #836260)
Patch0314: 0314-vmware_vga-fix-out-of-bounds-and-invalid-rects-updat.patch
# Fix vhost crash (bz #918272)
Patch0315: 0315-vhost-Fix-size-of-dirty-log-sync-on-resize.patch
# CVE-2013-1922: qemu-nbd block format auto-detection vulnerability (bz
# #952574, bz #923219)
Patch0316: 0316-Add-f-FMT-format-FMT-arg-to-qemu-nbd.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: SDL-devel zlib-devel which texi2html gnutls-devel cyrus-sasl-devel
BuildRequires: libaio-devel
BuildRequires: rsync
BuildRequires: pciutils-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: ncurses-devel
BuildRequires: libattr-devel
BuildRequires: usbredir-devel >= 0.4.1
BuildRequires: texinfo
%ifarch %{ix86} x86_64
BuildRequires: spice-protocol >= 0.8.1
BuildRequires: spice-server-devel >= 0.9.0
%endif
# For network block driver
BuildRequires: libcurl-devel
%if %{with rbd}
# For rbd block driver
BuildRequires: ceph-devel
%endif
# We need both because the 'stap' binary is probed for by configure
BuildRequires: systemtap
BuildRequires: systemtap-sdt-devel
# For smartcard NSS support
BuildRequires: nss-devel
# For XFS discard support in raw-posix.c
BuildRequires: xfsprogs-devel
# For VNC JPEG support
BuildRequires: libjpeg-devel
# For VNC PNG support
BuildRequires: libpng-devel
# For uuid generation
BuildRequires: libuuid-devel
# For BlueZ device support
BuildRequires: bluez-libs-devel
# For Braille device support
BuildRequires: brlapi-devel
%if %{with fdt}
# For FDT device tree support
BuildRequires: libfdt-devel
%endif
# For test suite
BuildRequires: check-devel
Requires: %{name}-user = %{epoch}:%{version}-%{release}
%if %{without x86only}
Requires: %{name}-system-x86 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-arm = %{epoch}:%{version}-%{release}
Requires: %{name}-system-cris = %{epoch}:%{version}-%{release}
Requires: %{name}-system-sh4 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-m68k = %{epoch}:%{version}-%{release}
Requires: %{name}-system-mips = %{epoch}:%{version}-%{release}
%endif
Requires: %{name}-img = %{epoch}:%{version}-%{release}

Obsoletes: %{name}-system-ppc
Obsoletes: %{name}-system-sparc

# Needed for F14->F16+ upgrade
# https://bugzilla.redhat.com/show_bug.cgi?id=694802
Obsoletes: openbios-common
Obsoletes: openbios-ppc
Obsoletes: openbios-sparc32
Obsoletes: openbios-sparc64

%define qemudocdir %{_docdir}/%{name}-%{version}

%description
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation. QEMU has two operating modes:

 * Full system emulation. In this mode, QEMU emulates a full system (for
   example a PC), including a processor and various peripherials. It can be
   used to launch different Operating Systems without rebooting the PC or
   to debug system code.
 * User mode emulation. In this mode, QEMU can launch Linux processes compiled
   for one CPU on another CPU.

As QEMU requires no host kernel patches to run, it is safe and easy to use.

%package kvm
Summary: QEMU metapackage for KVM support
Group: Development/Tools
%ifarch %{ix86} x86_64
Requires: qemu-system-x86 = %{epoch}:%{version}-%{release}
%endif

%description kvm
This is a meta-package that provides a qemu-system-<arch> package for native
architectures where kvm can be enabled. For example, in an x86 system, this
will install qemu-system-x86

%package  img
Summary: QEMU command line tool for manipulating disk images
Group: Development/Tools
# librbd (from ceph) added new symbol rbd_flush recently.  If you
# update qemu-img without updating librdb you get:
# qemu-img: undefined symbol: rbd_flush
# ** NB ** This can be removed after Fedora 17 is released.
Requires: ceph >= 0.37-2

%description img
This package provides a command line tool for manipulating disk images

%package  common
Summary: QEMU common files needed by all QEMU targets
Group: Development/Tools
Requires(post): /usr/bin/getent
Requires(post): /usr/sbin/groupadd
Requires(post): /usr/sbin/useradd
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%description common
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the common files needed by all QEMU targets

%package guest-agent
Summary: QEMU guest agent
Group: System Environment/Daemons
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description guest-agent
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides an agent to run inside guests, which communicates
with the host over a virtio-serial channel named "org.qemu.guest_agent.0"

This package does not need to be installed on the host OS.

%post guest-agent
if [ $1 -eq 1 ] ; then
    # Initial installation.
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun guest-agent
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade.
    /bin/systemctl stop qemu-guest-agent.service > /dev/null 2>&1 || :
fi

%postun guest-agent
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall.
    /bin/systemctl try-restart qemu-guest-agent.service >/dev/null 2>&1 || :
fi



%package user
Summary: QEMU user mode emulation of qemu targets
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires(post): systemd-units
Requires(postun): systemd-units
%description user
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the user mode emulation of qemu targets

%package system-x86
Summary: QEMU system emulator for x86
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Provides: kvm = 85
Obsoletes: kvm < 85
Requires: vgabios >= 0.6c-2
Requires: seabios-bin >= 0.6.0-2
Requires: sgabios-bin
Requires: ipxe-roms-qemu

%description system-x86
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for x86. When being run in a x86
machine that supports it, this package also provides the KVM virtualization
platform.

%if %{without x86only}
%package system-arm
Summary: QEMU system emulator for arm
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-arm
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for arm

%package system-mips
Summary: QEMU system emulator for mips
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-mips
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for mips

%package system-cris
Summary: QEMU system emulator for cris
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-cris
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for cris

%package system-m68k
Summary: QEMU system emulator for m68k
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-m68k
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for m68k

%package system-sh4
Summary: QEMU system emulator for sh4
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-sh4
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for sh4
%endif

%ifarch %{ix86} x86_64
%package kvm-tools
Summary: KVM debugging and diagnostics tools
Group: Development/Tools

%description kvm-tools
This package contains some diagnostics and debugging tools for KVM,
such as kvm_stat.
%endif

%prep
%setup -q -n qemu-kvm-%{version}

# Upstream USB bits and flow control series
%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1
%patch0006 -p1
%patch0007 -p1
%patch0008 -p1
%patch0009 -p1
%patch0010 -p1
%patch0011 -p1
%patch0012 -p1
%patch0013 -p1
%patch0014 -p1
%patch0015 -p1
%patch0016 -p1
%patch0017 -p1
%patch0018 -p1
%patch0019 -p1
%patch0020 -p1
%patch0021 -p1
%patch0022 -p1
%patch0023 -p1
%patch0024 -p1
%patch0025 -p1
%patch0026 -p1
%patch0027 -p1
%patch0028 -p1
%patch0029 -p1
%patch0030 -p1
%patch0031 -p1
%patch0032 -p1
%patch0033 -p1
%patch0034 -p1
%patch0035 -p1
%patch0036 -p1
%patch0037 -p1
%patch0038 -p1
%patch0039 -p1
%patch0040 -p1
%patch0041 -p1
%patch0042 -p1
%patch0043 -p1
%patch0044 -p1
%patch0045 -p1
%patch0046 -p1
%patch0047 -p1

# QXL backports from 1.1
%patch0101 -p1
%patch0102 -p1
%patch0103 -p1
%patch0104 -p1
%patch0105 -p1
%patch0106 -p1
%patch0107 -p1
%patch0108 -p1
%patch0109 -p1
%patch0110 -p1
%patch0111 -p1
%patch0112 -p1
%patch0113 -p1
%patch0114 -p1
%patch0115 -p1
%patch0116 -p1
%patch0117 -p1
%patch0118 -p1
%patch0119 -p1
%patch0120 -p1
%patch0121 -p1
%patch0122 -p1
%patch0123 -p1
%patch0124 -p1
%patch0125 -p1
%patch0126 -p1
%patch0127 -p1
%patch0128 -p1
%patch0129 -p1
%patch0130 -p1
%patch0131 -p1
%patch0132 -p1
%patch0133 -p1
%patch0134 -p1

# Spice volume control backports, all are upstream for 1.1
%patch0201 -p1
%patch0202 -p1
%patch0203 -p1
%patch0204 -p1
%patch0205 -p1
%patch0206 -p1
%patch0207 -p1
%patch0208 -p1
%patch0209 -p1

# F17 feature backports
%patch0301 -p1
%patch0302 -p1
# Remove O_NOATIME for 9p filesystems
%patch0303 -p1
# Fix booting NetBSD VM (bz #830261)
%patch0304 -p1
# Fix fedora guest hang with virtio console (bz #837925)
%patch0305 -p1
# Fix VNC audio tunnelling (bz #840653)
%patch0306 -p1
# CVE-2012-2652: Possible symlink attacks with -snapshot (bz #825697, bz
# #824919)
%patch0307 -p1
# Fix systemtap tapsets (bz #831763)
%patch0308 -p1
# Remove comma from 1.0.1 version number
%patch0309 -p1
# CVE-2012-3515 VT100 emulation vulnerability (bz #854600, bz #851252)
%patch0310 -p1
# Fix slirp crash (bz #845793)
%patch0311 -p1
# CVE-2012-6075: Buffer overflow in e1000 nic (bz #889301, bz #889304)
%patch0312 -p1
%patch0313 -p1
# Fix -vga vmware crashes (bz #836260)
%patch0314 -p1
# Fix vhost crash (bz #918272)
%patch0315 -p1
# CVE-2013-1922: qemu-nbd block format auto-detection vulnerability (bz
# #952574, bz #923219)
%patch0316 -p1


%build
# By default we build everything, but allow x86 to build a minimal version
# with only similar arch target support
%if %{with x86only}
    buildarch="i386-softmmu x86_64-softmmu i386-linux-user x86_64-linux-user"
%else
    buildarch="i386-softmmu x86_64-softmmu arm-softmmu cris-softmmu m68k-softmmu \
           mips-softmmu mipsel-softmmu mips64-softmmu mips64el-softmmu \
           sh4-softmmu sh4eb-softmmu \
           i386-linux-user x86_64-linux-user alpha-linux-user arm-linux-user \
           armeb-linux-user cris-linux-user m68k-linux-user mips-linux-user \
           mipsel-linux-user ppc-linux-user ppc64-linux-user ppc64abi32-linux-user \
           sh4-linux-user sh4eb-linux-user sparc-linux-user sparc64-linux-user \
           sparc32plus-linux-user" \
%endif


# --build-id option is used fedora 8 onwards for giving info to the debug packages.
extraldflags="-Wl,--build-id";
buildldflags="VL_LDFLAGS=-Wl,--build-id"

%ifarch s390
# drop -g flag to prevent memory exhaustion by linker
%global optflags %(echo %{optflags} | sed 's/-g//')
sed -i.debug 's/"-g $CFLAGS"/"$CFLAGS"/g' configure
%endif

%ifarch %{ix86} x86_64
# sdl outputs to alsa or pulseaudio depending on system config, but it's broken (#495964)
# alsa works, but causes huge CPU load due to bugs
# oss works, but is very problematic because it grabs exclusive control of the device causing other apps to go haywire
./configure --target-list=x86_64-softmmu \
            --prefix=%{_prefix} \
            --sysconfdir=%{_sysconfdir} \
            --audio-drv-list=pa,sdl,alsa,oss \
            --disable-strip \
            --extra-ldflags="$extraldflags -pie -Wl,-z,relro -Wl,-z,now" \
            --extra-cflags="%{optflags} -fPIE -DPIE" \
            --enable-spice \
            --enable-mixemu \
%if %{without rbd}
            --disable-rbd \
%endif
%if %{without fdt}
            --disable-fdt \
%endif
            --enable-trace-backend=dtrace \
            --disable-werror \
            --disable-xen

echo "config-host.mak contents:"
echo "==="
cat config-host.mak
echo "==="

make V=1 %{?_smp_mflags} $buildldflags
./scripts/tracetool --dtrace --binary %{_bindir}/qemu-kvm \
  --target-arch x86_64 --target-type system --stap \
  --probe-prefix qemu.kvm < ./trace-events > qemu-kvm.stp
cp -a x86_64-softmmu/qemu-system-x86_64 qemu-kvm
make clean

%endif

./configure \
    --target-list="$buildarch" \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir} \
    --interp-prefix=%{_prefix}/qemu-%%M \
    --audio-drv-list=pa,sdl,alsa,oss \
    --disable-kvm \
    --disable-strip \
    --extra-ldflags="$extraldflags -pie -Wl,-z,relro -Wl,-z,now" \
    --extra-cflags="%{optflags} -fPIE -DPIE" \
    --disable-xen \
%ifarch %{ix86} x86_64
    --enable-spice \
    --enable-mixemu \
%endif
%if %{without rbd}
    --disable-rbd \
%endif
%if %{without fdt}
    --disable-fdt \
%endif
    --enable-trace-backend=dtrace \
    --disable-werror

echo "config-host.mak contents:"
echo "==="
cat config-host.mak
echo "==="

make V=1 %{?_smp_mflags} $buildldflags

gcc %{SOURCE6} -O2 -g -o ksmctl


%install
rm -rf $RPM_BUILD_ROOT

%define _udevdir /lib/udev/rules.d

install -D -p -m 0755 %{SOURCE4} $RPM_BUILD_ROOT/lib/systemd/system/ksm.service
install -D -p -m 0644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ksm
install -D -p -m 0755 ksmctl $RPM_BUILD_ROOT/lib/systemd/ksmctl

install -D -p -m 0755 %{SOURCE7} $RPM_BUILD_ROOT/lib/systemd/system/ksmtuned.service
install -D -p -m 0755 %{SOURCE8} $RPM_BUILD_ROOT%{_sbindir}/ksmtuned
install -D -p -m 0644 %{SOURCE9} $RPM_BUILD_ROOT%{_sysconfdir}/ksmtuned.conf

%ifarch %{ix86} x86_64
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/modules
mkdir -p $RPM_BUILD_ROOT%{_bindir}/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_udevdir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset

install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/modules/kvm.modules
install -m 0755 kvm/kvm_stat $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 qemu-kvm $RPM_BUILD_ROOT%{_bindir}/
install -m 0644 qemu-kvm.stp $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_udevdir}
%endif

make prefix="${RPM_BUILD_ROOT}%{_prefix}" \
     bindir="${RPM_BUILD_ROOT}%{_bindir}" \
     sharedir="${RPM_BUILD_ROOT}%{_datadir}/%{name}" \
     mandir="${RPM_BUILD_ROOT}%{_mandir}" \
     docdir="${RPM_BUILD_ROOT}%{_docdir}/%{name}-%{version}" \
     datadir="${RPM_BUILD_ROOT}%{_datadir}/%{name}" \
     sysconfdir="${RPM_BUILD_ROOT}%{_sysconfdir}" install
chmod -x ${RPM_BUILD_ROOT}%{_mandir}/man1/*
install -D -p -m 0644 -t ${RPM_BUILD_ROOT}%{qemudocdir} Changelog README TODO COPYING COPYING.LIB LICENSE

install -D -p -m 0644 qemu.sasl $RPM_BUILD_ROOT%{_sysconfdir}/sasl2/qemu.conf

rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/pxe*bin
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/pxe*rom
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/gpxe*rom
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/vgabios*bin
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/bios.bin
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/openbios-ppc
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/openbios-sparc32
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/openbios-sparc64
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/petalogix*.dtb
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/s390-zipl.rom
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/bamboo.dtb
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/slof.bin
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/spapr-rtas.bin
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/ppc_rom.bin
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/sgabios.bin
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/palcode-clipper

# the pxe gpxe images will be symlinks to the images on
# /usr/share/ipxe, as QEMU doesn't know how to look
# for other paths, yet.
pxe_link() {
  ln -s ../ipxe/$2.rom %{buildroot}%{_datadir}/%{name}/pxe-$1.rom
}

pxe_link e1000 8086100e
pxe_link ne2k_pci 10ec8029
pxe_link pcnet 10222000
pxe_link rtl8139 10ec8139
pxe_link virtio 1af41000
ln -s ../vgabios/VGABIOS-lgpl-latest.bin  %{buildroot}/%{_datadir}/%{name}/vgabios.bin
ln -s ../vgabios/VGABIOS-lgpl-latest.cirrus.bin %{buildroot}/%{_datadir}/%{name}/vgabios-cirrus.bin
ln -s ../vgabios/VGABIOS-lgpl-latest.qxl.bin %{buildroot}/%{_datadir}/%{name}/vgabios-qxl.bin
ln -s ../vgabios/VGABIOS-lgpl-latest.stdvga.bin %{buildroot}/%{_datadir}/%{name}/vgabios-stdvga.bin
ln -s ../vgabios/VGABIOS-lgpl-latest.vmware.bin %{buildroot}/%{_datadir}/%{name}/vgabios-vmware.bin
ln -s ../seabios/bios.bin %{buildroot}/%{_datadir}/%{name}/bios.bin
ln -s ../sgabios/sgabios.bin %{buildroot}/%{_datadir}/%{name}/sgabios.bin

mkdir -p $RPM_BUILD_ROOT%{_exec_prefix}/lib/binfmt.d
for i in dummy \
%ifnarch %{ix86} x86_64
    qemu-i386 \
%endif
%if %{without x86only}
%ifnarch alpha
    qemu-alpha \
%endif
%ifnarch arm
    qemu-arm \
%endif
    qemu-armeb \
%ifnarch mips
    qemu-mips qemu-mipsn32 qemu-mips64 \
%endif
%ifnarch mipsel
    qemu-mipsel qemu-mipsn32el qemu-mips64el \
%endif
%ifnarch m68k
    qemu-m68k \
%endif
%ifnarch ppc ppc64
    qemu-ppc \
%endif
%ifnarch sparc sparc64
    qemu-sparc \
%endif
%ifnarch s390 s390x
    qemu-s390x \
%endif
%ifnarch sh4
    qemu-sh4 \
%endif
    qemu-sh4eb \
%endif
; do
  test $i = dummy && continue
  grep /$i:\$ %{SOURCE1} > $RPM_BUILD_ROOT%{_exec_prefix}/lib/binfmt.d/$i.conf
  chmod 644 $RPM_BUILD_ROOT%{_exec_prefix}/lib/binfmt.d/$i.conf
done < %{SOURCE1}

# For the qemu-guest-agent subpackage install the systemd
# service and udev rules.
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT%{_udevdir}
install -m 0644 %{SOURCE10} $RPM_BUILD_ROOT%{_unitdir}
install -m 0644 %{SOURCE11} $RPM_BUILD_ROOT%{_udevdir}

%check
make check

%clean
rm -rf $RPM_BUILD_ROOT

%post system-x86
%ifarch %{ix86} x86_64
# load kvm modules now, so we can make sure no reboot is needed.
# If there's already a kvm module installed, we don't mess with it
sh %{_sysconfdir}/sysconfig/modules/kvm.modules || :
udevadm trigger --subsystem-match=misc --sysname-match=kvm --action=add || :
%endif

%post common
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl enable ksm.service >/dev/null 2>&1 || :
    /bin/systemctl enable ksmtuned.service >/dev/null 2>&1 || :
fi

getent group kvm >/dev/null || groupadd -g 36 -r kvm
getent group qemu >/dev/null || groupadd -g 107 -r qemu
getent passwd qemu >/dev/null || \
  useradd -r -u 107 -g qemu -G kvm -d / -s /sbin/nologin \
    -c "qemu user" qemu

%preun common
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable ksmtuned.service > /dev/null 2>&1 || :
    /bin/systemctl --no-reload disable ksm.service > /dev/null 2>&1 || :
    /bin/systemctl stop ksmtuned.service > /dev/null 2>&1 || :
    /bin/systemctl stop ksm.service > /dev/null 2>&1 || :
fi

%postun common
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart ksmtuned.service >/dev/null 2>&1 || :
    /bin/systemctl try-restart ksm.service >/dev/null 2>&1 || :
fi


%post user
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%postun user
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :


%files
%defattr(-,root,root)

%files kvm
%defattr(-,root,root)

%files common
%defattr(-,root,root)
%dir %{qemudocdir}
%doc %{qemudocdir}/Changelog
%doc %{qemudocdir}/README
%doc %{qemudocdir}/TODO
%doc %{qemudocdir}/qemu-doc.html
%doc %{qemudocdir}/qemu-tech.html
%doc %{qemudocdir}/COPYING
%doc %{qemudocdir}/COPYING.LIB
%doc %{qemudocdir}/LICENSE
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/keymaps/
%{_mandir}/man1/qemu.1*
%{_mandir}/man8/qemu-nbd.8*
%{_bindir}/qemu-nbd
%config(noreplace) %{_sysconfdir}/sasl2/qemu.conf
/lib/systemd/system/ksm.service
/lib/systemd/ksmctl
%config(noreplace) %{_sysconfdir}/sysconfig/ksm
/lib/systemd/system/ksmtuned.service
%{_sbindir}/ksmtuned
%config(noreplace) %{_sysconfdir}/ksmtuned.conf
%dir %{_sysconfdir}/qemu

%files guest-agent
%defattr(-,root,root,-)
%doc COPYING README
%{_bindir}/qemu-ga
%{_unitdir}/qemu-guest-agent.service
%{_udevdir}/99-qemu-guest-agent.rules

%files user
%defattr(-,root,root)
%if %{without x86only}
%{_exec_prefix}/lib/binfmt.d/qemu-*.conf
%endif
%{_bindir}/qemu-i386
%{_bindir}/qemu-x86_64
%if %{without x86only}
%{_bindir}/qemu-alpha
%{_bindir}/qemu-arm
%{_bindir}/qemu-armeb
%{_bindir}/qemu-cris
%{_bindir}/qemu-m68k
%{_bindir}/qemu-mips
%{_bindir}/qemu-mipsel
%{_bindir}/qemu-ppc
%{_bindir}/qemu-ppc64
%{_bindir}/qemu-ppc64abi32
%{_bindir}/qemu-sh4
%{_bindir}/qemu-sh4eb
%{_bindir}/qemu-sparc
%{_bindir}/qemu-sparc32plus
%{_bindir}/qemu-sparc64
%endif
%{_datadir}/systemtap/tapset/qemu-i386.stp
%{_datadir}/systemtap/tapset/qemu-x86_64.stp
%if %{without x86only}
%{_datadir}/systemtap/tapset/qemu-alpha.stp
%{_datadir}/systemtap/tapset/qemu-arm.stp
%{_datadir}/systemtap/tapset/qemu-armeb.stp
%{_datadir}/systemtap/tapset/qemu-cris.stp
%{_datadir}/systemtap/tapset/qemu-m68k.stp
%{_datadir}/systemtap/tapset/qemu-mips.stp
%{_datadir}/systemtap/tapset/qemu-mipsel.stp
%{_datadir}/systemtap/tapset/qemu-ppc.stp
%{_datadir}/systemtap/tapset/qemu-ppc64.stp
%{_datadir}/systemtap/tapset/qemu-ppc64abi32.stp
%{_datadir}/systemtap/tapset/qemu-sh4.stp
%{_datadir}/systemtap/tapset/qemu-sh4eb.stp
%{_datadir}/systemtap/tapset/qemu-sparc.stp
%{_datadir}/systemtap/tapset/qemu-sparc32plus.stp
%{_datadir}/systemtap/tapset/qemu-sparc64.stp
%endif

%files system-x86
%defattr(-,root,root)
%{_bindir}/qemu-system-i386
%{_bindir}/qemu-system-x86_64
%{_datadir}/%{name}/bios.bin
%{_datadir}/%{name}/sgabios.bin
%{_datadir}/%{name}/linuxboot.bin
%{_datadir}/%{name}/multiboot.bin
%{_datadir}/%{name}/mpc8544ds.dtb
%{_datadir}/%{name}/vapic.bin
%{_datadir}/%{name}/vgabios.bin
%{_datadir}/%{name}/vgabios-cirrus.bin
%{_datadir}/%{name}/vgabios-qxl.bin
%{_datadir}/%{name}/vgabios-stdvga.bin
%{_datadir}/%{name}/vgabios-vmware.bin
%{_datadir}/%{name}/pxe-e1000.rom
%{_datadir}/%{name}/pxe-virtio.rom
%{_datadir}/%{name}/pxe-pcnet.rom
%{_datadir}/%{name}/pxe-rtl8139.rom
%{_datadir}/%{name}/pxe-ne2k_pci.rom
%config(noreplace) %{_sysconfdir}/qemu/target-x86_64.conf
%{_datadir}/systemtap/tapset/qemu-system-i386.stp
%{_datadir}/systemtap/tapset/qemu-system-x86_64.stp

%ifarch %{ix86} x86_64
%{_bindir}/qemu-kvm
%{_sysconfdir}/sysconfig/modules/kvm.modules
%{_udevdir}/80-kvm.rules
%{_datadir}/systemtap/tapset/qemu-kvm.stp
%endif

%ifarch %{ix86} x86_64
%files kvm-tools
%defattr(-,root,root,-)
%{_bindir}/kvm_stat
%endif

%if %{without x86only}

%files system-arm
%defattr(-,root,root)
%{_bindir}/qemu-system-arm
%{_datadir}/systemtap/tapset/qemu-system-arm.stp

%files system-mips
%defattr(-,root,root)
%{_bindir}/qemu-system-mips
%{_bindir}/qemu-system-mipsel
%{_bindir}/qemu-system-mips64
%{_bindir}/qemu-system-mips64el
%{_datadir}/systemtap/tapset/qemu-system-mips.stp
%{_datadir}/systemtap/tapset/qemu-system-mipsel.stp
%{_datadir}/systemtap/tapset/qemu-system-mips64el.stp
%{_datadir}/systemtap/tapset/qemu-system-mips64.stp

%files system-cris
%defattr(-,root,root)
%{_bindir}/qemu-system-cris
%{_datadir}/systemtap/tapset/qemu-system-cris.stp

%files system-m68k
%defattr(-,root,root)
%{_bindir}/qemu-system-m68k
%{_datadir}/systemtap/tapset/qemu-system-m68k.stp

%files system-sh4
%defattr(-,root,root)
%{_bindir}/qemu-system-sh4
%{_bindir}/qemu-system-sh4eb
%{_datadir}/systemtap/tapset/qemu-system-sh4.stp
%{_datadir}/systemtap/tapset/qemu-system-sh4eb.stp

%endif

%files img
%defattr(-,root,root)
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_mandir}/man1/qemu-img.1*

%changelog
* Sat Apr 20 2013 Cole Robinson <crobinso@redhat.com> - 2:1.0.1-6
- CVE-2013-1922: qemu-nbd block format auto-detection vulnerability (bz
  #952574, bz #923219)

* Tue Apr 02 2013 Cole Robinson <crobinso@redhat.com> - 2:1.0.1-5
- Fix -vga vmware crashes (bz #836260)
- Fix vhost crash (bz #918272)
- Fix kvm module permissions after first install (bz #907215)

* Wed Jan 30 2013 Kyle McMartin <kmcmarti@redhat.com> - 2:1.0.1-4
- pci: fix unaligned writes to pci config index register (rhbz#830261)
   (resulted in NetBSD being unable to boot in a VM.)

* Wed Jan 16 2013 Cole Robinson <crobinso@redhat.com> - 2:1.0.1-3
- CVE-2012-6075: Buffer overflow in e1000 nic (bz #889301, bz #889304)

* Sun Oct 07 2012 Cole Robinson <crobinso@redhat.com> - 1.0.1-2
- Remove comma from 1.0.1 version number
- CVE-2012-3515 VT100 emulation vulnerability (bz #854600, bz #851252)
- Fix slirp crash (bz #845793)
- Fix KVM module permissions after install (bz #863374)

* Sun Jul 29 2012 Cole Robinson <crobinso@redhat.com> - 1.0.1-1
- Fix VNC audio tunnelling (bz 840653)
- CVE-2012-2652: Possible symlink attacks with -snapshot (bz 825697, bz
  824919)
- Fix systemtap tapsets (bz 831763)
- Don't renable ksm on update (bz 815156)
- Bump usbredir dep (bz 812097)
- Fix RPM install error on non-virt machines (bz 660629)
- Obsolete openbios to fix upgrade dependency issues (bz 694802)

* Wed Jul 18 2012 Cole Robinson <crobinso@redhat.com> - 1.0-18
- Fix fedora guest hang with virtio console (bz 837925)

* Mon Apr 23 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.0-17
- Fix install failure due to set -e (rhbz #815272)

* Mon Apr 23 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.0-16
- Fix kvm.modules to exit successfully on non-KVM capable systems (rhbz #814932)

* Thu Apr 19 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.0-15
- Add a couple of backported QXL/Spice bugfixes
- Add spice volume control patches

* Fri Apr 6 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.0-12
- Add back PPC and SPARC user emulators
- Update binfmt rules from upstream

* Mon Apr  2 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.0-11
- Some more USB bugfixes from upstream

* Thu Mar 29 2012 Eduardo Habkost <ehabkost@redhat.com> - 2:1.0-12
- Fix ExclusiveArch mistake that disabled all non-x86_64 builds on Fedora

* Wed Mar 28 2012 Eduardo Habkost <ehabkost@redhat.com> - 2:1.0-11
- Use --with variables for build-time settings

* Wed Mar 28 2012 Daniel P. Berrange <berrange@redhat.com> - 2:1.0-10
- Switch to use iPXE for netboot ROMs

* Thu Mar 22 2012 Daniel P. Berrange <berrange@redhat.com> - 2:1.0-9
- Remove O_NOATIME for 9p filesystems

* Mon Mar 19 2012 Daniel P. Berrange <berrange@redhat.com> - 2:1.0-8
- Move udev rules to /lib/udev/rules.d (rhbz #748207)

* Fri Mar  9 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.0-7
- Add a whole bunch of USB bugfixes from upstream

* Mon Feb 13 2012 Daniel P. Berrange <berrange@redhat.com> - 2:1.0-6
- Add many more missing BRs for misc QEMU features
- Enable running of test suite during build

* Tue Feb 07 2012 Justin M. Forbes <jforbes@redhat.com> - 2:1.0-5
- Add support for virtio-scsi

* Sun Feb  5 2012 Richard W.M. Jones <rjones@redhat.com> - 2:1.0-4
- Require updated ceph for latest librbd with rbd_flush symbol.

* Tue Jan 24 2012 Justin M. Forbes <jforbes@redhat.com> - 2:1.0-3
- Add support for vPMU
- e1000: bounds packet size against buffer size CVE-2012-0029

* Fri Jan 13 2012 Justin M. Forbes <jforbes@redhat.com> - 2:1.0-2
- Add patches for USB redirect bits
- Remove palcode-clipper, we don't build it

* Wed Jan 11 2012 Justin M. Forbes <jforbes@redhat.com> - 2:1.0-1
- Add patches from 1.0.1 queue

* Fri Dec 16 2011 Justin M. Forbes <jforbes@redhat.com> - 2:1.0-1
- Update to qemu 1.0

* Tue Nov 15 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.15.1-3
- Enable spice for i686 users as well

* Thu Nov 03 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.15.1-2
- Fix POSTIN scriplet failure (#748281)

* Fri Oct 21 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.15.1-1
- Require seabios-bin >= 0.6.0-2 (#741992)
- Replace init scripts with systemd units (#741920)
- Update to 0.15.1 stable upstream
  
* Fri Oct 21 2011 Paul Moore <pmoore@redhat.com>
- Enable full relro and PIE (rhbz #738812)

* Wed Oct 12 2011 Daniel P. Berrange <berrange@redhat.com> - 2:0.15.0-6
- Add BR on ceph-devel to enable RBD block device

* Wed Oct  5 2011 Daniel P. Berrange <berrange@redhat.com> - 2:0.15.0-5
- Create a qemu-guest-agent sub-RPM for guest installation

* Tue Sep 13 2011 Daniel P. Berrange <berrange@redhat.com> - 2:0.15.0-4
- Enable DTrace tracing backend for SystemTAP (rhbz #737763)
- Enable build with curl (rhbz #737006)

* Thu Aug 18 2011 Hans de Goede <hdegoede@redhat.com> - 2:0.15.0-3
- Add missing BuildRequires: usbredir-devel, so that the usbredir code
  actually gets build

* Thu Aug 18 2011 Richard W.M. Jones <rjones@redhat.com> - 2:0.15.0-2
- Add upstream qemu patch 'Allow to leave type on default in -machine'
  (2645c6dcaf6ea2a51a3b6dfa407dd203004e4d11).

* Sun Aug 14 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.15.0-1
- Update to 0.15.0 stable release.

* Thu Aug 04 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.15.0-0.3.201108040af4922
- Update to 0.15.0-rc1 as we prepare for 0.15.0 release

* Thu Aug  4 2011 Daniel P. Berrange <berrange@redhat.com> - 2:0.15.0-0.3.2011072859fadcc
- Fix default accelerator for non-KVM builds (rhbz #724814)

* Thu Jul 28 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.15.0-0.1.2011072859fadcc
- Update to 0.15.0-rc0 as we prepare for 0.15.0 release

* Tue Jul 19 2011 Hans de Goede <hdegoede@redhat.com> - 2:0.15.0-0.2.20110718525e3df
- Add support usb redirection over the network, see:
  http://fedoraproject.org/wiki/Features/UsbNetworkRedirection
- Restore chardev flow control patches

* Mon Jul 18 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.15.0-0.1.20110718525e3df
- Update to git snapshot as we prepare for 0.15.0 release

* Wed Jun 22 2011 Richard W.M. Jones <rjones@redhat.com> - 2:0.14.0-9
- Add BR libattr-devel.  This caused the -fstype option to be disabled.
  https://www.redhat.com/archives/libvir-list/2011-June/thread.html#01017

* Mon May  2 2011 Hans de Goede <hdegoede@redhat.com> - 2:0.14.0-8
- Fix a bug in the spice flow control patches which breaks the tcp chardev

* Tue Mar 29 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-7
- Disable qemu-ppc and qemu-sparc packages (#679179)

* Mon Mar 28 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-6
- Spice fixes for flow control.

* Tue Mar 22 2011 Dan Horák <dan[at]danny.cz> - 2:0.14.0-5
- be more careful when removing the -g flag on s390

* Fri Mar 18 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-4
- Fix thinko on adding the most recent patches.

* Wed Mar 16 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-3
- Fix migration issue with vhost
- Fix qxl locking issues for spice

* Wed Mar 02 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-2
- Re-enable sparc and cris builds

* Thu Feb 24 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-1
- Update to 0.14.0 release

* Fri Feb 11 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-0.1.20110210git7aa8c46
- Update git snapshot
- Temporarily disable qemu-cris and qemu-sparc due to build errors (to be resolved shorly)

* Tue Feb 08 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-0.1.20110208git3593e6b
- Update to 0.14.0 rc git snapshot
- Add virtio-net to modules

* Wed Nov  3 2010 Daniel P. Berrange <berrange@redhat.com> - 2:0.13.0-2
- Revert previous change
- Make qemu-common own the /etc/qemu directory
- Add /etc/qemu/target-x86_64.conf to qemu-system-x86 regardless
  of host architecture.

* Wed Nov 03 2010 Dan Horák <dan[at]danny.cz> - 2:0.13.0-2
- Remove kvm config file on non-x86 arches (part of #639471)
- Own the /etc/qemu directory

* Mon Oct 18 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-1
- Update to 0.13.0 upstream release
- Fixes for vhost
- Fix mouse in certain guests (#636887)
- Fix issues with WinXP guest install (#579348)
- Resolve build issues with S390 (#639471)
- Fix Windows XP on Raw Devices (#631591)

* Tue Oct 05 2010 jkeating - 2:0.13.0-0.7.rc1.1
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-0.7.rc1
- Flip qxl pci id from unstable to stable (#634535)
- KSM Fixes from upstream (#558281)

* Tue Sep 14 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-0.6.rc1
- Move away from git snapshots as 0.13 is close to release
- Updates for spice 0.6

* Tue Aug 10 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-0.5.20100809git25fdf4a
- Fix typo in e1000 gpxe rom requires.
- Add links to newer vgabios

* Tue Aug 10 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-0.4.20100809git25fdf4a
- Disable spice on 32bit, it is not supported and buildreqs don't exist.

* Mon Aug 9 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-0.3.20100809git25fdf4a
- Updates from upstream towards 0.13 stable
- Fix requires on gpxe
- enable spice now that buildreqs are in the repository.
- ksmtrace has moved to a separate upstream package

* Tue Jul 27 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-0.2.20100727gitb81fe95
- add texinfo buildreq for manpages.

* Tue Jul 27 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-0.1.20100727gitb81fe95
- Update to 0.13.0 upstream snapshot
- ksm init fixes from upstream

* Tue Jul 20 2010 Dan Horák <dan[at]danny.cz> - 2:0.12.3-8
- Add avoid-llseek patch from upstream needed for building on s390(x)
- Don't use parallel make on s390(x)

* Tue Jun 22 2010 Amit Shah <amit.shah@redhat.com> - 2:0.12.3-7
- Add vvfat hardening patch from upstream (#605202)

* Fri Apr 23 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.3-6
- Change requires to the noarch seabios-bin
- Add ownership of docdir to qemu-common (#572110)
- Fix "Cannot boot from non-existent NIC" error when using virt-install (#577851)

* Thu Apr 15 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.3-5
- Update virtio console patches from upstream

* Mon Mar 11 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.3-4
- Detect cdrom via ioctl (#473154)
- re add increased buffer for USB control requests (#546483)

* Wed Mar 10 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.3-3
- Migration clear the fd in error cases (#518032)

* Tue Mar 09 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.3-2
- Allow builds --with x86only
- Add libaio-devel buildreq for aio support

* Fri Feb 26 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.3-1
- Update to 0.12.3 upstream
- vhost-net migration/restart fixes
- Add F-13 machine type
- virtio-serial fixes

* Tue Feb 09 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.2-6
- Add vhost net support.

* Thu Feb 04 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.2-5
- Avoid creating too large iovecs in multiwrite merge (#559717)
- Don't try to set max_kernel_pages during ksm init on newer kernels (#558281)
- Add logfile options for ksmtuned debug.

* Wed Jan 27 2010 Amit Shah <amit.shah@redhat.com> - 2:0.12.2-4
- Remove build dependency on iasl now that we have seabios

* Wed Jan 27 2010 Amit Shah <amit.shah@redhat.com> - 2:0.12.2-3
- Remove source target for 0.12.1.2

* Wed Jan 27 2010 Amit Shah <amit.shah@redhat.com> - 2:0.12.2-2
- Add virtio-console patches from upstream for the F13 VirtioSerial feature

* Mon Jan 25 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.2-1
- Update to 0.12.2 upstream

* Fri Jan 10 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.1.2-3
- Point to seabios instead of bochs, and add a requires for seabios

* Mon Jan  4 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.1.2-2
- Remove qcow2 virtio backing file patch

* Mon Jan  4 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.1.2-1
- Update to 0.12.1.2 upstream
- Remove patches included in upstream

* Fri Nov 20 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-12
- Fix a use-after-free crasher in the slirp code (#539583)
- Fix overflow in the parallels image format support (#533573)

* Wed Nov  4 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-11
- Temporarily disable preadv/pwritev support to fix data corruption (#526549)

* Tue Nov  3 2009 Justin M. Forbes <jforbes@redhat.com> - 2:0.11.0-10
- Default ksm and ksmtuned services on.

* Thu Oct 29 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-9
- Fix dropped packets with non-virtio NICs (#531419)

* Wed Oct 21 2009 Glauber Costa <gcosta@redhat.com> - 2:0.11.0-8
- Properly save kvm time registers (#524229)

* Mon Oct 19 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-7
- Fix potential segfault from too small MSR_COUNT (#528901)

* Fri Oct  9 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-6
- Fix fs errors with virtio and qcow2 backing file (#524734)
- Fix ksm initscript errors on kernel missing ksm (#527653)
- Add missing Requires(post): getent, useradd, groupadd (#527087)

* Tue Oct  6 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-5
- Add 'retune' verb to ksmtuned init script

* Mon Oct  5 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-4
- Use rtl8029 PXE rom for ne2k_pci, not ne (#526777)
- Also, replace the gpxe-roms-qemu pkg requires with file-based requires

* Thu Oct  1 2009 Justin M. Forbes <jmforbes@redhat.com> - 2:0.11.0-3
- Improve error reporting on file access (#524695)

* Mon Sep 28 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-2
- Fix pci hotplug to not exit if supplied an invalid NIC model (#524022)

* Mon Sep 28 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-1
- Update to 0.11.0 release
- Drop a couple of upstreamed patches

* Wed Sep 23 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.92-5
- Fix issue causing NIC hotplug confusion when no model is specified (#524022)

* Wed Sep 16 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.92-4
- Fix for KSM patch from Justin Forbes

* Wed Sep 16 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.92-3
- Add ksmtuned, also from Dan Kenigsberg
- Use %_initddir macro

* Wed Sep 16 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.92-2
- Add ksm control script from Dan Kenigsberg

* Mon Sep  7 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.92-1
- Update to qemu-kvm-0.11.0-rc2
- Drop upstreamed patches
- extboot install now fixed upstream
- Re-place TCG init fix (#516543) with the one gone upstream

* Mon Sep  7 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.10.rc1
- Fix MSI-X error handling on older kernels (#519787)

* Fri Sep  4 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.9.rc1
- Make pulseaudio the default audio backend (#519540, #495964, #496627)

* Thu Aug 20 2009 Richard W.M. Jones <rjones@redhat.com> - 2:0.10.91-0.8.rc1
- Fix segfault when qemu-kvm is invoked inside a VM (#516543)

* Tue Aug 18 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.7.rc1
- Fix permissions on udev rules (#517571)

* Mon Aug 17 2009 Lubomir Rintel <lkundrak@v3.sk> - 2:0.10.91-0.6.rc1
- Allow blacklisting of kvm modules (#517866)

* Fri Aug  7 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.5.rc1
- Fix virtio_net with -net user (#516022)

* Tue Aug  4 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.4.rc1
- Update to qemu-kvm-0.11-rc1; no changes from rc1-rc0

* Tue Aug  4 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.3.rc1.rc0
- Fix extboot checksum (bug #514899)

* Fri Jul 31 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.2.rc1.rc0
- Add KSM support
- Require bochs-bios >= 2.3.8-0.8 for latest kvm bios updates

* Thu Jul 30 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.1.rc1.rc0
- Update to qemu-kvm-0.11.0-rc1-rc0
- This is a pre-release of the official -rc1
- A vista installer regression is blocking the official -rc1 release
- Drop qemu-prefer-sysfs-for-usb-host-devices.patch
- Drop qemu-fix-build-for-esd-audio.patch
- Drop qemu-slirp-Fix-guestfwd-for-incoming-data.patch
- Add patch to ensure extboot.bin is installed

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.10.50-14.kvm88
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Glauber Costa <glommer@redhat.com> - 2:0.10.50-13.kvm88
- Fix bug 513249, -net channel option is broken

* Thu Jul 16 2009 Daniel P. Berrange <berrange@redhat.com> - 2:0.10.50-12.kvm88
- Add 'qemu' user and group accounts
- Force disable xen until it can be made to build

* Thu Jul 16 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-11.kvm88
- Update to kvm-88, see http://www.linux-kvm.org/page/ChangeLog
- Package mutiboot.bin
- Update for how extboot is built
- Fix sf.net source URL
- Drop qemu-fix-ppc-softmmu-kvm-disabled-build.patch
- Drop qemu-fix-pcspk-build-with-kvm-disabled.patch
- Cherry-pick fix for esound support build failure

* Wed Jul 15 2009 Daniel Berrange <berrange@lettuce.camlab.fab.redhat.com> - 2:0.10.50-10.kvm87
- Add udev rules to make /dev/kvm world accessible & group=kvm (rhbz #497341)
- Create a kvm group if it doesn't exist (rhbz #346151)

* Tue Jul 07 2009 Glauber Costa <glommer@redhat.com> - 2:0.10.50-9.kvm87
- use pxe roms from gpxe, instead of etherboot package.

* Fri Jul  3 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-8.kvm87
- Prefer sysfs over usbfs for usb passthrough (#508326)

* Sat Jun 27 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-7.kvm87
- Update to kvm-87
- Drop upstreamed patches
- Cherry-pick new ppc build fix from upstream
- Work around broken linux-user build on ppc
- Fix hw/pcspk.c build with --disable-kvm
- Re-enable preadv()/pwritev() since #497429 is long since fixed
- Kill petalogix-s3adsp1800.dtb, since we don't ship the microblaze target

* Fri Jun  5 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-6.kvm86
- Fix 'kernel requires an x86-64 CPU' error
- BuildRequires ncurses-devel to enable '-curses' option (#504226)

* Wed Jun  3 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-5.kvm86
- Prevent locked cdrom eject - fixes hang at end of anaconda installs (#501412)
- Avoid harmless 'unhandled wrmsr' warnings (#499712)

* Thu May 21 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-4.kvm86
- Update to kvm-86 release
- ChangeLog here: http://marc.info/?l=kvm&m=124282885729710

* Fri May  1 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-3.kvm85
- Really provide qemu-kvm as a metapackage for comps

* Tue Apr 28 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-2.kvm85
- Provide qemu-kvm as a metapackage for comps

* Mon Apr 27 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-1.kvm85
- Update to qemu-kvm-devel-85
- kvm-85 is based on qemu development branch, currently version 0.10.50
- Include new qemu-io utility in qemu-img package
- Re-instate -help string for boot=on to fix virtio booting with libvirt
- Drop upstreamed patches
- Fix missing kernel/include/asm symlink in upstream tarball
- Fix target-arm build
- Fix build on ppc
- Disable preadv()/pwritev() until bug #497429 is fixed
- Kill more .kernelrelease uselessness
- Make non-kvm qemu build verbose

* Fri Apr 24 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-15
- Fix source numbering typos caused by make-release addition

* Thu Apr 23 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-14
- Improve instructions for generating the tarball

* Tue Apr 21 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-13
- Enable pulseaudio driver to fix qemu lockup at shutdown (#495964)

* Tue Apr 21 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-12
- Another qcow2 image corruption fix (#496642)

* Mon Apr 20 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-11
- Fix qcow2 image corruption (#496642)

* Sun Apr 19 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-10
- Run sysconfig.modules from %post on x86_64 too (#494739)

* Sun Apr 19 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-9
- Align VGA ROM to 4k boundary - fixes 'qemu-kvm -std vga' (#494376)

* Tue Apr  14 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-8
- Provide qemu-kvm conditional on the architecture.

* Thu Apr  9 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-7
- Add a much cleaner fix for vga segfault (#494002)

* Sun Apr  5 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-6
- Fixed qcow2 segfault creating disks over 2TB. #491943

* Fri Apr  3 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-5
- Fix vga segfault under kvm-autotest (#494002)
- Kill kernelrelease hack; it's not needed
- Build with "make V=1" for more verbose logs

* Thu Apr 02 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-4
- Support botting gpxe roms.

* Wed Apr 01 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-2
- added missing patch. love for CVS.

* Wed Apr 01 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-1
- Include debuginfo for qemu-img
- Do not require qemu-common for qemu-img
- Explicitly own each of the firmware files
- remove firmwares for ppc and sparc. They should be provided by an external package.
  Not that the packages exists for sparc in the secondary arch repo as noarch, but they
  don't automatically get into main repos. Unfortunately it's the best we can do right
  now.
- rollback a bit in time. Snapshot from avi's maint/2.6.30
  - this requires the sasl patches to come back.
  - with-patched-kernel comes back.

* Wed Mar 25 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-0.12.kvm20090323git
- BuildRequires pciutils-devel for device assignment (#492076)

* Mon Mar 23 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.11.kvm20090323git
- Update to snapshot kvm20090323.
- Removed patch2 (upstream).
- use upstream's new split package.
- --with-patched-kernel flag not needed anymore
- Tell how to get the sources.

* Wed Mar 18 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.10.kvm20090310git
- Added extboot to files list.

* Wed Mar 11 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.9.kvm20090310git
- Fix wrong reference to bochs bios.

* Wed Mar 11 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.8.kvm20090310git
- fix Obsolete/Provides pair
- Use kvm bios from bochs-bios package.
- Using RPM_OPT_FLAGS in configure
- Picked back audio-drv-list from kvm package

* Tue Mar 10 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.7.kvm20090310git
- modify ppc patch

* Tue Mar 10 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.6.kvm20090310git
- updated to kvm20090310git
- removed sasl patches (already in this release)

* Tue Mar 10 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.5.kvm20090303git
- kvm.modules were being wrongly mentioned at %%install.
- update description for the x86 system package to include kvm support
- build kvm's own bios. It is still necessary while kvm uses a slightly different
  irq routing mechanism

* Thu Mar 05 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.4.kvm20090303git
- seems Epoch does not go into the tags. So start back here.

* Thu Mar 05 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.1.kvm20090303git
- Use bochs-bios instead of bochs-bios-data
- It's official: upstream set on 0.10

* Thu Mar  5 2009 Daniel P. Berrange <berrange@redhat.com> - 2:0.9.2-0.2.kvm20090303git
- Added BSD to license list, since many files are covered by BSD

* Wed Mar 04 2009 Glauber Costa <glommer@redhat.com> - 0.9.2-0.1.kvm20090303git
- missing a dot. shame on me

* Wed Mar 04 2009 Glauber Costa <glommer@redhat.com> - 0.92-0.1.kvm20090303git
- Set Epoch to 2
- Set version to 0.92. It seems upstream keep changing minds here, so pick the lowest
- Provides KVM, Obsoletes KVM
- Only install qemu-kvm in ix86 and x86_64
- Remove pkgdesc macros, as they were generating bogus output for rpm -qi.
- fix ppc and ppc64 builds

* Tue Mar 03 2009 Glauber Costa <glommer@redhat.com> - 0.10-0.3.kvm20090303git
- only execute post scripts for user package.
- added kvm tools.

* Tue Mar 03 2009 Glauber Costa <glommer@redhat.com> - 0.10-0.2.kvm20090303git
- put kvm.modules into cvs

* Tue Mar 03 2009 Glauber Costa <glommer@redhat.com> - 0.10-0.1.kvm20090303git
- Set Epoch to 1
- Build KVM (basic build, no tools yet)
- Set ppc in ExcludeArch. This is temporary, just to fix one issue at a time.
  ppc users (IBM ? ;-)) please wait a little bit.

* Tue Mar  3 2009 Daniel P. Berrange <berrange@redhat.com> - 1.0-0.5.svn6666
- Support VNC SASL authentication protocol
- Fix dep on bochs-bios-data

* Tue Mar 03 2009 Glauber Costa <glommer@redhat.com> - 1.0-0.4.svn6666
- use bios from bochs-bios package.

* Tue Mar 03 2009 Glauber Costa <glommer@redhat.com> - 1.0-0.3.svn6666
- use vgabios from vgabios package.

* Mon Mar 02 2009 Glauber Costa <glommer@redhat.com> - 1.0-0.2.svn6666
- use pxe roms from etherboot package.

* Mon Mar 02 2009 Glauber Costa <glommer@redhat.com> - 1.0-0.1.svn6666
- Updated to tip svn (release 6666). Featuring split packages for qemu.
  Unfortunately, still using binary blobs for the bioses.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 11 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.9.1-12
- Updated build patch. Closes Red Hat Bugzilla bug #465041.

* Wed Dec 31 2008 Dennis Gilmore <dennis@ausil.us> - 0.9.1-11
- add sparcv9 and sparc64 support

* Fri Jul 25 2008 Bill Nottingham <notting@redhat.com>
- Fix qemu-img summary (#456344)

* Wed Jun 25 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-10.fc10
- Rebuild for GNU TLS ABI change

* Wed Jun 11 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-9.fc10
- Remove bogus wildcard from files list (rhbz #450701)

* Sat May 17 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.9.1-8
- Register binary handlers also for shared libraries

* Mon May  5 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-7.fc10
- Fix text console PTYs to be in rawmode

* Sun Apr 27 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.9.1-6
- Register binary handler for SuperH-4 CPU

* Wed Mar 19 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-5.fc9
- Split qemu-img tool into sub-package for smaller footprint installs

* Wed Feb 27 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-4.fc9
- Fix block device checks for extendable disk formats (rhbz #435139)

* Sat Feb 23 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-3.fc9
- Fix block device extents check (rhbz #433560)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.1-2
- Autorebuild for GCC 4.3

* Tue Jan  8 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-1.fc9
- Updated to 0.9.1 release
- Fix license tag syntax
- Don't mark init script as a config file

* Wed Sep 26 2007 Daniel P. Berrange <berrange@redhat.com> - 0.9.0-5.fc8
- Fix rtl8139 checksum calculation for Vista (rhbz #308201)

* Tue Aug 28 2007 Daniel P. Berrange <berrange@redhat.com> - 0.9.0-4.fc8
- Fix debuginfo by passing -Wl,--build-id to linker

* Tue Aug 28 2007 David Woodhouse <dwmw2@infradead.org> 0.9.0-4
- Update licence
- Fix CDROM emulation (#253542)

* Tue Aug 28 2007 Daniel P. Berrange <berrange@redhat.com> - 0.9.0-3.fc8
- Added backport of VNC password auth, and TLS+x509 cert auth
- Switch to rtl8139 NIC by default for linkstate reporting
- Fix rtl8139 mmio region mappings with multiple NICs

* Sun Apr  1 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.9.0-2
- Fix direct loading of a linux kernel with -kernel & -initrd (bz 234681)
- Remove spurious execute bits from manpages (bz 222573)

* Tue Feb  6 2007 David Woodhouse <dwmw2@infradead.org> 0.9.0-1
- Update to 0.9.0

* Wed Jan 31 2007 David Woodhouse <dwmw2@infradead.org> 0.8.2-5
- Include licences

* Mon Nov 13 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.8.2-4
- Backport patch to make FC6 guests work by Kevin Kofler
  <Kevin@tigcc.ticalc.org> (bz 207843).

* Mon Sep 11 2006 David Woodhouse <dwmw2@infradead.org> 0.8.2-3
- Rebuild

* Thu Aug 24 2006 Matthias Saou <http://freshrpms.net/> 0.8.2-2
- Remove the target-list iteration for x86_64 since they all build again.
- Make gcc32 vs. gcc34 conditional on %%{fedora} to share the same spec for
  FC5 and FC6.

* Wed Aug 23 2006 Matthias Saou <http://freshrpms.net/> 0.8.2-1
- Update to 0.8.2 (#200065).
- Drop upstreamed syscall-macros patch2.
- Put correct scriplet dependencies.
- Force install mode for the init script to avoid umask problems.
- Add %%postun condrestart for changes to the init script to be applied if any.
- Update description with the latest "about" from the web page (more current).
- Update URL to qemu.org one like the Source.
- Add which build requirement.
- Don't include texi files in %%doc since we ship them in html.
- Switch to using gcc34 on devel, FC5 still has gcc32.
- Add kernheaders patch to fix linux/compiler.h inclusion.
- Add target-sparc patch to fix compiling on ppc (some int32 to float).

* Thu Jun  8 2006 David Woodhouse <dwmw2@infradead.org> 0.8.1-3
- More header abuse in modify_ldt(), change BuildRoot:

* Wed Jun  7 2006 David Woodhouse <dwmw2@infradead.org> 0.8.1-2
- Fix up kernel header abuse

* Tue May 30 2006 David Woodhouse <dwmw2@infradead.org> 0.8.1-1
- Update to 0.8.1

* Sat Mar 18 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-6
- Update linker script for PPC

* Sat Mar 18 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-5
- Just drop $RPM_OPT_FLAGS. They're too much of a PITA

* Sat Mar 18 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-4
- Disable stack-protector options which gcc 3.2 doesn't like

* Fri Mar 17 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-3
- Use -mcpu= instead of -mtune= on x86_64 too
- Disable SPARC targets on x86_64, because dyngen doesn't like fnegs

* Fri Mar 17 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-2
- Don't use -mtune=pentium4 on i386. GCC 3.2 doesn't like it

* Fri Mar 17 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-1
- Update to 0.8.0
- Resort to using compat-gcc-32
- Enable ALSA

* Mon May 16 2005 David Woodhouse <dwmw2@infradead.org> 0.7.0-2
- Proper fix for GCC 4 putting 'blr' or 'ret' in the middle of the function,
  for i386, x86_64 and PPC.

* Sat Apr 30 2005 David Woodhouse <dwmw2@infradead.org> 0.7.0-1
- Update to 0.7.0
- Fix dyngen for PPC functions which end in unconditional branch

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Feb 13 2005 David Woodhouse <dwmw2@infradead.org> 0.6.1-2
- Package cleanup

* Sun Nov 21 2004 David Woodhouse <dwmw2@redhat.com> 0.6.1-1
- Update to 0.6.1

* Tue Jul 20 2004 David Woodhouse <dwmw2@redhat.com> 0.6.0-2
- Compile fix from qemu CVS, add x86_64 host support

* Mon May 12 2004 David Woodhouse <dwmw2@redhat.com> 0.6.0-1
- Update to 0.6.0.

* Sat May 8 2004 David Woodhouse <dwmw2@redhat.com> 0.5.5-1
- Update to 0.5.5.

* Thu May 2 2004 David Woodhouse <dwmw2@redhat.com> 0.5.4-1
- Update to 0.5.4.

* Thu Apr 22 2004 David Woodhouse <dwmw2@redhat.com> 0.5.3-1
- Update to 0.5.3. Add init script.

* Thu Jul 17 2003 Jeff Johnson <jbj@redhat.com> 0.4.3-1
- Create.
