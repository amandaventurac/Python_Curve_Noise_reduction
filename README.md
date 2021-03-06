# Python_Curve_Noise_reduction

This project is a simple python script to perform specific curve noise reduction.
The script reads the input files (x = 1.txt {if x> 0}, y = 2.txt), creating and ploting two lists.
The bottom part of bifurcation is all noise. 
To filter the noise, linear regression is applied to the most linear part of the curve, then the extrapolated model is used to filter the right side of the curve.
The output is the graphs and two text files with filtered noise.
PS: these files are fictitious random data.

![initial curve](https://github.com/amandaventurac/Python_Curve_Noise_reduction/blob/main/before_noise_reduction.png)


Curve before noise reduction, the bottom of bifurcation is noise. The linear part of the curve will be used in linear regression:


![linreg](https://github.com/amandaventurac/Python_Curve_Noise_reduction/blob/main/linear_model.png)

The model is extrapolated to predict the right side of the curve, this prediction is used to filter the noise with small deviation criteria.


![final](https://github.com/amandaventurac/Python_Curve_Noise_reduction/blob/main/filteres_curve.png)

