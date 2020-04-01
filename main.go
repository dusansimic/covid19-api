package main

import (
	"log"
	"encoding/json"
	"io/ioutil"
	"net/http"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

type Country struct {
	Name string `json:"name"`
	Timeline []TimelineDay `json:"timeline"`
	States []State
}

type TimelineDay struct {
	Date string `json:"date"`
	Confirmed int `json:"confirmed"`
	NewConfirmed int `json:"newConfirmed"`
	Deaths int `json:"deaths"`
	NewDeaths int `json:"newDeaths"`
	Recovered int `json:"recovered"`
	NewRecovered int `json:"newRecovered"`
}

type State struct {
	Name string `json:"name"`
	Timeline []TimelineDay `json:"timeline"`
}

func main() {
	byteValue, err := ioutil.ReadFile("timelines.json")
	if err != nil {
		log.Fatalln("Unable to open data file!")
	}

	var countries []Country
	json.Unmarshal(byteValue, &countries)

	countriesMap := make(map[string]Country)
	for _, country := range countries {
		countriesMap[country.Name] = country
	}

	countries = nil

	gin.SetMode(gin.ReleaseMode)
	router := gin.Default()
	router.Use(cors.Default())

	api := router.Group("/api/v1")

	api.GET("/timeline", func (ctx *gin.Context) {
		countryName := ctx.Query("country")
		if countryName == "" {
			ctx.JSON(http.StatusBadRequest, gin.H{"error": "Country is not specified!"})
			return
		}

		country := countriesMap[countryName]
		if country.Name == "" {
			ctx.JSON(http.StatusBadRequest, gin.H{"error": "Country not found!"})
			return
		}

		getStates := ctx.Query("states")
		if getStates == "true" {
			ctx.JSON(http.StatusOK, country.States)
			return
		}

		ctx.JSON(http.StatusOK, country.Timeline)

	})

	router.Run()
}
