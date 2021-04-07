package com.algorithmia;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

import java.util.ArrayList;
import java.util.List;

@JsonIgnoreProperties(ignoreUnknown = true)
@Data
public class Node {
    private List<String> children;
    private Float reward;

    public Node() {
        setReward(0.0f);
        setChildren(new ArrayList<>());
    }

    public Node(@JsonProperty("reward") Float reward, @JsonProperty("children") List children) {
        this.children = children;
        this.reward = reward;
    }
}