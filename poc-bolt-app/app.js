import pkg from "@slack/bolt";
import sample from "./sample.json" with {type: "json"};
const { App } = pkg;

// Initializes your app with your bot token and signing secret
const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  signingSecret: process.env.SLACK_SIGNING_SECRET,
  socketMode: true,
  appToken: process.env.SLACK_APP_TOKEN,
});

const testChannelId = "C07LL5AG9V5";

async function publishMessage(id, data) {
  try {
    // Call the chat.postMessage method using the built-in WebClient
    const result = await app.client.chat.postMessage({
      // The token you used to initialize your app
      token: app.token,
      channel: id,
      blocks: [
        {
            "type": "rich_text",
            "elements": [
              {
                "type": "rich_text_preformatted",
                "elements": [
                  {
                    "type": "text",
                    "text": JSON.stringify(data, null, 2),
                  },
                ],
                "border": 0
              }
            ]
          }
        ]
      // You could also use a blocks[] array to send richer content
    });
      console.log(result.ts);
      putEmoji(result.ts);
      respondInThread(testChannelId, result.ts, "This is a thread");
  } catch (error) {
    console.error("ERROR", error);
  }
}

async function putEmoji(timestamp) {
    try {
        console.log("putEmoji, timestamp: ", timestamp);
        // Call the chat.postMessage method using the built-in WebClient
        const result = await app.client.reactions.add({
        // The token you used to initialize your app
        token: app.token,
        channel: testChannelId,
        name: "thumbsup",
        timestamp,
        
        });
        console.log(result);
    } catch (error) {
        console.error("ERROR", error);
    }
    
}

async function respondInThread(channel, thread_ts, text) {
  try {
    const result = await app.client.chat.postMessage({
      // The token you used to initialize your app
      token: app.token,
      channel,
      thread_ts,
      text,
    });
    console.log(result);
  } catch (error) {
    console.error("ERROR", error);
  }
}

(async () => {
  // Start your app
  await app.start(process.env.PORT || 3000);
  console.log("⚡️ Bolt app is running!");

  await publishMessage(testChannelId, data);
})();
