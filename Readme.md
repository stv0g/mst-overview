# MST Overview 

Generates the city overview for https://meine-stadt-transparent.de/

## Building

Install poetry, node and npm. Clone https://github.com/konstin/ris-vendor-stats and next to the project root https://github.com/OParl/resources.

```shell script
poetry install
poetry run ./main.py
npm install
npm run build
```

Open [dist/index.html](dist/index.html)
