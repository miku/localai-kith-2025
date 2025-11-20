package main

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"
)

// ANSI color codes
const (
	ColorReset  = "\033[0m"
	ColorGreen  = "\033[32m"
	ColorYellow = "\033[33m"
	ColorRed    = "\033[31m"
)

// OpenAI-compatible API request/response structs
type Message struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

type ChatRequest struct {
	Model    string    `json:"model"`
	Messages []Message `json:"messages"`
}

type ChatResponse struct {
	Choices []struct {
		Message struct {
			Content string `json:"content"`
		} `json:"message"`
	} `json:"choices"`
}

func main() {
	// Get Ollama host from environment variable
	ollamaHost := os.Getenv("OLLAMA_HOST")
	if ollamaHost == "" {
		ollamaHost = "http://localhost:11434" // Default if not set
	}
	apiURL := ollamaHost + "/v1/chat/completions"

	fmt.Printf("Using Ollama API at: %s\n", apiURL)

	// French sentences to translate (10-20 examples)
	// sentences := []string{
	// 	"Bonjour, comment allez-vous ?",
	// 	"Je voudrais un café s'il vous plaît.",
	// 	"Où se trouve la gare la plus proche ?",
	// 	"Combien ça coûte ?",
	// 	"Je ne comprends pas.",
	// 	"Quel temps fait-il aujourd'hui ?",
	// 	"Je suis perdu.",
	// 	"Pouvez-vous m'aider ?",
	// 	"Merci beaucoup !",
	// 	"À demain !",
	// }
	sentences := []string{
		"Je cherchai à grouper ces lettres de manière à former des mots.",
		"Viennent-ils du ciel ou de l'océan?",
	}

	totalScore := 0
	client := &http.Client{}

	for i, sentence := range sentences {
		fmt.Printf("\n[%d/%d] Translate to English:\n%s\n\n> ", i+1, len(sentences), sentence)

		// Read user translation
		reader := bufio.NewReader(os.Stdin)
		translation, _ := reader.ReadString('\n')
		translation = strings.TrimSpace(translation)

		// Prepare API request
		requestBody := ChatRequest{
			Model: "gpt-oss:120b", // Your local model name
			Messages: []Message{
				{
					Role: "system",
					Content: "You are a French language coach. Critique the translation from French to English. " +
						"Provide: 1) A score from 1-10, 2) Explanation of errors, 3) Correct translation. " +
						"Format response as: SCORE: [1-10]\nFEEDBACK: [text]",
				},
				{
					Role:    "user",
					Content: fmt.Sprintf("Original: %s\nTranslation: %s", sentence, translation),
				},
			},
		}

		// Send to local LLM using OLLAMA_HOST
		jsonData, _ := json.Marshal(requestBody)
		resp, err := client.Post(apiURL, "application/json", bytes.NewBuffer(jsonData))

		if err != nil {
			fmt.Printf("%sAPI error: %v%s\n", ColorRed, err, ColorReset)
			continue
		}
		if resp.StatusCode != http.StatusOK {
			log.Fatalf("http: %v", resp.StatusCode)
		}

		// Parse response
		var apiResp ChatResponse
		json.NewDecoder(resp.Body).Decode(&apiResp)
		resp.Body.Close()

		// Extract score and feedback
		content := apiResp.Choices[0].Message.Content

		// Parse score
		// Parse score
		var score int
		scoreFound := false

		// Make parsing case-insensitive and more flexible
		// Make parsing case-insensitive and strip markdown
		contentUpper := strings.ToUpper(content)
		if idx := strings.Index(contentUpper, "SCORE"); idx != -1 {
			scoreStr := content[idx+5:] // "SCORE" is 5 characters
			// Strip common punctuation and markdown
			scoreStr = strings.TrimLeft(scoreStr, ":*_ \t")
			if endIdx := strings.IndexAny(scoreStr, "\n/"); endIdx != -1 {
				scoreStr = scoreStr[:endIdx]
			}
			scoreStr = strings.TrimSpace(scoreStr)
			if _, err := fmt.Sscanf(scoreStr, "%d", &score); err == nil {
				totalScore += score
				scoreFound = true
			}
		}

		// Determine color based on score
		var colorPrefix string
		if scoreFound {
			switch {
			case score >= 8:
				colorPrefix = ColorGreen
			case score >= 5:
				colorPrefix = ColorYellow
			default:
				colorPrefix = ColorRed
			}
		} else {
			colorPrefix = "\033[37m" // White if score not found
		}

		// Print colored feedback
		fmt.Printf("\n%s%s%s\n", colorPrefix, content, ColorReset)
	}

	// Final score
	avgScore := float64(totalScore) / float64(len(sentences))
	var finalColor string
	switch {
	case avgScore >= 8:
		finalColor = ColorGreen
	case avgScore >= 5:
		finalColor = ColorYellow
	default:
		finalColor = ColorRed
	}

	fmt.Printf("\n%s=== Session Complete ===%s\nYour average score: %s%.1f/10%s\n",
		finalColor, ColorReset, finalColor, avgScore, ColorReset)
}
