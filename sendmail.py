# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.mail import Message
from flask.ext.mail import Mail
from flask import request
app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'dbissa94@gmail.com',
    MAIL_PASSWORD = 'test',
))
mail = Mail(app)

@app.route('/send_mail',methods=["POST"])
def send_mail():
    data = request.get_json(force=True)
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    gender = data.get('gender')
    date_of_birth = data.get("dob")
    image = data.get("image")
    message_body = data.get("message")
    message = '''Hi, \n my details are \n name:{0} \n email:{1}\n phone:{2} \n
                 gender:{3} \n dob:{4} \n message:{5} \n'''.format(name,email,phone,gender,date_of_birth,message_body)
    msg = Message(body=message,
                  subject="Quick Contact",
                  sender="dbissa94@gmail.com",
                  recipients=["dbissa94@gmail.com"])

    for i in range(len(image)):
        print len(image)
        img_data = image[i].encode('utf-8')
        binary_data = img_data.split(',')
        bin_type = binary_data[0]
        print bin_type
        bin_data = binary_data[1]
        regex = r"(data:)(\w*)(\/)(\w+)"
        import re
        match = re.match(regex,bin_type)
        ext = match.group(4)
        name = match.group(2)

        fh = open("/home/divyang/PycharmProjects/untitled2/static/"+name + "."+ext, "wb")
        fh.write(bin_data.decode('base64'))
        fh.close()
        with app.open_resource(fh.name) as fp:
            msg.attach(name+"."+ext,"Image/png",fp.read())
        import  os
        os.remove(fh.name)
    try:
        mail.send(msg)
        return "Sent"
    except Exception as Failure:
        import traceback
        print traceback.format_exc(Failure)
        print Failure
        return "Failed"


if __name__ == '__main__':
    app.run(port=8443,debug=True)
