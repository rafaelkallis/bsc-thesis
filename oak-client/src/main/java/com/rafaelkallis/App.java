package com.rafaelkallis;

import com.mongodb.MongoClient;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import javax.jcr.query.Query;
import org.apache.jackrabbit.oak.api.Result;
import org.apache.jackrabbit.oak.api.ResultRow;
import org.apache.jackrabbit.oak.query.xpath.XPathToSQL2Converter;

public class App {
    public static void main(String[] args) {
        // final MongoClient m = new MongoClient();
        // m.dropDatabase("oak");
        // m.close();

        ClusterNode.initializePropertyIndex("pub");
        // performAvoidableConflict();
        // performQuery();
    }

    private static void performAvoidableConflict() {
        // assume
        invariant(ClusterNode.simpleWrite(root -> {
            root.getTree("/").addChild("home");
            root.getTree("/home").addChild("news");
            root.getTree("/home").addChild("loans");
            root.getTree("/home/news").addChild("breaking");
            root.getTree("/home/loans").addChild("rates");
            root.getTree("/home/news/breaking").setProperty("pub", "now");
        }, 1).commit(), "t3 failed");

        // act
        Commitable t4 = ClusterNode.simpleWrite(root -> root.getTree("/home/news/breaking").removeProperty("pub"), 1);
        Commitable t5 = ClusterNode.simpleWrite(root -> root.getTree("/home/loans/rates").setProperty("pub", "now"), 2);
        System.err.println("BEFORE !!!!!!!!!!!!!!!!!!!!!!!!!!!!");
        invariant(t4.commit() && t5.commit(), "t4 or t5 failed");
        System.err.println("AFTER !!!!!!!!!!!!!!!!!!!!!!!!!!!!");

        // assert
        invariant(ClusterNode.simpleWrite(root -> {
            invariant(root.getTree("/home/news/breaking").getProperty("pub") == null,
                    "/home/news/breaking still has property \"pub: now\"");
            invariant(root.getTree("/home/loans/rates").getProperty("pub") != null,
                    "/home/loans/rates doesn't have property \"pub: now\"");
        }, 1).commit(), "check failed");

        // cleanup
        invariant(ClusterNode.simpleWrite(root -> {
            root.getTree("/home/news/breaking").remove();
            root.getTree("/home/news").remove();
            root.getTree("/home/loans/rates").remove();
            root.getTree("/home/loans").remove();
            root.getTree("/home").remove();
        }, 1).commit(), "cleanup failed");
    }

    private static void performQuery() {
        // assume
        invariant(ClusterNode.simpleWrite(root -> {
            root.getTree("/").addChild("home");
            root.getTree("/home").addChild("news");
            root.getTree("/home/news").addChild("breaking");
            root.getTree("/home/news/breaking").setProperty("pub", "now");
        }, 1).commit(), "assume failed");

        // act
        invariant(ClusterNode.simpleWrite(root -> {
            try {
                final Result result = root.getQueryEngine().executeQuery(
                        new XPathToSQL2Converter().convert("//*[@pub='now']"), Query.JCR_SQL2, Collections.emptyMap(),
                        Collections.emptyMap());

                List<ResultRow> resultRows = new ArrayList<>();
                result.getRows().forEach(resultRows::add);

                // assert
                invariant(resultRows.size() == 1,
                        String.format("Invalid number of result rows. Expected 1, got %d", resultRows.size()));
                invariant("/home/news/breaking".equals(resultRows.get(0).getPath()), String.format(
                        "Invalid path returned. Expected /home/news/breaking, got %s", resultRows.get(0).getPath()));
            } catch (ParseException e) {
                invariant(false, e.getMessage());
            }

        }, 1).commit(), "act failed");

        invariant(ClusterNode.simpleWrite(root -> {
            root.getTree("/home/news/breaking").remove();
            root.getTree("/home/news").remove();
            ;
            root.getTree("/home").remove();
        }, 1).commit(), "cleanup failed");
    }

    private static void invariant(boolean predicate, String message) {
        if (!predicate) {
            System.err.println("\n=================================================");
            System.err.println(message);
            System.err.println("=================================================\n");
            throw new AssertionError(message);
        }
    }
}
