---
layout: post
title: Dissertation submitted
image: /img/diss_cover.png
tags: 
---


After a long year, I am happy to share that I have finished my Master's dissertation
titled Adaptive Motion Control for Autonomous Racing. I managed to create a 2-stage
system consisting of trajectory optimization and tracking, both of which share the
same model and adapt to dynamical changes online. The key is that the model is a
semi-parametric one consisting of a classical parametric model which does the larger
part of the prediction and a neural network which learns the residuals (or errors) of
the parametric model. This method, combines the strength of both modelling types,
resulting in a system which generalises well, learns accurate dynamics and adapts
robustly to changing dynamics. Sadly, it can only adapt to short-term changes in
dynamics due to the batch training nature of neural networks.

<div class="video-container">
    <iframe src="https://youtu.be/aLWXa95AEKE" frameborder="0" allowfullscreen>
    </iframe>
</div>

Even though I didn't achieve everything I had planned to, this experience has taught
me to look past the idealistic aspects of both motion control and machine learning,
but instead understand their fundamentals. I now realize that is more important
than getting good results.

A big thank you to Michael Mistry, Christoforos Chatzikomis, and Timo Völkl for
supporting me through this journey. I wouldn't have done it without you!

Sadly I cannot share my dissertation publicly, but you can find part 1 of my dissertaion
which sets the grounds [here](/files/Ignat_MInf1_project.pdf)
