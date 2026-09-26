import http from "node:http";

export function post(port) {
  return new Promise((resolve) => {
    const request = http.request({ hostname: "127.0.0.1", port, method: "POST" }, (response) => {
      response.resume();
      response.on("end", () => resolve("response"));
    });
    request.on("error", () => {});
    request.setTimeout(200, () => {
      request.destroy();
      resolve("timeout");
    });
    request.write("{}");
  });
}
