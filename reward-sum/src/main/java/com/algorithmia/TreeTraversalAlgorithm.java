package com.algorithmia;

public class TreeTraversalAlgorithm {

    public static void main(String[] args) {
        long startTime = System.nanoTime();
        System.out.println("=============== Tree Traversal Algorithm 1 ================");
        DFSTraversalAlgorithm obj = new DFSTraversalAlgorithm("http://algo.work/interview/a");
        obj.startAlgorithm();

        long endTime = System.nanoTime();
        long timeElapsed = endTime - startTime;
        System.out.println("Execution time in milliseconds : " +
                timeElapsed / 1000000);
    }

}
