'''
Handles plotting of different visualizations of data.
@author: JohnArne
'''
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random
import numpy as np
import utils
import random
import pickle
from Tkconstants import OFF

def plot_temporal_sentiment(data, filename="temporal"):
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
    f = plt.figure(figsize=(8, 6))  
      
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
    plt.ylim(0, 1)  
    plt.xlim(0, 101)  
      
    # Make sure your axis ticks are large enough to be easily read.  
    # You don't want your viewers squinting to read your plot.
#    y_ticks = []  
#    plt.yticks(range(0, 1, 10), [str(x) for x in range(0, 91, 10)], fontsize=14)  
    plt.xticks(fontsize=10)  
    plt.yticks(fontsize=10)
    # Provide tick lines across the plot to help your viewers trace along  
    # the axis ticks. Make sure that the lines are light and small so they  
    # don't obscure the primary data lines.  
    for y in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]:  
        plt.plot(range(1,105), [y] * len(range(1,105)), "--", lw=0.5, color="black", alpha=0.3)  
      
    # Remove the tick marks; they are unnecessary with the tick lines we just plotted.  
    plt.tick_params(axis="both", which="both", bottom="off", top="off",  
                    labelbottom="on", left="off", right="off", labelleft="on")  
      
    # Now that the plot is prepared, it's time to actually plot the data!  
    # Note that I plotted the labels in order of the highest % in the final year.  
    labels = data.keys()  
    y_poses = []  
    offsets = [0.02, 0.04,0.06,0.08,0.1,0.12, 0.14,0.16,0.18,0.2]
    for rank, column in enumerate(labels):  
        # Plot each line separately with its own color, using the Tableau 20  
        # color set in order.  
        plt.plot(data[column][0], data[column][1], lw=1.0, color=tableau20[rank])  
          
        # Add a text label to the right end of every line. Most of the code below  
        # is adding specific offsets y position because some labels overlapped.  
        y_pos = data[column][1][-1]
#        new_pos = None
#        offset_counter = 0
        for poses in y_poses:
            if y_pos < poses+0.01 and y_pos>poses:
                y_pos = y_pos+0.05
#                offset_counter += 1
                break
            if y_pos > poses-0.01 and y_pos<poses:
                y_pos = y_pos+0.05
#                offset_counter += 1
                break
            else:
                y_pos = y_pos
        y_poses.append(y_pos)
        # Again, make sure that all labels are large enough to be easily read  
        # by the viewer.  
        plt.text(101.5, y_pos, column, fontsize=8, color=tableau20[rank])  
      
    plt.savefig("figs/"+filename+".pdf", bbox_inches="tight");
    print "Figure done."  
   
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
    
def plot_combined_histogram(data, filename):
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
    ind = (np.arange(len(labels))*5.5)+0.55
    width = 1.1
    ax.bar(ind, precisions, width, color=tableau20[0], edgecolor="none")
    ax.bar(ind+width, recalls, width, color=tableau20[1], edgecolor="none")
    ax.bar(ind+(width)*2, f1s, width, color=tableau20[2], edgecolor="none")
    ax.bar(ind+(width)*3, accuracies, width, color=tableau20[3], edgecolor="none")
    
    #Create top bar labels
    for p, i in zip(precisions, ind):
        plt.text(i, p+0.01, "%0.2f" % p, fontsize=8, color=tableau20[0])
    for p, i in zip(recalls, ind+width):
        plt.text(i, p+0.01, "%0.2f" % p, fontsize=8, color=tableau20[1])
    for p, i in zip(f1s, ind+width*2):
        plt.text(i, p+0.01, "%0.2f" % p, fontsize=8, color=tableau20[2])
    for p, i in zip(accuracies, ind+width*3):
        plt.text(i, p+0.01, "%0.2f" % p, fontsize=8, color=tableau20[3])
    
    ax.spines["top"].set_visible(False)  
