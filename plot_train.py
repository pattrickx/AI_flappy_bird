import matplotlib.pyplot as plt
from IPython import display

plt.ion()

def plot(scores, mean_scores,caught_foods=None):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training')
    plt.subplot(2,1,1)
    plt.ylabel('Reward mean')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    # 
    # 
    if caught_foods:
        plt.subplot(2,1,2)
        plt.xlabel('Number of Games')
        plt.ylabel('Pipe Record')
        plt.plot(caught_foods)
        plt.ylim(ymin=0)
        plt.text(len(caught_foods)-1, caught_foods[-1], str(caught_foods[-1]))
    plt.show(block=False)
    plt.pause(0.1)
    