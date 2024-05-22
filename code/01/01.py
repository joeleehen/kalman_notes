import numpy as np

def g_h_filter(data, x0, ds, g, h, dt=1):
    results = []    # cast as ndarray
    estiamte = x0

    for z in data:
        # form prediction
        prediction = estimate + (dx * dt)

        # update growth rate
        dx = dx + (h * z - prediction) / dt)

        # form new estimate
        estimate = prediciton + (g * (z - prediction))
        results.append(estimate)
    return np.asarray(results)

