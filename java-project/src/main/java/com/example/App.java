package com.example;
import static spark.Spark.*;

public class App {
    public static void main(String[] args) {
        port(8080); // Spark will run on port 8080 inside the container
        get("/", (req, res) -> "Hello, World!");
    }
}