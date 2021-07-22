---
title: "Building a Search Engine on Kubernetes using Elasticsearch"
content_type: tutorial
weight: 60
---

<!-- overview -->

{{< warning >}}
This deployment is not suitable for production use cases, you need to benchmark or size your cluster according to your use case.
{{< /warning >}}

{{< note >}}
The files provided in this tutorial are using GA Deployment APIs and are specific to kubernetes version 1.16 and 1.20. You can also try it on newer Kubernetes version but some APIs might throw deprecated warnings. 
{{< /note >}}

## {{% heading "objectives" %}}

1. You will learn about deploying a stateful application Elasticsearch and a visualizer like Kibana on Kubernetes.
2. Then, you will build a simple React-based search app using Kubernetes as a backend.


## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}
The example shown on this page works with `kubectl` 1.16 and above.

1. Brief understanding of REST APIs.
2. High-level understanding of Elasticsearch.

<!-- lessoncontent --> 

# Creating an Elasticsearch Cluster

There are many ways to run software like Elasticsearch on Kubernetes. For example, you could use the docker images or a helm chart. I’m using the official Kubernetes operator here. 

An operator SDK helps you run general-purpose software native to Kubernetes by adding application-specific controllers that automate application-specific business logic. For more details on Operators, you might want to visit the [Operator SDK website](https://sdk.operatorframework.io/) & [Operator Hub](https://operatorhub.io/).


### Installing Elastic Cloud on Kubernetes (ECK) operator: 


```
$ kubectl apply -f https://download.elastic.co/downloads/eck/1.6.0/all-in-one.yaml
```



### Checking the logs of Operator


```
$ kubectl -n elastic-system logs -f statefulset.apps/elastic-operator
```



### Creating a three-node Elasticsearch cluster:

We will create a three-node Elasticsearch cluster with the load balancer to expose the cluster publically. But, of course, you can choose not to do it if you only want the cluster to be accessible locally. 


```
cat <<EOF | kubectl apply -f -
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: 7.13.2
  http:
    service:
      spec:
        type: LoadBalancer
  nodeSets:
  - name: default
    count: 3
    config:
      node.store.allow_mmap: false
EOF
```



### Checking the health of the Elasticsearch cluster


```
$kubectl get elasticsearch
```


Did you notice? Instead of querying the pods, now we could query Elasticsearch like any other native resource of Kubernetes.  


```
$kubectl get pods -w

$kubectl logs -f quickstart-es-

$kubectl get service quickstart-es-http
```


The operator configures the cluster with basic security enabled, generates a password for the default user `elastic`, and stores it in the Kubernetes secrets. It also encrypts data between the nodes.  

Let us retrieve the same and store it in an environment variable for future access.


```
$PASSWORD=$(kubectl get secret quickstart-es-elastic-user -o=jsonpath='{.data.elastic}' | base64 --decode)

$echo $PASSWORD

$curl -u "elastic:$PASSWORD" -k "https://quickstart-es-http:9200"
```


**Note:** 



1. You could access the cluster provided that you are in the same network (for ex: via a container running). Otherwise, you could replace “quickstart-es-http” with the IP address/localhost provided by the load balancer. 
2. `$PASSWORD `is automatically generated for default user `elastic` and can be used to log in to Kibana in the next step.


# Creating Kibana


```
$cat <<EOF | kubectl apply -f -
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: quickstart
spec:
  version: 7.13.2
  http:
    service:
      spec:
        type: LoadBalancer
  count: 1
  elasticsearchRef:
    name: quickstart
EOF
```


You can run the below command to see if Kibana is deployed and the status of its.” health. Depending on your infrastructure and k8s cluster, it might take 30 seconds to 120 seconds.


```
$kubectl get kibana -w
```



### Kibana Dev Tools

Pick up the External IP Address of the Kibana using the below command.


```
$ kubectl get svc
```


Open Kibana in a web browser with `https://<IP_ADDRESS>:5601. `Proceed by ignoring the certificate warning. Enter the username as `elastic` and the default auto-generated password by the elastic operator. 

Screenshots for reference.


![Login to Kibana](1-login-kibana.png)


Click on “Explore on my own”...



![Click on explore on my own](2-explore-on-my-own-kibana.png)


You should see below home page.



![Homepage of Kibana](3-homepage-kibana.png)


Search for Dev Tools in the search bar. Hit “Command + /” on Mac OR “CTRL + /” on Windows.



![Dev Tools quick search](4-devtools-search.png)


You will reach “Dev Tools.” 



![Dev Tools in Kibana](5-devtools-kibana.png)



# Create an Index

Execute all the commands below in the Kibana Dev tools. 


```
PUT national-parks
```



### Creating a Schema

Elasticsearch is a schema-free datastore but not schema-less. Every index will have a schema defined, and you can find the schema of the documents stored in an index using the `_mapping` endpoint. 

If you have not defined the mapping, Elasticsearch would automatically detect the fields in the document and assign relevant field types (Text, Keyword, Long, Double). 

We will define the mapping and then ingest the documents into Elasticsearch. Here, we will use “US national parks” as a sample dataset. 

A sample document -- 


```
{
   "description":"Covering most of Mount Desert Island and other coastal islands, Acadia features the tallest mountain on the Atlantic coast of the United States, granite peaks, ocean shoreline, woodlands, and lakes. There are freshwater, estuary, forest, and intertidal habitats.",
   "nps_link":"https://www.nps.gov/acad/index.htm",
   "states":[
      "Maine"
   ],
   "title":"Acadia",
   "id":"park_acadia",
   "visitors":3303393,
   "world_heritage_site":false,
   "location":"44.35,-68.21",
   "acres":49057.36,
   "square_km":198.5,
   "date_established":"1919-02-26T06:00:00Z"
}
```



### Schema for the above document

```
POST national-parks/_mapping
{
    "properties": {
      "states": {
        "type": "text"
      },
      "date_established": {
        "type": "date"
      },
      "description": {
        "type": "text"
      },
      "title": {
        "type": "text"
      },
      "acres": {
        "type": "float"
      },
      "nps_link": {
        "type": "keyword"
      },
      "visitors": {
        "type": "long"
      },
      "location": {
        "type": "geo_point"
      },
      "id": {
        "type": "keyword"
      },
      "world_heritage_site": {
        "type": "boolean"
      },
      "square_km": {
        "type": "float"
      }
    }
} 
```



# Ingesting the data

Download the sample national park dataset from [here](https://raw.githubusercontent.com/elastic/search-ui/master/examples/elasticsearch/data/national-es-bulk-index.json). 

Copy the content of the JSON file and paste it as a body to the below request. Execute the request in the Dev Tools page of Kibana, similar to the above step. 

```
POST _bulk 
{
  <JSON_CONTENT_GOES_HERE>
}
```

### Searching via API

Without a UI, you could simply search the index using the _search endpoint.


```
GET national-parks/_search
{
  "query": {
    "terms": {
      "world_heritage_site": [
        "false"
      ]
    }
  }
}
```



### Using a Sample UI

Lastly, you could build a web application on the Elasticsearch APIs using any front-end framework like Vue, gatsby, or even backend Java-based frameworks. 

Here we will be using an Open-source UI library called “[search-ui](https://github.com/elastic/search-ui/),” which directly connects to the Elasticsearch search endpoint. 


```
$ git clone https://github.com/elastic/search-ui

$ cd search-ui/examples/elasticsearch
```


Install all the node dependencies with the below command.


```
$ npm install 

$ ELASTICSEARCH_HOST=https://elastic:{$PASSWORD}@{IP_ADDRESS} npm start
```


The UI will open the web browser on `localhost:3000. `



![Search UI](6-search-ui.png)

## {{% heading "cleanup" %}}

Below command deletes all the resources created by operator

```
$ kubectl get namespaces --no-headers -o custom-columns=:metadata.name | xargs -n1 kubectl delete elastic --all -n

```

And then, you can also uninstall the Elastic cloud on Kubernets operator installed. 

```
$ kubectl delete -f https://download.elastic.co/downloads/eck/1.6.0/all-in-one.yaml
```

## {{% heading "whatsnext" %}}

We have installed an Elastic operator on Kubernetes, created a three(3) node Elasticsearch cluster, Created a Kibana instance, Ingested data, made it ready for the Search app. 

But to deploy to take this to production further, there are few things that one needs to think like the storage classes offered by different Kubernetes services, Elasticsearch security specifics., because we’re using a default user, etc.

If you are looking for more details or examples on the operator, kindly refer to the below links:

* [Troubleshooting Elastic Cloud on Kubernetes Operator](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-troubleshooting.html)
* [Usage with Service meshes](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-service-meshes.html)
* [Raise a GitHub issue](https://github.com/elastic/cloud-on-k8s/issues)