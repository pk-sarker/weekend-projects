package com.algorithmia;

import java.util.HashMap;
import java.util.concurrent.*;

/**
 * This class is contains the functionality to traverse
 * a set of urls represented in a tree using DFS.
 */
public class DFSTraversalAlgorithm {
    private float sumOfRewards = 0;
    public HashMap<String, Node> visited = new HashMap<>();
    private String startUrl = "";

    public DFSTraversalAlgorithm(String startUrl){
        this.startUrl = startUrl;
    }

    /**
     * Method to increment reward sum. This is a synchronized method to make
     * the increment thread-safe.
     * @param value Reward value of a url
     */
    public synchronized void incrementSum(float value){
        this.sumOfRewards += value;
    }

    /**
     * Method to get reward sum.
     * @return Returns the sum of all returns.
     */
    public synchronized float getSum(){
        return this.sumOfRewards;
    }

    /**
     * Method to mark a url/node visited. All the visited
     * url are stored in a HashMap with url as key and
     * their response as value.
     *
     * @param url URL is the url provided
     * @param node Response of the URL HTTP call
     */
    public synchronized void markVisited(String url, Node node){
        this.visited.computeIfAbsent(url, k-> node);
    }

    /**
     * Method to check if a url is already called or visited.
     * @param url  URL is the url provided
     * @return
     */
    public synchronized boolean checkIfVisited(String url){
        return this.visited.containsKey(url);
    }

    /**
     * Method to get http response by url.
     *
     * @param url URL is the url provided
     * @return
     */
    public synchronized Node getVisitedNode(String url){
        if (this.visited.containsKey(url)) {
            return this.visited.get(url);
        }
        return null;
    }

    /**
     * Method to start the algorithm.
     * ExecutorService has been used to manage the tasks by fixed set of threads.
     */
    public void startAlgorithm() {
        System.out.println("Status: Running ...");
        var poolSize = 20;
        ExecutorService executorService = Executors.newFixedThreadPool(poolSize);

        httpHelper(this.startUrl, executorService);

        System.out.println("Status: Complete ...");
        System.out.println("Sum of Rewards: " + getSum());
        executorService.shutdown();
    }

    /**
     * This method helps to make the HTTP request
     * @param url
     * @param executorService
     */
    public void httpHelper(String url, ExecutorService executorService) {
        Node node = new Node();
        if (checkIfVisited(url)) {
            node = getVisitedNode(url);
        } else {
            Callable worker = new HttpWorker(url);
            Future<Node> future = executorService.submit(worker);
            try {
                node = future.get();
                markVisited(url, node);
            } catch (InterruptedException e) {
                e.printStackTrace();
            } catch (ExecutionException e) {
                e.printStackTrace();
            }
        }

        incrementSum(node.getReward());

        if (node.getChildren() != null) {
            node.getChildren().forEach((String childUrl) -> {
                httpHelper(childUrl, executorService);
            });
        }
    }
}
