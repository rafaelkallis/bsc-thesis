A content store is a database system which supports hierarchical (tree-structured) data.
It behaves similar to a traditional file system, that is, storing files/ data annotated with metadata.
Like common relational DBMSs, content stores also can provide transactions and querying.
Apache Jackrabbit Oak (reference) is such a tree-structured content store, with two design goals in mind.
It needs to be able to operate in a distributed environment and guarantee write throughput.
Multiple Oak instances can work concurrently by making use of MVCC (reference), a commonly used optimistic technique.
Whilst Oak is responsible for handling the logic (?), Oak does not persist the data itself.
It relies on MongoDB (reference), a popular document store, to persist the data.
Although Oak is an Open-source project, it is being actively maintained by Adobe (reference). 
Adobe makes use of Oak in one of their products, specifically the Adobe Experience Manager (AEM).

// Diagram:
[AEM1] [AEM2] [AEM3] (Application Tier)
   |     |   /
[Oak1] [Oak2] (Database Tier)
   |    /
[MongoDB] (Persistence Tier)
//Figure 1

In the following pages, we will take a closer look at Oak.
Specifically, we will see how Oak handles querying, writing and concurrency control.
After that I will introduce you to an instance of a problem Oak is having and we will briefly introduce a solution which results in higher throughput under certain circumstances.
We will revisit Oak's reference implementations and modify them in order to satisfy our solution.
Lastly, we will formalize the solution.

### 2) Persistance tier

Before we get into the mechanics of Oak, we need to understand how Oak chose to persist data.
As mentioned earlier, Oak's data is tree-structured.
Figure 2 shows a tree alongside its persisted representation.
Each tree node is persisted in the shape of a JSON document in MongoDB.
Each node is identifiable its tree-depth concatenated with its absolute path from the root node, denoted as "_id".
A node's properties, are represented by key-value pairs inside the node's JSON document.
"_id" can be considered as a property.

[
    { "_id": "0:/",    /* ... */ },
    { "_id": "1:/a",   /* ... */ },
    { "_id": "2:/a/b", /* ... */ },
    { "_id": "2:/a/c", /* ... */ }
]

            root
               \              
                a                  
                | \                 
                b  c             
    
// Figure 2.1: internal node representation.

In order to support MVCC, Oak keeps a history of values each property had in the past such that we are able to tell when each value was persisted and which Oak instance committed the change. 
In Figure 3, we take a look at node "/a/c" and see how "x"'s value changes over time.
Each value's key is composed with a timestamp, a counter that is used to differentiate between value changes during the same instance of time and the identifier of the oak instance committing the change.
Let's consider "r15cac0dbb00-0-2".
"r" is a standard prefix and can be neglected.
"15cac0dbb00" is an timestamp in hexadecimal encoding which represents the time during which the change was committed.
"0" tells that the change was the 1st change of the specific property during that instance of time.
"2" tells that the change was committed by the Oak instance which is identified with 2.

[
    {
        "_id": "2:/a/c", 
        "x": {
            "r15ca9f191c0-0-1": "1",
            "r15cabff1500-0-2": "2",
            "r15cac0dbb00-0-2": "3"
        },
        /* ... */
    },
    /* ... */
]
// Figure 2.2: extended internal node representation

### 3) Oak basic ops

In this chapter we will try to understand how Oak handles basic operations such as queries and writes.

#### 3.1) Querying

Oak is commonly queried using content-and-structure (CAS) queries.
A CAS query returns all children of a given node, which have a given property set to a given value.

Definition 3.1.1 (CAS-query): Q_{k,v,m} = {n | n[k] == v && n ∈ desc(m)}, where k denotes the property name (key), v the value, m a node, n[k] property k of node n, desc(m) all descendants of node m.

// Example 3.1.1
G:
        [root]
             \        
            [a, x: "3"] 
                |       \
            [b, x:"3"]   [c]

Q_{x, 3, a} = { b }

In order to answer CAS queries efficiently, a property index (PI) can be implemented. A PI can look as follows:

// Example 3.1.2
G:
        [root]
      /          \        
    [index]      [a, x: "3"] 
     |           |       \
    [x]       [b, x:"3"]   [c]
     |
    [3]
     |
    [a]
     |
    [b]

By structuring the PI as shown above, a CAS query can be executed as follows:

// Algorithm 3.1 (QueryPI)
Input: Triple(k, v, m), where k is a property, v a value and m a node.
|   n <- /index
|   foreach λ ∈ < k, v, ... , par(m)[λ], m[λ] > do
|   |   n <- n | /λ
|   |   if n does not exist then
|   |_  |_  return ø
|   r <- ø
|   foreach node d ∈ desc(n) do
|   |   if d[k] = v then 
|   |_  |_  r <- r U { d }
|_  return r
Where λ is a node's label, i.e node /a/c has "c" as a label , | is the concatenation operator, par(m) returns the parent node of m and d[k] returns the latest value of property k on node d.

