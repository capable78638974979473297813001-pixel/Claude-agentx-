import React from "react";

export function Field({ label }) {
  return React.createElement("input", { "aria-label": label });
}
