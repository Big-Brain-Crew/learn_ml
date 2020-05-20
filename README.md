# learn_ml
A tool for easily training and deploying machine learning models to edge hardware.

Run these commands from the root directory to test the current state:


```
python3 tests/test_pipeline_config_generator.py
python3 tests/test_pipeline_generator.py 
python3 train.py
```

The first script will create `generators/preprocessor/pipeline.json` and the second script will use this JSON to create `generators/preprocessor/pipeline.py`. A MNIST model can then be trained using this generated dataset pipeline.