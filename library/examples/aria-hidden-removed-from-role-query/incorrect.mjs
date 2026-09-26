import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire(path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../package.json"));
const { getByRole } = require("@testing-library/dom");

export function saveButton(container) {
  return getByRole(container, "button", { name: "Save" });
}
