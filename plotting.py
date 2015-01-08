'''
Handles plotting of different visualizations of data.
@author: JohnArne
'''
import matplotlib.pyplot as plt
import random
import numpy as np

def plot_temporal_sentiment(data):
    """
    Plots the temporal sentiment using the given data.
    """
    tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),  
                 (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),  
                 (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),  
                 (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),  
                 (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]  
      
    # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.  
    for i in range(len(tableau20)):  
        r, g, b = tableau20[i]  
        tableau20[i] = (r / 255., g / 255., b / 255.)  
      
    # You typically want your plot to be ~1.33x wider than tall. This plot is a rare  
    # exception because of the number of lines being plotted on it.  
    # Common sizes: (10, 7.5) and (12, 9)  
    f = plt.figure(figsize=(6, 7))  
      
    # Remove the plot frame lines. They are unnecessary chartjunk.  
    ax = plt.subplot(111)  
    ax.spines["top"].set_visible(False)  
    ax.spines["bottom"].set_visible(False)  
    ax.spines["right"].set_visible(False)  
    ax.spines["left"].set_visible(False)  
      
    # Ensure that the axis ticks only show up on the bottom and left of the plot.  
    # Ticks on the right and top of the plot are generally unnecessary chartjunk.  
    ax.get_xaxis().tick_bottom()  
    ax.get_yaxis().tick_left()  
      
    # Limit the range of the plot to only where the data is.  
    # Avoid unnecessary whitespace.  
    plt.ylim(0, 90)  
    plt.xlim(0, 60)  
      
    # Make sure your axis ticks are large enough to be easily read.  
    # You don't want your viewers squinting to read your plot.  
    plt.yticks(range(0, 91, 10), [str(x) for x in range(0, 91, 10)], fontsize=14)  
    plt.xticks(fontsize=14)  
      
    # Provide tick lines across the plot to help your viewers trace along  
    # the axis ticks. Make sure that the lines are light and small so they  
    # don't obscure the primary data lines.  
    for y in range(10, 91, 10):  
        plt.plot(range(1,60), [y] * len(range(1,60)), "--", lw=0.5, color="black", alpha=0.3)  
      
    # Remove the tick marks; they are unnecessary with the tick lines we just plotted.  
    plt.tick_params(axis="both", which="both", bottom="off", top="off",  
                    labelbottom="on", left="off", right="off", labelleft="on")  
      
    # Now that the plot is prepared, it's time to actually plot the data!  
    # Note that I plotted the majors in order of the highest % in the final year.  
    majors = ['No target', 'Erna Solberg', 'Rosenborg']  
      
    for rank, column in enumerate(majors):  
        # Plot each line separately with its own color, using the Tableau 20  
        # color set in order.  
        plt.plot(data[column][0], data[column][1], lw=2.5, color=tableau20[rank])  
          
        # Add a text label to the right end of every line. Most of the code below  
        # is adding specific offsets y position because some labels overlapped.  
        y_pos = data[column][1][-1] - 0.5  
          
        # Again, make sure that all labels are large enough to be easily read  
        # by the viewer.  
        plt.text(76.5, y_pos, column, fontsize=14, color=tableau20[rank])  
      
    plt.savefig("figs/temporal_sentiments.pdf", bbox_inches="tight");  
   
def plot_performance_histogram(data, filename):
    """
    Plots the performance of different algorithms.
    """
    tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),  
                 (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),  
                 (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),  
                 (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),  
                 (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]  
      
    # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.  
    for i in range(len(tableau20)):  
        r, g, b = tableau20[i]  
        tableau20[i] = (r / 255., g / 255., b / 255.)  
      
    # You typically want your plot to be ~1.33x wider than tall. This plot is a rare  
    # exception because of the number of lines being plotted on it.  
    # Common sizes: (10, 7.5) and (12, 9)  
    f = plt.figure()  
      
    # Remove the plot frame lines. They are unnecessary chartjunk.  
    ax = plt.subplot(111)  
    
    labels = data.keys()
    print labels
    precisions = [data[key][0] for key in labels] 
    recalls = [data[key][1] for key in labels]
    f1s = [data[key][2] for key in labels]
    accuracies = [data[key][3] for key in labels]

    #Create bars    
    ind = (np.arange(len(labels))*2)+0.25
    width = 0.35
    ax.bar(ind, precisions, width, color=tableau20[0], edgecolor="none")
    ax.bar(ind+width, recalls, width, color=tableau20[1], edgecolor="none")
    ax.bar(ind+width*2, f1s, width, color=tableau20[2], edgecolor="none")
    ax.bar(ind+width*3, accuracies, width, color=tableau20[3], edgecolor="none")
    
    #Create top bar labels
    for p, i in zip(precisions, ind):
        plt.text(i+0.03, p+0.01, "%0.2f" % p, fontsize=10, color=tableau20[0])
    for p, i in zip(recalls, ind+width):
        plt.text(i+0.03, p+0.01, "%0.2f" % p, fontsize=10, color=tableau20[1])
    for p, i in zip(f1s, ind+width*2):
        plt.text(i+0.03, p+0.01, "%0.2f" % p, fontsize=10, color=tableau20[2])
    for p, i in zip(accuracies, ind+width*3):
        plt.text(i+0.03, p+0.01, "%0.2f" % p, fontsize=10, color=tableau20[3])
    
    ax.spines["top"].set_visible(False)  
