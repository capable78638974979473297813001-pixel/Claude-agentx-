import React from "react";

export function Counter() {
  const [count, setCount] = React.useState(0);
  React.useEffect(() => {
    const id = setInterval(() => setCount((value) => value + 1), 1000);
    return () => clearInterval(id);
  }, []);
  return React.createElement("span", { id: "n" }, String(count));
}
