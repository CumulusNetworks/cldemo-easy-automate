# DEPRECATED
## This repo is no longer maintained.<br>For a list of current demos, please visit:<br>https://gitlab.com/cumulus-consulting/goldenturtle/<br><br><br>

Easy Automation Demo
====================
This demo shows how to get started with automation by starting with the configuration already on the switches in your network. The ideal audience for this demo is an organization with a small network who aspires to migrate from a transactional operation scheme to an infrastructure-as-code scheme. This demo is designed to be used as a starting point in order to become comfortable with 

Infrastructure as Code
----------------------
Infrastructure is usually configured *transactionally*. This means that when an operator wants to configure a device, they will incrementally apply changes to the device. The configuration of the device is the history of all transactional changes that have been made. While this often meets the requirements of small organizations, there are some drawbacks that come with transactional changes in IT.

 * Backups can fall out of sync with the actual machine states
 * Difficult for peers to review configuration before it goes live
 * Requires downtime for live application and testing to make sure changes went through error-free
 * Restoring from backups may be time consuming and error prone

A simplified description of the transactional model consists of two steps: apply changes to all devices, then update the backup with the changes made. In the *Infrastracture as Code* model, the process is reversed: edit the "backup", then apply the updated "backup" to all of the devices.

Infrastructure as Code involves keeping a gold standard version of the entire configuration in some centralized location, and then applying a tool to convert the gold standard to live configuration on the boxes. This addresses the three limitations raised earlier since there are no more backups (devices should always be up to the gold standard), peers have lots of time to review proposed changes for errors before deployment, downtime can be reduced since automation tools convert the gold standard to automation much faster than human operators can apply it. Finally, restoring from backups is easy, since the process for application and restoring from a backup is standardized.


Getting Started
---------------
This github repository contains two tools: a program that will retrieve configuration from switches in the network, and an Ansible playbook that will apply configuration to switches. We will create a virtual topology, configure it, make a backup, and then apply a change using the infrastructure as code methodology.

### Build the virtual topology
Be sure that you have Vagrant 1.8.x and Virtualbox 5.0.x installed.

    git clone https://github.com/cumulusnetworks/cldemo-vagrant
    cd cldemo-vagrant
    vagrant up oob-mgmt-server oob-mgmt-switch leaf01 leaf02
    vagrant ssh oob-mgmt-server
    sudo su - cumulus

### Manually configure the network on the two switches

    ssh leaf01
    sudo su
    echo "auto swp49" >> /etc/network/interfaces
    echo "iface swp49" >>  /etc/network/interfaces
    echo "address 10.50.0.0/31" >> /etc/network/interfaces
    ifup swp49
    exit
    exit
    ssh leaf02
    sudo su
    echo "auto swp49" >> /etc/network/interfaces
    echo "iface swp49" >>  /etc/network/interfaces
    echo "address 10.50.0.1/31" >> /etc/network/interfaces
    ifup swp49
    ping 10.50.0.0
    exit
    exit

### Create a fork of cldemo-easy-automate
On Github, create a fork of https://github.com/cumulusnetworks/cldemo-easy-automate - this will represent your gold standard config.

    git clone https://github.com/MYFORK/cldemo-easy-automate
    cd easyautomate
    python collect.py leaf01,leaf02
    git config --global user.email "you@example.com"
    git config --global user.name "Your Name"
    git add --all
    git commit -am "First pull of config"
    git push

Look on github and see the configs.

![img/fig3.png](img/fig3.png)

### Edit the gold standard and apply changes
On Github, you can edit files directly. Edit `/etc/network/interfaces` for leaf01 and leaf02 to add an ip address on swp50.

![img/fig1.png](img/fig4.png)
![img/fig1.png](img/fig5.png)

On your out of band management server, pull the changes you made and apply them using the ansible playbook.

    git pull
    ansible-playbook deploy.yml
    ssh leaf01
    ping 10.51.0.1

### Simulate a network failure and restore from gold standard
We will now simulate a network failure by destroying our entire topology and reprovisioning from scratch using our infrastructure as code!

    vagrant destroy -f
    vagrant up oob-mgmt-server oob-mgmt-switch leaf01 leaf02
    vagrant ssh oob-mgmt-server
    sudo su - cumulus
    git clone https://github.com/MYFORK/cldemo-easy-automate
    cd easyautomate
    ansible-playbook deploy.yml
