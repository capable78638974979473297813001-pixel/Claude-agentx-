import React from "react";

export function Field({ label, ref }) {
  return React.createElement("input", { "aria-label": label, ref });
}
