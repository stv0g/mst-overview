set -e

rm -rf dist
poetry run ./main.py
npm run build
cd ../meine-stadt-transparent
cp Readme.md docs/index.md
../mst-overview/.venv/bin/mkdocs build --clean
cp -r etc site/etc
cd ../mst-overview
cp -r ../meine-stadt-transparent/site dist/docs