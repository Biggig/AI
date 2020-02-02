import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.randn(6, 4), columns=['a', 'b', 'c', 'd'])
print(df)