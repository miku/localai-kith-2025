package main

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strings"
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
	// French sentences to translate (10-20 examples)
	sentences := []string{
		"Bonjour, comment allez-vous ?",
		"Je voudrais un café s'il vous plaît.",
		"Où se trouve la gare la plus proche ?",
		"Combien ça coûte ?",
		"Je ne comprends pas.",
		"Quel temps fait-il aujourd'hui ?",
		"Je suis perdu.",
		"Pouvez-vous m'aider ?",
		"Merci beaucoup !",
		"À demain !",
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

		// Send to local LLM (adjust URL to your setup)
		jsonData, _ := json.Marshal(requestBody)
		resp, err := client.Post("http://chiba:11434/v1/chat/completions",
			"application/json", bytes.NewBuffer(jsonData))

		if err != nil {
			fmt.Printf("API error: %v\n", err)
			continue
		}

		// Parse response
		var apiResp ChatResponse
		json.NewDecoder(resp.Body).Decode(&apiResp)
		resp.Body.Close()

		// Extract score and feedback
		content := apiResp.Choices[0].Message.Content
		fmt.Printf("\n%s\n", content)

		// Parse score (simple implementation)
		if strings.Contains(content, "SCORE: ") {
			scoreStr := strings.Split(content, "SCORE: ")[1]
			scoreStr = strings.Split(scoreStr, "\n")[0]
			var score int
			fmt.Sscanf(scoreStr, "%d", &score)
			totalScore += score
		}
	}

	// Final score
	fmt.Printf("\n=== Session Complete ===\nYour average score: %.1f/10\n",
		float64(totalScore)/float64(len(sentences)))
}
