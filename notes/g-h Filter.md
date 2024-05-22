# g-h Filter
I was a dumbass and accidentally deleted my notes/code. Thankfully I didn't have much, and what 
little I did have covered pretty basic stuff.
The gist behind a g-h filter is simple. We have some (unobserved) state that we want to estimate. We have inaccurate/noisy measurement(s) and have constructed model(s) for the state we're estimating. Our estimate is  a **blend** our prediction and our measurement, and we assign different static *weights* to emphasize either our prediction or our measurement.

![[Pasted image 20240522144136.png]]

For example, let's say we measure ourselves on a scale every day, and we estimate we gain one pound each day.
$$estimate = prediction + \Bigl(g \times \underbrace{(measurement - prediction)}_{residual} \Bigr)$$
Let's say we start at 160 pounds. We believe, for some reason, that our prediction is *more likely to be correct* than our measurement; we'll express this belief by scaling our measurement by an arbitrary factor of $\frac{4}{10}$. Finally, the scale shows we weigh 158 pounds on the second day. Our second day estimate for our weight is given by
$$\hat{x}_{t+1} = \underbrace{(160+1)}_{prediction} + \frac{4}{10}(158 - 161) = 159.8$$
Our prediction is based on our belief that we gain a pound a day, but we just pulled that out of our ass. Instead of random guessing, we can use old data to update our weight gain at each time step:
$$\text{new gain} = \text{old gain} + \Bigl( h \times \frac{\text{measurement} - \text{predicted weight}}{\text{time step}} \Bigr)$$
We'll pick an arbitrary scaling factor $h$ for the change in measurement over time.
$$\text{new gain} = \text{old gain} + \Bigl( \frac{1}{3} \times \frac{\text{measurement} - \text{predicted weight}}{\text{1 day}} \Bigr)$$
and that's a g-h filter!

>[!abstract] Python Implementation
>```python
>def g_h_filter(data, x0, ds, g, h, dt=1):
>	results = []    # cast as ndarray
>	estimate = x0
>	
>	for z in data:
>		# form prediction
>		prediction = estimate + (dx * dt)
>		
>		# update growth rate
>		dx = dx + (h * (z - prediction) / dt)
>		
>		# form new estimate
>		
>		estimate = prediction + (g * (z - prediction))
>		results.append(estimate)
>	return np.asarray(results)
>```


g-h filters are a *family* of filters, including the Kalman Filter! Each filter is differentiated by how $g$ and $h$ are chosen. The Kalman filter varies them dynamically at each step.

## Example: Tracking a Train
Trains are heavy and slow, so they can't change speed very quickly. They're also on a track, so they can't change direction except by slowing, stopping, and reversing. As such, we can feel confident in our predictions of position in the near future given we know the train's approximate position and velocity. $\underline{\text{A train can't change its velocity much in a couple of seconds}}$.

We write a filter for the train. We measure his position (the train's name is Gary) once per second with an error of $\pm$ 500 meters.
If we rely purely on (simulated) measurements, we get the following 'estimates' on position.
![[Pasted image 20240522151356.png]]
This kinda sucks; trains don't move that sporadically.
So how do we choose $g$ and $h$? We don't have a theory for this, so we'll just wing it without mathematical rigor. We know our measurements are inaccurate, so we'll assign them relatively little weight. This means choosing a small $g$! We also know that trains can't change velocity quickly, so we'll de-emphasize changes in change with a small $h$.
```python 
data=g_h_filter(data=zs, x0=pos, dx=15, dt=1., g=0.1, h=0.0001)
```
![[Pasted image 20240522151841.png|500]]
We can make $g$ larger; measurements are more important to our estimates.
![[Pasted image 20240522151930.png|500]]
$g = 0.2$ shows a lot of small fluctuations in position. We know this is impossible for a train to do, so any choice of $g > 0.2$ is a poor choice.
Let's see a poor choice of $h$:
![[Pasted image 20240522152121.png|500]]
The position changes smoothly because of the small $g$, but the large $h$ makes the filter *very reactive* to the measurements! Within a few seconds, the rapidly changing measurement implies a large velocity change, and a large $h$ tells the filter to **react to those changes quickly**. The filter changes the velocity faster than Gary ever could.