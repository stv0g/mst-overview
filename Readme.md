# MST Overview 

Generates the city overview for https://meine-stadt-transparent.de/

## Building

Install poetry, node and npm. Clone https://github.com/konstin/ris-vendor-stats, https://github.com/OParl/resources and https://github.com/meine-stadt-transparent/meine-stadt-transparent next to the project root

```shell script
poetry install
poetry run ./main.py
npm install
npm run build
cd ../meine-stadt-transparent
cp Readme.md docs/index.md
mkdocs build --clean
cp -r envs site/envs
cd ../mst-overview
cp -r ../meine-stadt-transparent/site dist/site
```

Open [dist/index.html](dist/index.html)
