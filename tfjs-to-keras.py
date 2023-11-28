import tensorflowjs as tfjs
import tensorflow as tf

def convert_tfjs_to_keras(tfjs_model_path, keras_model_output_path):
    # Load the TensorFlow.js model
    model = tfjs.converters.load_keras_model(tfjs_model_path)
    
    # Save the model in Keras format
    model.save(keras_model_output_path)
    print(f"Model converted and saved to {keras_model_output_path}")

# Example usage
tfjs_model_path = 'path/to/tensorflowjs/model.json'  # Path to the .json file
keras_model_output_path = 'path/to/save/keras/model' # Path to save the Keras model

convert_tfjs_to_keras(tfjs_model_path, keras_model_output_path)
