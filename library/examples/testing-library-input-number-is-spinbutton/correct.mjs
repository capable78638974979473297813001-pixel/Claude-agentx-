import { getByRole } from "@testing-library/dom";

export function amount(container) {
  return getByRole(container, "spinbutton", { name: "Amount" });
}
