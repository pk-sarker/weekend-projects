# Tree Traversal Algorithm

One of the trickiest, and yet most common, challenges in programming comes from dealing with parallelization and asynchronous code. We have a server already set up with some API endpoints to query. An example starting point is:

```
GET http://algo.work/interview/a
```

Each endpoint returns JSON of the form:

```
{
  "children": [
    "http://algo.work/interview/b",
    "http://algo.work/interview/c"
  ],
  "reward": 1
}
```

Your challenge is to write an algorithm that traverses the entire collection of nodes and returns the sum of their rewards. Each reward should only be counted a single time. The input to the algorithm will be a URL for a node to begin with, such as http://algo.work/interview/a.

The node whose JSON result appears above has a reward of 1, and it has links to two other nodes which are part of the collection.

### Notes: 
- This is a gradle project with core java programming, no framework has been used.
- Java version 15 has been used.
- Used IntelliJ Idea.
- Dependencies: 
    - For serialization and deserialization [Jackson](https://mvnrepository.com/artifact/com.fasterxml.jackson.core/jackson-databind/2.0.1)

# build 
Build location: `<ProjectRootDirectory>/build/libs`

# Run
```
java15 -jar AlgorithmiaTest-1.0-SNAPSHOT.jar 
```
