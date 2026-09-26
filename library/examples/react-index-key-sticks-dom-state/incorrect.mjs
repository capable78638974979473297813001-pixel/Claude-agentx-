import React from "react";

export function List({ items }) {
  return React.createElement(
    "div",
    null,
    items.map((item, index) =>
      React.createElement("input", { key: index, defaultValue: item }),
    ),
  );
}
