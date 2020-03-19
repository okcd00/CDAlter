# coding: utf-8
# ==========================================================================
#   Copyright (C) 2018-2020 All rights reserved.
#
#   filename : TextToSpeech.py
#   author   : chendian / okcd00@qq.com
#   origin   : junzew / HanTTS
#   date     : 2020-03-09
#   desc     : TTS class
# ==========================================================================
import os
import time
import wave
import json
import _thread
import pyaudio
import CDMouth.atc as atc
from pathlib import Path
from pypinyin import lazy_pinyin, TONE3
from pydub import AudioSegment
from pydub.silence import split_on_silence


class TextToSpeech:
    CHUNK = 1024
    punctuation = [
        '，', '。', '？', '！', '“', '”', '；', '：', '（', "）",
        ":", ";", ",", ".", "?", "!", "\"", "\'", "(", ")"]

    def __init__(self):
        self.delay = 0.450
        self.root_path = '../'
        self.source_dir = os.path.join(
            self.root_path, 'CDMouth', 'syllables/')
        pass

    def speak(self, text):
        syllables = lazy_pinyin(text, style=TONE3)
        print(syllables)
        delay = 0

        def pre_process(_syl):
            temp = []
            for _s in _syl:
                for p in TextToSpeech.punctuation:
                    _s = _s.replace(p, "")
                if _s.isdigit():
                    _s = atc.num2chinese(_s)
                    new_sounds = lazy_pinyin(_s, style=TONE3)
                    for e in new_sounds:
                        temp.append(e)
                else:
                    temp.append(_s)
            return temp

        syllables = pre_process(syllables)
        for syllable in syllables:
            path = self.source_dir + syllable + ".wav"
            _thread.start_new_thread(TextToSpeech._play_audio, (path, delay))
            delay += self.delay

    @staticmethod
    def mp3_to_wav(source_file_path, dest_path=None):
        if dest_path is None:
            dest_path = source_file_path.replace('.mp3', '.wav')
        sound = AudioSegment.from_mp3(source_file_path)
        sound.export(dest_path, format='wav')

    @staticmethod
    def split_wav(path, syllables=None, key='a', debug=False):
        # syllables in form of [['a1', 'a2', 'a3', 'a4', 'a'], ...]
        file = Path(path)
        if not file.is_file():
            raise Exception(path + " doesn't exist")
        if syllables is None:
            data = json.load(open('mapping.json'))
            syllables = data.get(key)
        sound_file = AudioSegment.from_wav(path)
        audio_chunks = split_on_silence(
            sound_file,
            min_silence_len=333,  # must be silent for at least 333ms
            silence_thresh=-32  # consider it silent if quieter than -32 dBFS
        )
        # from mapping.json in HanTTS
        for i, chunk in enumerate(audio_chunks):
            if debug:  # debug mode, ignore syllables list.
                out_file = "./pre/test{:03}".format(i) + '.wav'
            elif isinstance(syllables[0], list):  # nested list of 5 tones
                if i // 5 >= syllables.__len__():  # over-capacity chunks
                    syllable = 'oth{}'.format(i)
                    out_file = "./pre/" + syllable + '.wav'
                else:
                    syllable = syllables[i // 5]
                    print(syllable)
                    j = i % 5
                    if j != 4:  # 1st, 2nd, 3rd, 4th tone
                        out_file = "./pre/" + syllable + str(j + 1) + ".wav"
                    else:  # neutrual tone
                        out_file = "./pre/" + syllable + ".wav"
            else:  # a list of single tones
                if i >= syllables.__len__():  # over-capacity chunks
                    syllable = 'oth{}'.format(i)
                    out_file = "./pre/" + syllable + '.wav'
                else:
                    syllable = syllables[i]
                    print(syllable)
                    out_file = "./pre/" + syllable + ".wav"
            print("exporting", out_file)
            chunk.export(out_file, format="wav")
        return audio_chunks

    def synthesize(self, text, src, dst):
        """
        Synthesize .wav from text
        src is the folder that contains all syllables .wav files
        dst is the destination folder to save the synthesized file
        """
        print("Synthesizing ...")
        delay = 0
        increment = self.delay * 1000  # milliseconds
        pause = 500  # pause for punctuation
        syllables = lazy_pinyin(text, style=TONE3)

        # initialize to be complete silence, each character takes up ~500ms
        result = AudioSegment.silent(duration=500 * len(text))
        for syllable in syllables:
            path = src + syllable + ".wav"
            sound_file = Path(path)
            # insert 500 ms silence for punctuation marks
            if syllable in TextToSpeech.punctuation:
                short_silence = AudioSegment.silent(duration=pause)
                result = result.overlay(short_silence, position=delay)
                delay += increment
                continue
            # skip sound file that doesn't exist
            if not sound_file.is_file():
                continue
            segment = AudioSegment.from_wav(path)
            result = result.overlay(segment, position=delay)
            delay += increment

        directory = dst
        if not os.path.exists(directory):
            os.makedirs(directory)

        result.export(directory + "generated.wav", format="wav")
        print("Exported.")

    @staticmethod
    def _play_audio(path, delay):
        try:
            time.sleep(delay)
            wf = wave.open(path, 'rb')
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)
            data = wf.readframes(TextToSpeech.CHUNK)

            while data:
                stream.write(data)
                data = wf.readframes(TextToSpeech.CHUNK)

            stream.stop_stream()
            stream.close()
            p.terminate()
            return
        except Exception as e:
            print(e)
            pass


if __name__ == '__main__':
    tts = TextToSpeech()
    while True:
        _t = input('输入中文：')
        if str(_t).lower().startswith('exit'):
            break
        tts.speak(_t)

