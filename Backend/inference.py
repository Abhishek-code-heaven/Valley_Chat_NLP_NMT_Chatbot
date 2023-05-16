import sys
import os
from flask import Flask, request, jsonify
import json
import tensorflow as tf
from nmt import nmt
from core.tokenizer import tokenize, detokenize
from core.sentence import score_answers, replace_in_answers

# Set up Flask app
app = Flask(__name__)

# Global variables
infer_model = None
flags = None
hparams = None

# Silence TensorFlow logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def initialize_inference(out_dir, hparams):
    global infer_model, flags, hparams

    # Create flags for NMT model
    flags = nmt.default_hparams()
    flags.override_from_dict(hparams)
    flags.out_dir = out_dir

    # Create hparams for NMT model
    hparams = nmt.create_hparams(flags)

    # Create inference model
    infer_model = nmt.inference.NMTModel(hparams, None)

# Load NMT model for inference
initialize_inference(out_dir, hparams)

# Main inference function
@app.route('/', methods=['POST'])
def perform_inference():
    data = json.loads(request.data)
    question = data['message']

    # Perform inference
    answers = do_inference(question)
    answers = detokenize(answers)
    answers = replace_in_answers(answers, 'answers')
    answers_rate = score_answers(answers)

    # Select the answer with the highest score
    max_score = max(answers_rate)
    max_index = answers_rate.index(max_score)
    selected_answer = answers[max_index]

    # Prepare the response
    response = {
        'answers': answers,
        'index': max_index,
        'score': max_score,
        'selected_answer': selected_answer
    }

    return jsonify(response)

def do_inference(phrase):
    global infer_model, flags, hparams

    infer_data = [phrase]

    # Spawn new session
    with tf.Session(graph=infer_model.graph, config=tf.ConfigProto(allow_soft_placement=True)) as sess:
        # Load model
        loaded_infer_model = nmt.model_helper.load_model(infer_model.model, flags.ckpt, sess, "infer")

        # Run model (translate)
        sess.run(
            infer_model.iterator.initializer,
            feed_dict={
                infer_model.src_placeholder: infer_data,
                infer_model.batch_size_placeholder: hparams.infer_batch_size
            })

        # Calculate the number of translations to be returned
        num_translations_per_input = max(min(hparams.num_translations_per_input, hparams.beam_width), 1)
        translations = []

        try:
            nmt_outputs, _ = loaded_infer_model.decode(sess)

            # Iterate through responses
            for beam_id in range(num_translations_per_input):
                output = nmt_outputs[beam_id][0, :].tolist()

                # Format response
                translation = nmt.utils.format_text(output)
                translations.append(translation.decode('utf-8'))

        except tf.errors.OutOfRangeError:
            pass

        return translations

if __name__ == "__main__":
    app.run(debug=True)
