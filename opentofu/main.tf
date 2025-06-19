terraform {
  required_providers {
    proxmox = {
      source  = "Telmate/proxmox"
      version = "2.9.11"
    }
  }
}

provider "proxmox" {
  pm_api_url      = "https://10.10.1.0:8006/api2/json"
  pm_user         = "root@pam"
  pm_password     = "mateusz"
  pm_tls_insecure = true
}

# Nginx Proxy VM
resource "proxmox_vm_qemu" "proxy" {
  name        = "nginxproxy01"
  target_node = "50thfloor"

  clone = "ubuntu-template"

  cores  = 1
  memory = 1024

  disk {
    size    = "16G"
    type    = "scsi"
    storage = "local-lvm"
  }

  network {
    bridge    = "vmbr0"
    model     = "virtio"
    firewall  = true
    macaddr   = "5A:BC:0B:C2:4E:52"  # Use this MAC if you want it static
    link_down = false
    mtu       = 0
    queues    = 0
    rate      = 0
    tag       = -1
  }

  ipconfig0 = "ip=dhcp,ip6=dhcp"

  ciuser  = "ansible"
  sshkeys = file("~/.ssh/id_rsa.pub")
}

# App Prod
resource "proxmox_vm_qemu" "prod" {
  name        = "prod01"
  target_node = "50thfloor"

  clone = "ubuntu-template"

  cores  = 4
  memory = 4096

  disk {
    size    = "100G"
    type    = "scsi"
    storage = "local-lvm"
  }

  network {
    bridge    = "vmbr0"
    model     = "virtio"
    firewall  = true
    macaddr   = "1E:11:1B:32:42:39"
    link_down = false
    mtu       = 0
    queues    = 0
    rate      = 0
    tag       = -1
  }

  ipconfig0 = "ip=dhcp,ip6=dhcp"

  ciuser  = "ansible"
  sshkeys = file("~/.ssh/id_rsa.pub")
}

resource "proxmox_vm_qemu" "test" {
  name        = "test01"
  target_node = "50thfloor"

  clone = "ubuntu-template"

  cores  = 2
  memory = 2048

  disk {
    size    = "100G"
    type    = "scsi"
    storage = "local-lvm"
  }

  network {
    bridge    = "vmbr0"
    model     = "virtio"
    firewall  = true
    macaddr   = "1E:11:1B:32:42:40"
    link_down = false
    mtu       = 0
    queues    = 0
    rate      = 0
    tag       = -1
  }

  ipconfig0 = "ip=dhcp,ip6=dhcp"

  ciuser  = "ansible"
  sshkeys = file("~/.ssh/id_rsa.pub")
}

variable "vm_count" {
  default = 4
}

resource "proxmox_vm_qemu" "kubernetes" {
  count       = var.vm_count
  name        = "kubernetes${count.index + 1}"
  target_node = "50thfloor"

  clone = "ubuntu-template"

  cores  = 2
  memory = 2048

  disk {
    size    = "100G"
    type    = "scsi"
    storage = "local-lvm"
  }

  network {
    bridge    = "vmbr0"
    model     = "virtio"
    firewall  = true
    macaddr   = "1E:11:1B:32:42:40"
    link_down = false
    mtu       = 0
    queues    = 0
    rate      = 0
    tag       = -1
  }

  ipconfig0 = "ip=dhcp,ip6=dhcp"

  ciuser  = "ansible"
  sshkeys = file("~/.ssh/id_rsa.pub")
}

