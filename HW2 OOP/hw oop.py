from abc import ABC, abstractmethod


class Folder(ABC):
    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def open(self):
        pass

    # virtual
    def place(self):
        return "[I was in Folder]"


class File(Folder):
    smth = 128

    def move(self):
        return 12

    def open(self):
        return 15

    def place(self):
        return "[I was in File]"


class Properties(Folder):
    size = 512
    collision = 0

    def move(self):
        return 32

    def open(self):
        return 35

    def place(self):
        return "[I was in Properties]"

    # one more virtual
    def say(self):
        return "U cool :)"


class Shortcuts(File, Properties):
    def move(self):
        return 20

    def open(self):
        return 50

    def say(self):
        return "U very cool ;D"


a = Shortcuts()
print("", a.smth, a.size, a.collision, a.move(), a.open(), "\n", a.place(), a.say())
