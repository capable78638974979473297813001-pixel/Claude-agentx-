import React from "react";

export function List({ items }) {
  return React.createElement(
    "div",
    null,
    items.map((item) =>
      React.createElement("input", { key: item, defaultValue: item }),
    ),
  );
}