#    ax.spines["bottom"].set_visible(False)  
    ax.spines["right"].set_visible(False)  
    ax.spines["left"].set_visible(False)
    ax.set_xticks(ind+width*2)  
    ax.set_xticklabels([l.split('+')[0]+"\n"+l.split('+')[1] for l in labels])  
    # Ensure that the axis ticks only show up on the bottom and left of the plot.  
    # Ticks on the right and top of the plot are generally unnecessary chartjunk.  
    ax.get_xaxis().tick_bottom()  
    ax.get_yaxis().tick_left()  

    for y in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8]:  
        plt.plot(range(0,29), [y] * len(range(0,29)), "--", lw=0.5, color="black", alpha=0.3)  
      
    # Remove the tick marks; they are unnecessary with the tick lines we just plotted.  
    plt.tick_params(axis="both", which="both", bottom="off", top="off",  
                    labelbottom="on", left="off", right="off", labelleft="on",labelcolor=tableau20[14])  
  
    plt.savefig('figs/'+filename+".pdf", bbox_inches="tight");  
    print "Done"
    
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
    values = [data[key] for key in labels]
    print values
    print labels 
    sorted_values_and_labels = [list(x) for x in zip(*sorted(zip(values,labels)))]
    print "Sorted:", sorted_values_and_labels
    values = sorted_values_and_labels[0]
    labels = sorted_values_and_labels[1]
    #Create bars    
    ind = (np.arange(len(labels)))
    width = 0.7
    for v,i in zip(values,ind):
        ax.bar(i, v, width, color=tableau20[14], edgecolor="none")
    
    #Create top bar labels
    for p, i, l in zip(values, ind, labels):
        plt.text(i, p+0.01 if p>0 else p-0.03, l, fontsize=8, color=tableau20[14])

    ax.spines["top"].set_visible(False)  
    ax.spines["bottom"].set_visible(False)  
    ax.spines["right"].set_visible(False)  
    ax.spines["left"].set_visible(False)
    ax.set_xticks(ind+width*2)  
    ax.set_xticklabels([" " for _ in labels])  
    # Ensure that the axis ticks only show up on the bottom and left of the plot.  
    # Ticks on the right and top of the plot are generally unnecessary chartjunk.  
    ax.get_xaxis().tick_bottom()  
    ax.get_yaxis().tick_left()  

    for y in [-0.4,-0.3,-0.2,-0.1,0.0,0.1,0.2,0.3,0.4]:  
        plt.plot(range(0,18), [y] * len(range(0,18)), "--", lw=0.1, color="black", alpha=0.3)  
      
    # Remove the tick marks; they are unnecessary with the tick lines we just plotted.  
    plt.tick_params(axis="both", which="both", bottom="off", top="off",  
                    labelbottom="on", left="off", right="off", labelleft="on",labelcolor=tableau20[14])  
  
    plt.savefig('figs/'+filename+".pdf", bbox_inches="tight");  

    
def average_wordclasses(data, filename):
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

    for y in [1,2,3,4,5,6,7]:  
        plt.plot(range(0,7), [y] * len(range(0,7)), "--", lw=0.5, color="black", alpha=0.3)  
      
    # Remove the tick marks; they are unnecessary with the tick lines we just plotted.  
    plt.tick_params(axis="both", which="both", bottom="off", top="off",  
                    labelbottom="on", left="off", right="off", labelleft="on",labelcolor=tableau20[14])  
  
    plt.savefig('figs/'+filename+".pdf", bbox_inches="tight");    
    
def detailed_average_wordclasses(data, filename):
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
    datalists = []
    for i in xrange(len(data[labels[0]])):
        datalists.append([data[key][i] for key in labels]) 

        
    #Create bars    
    ind = (np.arange(len(labels))*2.2)+0.2
    width = 0.1
    offset = np.arange(0.01, 1, 0.01)
    colorlist = [tableau20[0],tableau20[0],tableau20[0],tableau20[1],tableau20[4],tableau20[5],tableau20[6],tableau20[7],tableau20[2],tableau20[2],tableau20[2],tableau20[2],tableau20[2],
                 tableau20[13],tableau20[14],tableau20[15],tableau20[16],tableau20[3]]
    for i in xrange(len(datalists)):
        bar = ax.bar(ind+width*i, datalists[i], width, color=colorlist[i], edgecolor="none")
    #Create top bar labels
