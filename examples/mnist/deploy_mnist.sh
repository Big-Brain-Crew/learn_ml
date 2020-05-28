python3 ../../learn_ml/coral_inference/convert_to_edgetpu.py -m model -r representative_dataset.npy
cp model_edgetpu.tflite ../../learn_ml/coral_inference/mnist_quant_edgetpu.tflite
cd ../../learn_ml/coral_inference && python3 deploy.py -m mnist_quant_edgetpu.tflite -a 192.168.1.24 -p ""
