# Vertical Farming project settings 

**Author**: *Bauyrzhan Zhakanov*, [bauyrzhan.zhakanov@gmail.com](bauyrzhan.zhakanov@gmail.com)

## Introduction

As the World population is growing in a rapid rate, the food production requires more efficient and resilient technology to feed humanity. Moreover, the climate change and geopolitical conflicts among countries caused social-economic issues in developing countries. To solve the food crisis issue, Vertical Farming project has been proposed.
The purpose of the project is to improve the architecture of a Vertical Farming with a help of IEC 61499 and Cloud services for enabling flexible automation.
Initially, hardware components of Vertical Farming remained the same except the addition of Logitech web camera to send the pictures for analysis into the cloud. Meanwhile inside the software components, the architecture was redesigned in IEC 61499 with Schneider Electric's Ecostruxture Automation Expert 21.2 that supports Cloud communication. As the choice of the cloud services Microsoft Azure was considered. The software architecture of Vertical Farming was divided into five layers: Control, Recipe, Organization, Service, and Execution. With an addition of the sixth layer, Vertical Farming has a potential to use machine learning algorithms for fine-tuning the control settings based on plant pictures. Finally those modification of the system would change its control settings to efficiently produce more yield.

## Control
The communication is going to be established through Raspberry Pi as a medium communicator. To take the visual data, Logitech web camera was connected to Raspberry Pi as part of Electrical Junction Box. The general architecture of Cloud based communication would be as following Figure. 

![comm_rasp](https://github.com/BZWayne/vf_connection/blob/main/comm_rasp.png)
