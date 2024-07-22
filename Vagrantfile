Vagrant.configure(2) do |config|
    config.ssh.insert_key = false

    config.vm.define "vagrant_cheetah" do |v|
        v.vm.box = "ubuntu/focal64"
        v.vm.hostname = "cheetah"
        v.vm.network "public_network", bridge: "enp4s0"

        v.vm.provision "shell",
            run: "always",
            inline: "ip route del default via 10.0.2.2"

        v.vm.provider "virtualbox" do |vb|
            vb.memory = 8192
            vb.cpus = 4
        end
    end
end
