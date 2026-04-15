ISO_NAME=ubuntu-22.04.5-desktop-amd64.iso
GCOW_NAME=ubuntu-amd64.qcow2

create_disk:
	qemu-img create -f qcow2 $(GCOW_NAME) 60G

get_ubuntu_iso:
	wget https://releases.ubuntu.com/jammy/$(ISO_NAME)

install:
	qemu-system-x86_64 \
	-m 8G \
	-cdrom $(ISO_NAME) \
	-hda $(GCOW_NAME) \
	-boot d

boot:
	qemu-system-x86_64 \
	-m 12G \
	-hda $(GCOW_NAME) \
	-boot c
