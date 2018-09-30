import subprocess
import tempfile
import wave
import StringIO
import os


class Speak():

    def __init__(self):
        self.lang = 'en-US'
        self.temp_folder = '/tmp/'

    def exec_pico2wave(self, args):
        command =['pico2wave', '-l', self.lang]
        command.extend(args)
        p = subprocess.Popen(command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        result = iter(p.stdout.readline, b'')
        response = []
        for line in result:
            response.append(line)
        
        return response

    def wav(self, message):
        record = None
        with tempfile.NamedTemporaryFile(suffix='.wav') as f:
            print f.name
            msg = message.encode('utf8')
            args = ['-w', f.name, msg]
            self.exec_pico2wave(args)
            #f.seek(0)
            #record = f.read()
            os.system('aplay ' +  f.name)
            
    def speak(self, msg):
        voice = self.wav(msg)


#spk = Speak()
#spk.speak("Hello World!") 
