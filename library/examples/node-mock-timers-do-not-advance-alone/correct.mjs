import { mock } from "node:test";

export function advance() {
  mock.timers.tick(5000);
}
