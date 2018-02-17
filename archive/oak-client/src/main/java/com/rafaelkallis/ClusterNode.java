package com.rafaelkallis;

import com.mongodb.MongoClient;
import org.apache.jackrabbit.oak.InitialContent;
import org.apache.jackrabbit.oak.Oak;
import org.apache.jackrabbit.oak.api.*;
import org.apache.jackrabbit.oak.plugins.document.DocumentMK;
import org.apache.jackrabbit.oak.plugins.document.DocumentNodeStore;
import org.apache.jackrabbit.oak.plugins.index.property.PropertyIndexEditorProvider;
import org.apache.jackrabbit.oak.spi.security.OpenSecurityProvider;

import javax.jcr.NoSuchWorkspaceException;
import javax.security.auth.login.LoginException;
import java.util.Collections;
import java.util.function.Consumer;

public class ClusterNode {

    private int clusterId;
    private boolean ready;

    private MongoClient mongoClient;
    private DocumentNodeStore nodeStore;
    private ContentRepository contentRepository;

    private ClusterNode(int clusterId) {
        this.clusterId = clusterId;
        this.ready = false;
    }

    public synchronized static ClusterNode create(int clusterId) {
        return new ClusterNode(clusterId);
    }

    public ClusterNode setUp() {
        if (!this.ready) {
            this.mongoClient = new MongoClient();
            this.nodeStore = new DocumentMK.Builder()
                    .setMongoDB(this.mongoClient.getDB("oak"))
                    .setClusterId(this.clusterId)
                    .setVolatilityThreshold(4)
                    .setSlidingWindowLength(24 * 60 * 60 * 1000)
                    .getNodeStore();

            final Oak oak = new Oak(nodeStore)
                    .with(new InitialContent())
                    .with(new OpenSecurityProvider())
                    .with(new PropertyIndexEditorProvider());

            this.contentRepository = oak.createContentRepository();
            this.ready = true;
        }
        return this;
    }

    public ClusterNode tearDown() {
        if (this.ready) {
            this.nodeStore.dispose();
            this.nodeStore = null;
            this.mongoClient.close();
            this.mongoClient = null;
            this.contentRepository = null;
            this.ready = false;
        }
        return this;
    }

    public ContentSession requestSession() {
        if (!this.ready) {
            throw new RuntimeException(String.format("ClusterNode %d is not ready", this.clusterId));
        }
        try {
            return this.contentRepository.login(null, "default");
        } catch (LoginException | NoSuchWorkspaceException ignored) {
            throw new RuntimeException(String.format("ClusterNode %d failed to start session", this.clusterId));
        }
    }

    public static Commitable simpleWrite(Consumer<Root> f, int clusterId) {
        return ClusterNode.simpleWrite(f, ClusterNode.create(clusterId));
    }

    public static Commitable simpleWrite(Consumer<Root> f, ClusterNode clusterNode) {
        clusterNode.setUp();
        try {
            final ContentSession contentSession = clusterNode.requestSession();
            final Root root = contentSession.getLatestRoot();
            f.accept(root);
            return () -> {
                try {
                    root.commit();
                    return true;
                } catch (CommitFailedException ignored) {
                } finally {
                    clusterNode.tearDown();
                }
                return false;
            };
        } catch (Exception e) {
            clusterNode.tearDown();
            return () -> false;
        }
    }

    public static void initializePropertyIndex(final String propName) {
        ClusterNode.simpleWrite(root -> {
            Tree index = root.getTree("/oak:index");
            if (!index.hasChild(propName)) {
                Tree prop = index.addChild(propName);
                prop.setProperty("type", "property");
                prop.setProperty("jcr:primaryType", "oak:QueryIndexDefinition", Type.NAME);
                prop.setProperty("propertyNames", propName, Type.NAME);
                prop.setProperty("unique", false);
                prop.setProperty("reindex", true);
            }
        }, 100).commit();
    }
}