#    ax.spines["bottom"].set_visible(False)  
    ax.spines["right"].set_visible(False)  
    ax.spines["left"].set_visible(False)
    ax.set_xticks(ind+width*2)  
    ax.set_xticklabels(labels)  
    # Ensure that the axis ticks only show up on the bottom and left of the plot.  
    # Ticks on the right and top of the plot are generally unnecessary chartjunk.  
    ax.get_xaxis().tick_bottom()  
    ax.get_yaxis().tick_left()  

    for y in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8]:  
        plt.plot(range(0,7), [y] * len(range(0,7)), "--", lw=0.5, color="black", alpha=0.3)  
      
    # Remove the tick marks; they are unnecessary with the tick lines we just plotted.  
    plt.tick_params(axis="both", which="both", bottom="off", top="off",  
                    labelbottom="on", left="off", right="off", labelleft="on",labelcolor=tableau20[14])  
  
    plt.savefig('figs/'+filename+".pdf", bbox_inches="tight");  
    
def plot_pos_analysis(data, filename):
    """
    Plots the performance of different algorithms.
    """
    tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),  
                 (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),  
                 (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),  
                 (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),  
                 (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]  
      
    # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.  
    for i in range(len(tableau20)):  
        r, g, b = tableau20[i]  
        tableau20[i] = (r / 255., g / 255., b / 255.)  
      
    # You typically want your plot to be ~1.33x wider than tall. This plot is a rare  
    # exception because of the number of lines being plotted on it.  
    # Common sizes: (10, 7.5) and (12, 9)  
    f = plt.figure()  
      
    # Remove the plot frame lines. They are unnecessary chartjunk.  
    ax = plt.subplot(111)  
    
    labels = data.keys()
    print labels
    precisions = [data[key][0] for key in labels] 
    recalls = [data[key][1] for key in labels]
    f1s = [data[key][2] for key in labels]
    accuracies = [data[key][3] for key in labels]

    #Create bars    
    ind = (np.arange(len(labels))*2)+0.25
    width = 0.35
    ax.bar(ind, precisions, width, color=tableau20[0], edgecolor="none")
    ax.bar(ind+width, recalls, width, color=tableau20[1], edgecolor="none")
    ax.bar(ind+width*2, f1s, width, color=tableau20[2], edgecolor="none")
    ax.bar(ind+width*3, accuracies, width, color=tableau20[3], edgecolor="none")
    
    #Create top bar labels
    for p, i in zip(precisions, ind):
        plt.text(i+0.03, p+0.01, "%0.2f" % p, fontsize=10, color=tableau20[0])
    for p, i in zip(recalls, ind+width):
        plt.text(i+0.03, p+0.01, "%0.2f" % p, fontsize=10, color=tableau20[1])
    for p, i in zip(f1s, ind+width*2):
        plt.text(i+0.03, p+0.01, "%0.2f" % p, fontsize=10, color=tableau20[2])
    for p, i in zip(accuracies, ind+width*3):
        plt.text(i+0.03, p+0.01, "%0.2f" % p, fontsize=10, color=tableau20[3])
    
    ax.spines["top"].set_visible(False)  
#    ax.spines["bottom"].set_visible(False)  
    ax.spines["right"].set_visible(False)  
    ax.spines["left"].set_visible(False)
    ax.set_xticks(ind+width*2)  
    ax.set_xticklabels(labels)  
    # Ensure that the axis ticks only show up on the bottom and left of the plot.  
    # Ticks on the right and top of the plot are generally unnecessary chartjunk.  
    ax.get_xaxis().tick_bottom()  
    ax.get_yaxis().tick_left()  

    for y in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8]:  
        plt.plot(range(0,7), [y] * len(range(0,7)), "--", lw=0.5, color="black", alpha=0.3)  
      
    # Remove the tick marks; they are unnecessary with the tick lines we just plotted.  
    plt.tick_params(axis="both", which="both", bottom="off", top="off",  
                    labelbottom="on", left="off", right="off", labelleft="on",labelcolor=tableau20[14])  
  
    plt.savefig('figs/'+filename+".pdf", bbox_inches="tight");  
    
def plot_dataset_stats(data):
    """
    Plots histograms of the dataset statistics using the given data.
    """

    
#    data = {"Erna Solberg": [range(0,100),[random.randint(20,50) for _ in range(0,100)]],
#            "Rosenborg": [range(0,100),[random.randint(40,60) for _ in range(0,100)]],
#            "No target": [range(0,100),[random.randint(30,40) for _ in range(0,100)]]}
#    for key in data.keys():
#        print len(data[key][0])
#        print len(data[key][1])
#    plot_temporal_sentiment(data)
if __name__ == '__main__':
    data = {"Naive Bayes": [0.645, 0.6, 0.5, 0.69],
            "SVM": [0.7, 0.8, 0.82, 0.87],
            "MaxEnt": [0.81, 0.72, 0.71, 0.79]}
    plot_performance_histogram(data, "svm_sub_performance")

