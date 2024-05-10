import sounddevice as sd
import threading
import librosa
import numpy as np
import sys

class MusicAnalyser:

    def __init__(self, file_path):
    
        #load file
        self.y, self.sr = librosa.load(file_path)
        self.ptr = 0
        
        #FFT
        win_size = 2048
        self.fft = np.abs(librosa.stft(self.y, n_fft=win_size, hop_length=win_size//2, win_length=win_size//2))
        self.fft_vals = np.zeros((win_size//2)+1)
        
        #Beat info
        self.tempo, self.beats = librosa.beat.beat_track(y=self.y, sr=self.sr, units='samples')
        self.beat_ptr = 0
        self.amplitude = 0
        
        class AudioTask:
            def __init__(self):
                self._running = True
            def terminate(self):
                self._running = False
            def run(self, action):
                action()

        
        c = AudioTask()
        t = threading.Thread(target = c.run, args = (self.play_audio_file,))
        t.start()
    
    #Has there been a beat since this was last called?
    def is_beat(self):
        next_beat = self.beats[self.beat_ptr]
        is_beat = False
        if next_beat < self.ptr:
            is_beat = True
            self.beat_ptr += 1
        return is_beat
        

    def play_audio_file(self):

        sd.default.samplerate = self.sr
        sd.default.channels = 1 
        def callback(outdata, frames, time, status):
            if status:
                print(status, file=sys.stderr)
            output_signal = self.y[self.ptr:self.ptr +frames]
            self.ptr += frames
            if self.ptr > len(self.y):
                wrap_ptr = self.ptr - len(self.y)
                wrap_signal = self.y[0:wrap_ptr]
                output_signal = np.concatenate((output_signal,wrap_signal))
                self.ptr = wrap_ptr
            output_signal = np.expand_dims(output_signal, axis=1)
            outdata[:] = output_signal
            current_fft_ptr = self.ptr//len(self.fft_vals)
            self.fft_vals = self.fft[:,current_fft_ptr]
            self.amplitude = np.mean(np.abs(output_signal))

        with sd.OutputStream(channels=1, callback=callback,
                             samplerate=self.sr):
            print('#' * 80)
            print('press Return to kill  music')
            print('#' * 80)
            input()
            



