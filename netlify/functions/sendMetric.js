const net = require("net");

const HG_HOST = "carbon.hostedgraphite.com";
const HG_PORT = 2003;
const HG_API_KEY = "8770573a-2e24-4ad5-9d1f-f69afca83321";

exports.handler = async (event) => {
  try {
    if (event.httpMethod !== "POST") {
      return { statusCode: 405, body: "Method Not Allowed" };
    }

    const body = JSON.parse(event.body || "{}");
    const metricName = body.metricName;
    const value = Number.isFinite(body.value) ? body.value : 1;

    if (!metricName) {
      return { statusCode: 400, body: "Missing metricName" };
    }

    const ts = Math.floor(Date.now() / 1000);
    const line = `${HG_API_KEY}.itcos.${metricName} ${value} ${ts}\n`;

    await new Promise((resolve, reject) => {
      const socket = net.createConnection(HG_PORT, HG_HOST, () => {
        socket.write(line);
        socket.end();
      });
      socket.on("error", reject);
      socket.on("close", resolve);
    });

    return {
      statusCode: 200,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ok: true }),
    };
  } catch (e) {
    return { statusCode: 500, body: "Error sending metric" };
  }
};