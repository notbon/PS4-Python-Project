from ev3dev.ev3 import *

Sound.speak("You have pressed L2, Megalovania shall play now...").wait() #Press L2 to play Megalovoania song.
Sound.tone([(1174, 100, 100),
(1174, 100, 100),
(2349, 150, 100),
(1760, 150, 100),
(1661, 100, 100),
(1567, 150, 100),
(1396, 150, 100),
(1174, 150, 100),
(1396, 100, 100),
(1567, 100, 100),
(1046, 100, 100),
(1046, 100, 100),
(2349, 100, 100),
(1760, 150, 150),
(1661, 150, 100),
(1567, 150, 100),
(1396, 150, 100),
(1174, 100, 100),
(1396, 100, 100),
(1576, 100, 100),
(1975, 100, 100),
(1975, 100, 100),
(2349, 150, 100),
(1760, 150, 150),
(1661, 150, 100),
(1567, 150, 100),
(1396, 150, 100),
(1174, 100, 100),
(1396, 100, 100),
(1567, 100, 100)
]).wait()
