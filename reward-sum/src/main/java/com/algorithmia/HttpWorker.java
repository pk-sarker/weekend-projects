package com.algorithmia;

import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.util.concurrent.Callable;
import java.util.concurrent.CompletableFuture;

import static java.net.URI.*;

public class HttpWorker implements Callable<Node> {
    private String url;

    HttpWorker(String url) {
        this.url = url;
    }
    public Node call() throws  Exception {
        var client = HttpClient.newHttpClient();
        // create a request
        var request = HttpRequest.newBuilder()
                .uri(create(this.url))
                .header("accept", "application/json")
                .build();

        CompletableFuture<Node> future  = client.sendAsync(request, new JsonBodyHandler<>(Node.class))
                .thenApply((resp) -> {
                    Node node = resp.body().get();
                    return node;
                });
        return future.get();
    }
}
