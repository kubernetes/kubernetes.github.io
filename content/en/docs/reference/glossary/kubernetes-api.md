---
title: Kubernetes API
id: kubernetes-api
date: 2018-04-12
full_link: /docs/concepts/overview/kubernetes-api/
short_description: >
  The application that serves Kubernetes functionality through a RESTful interface and stores the state of the cluster.

aka: 
tags:
- fundamental
- architecture
---
 The application that serves Kubernetes functionality through a RESTful interface and stores the state of the cluster.

<!--more--> 

Kubernetes resources and "records of intent" are all stored as API objects, and modified via RESTful calls to the API. The API allows configuration to be managed in a declarative way. Users can interact with the Kubernetes API directly, or via tools like `kubectl`. The core Kubernetes API is flexible and can also be extended to support custom resources.

