---
layout: post
title: Why Behaviour Cloning?
subtitle: How BC worked where RL failed
image: /img/blog/2025-01-31-why-bc-not-rl/bc.png
bibliography: papers.bib
tags: [robotics, research, long]
header-includes:
  - \usepackage[ruled,vlined,linesnumbered]{algorithm2e}
  - \usepackage{amssymb}
  - \usepackage{amsmath}
  - \usepackage{mathtools}
  - \usepackage{amsthm}
---

Everybody *wants* to love Reinforcement Learning (RL)! It was the 3rd most popular topic at NeurIPS 2024, just after CV and NLP 🤯! Hell, I self-identify as an RL person. However, the unfortuante reality is that RL has failed to deliver when it comes to robotics. There's a new kid on the block called Behaviour Cloning (BC) that only in a couple of years did what RL couldn't in decades. I recently did a little foray into the world of BC and now want to share what I learned.

![Generated with ChatGPT](/img/blog/2025-01-31-why-bc-not-rl/bc.png)


**Table of contents**
* TOC
{:toc}

What can RL do?
=================
<!-- 
- RL basics; why the math is elegant; roots in optimal control
- what do we really mean with deep RL. The flaw of sample inefficiency; reduced to simulations.
- what has actually worked - locomotion sim2real
- these types of cyclic high-speed actions; but then can't we still solve that with classical control?
-->

Everybody *wants* to love RL! It is mathematically elegant and follows our real-world intuition. It mimics how we humans learn by trial and error and follows concepts from psychology about reward and punishment. Mathematically, RL problems are formulated as some flavor of a Markov Descision Process (MDP) where we have a state $s_t$ and action $a_t$ at time $t$ which follow some dynamics function $s_{t+1} = f(s_t, a_t)$. The mathematical goal then is to maximize a sequence of rewards given by $r(s_t, a_t)$.

$$ \max_{\{a_0, .., a_T\}} J = \max_{\{a_0, .., a_T\}} \sum_{t=0}^{T} r(s_t, a_t)$$

Such a beautiful formula! It is simple, general, and follows the temporal dependencies of the real-world! I can't wait to solve all of robotics with it! (me at the start of my PhD) The issue though is that this is a **very hard** equation to solve.

What makes it hard, unlike the much more successful world of supervised learning, RL has an added temporal dimension and has to reason about the consequences of actions at different times. In a way, has to explore to find the solution, usually by sampling random actions ${a_0, .., a_T}$. This requires a lot of data. You've probably seen a couple of walking robots powered by RL such as this one:

