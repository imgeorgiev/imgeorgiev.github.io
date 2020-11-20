---
layout: post
title: My first paper
subtitle: I got my first research paper accepted into an internal conference! 
image: /img/sim_crop.png
tags: [robotics, updates]
---

As a byproduct of my [Master's thesis](http://imgeorgiev.com/2020-06-06-dissertation) I have
had my first paper accepted into the [Conference of Robot Learning 2020](https://www.robot-learning.org/).
The paper is titled Iterative Semi-parametric Dynamics Model Learning For Autonomous Racing which
is quite self-explanatory. You can [read it on arxiv](https://arxiv.org/abs/2011.08750). It was
a big team-effort and I couldn't have done it without all the co-authors who helped me and
mentored me along the way.

## Abstact

Accurately modeling robot dynamics is crucial to safe and efficient motion control. In this paper, we develop and apply an iterative learning semi-parametric model, with a neural network, to the task of autonomous racing with a Model Predictive Controller (MPC). We present a novel non-linear semi-parametric dynamics model where we represent the known dynamics with a parametric model, and a neural network captures the unknown dynamics. We show that our model can learn more accurately than a purely parametric model and generalize better than a purely non-parametric model, making it ideal for real-world applications where collecting data from the full state space is not feasible. We present a system where the model is bootstrapped on pre-recorded data and then updated iteratively at run time. Then we apply our iterative learning approach to the simulated problem of autonomous racing and show that it can safely adapt to modified dynamics online and even achieve better performance than models trained on data from manual driving.

## Video

{% include youtubePlayer.html id="_zYue3xXkxM" %}
