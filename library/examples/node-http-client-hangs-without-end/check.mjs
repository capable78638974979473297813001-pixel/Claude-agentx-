import http from "node:http";
import { post as badPost } from "./incorrect.mjs";
import { post as goodPost } from "./correct.mjs";

const server = http.createServer((request, response) => {
  const chunks = [];
  request.on("data", (chunk) => chunks.push(chunk));
  request.on("end", () => response.end("ok"));
});

await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
const { port } = server.address();
try {
  const bad = await badPost(port);
  if (bad !== "timeout") throw new Error(bad);
  console.log("incorrect: observed", bad);
  const good = await goodPost(port);
  if (good !== "ok") throw new Error(good);
  console.log("correct: ok", good);
} finally {
  server.close();
}