#    for p, i in zip(precisions, ind):
#        plt.text(i+0.03, p+0.01, "%0.2f" % p, fontsize=10, color=tableau20[0])
#    for p, i in zip(recalls, ind+width):
#        plt.text(i+0.03, p+0.01, "%0.2f" % p, fontsize=10, color=tableau20[1])
#    for p, i in zip(f1s, ind+width*2):
#        plt.text(i+0.03, p+0.01, "%0.2f" % p, fontsize=10, color=tableau20[2])
#    for p, i in zip(accuracies, ind+width*3):
#        plt.text(i+0.03, p+0.01, "%0.2f" % p, fontsize=10, color=tableau20[3])
    
    ax.spines["top"].set_visible(False)  
#    ax.spines["bottom"].set_visible(False)  
    ax.spines["right"].set_visible(False)  
    ax.spines["left"].set_visible(False)
    ax.set_xticks(ind+width*9)  
    ax.set_xticklabels(labels)  
    # Ensure that the axis ticks only show up on the bottom and left of the plot.  
    # Ticks on the right and top of the plot are generally unnecessary chartjunk.  
    ax.get_xaxis().tick_bottom()  
    ax.get_yaxis().tick_left()  

    for y in [0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.4,2.6,2.8,3.0]:  
        plt.plot(range(0,8), [y] * len(range(0,8)), "--", lw=0.5, color="black", alpha=0.3)  
      
    # Remove the tick marks; they are unnecessary with the tick lines we just plotted.  
    plt.tick_params(axis="both", which="both", bottom="off", top="off",  
                    labelbottom="on", left="off", right="off", labelleft="on",labelcolor=tableau20[14])  
  
    plt.savefig('figs/'+filename+".pdf", bbox_inches="tight");    
    
def plot_entity_histogram(data, filename):
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

def load_incremental_data():
    f1_data= pickle.load(open('incremental_f1100',"rb"))
    acc_data=pickle.load(open('incremental_acc100',"rb"))
    print f1_data
    print acc_data
    for key in f1_data.keys():
        f1list = f1_data[key]
        f1_data[key] = [range(5,101,5),f1list]
        acclist = acc_data[key]
        acc_data[key] = [range(5,101,5),acclist]
    f1svm_data = {}
    f1nb_data = {}
    f1me_data = {}
    accsvm_data = {}
    accnb_data = {}
    accme_data = {}
    for key in f1_data.keys():
        if key[:3]=="SVM":
            f1svm_data[key] = f1_data[key]
        elif key[:2]=="NB":
            f1nb_data[key] = f1_data[key]
        elif key[:6]=="MaxEnt":
            f1me_data[key] = f1_data[key]
    for key in acc_data.keys():
        if key[:3]=="SVM":
            accsvm_data[key] = acc_data[key]
        elif key[:2]=="NB":
            accnb_data[key] = acc_data[key]
        elif key[:6]=="MaxEnt":
            accme_data[key] = acc_data[key]
    
    
    return f1svm_data, f1nb_data, f1me_data, accsvm_data, accnb_data, accme_data
            

def plot_subjectivity_aggregates(data, filename="temporal"):
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
    f = plt.figure(figsize=(9, 6))  
    ind = np.arange(len(data['Targets'][0]))
    # Remove the plot frame lines. They are unnecessary chartjunk.  
    ax = plt.subplot(111)  
    ax.spines["top"].set_visible(False)  
    ax.spines["bottom"].set_visible(False)  
    ax.spines["right"].set_visible(False)  
    ax.spines["left"].set_visible(False)  
    ax.set_xticks(ind+0.25)
    ax.set_xticklabels(['%.2f' % x for x in data['Targets'][0]])   
    # Ensure that the axis ticks only show up on the bottom and left of the plot.  
    # Ticks on the right and top of the plot are generally unnecessary chartjunk.  
    ax.get_xaxis().tick_bottom()  
    ax.get_yaxis().tick_left()  
    ax.bar(ind, data['Frequencies'][1], 0.5, color=tableau20[14], edgecolor="none")
      
    # Limit the range of the plot to only where the data is.  
    # Avoid unnecessary whitespace.  
    plt.ylim(0, 70)  
    plt.xlim(0, 19)
      
    # Make sure your axis ticks are large enough to be easily read.  
    # You don't want your viewers squinting to read your plot.
