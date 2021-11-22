# SpiralMusic_python
A python program for visualizing MIDI files, and displaying them in a spiral layout

For a hardware version using Teensy & LED displays see here: https://github.com/mechatronicsguy/SpiralMusic_Teensy

## Who is this software for?

People like me, who kinda like music, but are often left confused by the notation. 

e.g. Take this picture: Are these *three different chords*, or actually *the same chord voiced three different ways*? 
![Musical notation](https://github.com/mechatronicsguy/SpiralMusic_python/blob/main/pics/4tcqogmi_transposed_v01.png?raw=true)

I could stare at this for a couple of minutes and still not be 100% sure. 


But I could tell immediately after seeing this: 
![Same Musical notation in spiral GIF form](https://github.com/mechatronicsguy/SpiralMusic_python/blob/main/pics/4tcqogmi%20animation%20full%20v01.gif?raw=true)

## Software features
* Simple & open source. Built around Pygame & MIDO library
* Reads ordinary MIDI files
* Different instruments show up as different colours
* Tracks program change messages in order to display which instruments are used on which channel

## Features of the visualizing method: 
* You can see an entire orchestra "Cooperating" to make a chord, wtihout having to read 6 sets of sheet music simultaneously
* Makes it extremely easy to see transpositions (just rotations)
* Melodic inversion is just a mirror flip
* Notes played stay visible for a time as a 'histogram'. Key signature can be inferred from this
* Different instruments (midi channels) are different colours. Can see contributions of each instrument to the whole

All chords have very simple and recognizable shapes, regardless of key:

![Chord shapes](https://github.com/mechatronicsguy/SpiralMusic_python/blob/main/pics/Chord%20shapes%20small%20v01.jpg?raw=true)



https://user-images.githubusercontent.com/955307/142713611-d7514a49-bbaa-462b-8e3b-9fe1f043b4a9.mp4


Some more examples: 

https://www.youtube.com/watch?v=fZ3JxfQlj_A

https://www.youtube.com/watch?v=Y0DqMEkbHkw

https://www.youtube.com/watch?v=-hYWCuFySls
