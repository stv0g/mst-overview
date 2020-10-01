set -e

if [ ! -d ".venv" ]; then
  poetry install
fi

if [ ! -d "node_modules" ]; then
  npm ci
fi

if [ ! -d "ris-vendor-stats" ]; then
  git clone https://github.com/konstin/ris-vendor-stats
fi

if [ ! -d "resources" ]; then
  git clone https://github.com/OParl/resources
fi

rm -rf dist
poetry run ./main.py
npm run build
cd ../meine-stadt-transparent
cp Readme.md docs/index.md
../mst-overview/.venv/bin/mkdocs build --clean
cp -r etc site/etc
cd ../mst-overview
cp -r ../meine-stadt-transparent/site dist/docs