![](https://media.licdn.com/dms/image/v2/D4E22AQHEFANFi7GXuQ/feedshare-shrink_2048_1536/feedshare-shrink_2048_1536/0/1719093619338?e=2147483647&v=beta&t=o4xCJRw-HpQhGCvYluGUzA8Hvpp_-Di8JwY7NdxeTy8)

If you follow the origin work of this [1] you'll quickly realize that these RL models need the order of ~$10^9$ data samples to work! That is ~231 robot days of data. The kicker? Since RL has to explore, most of this data is the robot falling over. This has limited RL only to simulation. This opens Pandora's box - how do we make our simulations fast? how do we make them accurate? how do we transfer policies from simulation to the real world? None the less, a lot of amazing research has addressed many of these questions and now we have pretty well performing robots!


[![DEEP Robotics](https://img.youtube.com/vi/yPFXBLavoro/0.jpg)](https://www.youtube.com/watch?v=yPFXBLavoro "DEEP Robotics")

(OK that was actually pretty cool)

These tasks that RL does really well is what I call **cyclic tasks**. From control theory, cyclic behaviour is when the optimal trajectory converges to a closed loop (cycle) regardless of initial conditions. Mathemtically, you have an optimal trajectory $A=\{a_0, a_1, a_2, .., a_H\}$ that is sufficient to solve the task i.e. $$\text{argmax} J = \{A, A, A, ...\}$$. Cyclic tasks are ones that can be solved with cyclic behaviour.

While intuitively appealing, we can't use this to quantify cyclic behaviour. I am not sure what we can use, but I found two patterns - (1) stable value functions and (2) convex objectives after stochastic smoothing.

In my AHAC paper [9], I had an experiment with an Anymal quadruped running as fast as possible.

<div class="embed-responsive" embed-responsive-16by9>
  <video class="embed-responsive-item" controls>
    <source src="/img/blog/2025-01-31-why-bc-not-rl/anymal.mp4" type="video/mp4">
  </video>
</div>

If we now take the critic of converged AHAC on this task (or any critic really) and plot the value function with respect to time, we see that the value function converges around a single value. The converged value will vary per algorithm and parametarization but this is one common pattern of cyclic tasks.

$$ V(s_t) = \mathbb{E} \bigg[ \sum_{t'=t}^{T} \gamma r(s_{t'}, a_{t'}) \bigg] $$

![](/img/blog/2025-01-31-why-bc-not-rl/value.png)

The second common pattern I found is that these cyclic tasks appear convex after stochastic smoothing (see [What makes RL tick](https://www.imgeorgiev.com/2024-03-15-stochastic-rl/)). Below I take the converged and optimal Anymal running policy, select a **single parameter** from the actor neural network and change it to get a pseudo-landscape for the problem.

![](/img/blog/2025-01-31-why-bc-not-rl/anymal_landscape.jpeg)
TODO update so that it's cleaner and has only the blue plot. Also TODO apply stochastic smoothing

While this landscape is absolutely not convex, if you apply sufficient smoothing to it, it becomes pretty easy to solve for most RL algorithms. This stochastic smoothing is what has enabled RL to do what classical control hasn't been able to. All cyclic tasks I've seen exhibit good convexity after smoothing.


What can RL not do?
=================
<!-- 
- sequentally convex tasks; give little sketch; introduce pusht task
- staying within distribution; give little sketch
- multi-task scaling to robot foundational models; noise in value function -->

RL looks pretty magical so far, you can't just tell me it's bad now! In my opinion RL **is terrible at non-cyclic tasks**.

The simplest example - pick and place. Can you get it to work? probably. However, it doesn't matter how many days you spend reward engineering this, RL is still going to be terrible at this task! Let's take the very well engineered [StackCube task from Maniskill3](https://maniskill.readthedocs.io/en/latest/tasks/table_top_gripper/index.html#stackcube-v1).

<div class="embed-responsive embed-responsive-1by1">
  <video class="embed-responsive-item" controls>
    <source src="https://github.com/haosulab/ManiSkill/raw/main/figures/environment_demos/StackCube-v1_rt.mp4" type="video/mp4">
  </video>
</div>

Their [reward function](https://github.com/haosulab/ManiSkill/blob/main/mani_skill/envs/tasks/tabletop/stack_cube.py#L145) is a whopping 36 lines of code! They have 3 modes of reward (1) bring robot arm to cube to pick, (2) grasp cube on put on top of other cube and (3) ungrasp cube on top of the other cube. Here is a scetch of how I *think* that translates to a value function over time.

![](/img/blog/2025-01-31-why-bc-not-rl/cube_value.jpeg)

That looks significantly less straightforward to solve. Imagine you're an RL algorithm osciliating between those different states of the task. As you can imagine that create a significantly more challening optimization landscape.

However, the focus of this blog is the PushT task. It's a contact-rich, highly non-convex task where a robot mush push a T-shaped object into a goal pose. The success critera is 95% overlap and the most straightforward reward is:

```
reward = clip(coverage / success_threshold, 0.0, 1.0)
```

<div class="embed-responsive embed-responsive-1by1">
  <video class="embed-responsive-item" controls>
    <source src="/img/blog/2025-01-31-why-bc-not-rl/pusht.mp4" type="video/mp4">
  </video>
</div>

This is an incredibly hard task for RL to do. Why? To succeed, you need to push from different positions, which means making or breaking contact. However, a typical RL value function will tell us that the highest value is to stay close to the T. In other words, RL gets stuck in the natural local minima of the task. I tried applying TD-MPC2 [8], an actor-critic approach with online planning to the task. I chose it because I thought it had the highest chance of success, but it still gets 0% success.

<div class="embed-responsive embed-responsive-1by1">
  <video class="embed-responsive-item" controls>
    <source src="/img/blog/2025-01-31-why-bc-not-rl/pusht_tdmpc2.mp4" type="video/mp4">
  </video>
</div>

<details>
  <summary>Experiment details</summary>
  Here I am using the official TD-MPC2 implementation and the PushT implementation from huggingface. I have trained TD-MPC2 online for 10M timesteps and episode length 300. Using only state observations and the default hyper-parameters. Over 50 evaluation episodes, I get 0% success rate.
</details>

Why can't RL solve it? To find out let us investigate the optimization landscape for the actor $$J(a_t) = Q(s_t, a_t)$$ where the actor is trying to find the action that maximizes the value function. Using this simple actor objective, we can take the converged critic, replay an expert demo and at each timstep state $s_t$ sample $a_t$ across the full range.

<div class="embed-responsive embed-responsive-21by9">
  <video class="embed-responsive-item" controls>
    <source src="/img/blog/2025-01-31-why-bc-not-rl/pusht_tdmpc_landscape.mp4" type="video/mp4">
  </video>
</div>

Darker colors indicate high value (low loss) and light colors indicate low value (high loss). The cross is the action taken in the dataset. Pause and replay the video. Observe the times at which the agent has to break contact and go away from the object. These actions form local minima from which RL struggles to escape. Here I want to highlight that this isn't an issue with TD-MPC2. Matter of fact, the best RL algrotihms, PPO, DreamerV3 and TD-MPC2 all can't solve this seemingly simple task [3]. I think it is a mismatch between the RL problem formulation and the task at hand.

This isn't actually the full story, in the optimization landscape above, I was using a fixed critic which means that my actor had a fixed objective. In practice, most algorithms like TD-MPC2 have an actor-critic architecture where the both are updated one after the other. **This means that our actor has a moving target!** From an optimization point of view, that is a disaster. Here is the disaster visualized:

<div class="embed-responsive embed-responsive-21by9">
  <video class="embed-responsive-item" controls>
    <source src="/img/blog/2025-01-31-why-bc-not-rl/pusht_tdmpc_landscape_moving.mp4" type="video/mp4">
  </video>
</div>

<details>
  <summary>Experiment details</summary>
  This experiment was designed to show the moving actor objective throughout the lifetime of an RL learning loop. By lifetime I mean from policy initialization to policy convergence. In this experiment I start with an untrained TD-MPC2 and at t=25,50,75 I load TD-MPC2 weights that represent different stages of convergence. The weights at t=75 are full converged. You can see that each consequitive set of weights has more optimal value function. Unfortunately, this still doesn't help the algorithm escape the natural local minima of the problem.
</details>

This don't look too good for RL, but there is yet one more issue. RL optimization is just painfully inefficient because we're stuck with zeroth-order graidents [10]. Since we usually assume that the environment is unknown, we can't compute gradients and we are limited to only TD learning approaches. They work, they just require a lot of data! Interestingly enough, even if we can learn the environment dynamics, that still doesn't help us learn a value function faster [11].

In summary, the **fundemental issues with RL** are:
1. It is bad at non-cyclic tasks due to the natural local minima of the tasks.
2. The policy objective is a moving target, making learning inefficient and unstable.
3. By definition we are stuck with inefficient optimizaiton.

<details>
  <summary>Can you actually get RL to solve PushT?</summary>
  It might be possible to engineer a better reward to solve the task, but that is a seperate bucket of issues. <a href="/https://github.com/haosulab/ManiSkill/blob/main/mani_skill/envs/tasks/tabletop/push_t.py">Maniskill3 tried that with some success.</a>. While possible, I want you to ponder the question, is this really the right toolbox for this task?
</details>


<!-- ### Out of distribution

Another flaw of RL is that it can overestimate the value of out of distribution states. That can later be exploited by the actor to go out of distribution and as we all know, a lot of spooky and weird things happen when learning goes outside of distribution. The kicker? Going out of distribution in CV means showing you a cat instead of a dog in your google search. Going out of distribution in robotics likely means a several thousand dollar mistake. Let's show this on our simple PushT task but (1) modified it such that if the agent goes outside of a zone, it dies. (2) We give it human domnstrations of the task that don't go in the red zones (remember we don't want to break our robots). (3) Plotting the value landscape shows that depending on the magic of deep learning initialization, you can end up with your model inferring high value in of the bad OOD areas. If you now deploy this policy, you might find that your robot very confidently wants to jump off a cliff. 

![](/img/blog/2025-01-31-why-bc-not-rl/pusht_ood.jpeg)
TODO make this a side by side video as above.

But Ignat, RL has been shown to work even without these issues! Yes, it absolutely does. The quadruped videos above are a prime example of this. You can do sim2real. You can engineer some fail safe based on classical methods. Solutions exist but they are all bandaids for the fundamental limitations of RL when applied to robots! -->



The beautiful simplicity of BC
================
<!-- 
- introduce simplified ACT
- data pipeline of behaviour cloning
- how it solves sequentially convex tasks
- BC still has it's limitations: OOD is still an issue. It theoretically can't get the optimal policy. But it's darn simple -->

If you've been around in robotics, you've probably noticed the new cool kid on the block - Behaviour Cloning (BC). Influential work such as Diffusion Policy [4], OpenVLA [5] and $\pi_0$ [6] did pretty incredible manipulation tasks such as folding a T-shirt or picking graps from a plastic box with a spoon directly from image observations. Meanwhile in RL we still struggle to stack cubes with priviledged state information.

<div class="embed-responsive embed-responsive-4by3">
  <video class="embed-responsive-item" controls>
    <source src="https://dnrjl01ydafck.cloudfront.net/v3/upload/processed_collage.mp4" title="Pi-0 model from Phyiscal Intelligencce" type="video/mp4">
  </video>
</div>

Why does BC work where RL hasn't? I think it's manily due to two reason (1) it's **simple** and (2) **supervised learning** is an easier problem defintion to optimize over. Let's see why by studying one of the simplest, yet impressive BC algorithms - Action Chunking Transformer (ACT) [7]. It's super simple!
1. Collect some expert demonstration data (usually via teleoperation).
2. Get observation from observation $o_t$ from your offline dataset.
3. Tokenize images with a pre-trained ResNet. Tokenize state data with an MLP.
4. Feed both into a transformer encoder-decoder and predict a trajectory $$\hat{A}_t = \pi_\theta (o_t)$$ and train it to regress some ground truth (expert data) using supervised learning:

$$ J(\theta) = \| A_t - \pi_\theta(o_t) \|_1 $$

![](/img/blog/2025-01-31-why-bc-not-rl/act_arch.jpeg)

I took 200 expert demos and trained a simple ACT policy to solve PushT with 78% success rate (a big jump from RL's 0%)!

<div class="embed-responsive embed-responsive-1by1">
  <video class="embed-responsive-item" controls>
    <source src="/img/blog/2025-01-31-why-bc-not-rl/pusht_act.mp4" type="video/mp4">
  </video>
</div>

<details>
  <summary>Experiment details</summary>
  For this I used my <a href="https://github.com/imgeorgiev/ImitationHype">own implementation of ACT</a> which is a simplified but better version of the original [7]. I took the 200 episode demos from the Diffusion Policy [4] and trained from images. Note that this makes it a significantly harder task than the RL experiments before. I used 224x224 images with a 4-layer transformer encoder-decoder and trained for 20 epochs. Training took about ~22h on my M1 Max Mac. Success rate in the end was 78% over 50 evals.
</details>


Why does this work so much better, especially with such a simple algorithm? There are many answers to this question but I think BC elegantly addresses the issues I mentioned before with RL:
1. By problem definition, the objective is fully convex.
2. The objective is fixed.
3. The objective can be optimized efficiently with standard first-order gradient optimizaiton. 

Let's demonstrate the convexity of the problem by plotting the policy objective over an expert demonstration again:

<div class="embed-responsive embed-responsive-21by9">
  <video class="embed-responsive-item" controls>
    <source src="/img/blog/2025-01-31-why-bc-not-rl/pusht_bc_landscape.mp4" type="video/mp4">
  </video>
</div>

How exciting! A smooth problem optimization landscape without local minima! This makes BC better-posed to solve these non-cyclic tasks.

That being said, BC isn't perfect and it has it's issues:
1. You need to manually collect expensive teleoperation data. That being said, this is still cheaper than RL breaking your robot.
2. By mathematical definition, BC can't do better than the demonstrations given. But hey, suboptimal is better than complete failure.


That being said, BC is SIMPLE and that is it's greatest strength. I'll leave you with a quote from a friend:

> You can probably theoretically do everything that BC does with classical robotics methods. However, that would need a huge team of people collaborating for years to get any reasonable for of generalisability. Meanwhile, BC can achieve the same results with 3 people and a couple of weeks. The best part? Solving new tasks just involves adding more data!


Out of distribution
================
Wether it is a good idea or not, what works currently in robot learning is **offline training**. That is only natural for BC and RL can still be applied in the form of offline RL. However, how do they compare in terms of Out of Distribution (OOD) performance. While this is well studied in most ML domains (just add more data hehe), in robotics it is more challenging. Even if you are currently in-distribution, you can still take actions that can take you to an OOD state space. Going OOD in robotics, usually means breaking a robot or even putting humans at risk.

High stakes, so how do BC and RL compare? Let's set up an imaginary experiment. Use a limited version of PushT where if the robot goes within 1/10th of the corner, it does. Assume the robot is expensive to replace. Due to that, we can't leave RL to train online, we can only collect offline data from human operators. Human operators also don't want to break the robots, so they collect demos that are within the good operating space. Then we use this data to offline train BC and RL. I collected 200 episodes and assumed that we always start in distribution (not realistic).

![](/img/blog/2025-01-31-why-bc-not-rl/pusht_ood.jpeg)

The case for BC is simple, as long as it stays in-distribution, it will predict correctly and continue to stay in-distribution. Naturally this gets harder as you get to more complex problems, but for our simple problem it holds surprisingly well! I re-trained ACT on this new dataset and got 84% task success rate and 2% death rate! Surprisngly, better than before! I suspect that is because I have limited my problem space and always start in-distribution. Thus, for our very simple problem BC works marvelously well!

Now RL is a different topic, by problem definition, RL has to *explore* to find its optimal solution. Unfortuantely, in our imaginary problem, exploring might sometimes mean death. In the common actor-critic architecture, this phenomena is surprisngly common. Value critic incorrectly extrapolates high reward OOD, actor hasn't seen the OOD data and just predicts garbage. This results in a vicious loop of RL "confidently jumping off a cliff". Let's see this in a practical example though! Here is a visualization of the problem landscape of TD-MPC2 offline trained on this task. 

<div class="embed-responsive embed-responsive-21by9">
  <video class="embed-responsive-item" controls>
    <source src="/img/blog/2025-01-31-why-bc-not-rl/pusht_tdmpc_landscape_dead.mp4" type="video/mp4">
  </video>
</div>

The RL agent wants to jump off a cliff to its death pretty confidently. Now if this is a humanoid robot, that would be about a 6-figure mistake. In contrast, BC doesn't have this fundamental issue simply due to it's problem definition


Conclusion
================

Everybody wants to love RL. I want to love RL! However, I can't ignore the simple elegance and performance of modern BC. In summary these in my opinion are the pros and cons of BC vs RL:
* :white_check_mark: Much simpler.
* :white_check_mark: The policy objective is convex and fixed.
* :white_check_mark: Can be optimized efficiently.
* :white_check_mark: Tends to stay in data distribution.
* :red_circle: Theoretically can't surpass training data perforamnce
* :red_circle: Requires teleoperating your target robot.


Here is a direct comparison between the optimization landscapes of RL and BC. Ask yourself, which one do you want to solve?

<div class="embed-responsive embed-responsive-21by9">
  <video class="embed-responsive-item" controls>
    <source src="/img/blog/2025-01-31-why-bc-not-rl/merged.mp4" type="video/mp4">
  </video>
</div>
<p align="center">
  Comparison between optimization landscapes when replaying an expert demo. Left is visualization of the environment. Middle is the BC optimization landscape. Right is the RL optimization landscape.
</p>

There's a huge race right now with multiple industry labs and startups pushing multi-task BC methods do their limits. The next few years will be excitign to say the least! Who knows, maybe RL will make a come back just like it did with ChatGPT. It's an exciting time to be in robotics!

Thank you for making it this far. I hope that you learned something!

If you have any comments or suggestions, [shoot me an email](mailto:ignat@imgeorgiev.com)!

Something in the middle?
================
TODO

References
================

  
* [1] [Rudin et al. Learning to Walk in Minutes Using Massively Parallel Deep Reinforcement Learning](https://arxiv.org/abs/2109.11978)
* [2] [Christopher et al. Limit Cycles of Differential Equations](https://link.springer.com/book/10.1007/978-3-030-59656-9)
* [3] [Zhou et al. DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning](https://arxiv.org/abs/2411.04983)
* [4] [Chi et al. Diffusion Policy: Visuomotor Policy Learning via Action Diffusion](https://arxiv.org/abs/2303.04137)
* [5] [Kim et al. OpenVLA: An Open-Source Vision-Language-Action Model](https://arxiv.org/abs/2406.09246)
* [6] [Black et a. π0: A Vision-Language-Action Flow Model for General Robot Control](https://arxiv.org/html/2410.24164v1)
* [7] [Zhao et al. Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware](https://arxiv.org/abs/2304.13705)
* [8] [Hansen et al. TD-MPC2: Scalable, Robust World Models for Continuous Control](https://arxiv.org/abs/2310.16828)
* [9] [Georgiev et al., Adaptive Horizon Actor-Critic for Policy Learning in Contact-Rich Differentiable Simulation](https://adaptive-horizon-actor-critic.github.io/)
* [10] [Mohamed et al., Monte Carlo Gradient Estimation in Machine Learning](https://arxiv.org/abs/1906.10652)
* [11] [Amos et al., On the model-based stochastic value gradient for continuous reinforcement learning](https://arxiv.org/abs/2008.12775)
