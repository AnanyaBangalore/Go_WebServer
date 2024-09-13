package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import javax.annotation.PostConstruct;
import java.io.BufferedReader;
import java.io.InputStreamReader;

@SpringBootApplication
public class DemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }

    @PostConstruct
    public void deployHelmChart() {
        try {
            // Deploy the Helm chart
            executeCommand("helm install my-pods src/main/resources/helm/my-pods-chart");

            System.out.println("Helm chart deployed: NGINX, BusyBox, and Alpine pods are running in Minikube.");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void executeCommand(String command) throws Exception {
        Process process = Runtime.getRuntime().exec(command);
        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        String line;
        while ((line = reader.readLine()) != null) {
            System.out.println(line);
        }
        process.waitFor();
    }
}
