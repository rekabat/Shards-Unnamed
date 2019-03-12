import pygame as pg


class SoundEffects:

    def __init__(self, soundfiles):
        self.filelist = soundfiles
        self.pgSoundDict = self._genSoundDict(soundfiles)
        self.sounds = self.pgSoundDict.keys()

    def _genSoundDict(self, soundfiles):
        pgSoundDict = {}
        for sound in soundfiles:
            pgSoundDict[sound.split(".")[0]] = pg.mixer.Sound(sound)
        return pgSoundDict

    def play(self, sound):
        try:
            self.pgSoundDict[sound].play()
        except KeyError:
            print("Invalid sound: " + sound)

    def randPlay(self):
        self.play(self.sounds[randint(0, len(self.sounds) - 1)])


if __name__ == '__main__':
    import os
    from random import randint

    pg.init()
    soundfiles = ['sounds/' + file for file in os.listdir('sounds')]
    audio = SoundEffects(soundfiles)

    while True:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                audio.randPlay()
