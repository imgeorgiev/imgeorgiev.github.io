---
layout: post
title: Debugging RL for continuous-time tasks
author: Ignat Georgiev
tags: [reinforcement learning]
---

What I've learned:
- if you have the chance, do offline RL! Will save you time and headaches. Give a practical example in numbers. D4RL datasets
- critic error should tend to 0, if it doesn't your model can't capture the complexity required
- neural networks and catastrophic forgetting. In general for neural networks, the more data you have and the more diverse it is, the better chances you will get of them learning correctly. Therefore, if you're using neural nets of any kind with off-policy RL (i.e. you have a replay buffer), then I'd advise to make that as large as humanly possible. Give examples
- data normalisation. Neural networks like it, can be implemented directly in the replay buffer or on top of it.