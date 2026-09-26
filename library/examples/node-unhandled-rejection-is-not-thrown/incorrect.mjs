export function fire() {
  try {
    Promise.reject(new Error("nope"));
    return "fell-through";
  } catch {
    return "caught";
  }
}
