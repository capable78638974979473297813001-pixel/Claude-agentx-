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