We see that Algorithms 3.1's performance is dependent on the node m's tree depth (1st loop) and on the number of descendants of n (2nd loop). 

Descendants of a node in the PI are not guaranteed to satisfy a CAS query. 
Let's consider example 3.1.2
QueryPI(x, 3, /) results in { "/a", "/a/b" }.
Assume now that "/a" does not have a property "x" anymore.
QueryPI'(x, 3, /) results in { "/a/b" } but the PI remains unchanged (PI = PI').
"/a" still is a member of PI' (under /index/x/3) but does not satisfy the CAS query.

### 3.2) Updates

In this chapter we will see how Oak handles writes. 
An update is roughly composed as follows:

- Make copy of latest tree
- Calculate write set
- Perform optimistic techniques (check whether another update interferes)
- Commit changes
- Make changes visible to other Oak instances

We will make use of the following example for the rest of the chapter:

// Example 3.1.2
G0:
        [root]
      /          \        
    [index]          [a] 
     |               |   \
    [x]       [b, x:true]   [c]
     |
    [true]
     |
    [a]
     |
    [b]

G1:
        [root]
      /          \        
    [index]          [a] 
     |               |   \
    --[x]--       [b, --x:true--]   [c]
     |
    --[true]--
     |
    --[a]--
     |
    --[b]--

G0 is the initial state. Transaction T1 generates G1 based on G0. 
T_1 removes property x from "/a/b".

Definition 3.2.1 (Write Set) The write set DeltaT_j of a transaction T_j are all node- and property changes made by T_j. With G^i being T^i's tree, DeltaT_j is defined as follows.

DeltaT_j = { wn(n^j) | n^i ∉ N(G^i) && n^j ∈ N(G^j) || n^i ∈ N(G^i) && n^j ∉ N(G^j) } U {wp(n^j, k) | n^i ∈ N(G^i) && n^j ∈ N(G^j) && n^i[k] != n^j[k] }

wn denotes write node.
wp denotes write property.

For example, 

DeltaT_1 = {
    wp(/a/b, x),
    wn(/index/x),
    wn(/index/x/true),
    wn(/index/x/true/a),
    wn(/index/x/true/a/b),
}

Note that if we remove property "x" from "/a/b", we also have to update the PI.

After T_1 calculates the write set, it check whether other transactions had conflicting updates.
We will see how a transaction determines wether there are conflicting changes later.
In order to keep things simple, we will assume that T_1 started after all other transactions finished, which implies there are no conflicting changes. (reference: Database Systems, Catherine Ricardo p. 445).

Since we passed the validation we can commit the changes.
All actions specified in the write set are commited.
The following example depict all scenarios

a) wp(/a/c, x) (property x:true added)
[
    {
        "_id": "2:/a/c",
        "x": {
            "r15cabff1500-0-1": true
        },
        /* ... */
    },
    /* ... */
]


b) wp(/a/c, x) (property x:true -> x:false modified)
[
    {
        "_id": "2:/a/c",
        "x": {
            "r15cabff1500-0-1": true,
            "r15cac0dbb00-0-1": false
        },
        /* ... */
    },
    /* ... */
]

c) wp(/a/c, x) (property x removed)
[
    {
        "_id": "2:/a/c",
        "x": {
            "r15cabff1500-0-1": true,
            "r15cac0dbb00-0-1": false,
            "r15cad0cbc00-0-1": null
        },
        /* ... */
    },
    /* ... */
]    

d) wn(/a/c/d) (node /a/c/d added)
[
    {
        "_id": "3:/a/c/d",
        "_deleted": {
            "r15cabff1500-0-1": false
        },
        /* ... */
    },
    /* ... */
]

e) wn(/a/c/d) (node /a/c/d removed)
[
    {
        "_id": "3:/a/c/d",
        "_deleted": {
            "r15cabff1500-0-1": false,
            "r15cac0dbb00-0-1": true
        },
        /* ... */
    },
    /* ... */
]



G2:
        [root]
      /          \        
    [index]          [a] 
     |               |   \
    [x]   [b, x:true] ++[c, x:true]++
     |
    [true]
     |
    [a]
   /   \
[b]     ++[c]++
T_2 adds property x: true to "/a/c".

DeltaT_2 = {
    wp(/a/c, x),
    wn(/index/x/true/a/c),
}