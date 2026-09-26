import { getByRole } from "@testing-library/dom";

export function saveButton(container) {
  return getByRole(container, "button", { name: "Save draft" });
}
