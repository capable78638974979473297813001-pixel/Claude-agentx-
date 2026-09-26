import React from "react";

export function Probe({ calls }) {
  React.useEffect(() => {
    calls.count += 1;
  }, [calls]);
  return null;
}
