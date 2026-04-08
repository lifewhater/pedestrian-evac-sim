import seaborn as sns
import matplotlib.pyplot as plt
from src.static_field import static_field

sns.set_theme(style="darkgrid")
iris = sns.load_dataset(static_field)

f, ax = plt.subplots(figsize = (8,8))
ax.set_aspect("equal")

sns.kdeplot(
    data=iris.query("agents != time"),
)