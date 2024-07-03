Vagrant.configure(2) do |config|
    config.ssh.insert_key = false

    config.vm.define "vagrant_cheetah" do |v|
        v.vm.box = "ubuntu/focal64"
        v.vm.network "forwarded_port", guest: 25565, host: 25565
        v.vm.network "forwarded_port", guest: 25575, host: 25575
        v.vm.network "forwarded_port", guest: 9100, host: 9100
        v.vm.provider "virtualbox" do |vb|
            vb.memory = 4096
            vb.cpus = 2
        end
    end

    config.vm.define "vagrant_owl" do |v|
        v.vm.box = "ubuntu/focal64"
        v.vm.network "forwarded_port", guest: 3000, host: 3000
        v.vm.network "forwarded_port", guest: 9090, host: 9090
        v.vm.network "forwarded_port", guest: 80, host: 8080
        v.vm.network "forwarded_port", guest: 443, host: 8443
        v.vm.provider "virtualbox" do |vb|
            vb.memory = 2048
            vb.cpus = 1
        end
    end
end