#    y_ticks = []  
#    plt.yticks(range(0, 1, 10), [str(x) for x in range(0, 91, 10)], fontsize=14)  
    plt.xticks(fontsize=8)  
    plt.yticks(fontsize=10)
    # Provide tick lines across the plot to help your viewers trace along  
    # the axis ticks. Make sure that the lines are light and small so they  
    # don't obscure the primary data lines.  
    for y in [5,10,15,20,25,30,35,40,45,50, 55, 60, 65]:  
        plt.plot(range(0,20), [y] * len(range(0,20)), "--", lw=0.5, color="black", alpha=0.3)  
      
    # Remove the tick marks; they are unnecessary with the tick lines we just plotted.  
    plt.tick_params(axis="both", which="both", bottom="off", top="off",  
                    labelbottom="on", left="off", right="off", labelleft="on")  
      
    # Now that the plot is prepared, it's time to actually plot the data!  
    # Note that I plotted the labels in order of the highest % in the final year.  
    labels = [label for label in data.keys() if label!='Frequencies']  
    y_poses = []
    offsets = [0.02, 0.04,0.06,0.08,0.1,0.12, 0.14,0.16,0.18,0.2]
    for rank, column in enumerate(labels):  
        # Plot each line separately with its own color, using the Tableau 20  
        # color set in order.  
        plt.plot(ind+0.25, data[column][1], lw=1.0, color=tableau20[rank+1])  
          
        # Add a text label to the right end of every line. Most of the code below  
        # is adding specific offsets y position because some labels overlapped.  
        y_pos = data[column][1][-1]
#        new_pos = None
#        offset_counter = 0
        for poses in y_poses:
            if y_pos < poses+1 and y_pos>=poses:
                y_pos = y_pos+2
#                offset_counter += 1
                break
            if y_pos > poses-1 and y_pos<=poses:
                y_pos = y_pos+2
#                offset_counter += 1
                break
            else:
                y_pos = y_pos
        y_poses.append(y_pos)
        # Again, make sure that all labels are large enough to be easily read  
        # by the viewer.  
        plt.text(19, y_pos, column, fontsize=8, color=tableau20[rank+1])  
    plt.savefig("figs/"+filename+".pdf", bbox_inches="tight");
    print "Figure done."  

def plot_polarity_aggregates(data, filename="temporal"):
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
    f = plt.figure(figsize=(9, 6))  
    ind = np.arange(len(data['Targets'][0]))
    # Remove the plot frame lines. They are unnecessary chartjunk.  
    ax = plt.subplot(111)  
    ax.spines["top"].set_visible(False)  
    ax.spines["bottom"].set_visible(False)  
    ax.spines["right"].set_visible(False)  
    ax.spines["left"].set_visible(False)  
    ax.set_xticks(ind+0.25)
    ax.set_xticklabels(['%.2f' % x for x in data['Targets'][0]])   
    # Ensure that the axis ticks only show up on the bottom and left of the plot.  
    # Ticks on the right and top of the plot are generally unnecessary chartjunk.  
    ax.get_xaxis().tick_bottom()  
    ax.get_yaxis().tick_left()  
    ax.bar(ind, data['Frequencies'][1], 0.5, color=tableau20[14], edgecolor="none")
      
    # Limit the range of the plot to only where the data is.  
    # Avoid unnecessary whitespace.  
    plt.ylim(-1, 1)  
    plt.xlim(0, 19.5)
      
    # Make sure your axis ticks are large enough to be easily read.  
    # You don't want your viewers squinting to read your plot.
#    y_ticks = []  
#    plt.yticks(range(0, 1, 10), [str(x) for x in range(0, 91, 10)], fontsize=14)  
    plt.xticks(fontsize=8)  
    plt.yticks(fontsize=10)
    # Provide tick lines across the plot to help your viewers trace along  
    # the axis ticks. Make sure that the lines are light and small so they  
    # don't obscure the primary data lines.  
