# Homemade COVID-19 REST API

This is a simple REST API that I wrote during quarantine. It gets latest data form [Johns Hopkins GitHub repo](https://github.com/CSSEGISandData/COVID-19) and parses it into JSON. The API loads the JSON data and servers it.

You can test it out [here](http://covid19.dusansimic.me/api/v1/timeline?country=Serbia) but I encourage You to set one up for yourself.

## Build

You first need to get the data and parse it.

```bash
$ sh get_data.sh

$ python3 parse.py
```

After that You'll need to compile the API. Just first get the required dependencies.
```sh
$ go get github.com/gin-contrib/cors

$ go get github.com/gin-gonic/gin
```

Then just run the build command.
```sh
$ go build
```

If everything works out fine, You should now have a binary named after the parent directory. It's probably going to be `covid19-api`.

Just run that binary and You're good to go.

If You want to specify a port on which the API will be running, set the PORT environment variable before running the binary. Otherwise it'll be server on port `8080`.

## Usage

To get the timeline of COVID-19 patients, just set the query parameter `country` to the name of the country.
```
http://localhost:8080/api/v1/timeline?country=Serbia
```

To get the timeline data in all states of a specific country, add `states` parameter and set it to lowercase `true`.
```
http://localhost:8080/api/v1/timeline?country=Canada&states=true
```

## Related

[COVID-19 Graphs web app (uses this API)](https://github.com/dusansimic/covid19-graphs)

## License
[MIT](./LICENSE)
