package com.wistron.witlab.consumer;

import org.apache.kafka.clients.consumer.*;
import org.apache.kafka.common.TopicPartition;
import org.apache.kafka.common.record.TimestampType;

import java.time.Duration;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;

public class Consumer_08_CommitSpecified {
    public static void main(String[] args) {
        // 步驟1. 設定要連線到Kafka集群的相關設定
        Properties props = new Properties();

        props.put("bootstrap.servers", "localhost:9092"); // Kafka集群在那裡?
        props.put("group.id", "CG1"); // <-- 這就是ConsumerGroup
        props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer"); // 指定msgKey的反序列化器
        props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer"); // 指定msgValue的反序列化器

        props.put("auto.offset.reset", "earliest"); // 是否從這個ConsumerGroup尚未讀取的partition/offset開始讀

        props.put("enable.auto.commit", "false");

        // 步驟2. 產生一個Kafka的Consumer的實例
        Consumer<String, String> consumer = new KafkaConsumer<>(props);

        // 步驟3. 指定想要訂閱訊息的topic名稱
        String topicName = "ak03.test";

        // 步驟4. 讓Consumer向Kafka集群訂閱指定的topic
        consumer.subscribe(Arrays.asList(topicName));

        // 步驟5. 產生一個紀錄TopicPartition與Offset的容器
        Map<TopicPartition, OffsetAndMetadata> currentOffsets = new HashMap<>();
        // 步驟6. 持續的拉取Kafka有進來的訊息
        int recordCount = 0;
        try {
            System.out.println("Start listen incoming messages ...");
            // 請求Kafka把新的訊息吐出來
            ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(1000));

            // 紀錄現在的TopicPartition與Offset
            currentOffsets.put(new TopicPartition(topicName, 0), new OffsetAndMetadata(2, "no metadata"));

        } catch(Exception e) {
            // log.error("Unexpected error", e);
            e.printStackTrace();
        } finally {
            // 步驟6. 如果收到結束程式的訊號時關掉Consumer實例的連線
            consumer.close();
            System.out.println("Stop listen incoming messages");
        }
    }

    // 一個簡單的複製HashMap的函式
    private static Map<TopicPartition, OffsetAndMetadata> copyHashmap(Map<TopicPartition, OffsetAndMetadata> origin) {
        Map<TopicPartition, OffsetAndMetadata> copy = new HashMap<>();
        for(Map.Entry<TopicPartition, OffsetAndMetadata> entry : origin.entrySet()) {
            copy.put(entry.getKey(), entry.getValue());
        }
        return copy;
    }
}