#    for y in [5,10,15,20,25,30,35,40,45]: 
    for y in [-0.8,-0.6,-0.4,-0.2,0.2,0.4,0.6,0.8]:   
        plt.plot(range(0,20), [y] * len(range(0,20)), "--", lw=0.5, color="black", alpha=0.3)  
    plt.plot(range(0,20), [0] * len(range(0,20)), "--", lw=2.5, color="black", alpha=0.3)  
    # Remove the tick marks; they are unnecessary with the tick lines we just plotted.  
    plt.tick_params(axis="both", which="both", bottom="off", top="off",  
                    labelbottom="on", left="off", right="off", labelleft="on")  
      
    # Now that the plot is prepared, it's time to actually plot the data!  
    # Note that I plotted the labels in order of the highest % in the final year.  
    labels = [label for label in data.keys() if label!='Frequencies']  
    y_poses = []
    offsets = [0.02, 0.04,0.06,0.08,0.1,0.12, 0.14,0.16,0.18,0.2]
    for rank, column in enumerate(labels):  
        # Plot each line separately with its own color, using the Tableau 20  
        # color set in order.  
        plt.plot(ind+0.25, data[column][1], lw=1.0, color=tableau20[rank+1])  
          
        # Add a text label to the right end of every line. Most of the code below  
        # is adding specific offsets y position because some labels overlapped.  
        y_pos = data[column][1][-1]
#        new_pos = None
#        offset_counter = 0
        for poses in y_poses:
            if y_pos < poses+0.1 and y_pos>=poses:
                y_pos = y_pos+0.2
#                offset_counter += 1
                break
            if y_pos > poses-0.1 and y_pos<=poses:
                y_pos = y_pos-0.2
#                offset_counter += 1
                break
            else:
                y_pos = y_pos
        y_poses.append(y_pos)
        # Again, make sure that all labels are large enough to be easily read  
        # by the viewer.  
        plt.text(19, y_pos, column, fontsize=8, color=tableau20[rank+1])  
#    plt.text(19, 29.5, "Neutral", fontsize=8, color="black")  
    plt.savefig("figs/"+filename+".pdf", bbox_inches="tight");
    print "Figure done."  

def plot_temporal_topics(data, filename="temporal_topics"):
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
    f = plt.figure(figsize=(9, 6))
    ind = np.arange(len(data[data.keys()[0]][0]))
    # Remove the plot frame lines. They are unnecessary chartjunk.  
    ax = plt.subplot(111)  
    ax.spines["top"].set_visible(False)  
    ax.spines["bottom"].set_visible(False)  
    ax.spines["right"].set_visible(False)  
    ax.spines["left"].set_visible(False)  
    ax.set_xticks(ind+0.25)
    ax.set_xticklabels(['%.2f' % x for x in data[data.keys()[0]][0]])   
    # Ensure that the axis ticks only show up on the bottom and left of the plot.  
    # Ticks on the right and top of the plot are generally unnecessary chartjunk.  
    ax.get_xaxis().tick_bottom()  
    ax.get_yaxis().tick_left()  
    # Limit the range of the plot to only where the data is.  
    # Avoid unnecessary whitespace.  
    plt.ylim(0, 100)  
    plt.xlim(0, 8)
      
    # Make sure your axis ticks are large enough to be easily read.  
    # You don't want your viewers squinting to read your plot.
#    y_ticks = []  
#    plt.yticks(range(0, 1, 10), [str(x) for x in range(0, 91, 10)], fontsize=14)  
    plt.xticks(fontsize=6)  
    plt.yticks(fontsize=6)
    # Provide tick lines across the plot to help your viewers trace along  
    # the axis ticks. Make sure that the lines are light and small so they  
    # don't obscure the primary data lines.  
