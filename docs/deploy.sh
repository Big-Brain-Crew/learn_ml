#!/bin/bash

# ORG and REPO name
ORG=Big-Brain-Crew
REPO=learn_ml

# cd out of the repo
cd ..


# Clone the repo to the gh-pages branch
git clone -b gh-pages "https://$GH_TOKEN@github.com/$ORG/$REPO.git" gh-pages

cd gh-pages
ls

# Update git config.
git config user.name "Travis Builder"
git config user.email "$GH_EMAIL"

# Copy the HTML files to the gh-pages branch
cp -R ../$REPO/docs/_build/html/* ./

git add -A
git commit "Autodoc commit for $COMMIT."
git push -q origin gh-pages