from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Roll:
    pins: int


class Frame(ABC):

    def __init__(self):
        self.rolls: list[Roll] = []
        self._next_frame: [Frame] = None


    def next_frame(self):
        return self._next_frame

    def total_pins(self) -> int:
        return sum(roll.pins for roll in self.rolls)

    def strike(self):
        return len(self.rolls) > 0 and self.rolls[0].pins == 10

    def spare(self):
        return len(self.rolls) == 2 and self.rolls[0].pins + self.rolls[1].pins == 10

    @abstractmethod
    def add_roll(self, pins: int):
        raise NotImplementedError

    @abstractmethod
    def score(self) -> int:
        raise NotImplementedError

    def __str__(self) -> str:
        if len(self.rolls) == 0:
            return ""
        elif len(self.rolls) == 1:
            if self.strike():
                return "X"
            else:
                return f"{self.rolls[0].pins} | "
        elif len(self.rolls) == 2:
            if self.spare():
                return f"{self.rolls[0].pins} | /"
            else:
                return f"{self.rolls[0].pins} | {self.rolls[1].pins}"


class NormalFrame(Frame):
    def __init__(self):
        super().__init__()

    def add_roll(self, pins: int):
        if pins + self.total_pins > 10:
            raise ("A frame's rolls cannot exceed 10 pins")

        if len(self.rolls) < 2:
            self.rolls.append(Roll(pins))

    def score(self) -> int:
        points = self.total_pins
        if self.strike():
            if len(self.next_frame.rolls) == 2:
                points += self.next_frame.total_pins
            elif len(self.next_frame.rolls) == 1:
                points += self.next_frame.rolls[0].pins
                if len(self.next_frame.next_frame.rolls) > 0:
                    points += self.next_frame.next_frame.rolls[0].pins
        elif self.spare():
            if len(self.next_frame.rolls) > 0:
                points += self.next_frame.rolls[0].pins

        return points


class juego:

    MAX_FRAMES = 10

    def __init__(self):
        self.frames: list[Frame] = []
        self._init_frames()
        self.roll_count: int = 0

    def current_frame_index(self) -> int:
        if self.roll_count < (juego.MAX_FRAMES * 2):
            return self.roll_count // 2
        else:
            return juego.MAX_FRAMES - 1

    def current_frame(self) -> Frame:
        return self.frames[self.current_frame_index]


    def _init_frames(self):
        frame = NormalFrame()

        for i in range(9):
            if i < 8:
                next_frame = NormalFrame()
            else:
                next_frame = Frame()
            frame.next_frame = next_frame
            self.frames.append(frame)
            frame = next_frame

        self.frames.append(frame)

    def roll(self, pins: int):
        self.frames[self.current_frame_index].add_roll(pins)
        if self.frames[self.current_frame_index].is_strike():
            self.roll_count += 2
        else:
            self.roll_count += 1

    def score(self) -> int:
        if self.current_frame_index < juego.MAX_FRAMES - 1:
            raise IndexError("There are not enough frames to calculate score")

        return sum(frame.score() for frame in self.frames)