#    for y in [5,10,15,20,25,30,35,40,45]: 
    for y in range(0,100,5):   
        plt.plot(range(0,8), [y] * len(range(0,8)), "--", lw=0.5, color="black", alpha=0.3)  
    plt.plot(range(0,8), [50] * len(range(0,8)), "--", lw=2.5, color="black", alpha=0.3)  
    # Remove the tick marks; they are unnecessary with the tick lines we just plotted.  
    plt.tick_params(axis="both", which="both", bottom="off", top="off",  
                    labelbottom="on", left="off", right="off", labelleft="on")  
      
    # Now that the plot is prepared, it's time to actually plot the data!  
    # Note that I plotted the labels in order of the highest % in the final year.  
    labels = data.keys()  
    y_poses = []
    offsets = [0.02, 0.04,0.06,0.08,0.1,0.12, 0.14,0.16,0.18,0.2]
    for rank, column in enumerate(labels):  
        # Plot each line separately with its own color, using the Tableau 20  
        # color set in order.  
        for i in range(len(data[column][1])):
            data[column][1][i] = data[column][1][i] +50
        plt.plot(ind+0.25, data[column][1], lw=1.0, color=tableau20[rank])  
          
        # Add a text label to the right end of every line. Most of the code below  
        # is adding specific offsets y position because some labels overlapped.  
        y_pos = data[column][1][-1]
#        new_pos = None
#        offset_counter = 0
        for poses in y_poses:
            if y_pos < poses+5 and y_pos>=poses:
                y_pos = y_pos+8
#                offset_counter += 1
                break
            if y_pos > poses-5 and y_pos<=poses:
                y_pos = y_pos-8
#                offset_counter += 1
                break
            else:
                y_pos = y_pos
        y_poses.append(y_pos)
        # Again, make sure that all labels are large enough to be easily read  
        # by the viewer.  
        try:
            plt.text(8.2, y_pos, column, fontsize=8, color=tableau20[rank])
        except UnicodeDecodeError:
            plt.text(8.2, y_pos, column.decode('utf8'), fontsize=8, color=tableau20[rank])
    plt.text(8.2, 49.5, "Neutral", fontsize=8, color="black")  
    plt.savefig("figs/"+filename+".pdf", bbox_inches="tight");
    print "Figure done."
    
if __name__ == '__main__':
#    f1svm_data, f1nb_data, f1me_data, accsvm_data, accnb_data, accme_data = load_incremental_data()
#    data = {"Erna Solberg": [range(0,100),[random.randint(20,50) for _ in range(0,100)]],
#            "rosenborg": [range(0,100),[random.randint(40,60) for _ in range(0,100)]],
#            "no target": [range(0,100),[random.randint(30,40) for _ in range(0,100)]]}
#    plot_temporal_sentiment(f1svm_data, 'incremental_f1svm')
#    plot_temporal_sentiment(f1nb_data, 'incremental_f1nb')
#    plot_temporal_sentiment(f1me_data, 'incremental_f1me')
#    plot_temporal_sentiment(accsvm_data, 'incremental_accuracysvm')
#    plot_temporal_sentiment(accnb_data, 'incremental_accuracynb')
#    plot_temporal_sentiment(accme_data, 'incremental_accuracyme')
    
#    data = {"SVM(SB)+SVM(PC)": [(0.72+0.79)/2, (0.66+0.80)/2, (0.69+0.76)/2, (0.67+0.78)/2],
#            "SVM(SB)+SVM(PB)": [(0.72+0.77)/2, (0.66+0.76)/2, (0.69+0.75)/2, (0.67+0.75)/2],
#            "SVM(SB)+MaxEnt(PC)":[(0.72+0.77)/2, (0.66+0.80)/2, (0.69+0.72)/2, (0.67+0.75)/2],
#            "MaxEnt(SB)+MaxEnt(PC)": [(0.70+0.77)/2, (0.66+0.80)/2, (0.61+0.72)/2, (0.63+0.75)/2],
#            "MaxEnt(SB)+SVM(PC)": [(0.70+0.79)/2, (0.66+0.80)/2, (0.61+0.76)/2, (0.63+0.78)/2]}
#    plot_combined_histogram(data, "combined")
    data = pickle.load(open('topically_aggregated_polarity', 'rb'))
    plot_temporal_topics(data, "temporal_topics")
