const bedrock = require('bedrock-protocol');

const botUsername = process.env.BOT_NAME || 'CraftBot_Pro';

console.log(`[Bot Startup] Connecting to server as: ${botUsername}...`);

const client = bedrock.createClient({
    host: process.env.MC_HOST,
    port: parseInt(process.env.MC_PORT) || 19132,
    username: botUsername,
    offline: true,
    skipPing: true
});

const jokes = [
    "Creeper ghumay ki diye? Blast blanket diye! 😂",
    "Minecraft-er skeleton gulo eto roddur e keno jay na? Bone loss hoye jabe bole! 💀",
    "Enderman kothao jete hole ki use kore? Teleport app! 📱",
    "Villager ra kiser dokan deye? 'Hrrrm' mart! 🛒"
];

let runtimeEntityId = null;

// Server theke game start packet paile console-e print hobe
client.on('start_game', (packet) => {
    runtimeEntityId = packet.runtime_entity_id;
    console.log(`[SUCCESS] Bot '${botUsername}' successfully server-er sathe যুক্ত (connected) hoyeche!`);
});

client.on('spawn', () => {
    console.log(`[SPAWN] Bot world-e spawn koreche. Chat-e message pathano hocche...`);
    sendChat("Hello guys! Ami server-e chole eshechi! 🤖");

    // Prottek 2 minute por por joke bolbe
    setInterval(() => {
        const randomJoke = jokes[Math.floor(Math.random() * jokes.length)];
        console.log(`[ACTION] Joke bola hocche: "${randomJoke}"`);
        sendChat(randomJoke);
    }, 120000);
});

// Kew chat korle console-e dekhabe ebong reply dibe
client.on('text', (packet) => {
    if (packet.type === 'chat' && packet.source_name !== botUsername) {
        const msg = packet.message.toLowerCase();
        const sender = packet.source_name;

        console.log(`[CHAT LOG] ${sender}: ${packet.message}`);

        if (msg.includes('hi bot') || msg.includes('hello bot')) {
            sendChat(`Kemon acho ${sender}? Ami ekjon AI bot!`);
        } else if (msg.includes('joke')) {
            const randomJoke = jokes[Math.floor(Math.random() * jokes.length)];
            sendChat(randomJoke);
        }
    }
});

// More gele console-e log dekhabe ebong respawn korbe
client.on('death_info', () => {
    console.log(`[DEATH] Bot more geche! Respawn korar chesta cholche...`);
    setTimeout(() => {
        client.queue('respawn', {
            position: { x: 0, y: 0, z: 0 },
            state: 2,
            runtime_entity_id: runtimeEntityId
        });
        sendChat("Ami abar respawn hoye gechi! 💀");
        console.log(`[RESPAWN] Bot successfully respawn koreche.`);
    }, 1500);
});

function sendChat(message) {
    client.queue('nethernet_packet', {});
    client.queue('text', {
        type: 'chat',
        needs_translation: false,
        source_name: botUsername,
        xuid: '',
        platform_chat_id: '',
        message: message
    });
}

client.on('disconnect', (packet) => {
    console.log(`[DISCONNECTED] Bot server theke disconnected hoyeche. Reason:`, packet);
});

client.on('error', (err) => {
    console.error(`[ERROR] Bot error kheyeche:`, err);
});
