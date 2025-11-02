import amqp from "amqplib"
import { RABBITMQ_URL } from "./config/env.ts";
import { sendMail } from "./utils.ts";

async function start() {
  try {
    console.log("[*] Connecting to RabbitMQ...");
    const connection = await amqp.connect(RABBITMQ_URL || "");
    const channel = await connection.createChannel();
    const queue = "audio";

    await channel.assertQueue(queue, { durable: false });
    console.log(`[*] Waiting for messages in ${queue}. To exit press CTRL+C`);

    channel.consume(queue, async (msg) => {
      if (msg !== null) {
        const messageStr = msg.content.toString();
        console.log(`[x] Received raw: ${messageStr}`);
        
        try {
            const { username, mp3_fid } = JSON.parse(messageStr);
            console.log(`[x] Parsed email: ${username}`);

            await sendMail(username, mp3_fid)
            console.log("[✔] Email sent successfully!");
        } catch (err) {
          console.error("[✖] Error in sendMail():", err);
        }
      }
    }, { noAck: true });
  } catch (error) {
    console.error("[!] RabbitMQ connection error:", error);
    setTimeout(start, 5000); // auto-reconnect after 5s
  }
}

start();