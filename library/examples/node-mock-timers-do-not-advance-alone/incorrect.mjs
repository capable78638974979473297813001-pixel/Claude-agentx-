export function schedule(flag) {
  setTimeout(() => {
    flag.fired = true;
  }, 5000);
}
