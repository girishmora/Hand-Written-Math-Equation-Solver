from flask import Flask, render_template, request
import base64
import io
from io import BytesIO
from PIL import Image
from Executablefile import predic
from keras.models import model_from_json
app = Flask(__name__)

@app.route('/')
def index():
	return render_template("interface.html")


@app.route('/predict/', methods=['GET','POST'])
def predict():
    oper = BytesIO(base64.urlsafe_b64decode(request.form['operation']))
    value = request.form['value']
    func(oper)
    json_file = open('model_final.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)# load weights into new model
    loaded_model.load_weights("model_final.h5")
    res=predic(value,loaded_model)
    return str(res)
# Parsing Image function
def func(imgData):
	rawBytes = imgData.getvalue()
	rawIO = io.BytesIO(rawBytes)
	rawIO.seek(0)
	byteImg = Image.open(rawIO)
	byteImg.save('output.png', 'PNG')

if __name__ == '__main__':
	app.run(threaded=True)
