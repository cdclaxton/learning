package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

func handlerA(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("From handler A\n"))
}

func handlerB(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("From handler B\n"))
}

func handlerC(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("From handler C\n"))
}

func handlerD(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("From handler D\n"))
}

func loggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		log.Println(r.RequestURI)
		next.ServeHTTP(w, r)
	})
}

func subRouterSpecificMiddleware1(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		log.Printf("Sub-router middleware 1: %s", r.RequestURI)
		next.ServeHTTP(w, r)
	})
}

func subRouterSpecificMiddleware2(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		log.Printf("Sub-router middleware 2: %s", r.RequestURI)
		next.ServeHTTP(w, r)
	})
}

func main() {
	router := mux.NewRouter()

	// Add router-wide middlware
	router.Use(loggingMiddleware)
	router.HandleFunc("/a", handlerA)

	// Create a sub-router
	subRouter1 := router.PathPrefix("/1").Subrouter()

	// Add sub-router specific middleware
	subRouter1.Use(subRouterSpecificMiddleware1)
	subRouter1.HandleFunc("/b", handlerB)
	subRouter1.HandleFunc("/c", handlerC)

	// Create a 2nd sub-router, but with the same path prefix as the 1st
	subRouter2 := router.PathPrefix("/1").Subrouter()
	subRouter2.Use(subRouterSpecificMiddleware2)
	subRouter2.HandleFunc("/d", handlerD)

	srv := &http.Server{
		Handler: router,
		Addr:    "127.0.0.1:8000",
	}

	fmt.Printf("Running server at %s\n", srv.Addr)
	log.Fatal(srv.ListenAndServe())
}
