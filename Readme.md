# MST Overview

Generates the city overview for https://meine-stadt-transparent.de/

## Building

Install poetry, node and npm.

```shell script
cd ..
git clone https://github.com/konstin/ris-vendor-stats
git clone https://github.com/OParl/resources
git clone https://github.com/meine-stadt-transparent/meine-stadt-transparent
cd -
```

```shell script
poetry install
npm install
```

Run `build.sh`. Open [dist/index.html](dist/index.html)
