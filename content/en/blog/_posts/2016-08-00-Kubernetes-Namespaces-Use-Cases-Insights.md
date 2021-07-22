---
title: " Kubernetes Namespaces: use cases and insights "
date: 2016-08-16
slug: kubernetes-namespaces-use-cases-insights
url: /blog/2016/08/Kubernetes-Namespaces-Use-Cases-Insights
---

_“Who's on first, What's on second, I Don't Know's on third”&nbsp;_

_[Who's on First?](https://www.youtube.com/watch?v=kTcRRaXV-fg) by Abbott and Costello_



**Introduction**  

Kubernetes is a system with several concepts. Many of these concepts get manifested as “objects” in the RESTful API (often called “resources” or “kinds”). One of these concepts is [Namespaces](/docs/user-guide/namespaces/). In Kubernetes, Namespaces are the way to partition a single Kubernetes cluster into multiple virtual clusters. In this post we’ll highlight examples of how our customers are using Namespaces.&nbsp;  

But first, a metaphor: Namespaces are like human family names. A family name, e.g. Wong, identifies a family unit. Within the Wong family, one of its members, e.g. Sam Wong, is readily identified as just “Sam” by the family. Outside of the family, and to avoid “Which Sam?” problems, Sam would usually be referred to as “Sam Wong”, perhaps even “Sam Wong from San Francisco”. &nbsp;  

Namespaces are a logical partitioning capability that enable one Kubernetes cluster to be used by multiple users, teams of users, or a single user with multiple applications without concern for undesired interaction. Each user, team of users, or application may exist within its Namespace, isolated from every other user of the cluster and operating as if it were the sole user of the cluster. (Furthermore, [Resource Quotas](/docs/admin/resourcequota/) provide the ability to allocate a subset of a Kubernetes cluster’s resources to a Namespace.)  

For all but the most trivial uses of Kubernetes, you will benefit by using Namespaces. In this post, we’ll cover the most common ways that we’ve seen Kubernetes users on Google Cloud Platform use Namespaces, but our list is not exhaustive and we’d be interested to learn other examples from you.  

**Use-cases covered**  

- Roles and Responsibilities in an enterprise for namespaces
- Partitioning landscapes: dev vs. test vs. prod
- Customer partitioning for non-multi-tenant scenarios
- When not to use namespaces

**Use-case #1: Roles and Responsibilities in an Enterprise**



A typical enterprise contains multiple business/technology entities that operate independently of each other with some form of overarching layer of controls managed by the enterprise itself. Operating a Kubernetes clusters in such an environment can be done effectively when roles and responsibilities pertaining to Kubernetes are defined.&nbsp;  

Below are a few recommended roles and their responsibilities that can make managing Kubernetes clusters in a large scale organization easier.


- Designer/Architect role: This role will define the overall namespace strategy, taking into account product/location/team/cost-center and determining how best to map these to Kubernetes Namespaces. Investing in such a role prevents namespace proliferation and “snowflake” Namespaces.
- Admin role: This role has admin access to all Kubernetes clusters. Admins can create/delete clusters and add/remove nodes to scale the clusters. This role will be responsible for patching, securing and maintaining the clusters. As well as implementing Quotas between the different entities in the organization. The Kubernetes Admin is responsible for implementing the namespaces strategy defined by the Designer/Architect.&nbsp;



These two roles and the actual developers using the clusters will also receive support and feedback from the enterprise security and network teams on issues such as security isolation requirements and how namespaces fit this model, or assistance with networking subnets and load-balancers setup.



Anti-patterns

1. Isolated Kubernetes usage “Islands” without centralized control: Without the initial investment in establishing a centralized control structure around Kubernetes management there is a risk of ending with a “mushroom farm” topology i.e. no defined size/shape/structure of clusters within the org. The result is a difficult to manage, higher risk and elevated cost due to underutilization of resources.
2. Old-world IT controls choking usage and innovation: A common tendency is to try and transpose existing on-premises controls/procedures onto new dynamic frameworks .This results in weighing down the agile nature of these frameworks and nullifying the benefits of rapid dynamic deployments.
3. Omni-cluster: Delaying the effort of creating the structure/mechanism for namespace management can result in one large omni-cluster that is hard to peel back into smaller usage groups.&nbsp;

**Use-case #2: Using Namespaces to partition development landscapes**



Software development teams customarily partition their development pipelines into discrete units. These units take various forms and use various labels but will tend to result in a discrete dev environment, a testing|QA environment, possibly a staging environment and finally a production environment. The resulting layouts are ideally suited to Kubernetes Namespaces. Each environment or stage in the pipeline becomes a unique namespace.



The above works well as each namespace can be templated and mirrored to the next subsequent environment in the dev cycle, e.g. dev-\>qa-\>prod. The fact that each namespace is logically discrete allows the development teams to work within an isolated “development” namespace. DevOps (The closest role at Google is called [Site Reliability Engineering](https://landing.google.com/sre/interview/ben-treynor.html) “SRE”) &nbsp;will be responsible for migrating code through the pipelines and ensuring that appropriate teams are assigned to each environment. Ultimately, DevOps is solely responsible for the final, production environment where the solution is delivered to the end-users.



A major benefit of applying namespaces to the development cycle is that the naming of software components (e.g. micro-services/endpoints) can be maintained without collision across the different environments. This is due to the isolation of the Kubernetes namespaces, e.g. serviceX in dev would be referred to as such across all the other namespaces; but, if necessary, could be uniquely referenced using its full qualified name serviceX.development.mycluster.com in the development namespace of mycluster.com.



Anti-patterns

1. Abusing the namespace benefit resulting in unnecessary environments in the development pipeline. So; if you don’t do staging deployments, don’t create a “staging” namespace.
2. Overcrowding namespaces e.g. having all your development projects in one huge “development” namespace. Since namespaces attempt to partition, use these to partition by your projects as well. Since Namespaces are flat, you may wish something similar to: projectA-dev, projectA-prod as projectA’s namespaces.

**Use-case #3: Partitioning of your Customers**



If you are, for example, a consulting company that wishes to manage separate applications for each of your customers, the partitioning provided by Namespaces aligns well. You could create a separate Namespace for each customer, customer project or customer business unit to keep these distinct while not needing to worry about reusing the same names for resources across projects.



An important consideration here is that Kubernetes does not currently provide a mechanism to enforce access controls across namespaces and so we recommend that you do not expose applications developed using this approach externally.



Anti-patterns

1. Multi-tenant applications don’t need the additional complexity of Kubernetes namespaces since the application is already enforcing this partitioning.
2. Inconsistent mapping of customers to namespaces. For example, you win business at a global corporate, you may initially consider one namespace for the enterprise not taking into account that this customer may prefer further partitioning e.g. BigCorp Accounting and BigCorp Engineering. In this case, the customer’s departments may each warrant a namespace.

**When Not to use Namespaces**  


In some circumstances Kubernetes Namespaces will not provide the isolation that you need. This may be due to geographical, billing or security factors. For all the benefits of the logical partitioning of namespaces, there is currently no ability to enforce the partitioning. Any user or resource in a Kubernetes cluster may access any other resource in the cluster regardless of namespace. So, if you need to protect or isolate resources, the ultimate namespace is a separate Kubernetes cluster against which you may apply your regular security|ACL controls.



Another time when you may consider not using namespaces is when you wish to reflect a geographically distributed deployment. If you wish to deploy close to US, EU and Asia customers, a Kubernetes cluster deployed locally in each region is recommended.



When fine-grained billing is required perhaps to chargeback by cost-center or by customer, the recommendation is to leave the billing to your infrastructure provider. For example, in Google Cloud Platform (GCP), you could use a separate GCP [Project](https://cloud.google.com/compute/docs/projects) or [Billing Account](https://support.google.com/cloud/answer/6288653) and deploy a Kubernetes cluster to a specific-customer’s project(s).



In situations where confidentiality or compliance require complete opaqueness between customers, a Kubernetes cluster per customer/workload will provide the desired level of isolation. Once again, you should delegate the partitioning of resources to your provider.



Work is underway to provide (a) ACLs on Kubernetes Namespaces to be able to enforce security; (b) to provide Kubernetes [Cluster Federation](https://kubernetes.io/blog/2016/07/cross-cluster-services). Both mechanisms will address the reasons for the separate Kubernetes clusters in these anti-patterns.&nbsp;



An easy to grasp **anti-pattern** for Kubernetes namespaces is versioning. You should not use Namespaces as a way to disambiguate versions of your Kubernetes resources. Support for versioning is present in the containers and container registries as well as in Kubernetes Deployment resource. Multiple versions should coexist by utilizing the Kubernetes container model which also provides for auto migration between versions with deployments. Furthermore versions scope namespaces will cause massive proliferation of namespaces within a cluster making it hard to manage.



**Caveat Gubernator**



You may wish to, but you cannot create a hierarchy of namespaces. Namespaces cannot be nested within one another. You can’t, for example, create my-team.my-org as a namespace but could perhaps have team-org.



Namespaces are easy to create and use but it’s also easy to deploy code inadvertently into the wrong namespace. Good DevOps hygiene suggests documenting and automating processes where possible and this will help. The other way to avoid using the wrong namespace is to set a [kubectl context](/docs/reference/generated/kubectl/kubectl-commands#-em-set-context-em-).&nbsp;



As mentioned previously, Kubernetes does not (currently) provide a mechanism to enforce security across Namespaces. You should only use Namespaces within trusted domains (e.g. internal use) and not use Namespaces when you need to be able to provide guarantees that a user of the Kubernetes cluster or ones its resources be unable to access any of the other Namespaces resources. This enhanced security functionality is being discussed in the Kubernetes Special Interest Group for Authentication and Authorization, get involved at [SIG-Auth](https://github.com/kubernetes/kubernetes/wiki/SIG-Auth).&nbsp;



_--Mike Altarace & Daz Wilkin, Strategic Customer Engineers, Google Cloud Platform_





- [Download](http://get.k8s.io/) Kubernetes
- Get involved with the Kubernetes project on [GitHub](https://github.com/kubernetes/kubernetes)
- Post questions (or answer questions) on [Stack Overflow](http://stackoverflow.com/questions/tagged/kubernetes)
- Connect with the community on [Slack](http://slack.k8s.io/)
- Follow us on Twitter [@Kubernetesio](https://twitter.com/kubernetesio) for latest updates
