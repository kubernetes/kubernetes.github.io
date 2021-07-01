---
title: Network Policy
id: network-policy
date: 2018-04-12
full_link: /docs/concepts/services-networking/network-policies/
short_description: >
  A specification of how groups of Pods are allowed to communicate with each other and with other network endpoints.

aka: 
tags:
- networking
- architecture
- extension
---
 A specification of how groups of Pods are allowed to communicate with each other and with other network endpoints.

<!--more--> 

Network Policies help you declaratively configure which Pods are allowed to connect to each other, which namespaces are allowed to communicate, and more specifically which port numbers to enforce each policy on. `NetworkPolicy` resources use labels to select Pods and define rules which specify what traffic is allowed to the selected Pods. Network Policies are implemented by a supported network plugin provided by a network provider. Be aware that creating a network resource without a controller to implement it will have no effect.

