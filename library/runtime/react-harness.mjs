import { JSDOM } from "jsdom";
import { createRoot } from "react-dom/client";
import { act } from "react";

export function installDom() {
  const dom = new JSDOM(
    "<!doctype html><html><body><div id=\"root\"></div></body></html>",
    { pretendToBeVisual: true, url: "http://localhost/" },
  );
  globalThis.window = dom.window;
  globalThis.document = dom.window.document;
  globalThis.HTMLElement = dom.window.HTMLElement;
  globalThis.Node = dom.window.Node;
  globalThis.Element = dom.window.Element;
  globalThis.DocumentFragment = dom.window.DocumentFragment;
  globalThis.IS_REACT_ACT_ENVIRONMENT = true;
  return dom;
}

export async function render(element) {
  const root = createRoot(document.getElementById("root"));
  await act(async () => {
    root.render(element);
  });
  return root;
}
