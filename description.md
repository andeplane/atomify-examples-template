# Introduction
In these simulations, we simulate atoms diffusing in a liquid and measure the diffusion coefficient using methods like mean square displacement and velocity auto correlation.

The mean square displacement is defined as 

$MSD = \langle (\vec x(t) - \vec x_0)^2\rangle  = \frac{1}{N}\sum_{i=1}^{N} |\vec x^{(i)}(t) - \vec x^{(i)}_0|^2$

and relates to the diffusion coefficient as

$D = \frac{\langle (\vec x(t) - \vec x_0)^2\rangle}{2D}$

where $D=2$ is the number of dimensions. We can also calculate the diffusion coefficient through a Green-Kubo relation given as

$D = \int_0^\infty dt \langle u(t) u(0) \rangle$, where $\langle u(t) u(0) \rangle$ is the velocity auto correlation function.