export async function fire() {
  try {
    await Promise.reject(new Error("nope"));
    return "fell-through";
  } catch (error) {
    return error.message;
  }
}
