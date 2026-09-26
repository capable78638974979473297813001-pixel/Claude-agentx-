---
id: go-http-shutdown-blocks-on-handler
area: backend
topic: go
task: unblock-http-shutdown
title: http.Server.Shutdown waits until the handler returns
description: Use when Shutdown returns context deadline exceeded while a handler is still inside Sleep or a request that never finishes.
triggers:
  - Server.Shutdown blocked
  - http shutdown timeout handler
  - close stop channel before Shutdown
  - handler still running after shutdown
aliases:
  - go
  - net/http
  - shutdown
related:
  - node-http-client-hangs-without-end
  - go-nil-pointer-stored-in-interface
sources:
  - https://pkg.go.dev/net/http#Server.Shutdown
commands:
  - python3 library/examples/go-http-shutdown-blocks-on-handler/check.py
---

# http.Server.Shutdown waits until the handler returns

`Server.Shutdown` stops accepting new connections and then waits for existing handlers to return. The docs say the method returns once handlers are done, or when the context expires. A handler that `time.Sleep`s for a second, with an in-flight `GET` and a shutdown timeout of 150ms, prints `blocked` on Go 1.22.2.

Selecting on `r.Context().Done()` in that same handler also printed `blocked` in this measurement. Do not treat that single run as proof that Shutdown never cancels the request context. What did return in time was an explicit `stop` channel closed before `Shutdown`: the handler's `select` takes that case and returns, and the process prints `returned`.

Close or cancel the thing the handler is waiting on, then call `Shutdown`. A timeout context passed to `Shutdown` only bounds the wait; it does not by itself abort a handler that ignores it.

## Incorrect

```go file=library/examples/go-http-shutdown-blocks-on-handler/incorrect.go
package main

import (
	"context"
	"fmt"
	"net"
	"net/http"
	"time"
)

func main() {
	ln, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		panic(err)
	}
	server := &http.Server{
		Handler: http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			time.Sleep(time.Second)
			w.WriteHeader(http.StatusNoContent)
		}),
	}
	go server.Serve(ln)
	go http.Get("http://" + ln.Addr().String())
	time.Sleep(30 * time.Millisecond)
	ctx, cancel := context.WithTimeout(context.Background(), 150*time.Millisecond)
	defer cancel()
	err = server.Shutdown(ctx)
	if err == nil {
		fmt.Println("returned")
		return
	}
	fmt.Println("blocked")
}
```

## Correct

```go file=library/examples/go-http-shutdown-blocks-on-handler/correct.go
package main

import (
	"context"
	"fmt"
	"net"
	"net/http"
	"time"
)

func main() {
	ln, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		panic(err)
	}
	stop := make(chan struct{})
	server := &http.Server{
		Handler: http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			select {
			case <-stop:
				return
			case <-time.After(time.Second):
				w.WriteHeader(http.StatusNoContent)
			}
		}),
	}
	go server.Serve(ln)
	go http.Get("http://" + ln.Addr().String())
	time.Sleep(30 * time.Millisecond)
	close(stop)
	ctx, cancel := context.WithTimeout(context.Background(), 150*time.Millisecond)
	defer cancel()
	err = server.Shutdown(ctx)
	if err != nil {
		fmt.Println("blocked")
		return
	}
	fmt.Println("returned")
}
```

## Verify

Run `python3 library/examples/go-http-shutdown-blocks-on-handler/check.py`.

## Sources

- https://pkg.go.dev/net/http#Server.Shutdown
