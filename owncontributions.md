# Own Contributions
This page gives an overview of individual contributions by the different members of the project. 
There was collaboration and discussions on many different parts between all members however, either in person or online.

## Aron

In preparation for investigating BLE devices, the best tool for fulfilling our project statement needed to be identified. 
On the preparation stage, we all investigated different tools, and I looked at how well Wireshark would function as a method of scanning and enumerating Bluetooth devices.
This did show promise, giving information such as the source and destination of each device, the protocol, length, and other information. 
The information we needed could be found with the help of the Bleak tool however, which also gave more flexibility as we could more easily work with a script of our own.

In the stage of code-writing, in addition to working on bluetoothscanner.py for reasons such as fixing inconsistencies or bugs that affected the program, I worked on testing to find where issues could lie.
This also involved doing some manual tests to investigate the accuracy of bluetoothscanner.py, which told us that there could be inaccuracies in the exact distance of a device,
even though it generally would be correct about how far away it was. 

