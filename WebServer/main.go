package main

import (
	"fmt"
	"log"
	"net/http"
	"sync"
)

var (
	database []struct {
		Name  string `json:"name"`
		Email string `json:"email"`
	}
	mu sync.Mutex
)

func welcomeHandler(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path != "/welcome" {
		http.Error(w, "404 not found", http.StatusNotFound)
		return
	}

	if r.Method != http.MethodGet {
		http.Error(w, "Method is not supported", http.StatusMethodNotAllowed)
		return
	}

	http.ServeFile(w, r, "./static/index.html")
}

func formHandler(w http.ResponseWriter, r *http.Request) {
	log.Println("Method:", r.Method, "Path:", r.URL.Path) // Log method and path

	if r.URL.Path != "/form" {
		http.Error(w, "404 not found", http.StatusNotFound)
		return
	}

	if r.Method == http.MethodPost {
		// Log the form values received
		name := r.FormValue("name")
		email := r.FormValue("email")
		log.Println("Received form data - Name:", name, "Email:", email)

		// Lock the mutex to safely update the slice
		mu.Lock()
		database = append(database, struct {
			Name  string `json:"name"`
			Email string `json:"email"`
		}{Name: name, Email: email})
		mu.Unlock()

		// Send a response with current entries in the database
		w.Header().Set("Content-Type", "text/plain") // Set content type to plain text
		fmt.Fprintf(w, "Current entries in the database:\n")
		for _, entry := range database {
			fmt.Fprintf(w, "Name: %s, Email: %s\n", entry.Name, entry.Email)
		}
		return
	}

	// Serve the form HTML for GET requests
	http.ServeFile(w, r, "./static/form.html")
}

func main() {
	// Serve static files from the "./static" directory
	fileServer := http.FileServer(http.Dir("./static"))
	http.Handle("/static/", http.StripPrefix("/static/", fileServer))

	http.HandleFunc("/form", formHandler)
	http.HandleFunc("/welcome", welcomeHandler)

	fmt.Println("Starting the server at port 8082.")
	err := http.ListenAndServe(":8082", nil)
	if err != nil {
		log.Fatal(err)
	}
}
