---
title: "Cold Starts: AWS vs Azure vs GCP"
date: 2023-02-19
draft: true
---
 
## TL;DR

**Disclaimer: These results are representative of my specific simulation setup. Simulations with different parameters may yield different results. For example: higher volume, larger function size, different language, different region etc…**


Overall, AWS was the easiest to set up and was the most stable in terms of function latency across all regions. GCP was the fastest in terms of client-side latency and I’m still not sure why this is the case. Given that the datacenters for each cloud provider are relatively close to each other, my best guess would be that GCP’s server-side performance is simply faster. 

If I were to deploy to production for my specific use-case of a fast and low volume function, I would most likely choose GCP since I would save an extra 100 - 300 milliseconds. However, if the function time was several seconds, I believe that AWS would become more attractive as the performant function time would start offsetting the client-side latency.

Azure’s client-side latency variance was quite high and appeared to be right-skewed. This combined with the numerous paper cuts in the integration, I would not use Azure in a production use-case at the moment.

Caveat: I’m not sure if I should weigh the client-side latency findings too heavily since client-side latency can be impacted by a number of external factors: physical location, server-side latency, network latency, DNS, etc..



## Interesting findings

* Even though my call pattern was low-volume (once per minute), AWS Lambda would cold start roughly once every ~130 minutes plus or minus 20 minutes. [Reference](#aws-cold-start-latencies-by-region)
* From a client-side latency perspective, GCP Cloud Functions were the fastest across all regions by 100’s of milliseconds in some cases. There are several explanations for this: 
 * Server side latency - the time between when the cloud provider receives the invoke request to when the function is invoked
 * Network latency - The network hops from the caller to the cloud providers are likely different and could impact latency
 * Local setup  - In my simulation, I called various cloud providers from a t2.micro EC2 instance in us-west-2. The results could have varied if I used a different network setup or even a different cloud provider.
* All 3 cloud providers are relatively stable when comparing overall client latencies. When comparing p90 client latencies, AWS and GCP were relatively stable while Azure’s variance was significantly larger in most regions. [Reference](#p90-client-side-latency)
* For overall function and client latencies, Azure kept up with AWS and GCP. However, performance started to vary by orders of magnitude when looking at p90.

## Background
Cloud providers typically provide serverless functions where users provide the business logic and the cloud provider will manage the compute resources, i.e. the functions. In this doc, I will be reviewing the following services:
* AWS - AWS Lambda
* Azure - Cloud Functions
* GCP - Cloud Functions

When a serverless function is called, or invoked, the cloud provider will run the user’s code on a container or instance. In this scenario, the total client-side latency is the following:
* User’s code makes request to cloud provider
* Cloud provider calls user’s function
* Run user’s function
* Get the output and return to user

If there is no container available, one will be provisioned. This action introduces additional overhead and is often referred to as a “cold-start”:
* User’s code makes request to cloud provider
* **Provision new container (<--- cold start)**
* Cloud provider calls user’s function
* Run user’s function
* Get the output and return to user

| ![diagram!](/images/cs/csDefinitions.png "diagram") |
|:--:|
| **Fig. 1 - Latency definitions** |


## Why do this?
In general, there is not a lot of visibility into how much time is spent inside the cloud provider outside of the user’s function. To be specific, these are the open questions that I am hoping to answer:
* How frequently do users see cold starts?
* What is the variance of function latency?
* What is the variance of client latency?


## Out of scope

### User isolation
By the nature of distributed systems, a spike in latency or errors for one user does not necessarily indicate a service-wide outage. As such, this analysis is not representative of overall service health. It can only be used to identify its own availability.
Other errors

There is a chance that requests could fail that are not related to the serverless functions availability. I will do my best to filter those requests out but it will be difficult to root cause those errors.

### Hosting
If the canary runs on the same infrastructure as some of the Cloud Functions, that may bias some of the results. For example, the canary running on an AWS EC2 instance calling Lambda may produce different results if the canary was running on completely isolated infrastructure.

## Simulation setup
I have a t2.micro EC2 instance launched in us-west-2 (Oregon). Once per minute, I will make requests to 4 regions in AWS, Azure, and GCP. I have chosen specific regions that are in close proximity to each other so that we can get as close to an apples to apples comparison as possible.


| Airport code | AWS                     | Azure                          | GCP                            |
| ------------ | ----------------------- | ------------------------------ | ------------------------------ |
| GRU          | sa-east-1 (São Paulo)   | Brazil South (São Paulo State) | southamerica-east1 (São Paulo) |
| IAD          | us-east-1 (N. Virginia) | East US (Virginia)             | us-east4 (north virginia)      |
| LHR          | eu-west-2 (London)      | UK South (London)              | europe-west2 (london)          |
| NRT          | ap-northeast-1 (Tokyo)  | Japan East (Tokyo)             | asia-northeast1 (Tokyo)        |


All functions are configured with the following:
* 128MB memory
* Python 3.8 runtime
* x86-based architecture

I am opting to NOT use additional provider-specific configurations that may help improve performance and reduce cold starts. For this simulation, I am interested in seeing how each service performs out of the box.

## Results

### Function Latency (excluding outliers)

#### Overall Function Latency by Region

![GRU Function Latency](/images/cs/FunctionLatencyGRU.png "GRU Function Latency")
![IAD Function Latency](/images/cs/FunctionLatencyIAD.png "IAD Function Latency")
![LHR Function Latency](/images/cs/FunctionLatencyLHR.png "LHR Function Latency")
![NRT Function Latency](/images/cs/FunctionLatencyNRT.png "NRT Function Latency")

**Winner: AWS**

#### p90 Function Latency by Region

![GRU P90 Function Latency](/images/cs/FunctionLatencyP90GRU.png "GRU P90 Function Latency")
![IAD P90 Function Latency](/images/cs/FunctionLatencyP90IAD.png "IAD P90 Function Latency")
![LHR P90 Function Latency](/images/cs/FunctionLatencyP90LHR.png "LHR P90 Function Latency")
![NRT P90 Function Latency](/images/cs/FunctionLatencyP90NRT.png "NRT P90 Function Latency")

### Client-side latency (excluding outliers)

#### Overall Client-side Latency

![GRU Client-side Latency](/images/cs/ClientLatencyGRU.png "GRU Client-side Latency")
![IAD Client-side Latency](/images/cs/ClientLatencyIAD.png "IAD Client-side Latency")
![LHR Client-side Latency](/images/cs/ClientLatencyLHR.png "LHR Client-side Latency")
![NRT Client-side Latency](/images/cs/ClientLatencyNRT.png "NRT Client-side Latency")

#### p90 Client-side Latency

![GRU P90 Client-side Latency](/images/cs/ClientLatencyP90GRU.png "GRU P90 Client-side Latency")
![IAD P90 Client-side Latency](/images/cs/ClientLatencyP90IAD.png "IAD P90 Client-side Latency")
![LHR P90 Client-side Latency](/images/cs/ClientLatencyP90LHR.png "LHR P90 Client-side Latency")
![NRT P90 Client-side Latency](/images/cs/ClientLatencyP90NRT.png "NRT P90 Client-side Latency")

### AWS Cold Start Latencies by Region

![AWS cold start Latency](/images/cs/AWSColdStartLatency.png "AWS Cold Start Latency")

### Time between cold starts

![AWS time between cold starts](/images/cs/ColdStartDeltaAWS.png "AWS Cold Start Delta")
![Azure time between cold starts](/images/cs/ColdStartDeltaAzure.png "Azure Cold Start Delta")
![GCP time between cold starts](/images/cs/ColdStartDeltaGCP.png "GCP Cold Start Delta")


### Azure and GCP cold starts
I would have liked to measure the impact of Azure and GCP cold starts as well but there is not a good mechanism for accurately measuring them at the invoke level.

Azure has the concept of a “HostInstanceId”, which represents the instance on which your invoke ran on. However, even if we interpret a new “HostInstanceId” as a cold start, it does not guarantee that Azure is not creating buffer instances in the back 


## Paper cuts

### AWS

Little to no issues here. Integration was very quick. I copy-pasted an example from [the boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.invoke) and it worked on the first try. I didn’t have to scan Cloudwatch Logs since the response from Lambda gives you the function duration and the init duration, if there was a cold start.


![Code works](/images/cs/notSure.png "Code works")

### GCP

Getting the Python Cloud Functions client to work with auth was a bit tedious. The documentation will eventually lead you to [this giant web page with all the method definitions](https://googleapis.dev/python/cloudfunctions/latest/functions_v2/function_service.html) that was a bit difficult to go through.

### Azure

Azure was the most painful integration. There were several fields I needed to set in order to get the function working. After I created function keys, they would automatically get deleted after some amount of time. After Googling, I found that I needed to update the lifecycle policy in the storage account. There were cases where Azure would just be missing logs from my invocations so I was unable to get some performance numbers.



