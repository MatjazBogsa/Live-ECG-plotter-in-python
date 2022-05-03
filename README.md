# ECG-plotter-in-python
Plotting of live or prerecorded ECG data on canvas with python and Tkinter. 

This came about as a side job on a biger project that required ECG ploting. 
I could't find any existing examples that could plot live ECG data, created my own. 
Here it is. Enjoj.

You can plug the functions into your own data stream, but you will have to tweak the settings quite a bit if your data differs from mine. 

!!!! Please note that this was never intended to work as an of-the-shelf, plug and play solution, but rather as a proof of concept !!!!

WARNING: My data is quite dirty and noisy and maybe even vrong. 
I don't know. We hacked an Chinese ECG reader, that came with excelet software that produces way better resoults than this. 
But wee needed raw data, long stroy short, mesurements might be misinterprited but the ECG form in there, and this is good enough for me. 

I first tried to implement it in matplotlib, but couldn't get the old data to be erased on the go. 
So I started drawing lines on the empty canvas and it works. 

