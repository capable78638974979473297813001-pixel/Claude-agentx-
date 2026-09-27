import { reactive } from "vue";

export function snapshot(props) {
  const count = props.count;
  return () => count;
}
