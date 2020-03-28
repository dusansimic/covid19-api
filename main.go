package main

import (
	"log"
	"encoding/json"
	"io/ioutil"
	"net/http"
	"github.com/gin-gonic/gin"
)

type Country struct {
	Name string `json:"name"`
	Timeline []TimelineDay `json:"timeline"`
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

func main() {
	byteValue, err := ioutil.ReadFile("timelines.json")
	if err != nil {
		log.Fatalln("Unable to open data file!")
	}

	var countries []Country
	json.Unmarshal(byteValue, &countries)

	gin.SetMode(gin.ReleaseMode)
	router := gin.Default()

	api := router.Group("/api/v1")

	api.GET("/timeline", func (ctx *gin.Context) {
		countryName := ctx.Query("country")
		if countryName == "" {
			ctx.JSON(http.StatusBadRequest, gin.H{"error": "Country is not specified!"})
			return
		}

		for _, country := range countries {
			if country.Name == countryName {
				ctx.JSON(http.StatusOK, country.Timeline)
				return
			}
		}

		ctx.JSON(http.StatusBadRequest, gin.H{"error": "Country not found!"})
	})

	router.Run()
}
