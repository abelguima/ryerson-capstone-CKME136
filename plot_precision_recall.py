'''
This is a file modified by Abel Ag Rb Guimaraes from sklearn
'''
from __future__ import print_function

###############################################################################
# In binary classification settings
# --------------------------------------------------------
#
# Create simple data
# ..................
#
# Try to differentiate the two first classes of the iris data
import numpy as np
import pandas as pd
from scipy import double

# what are your inputs, and what operation do you want to
# perform on each input. For example...
df = pd.read_csv('MODELS/Classify_Many_Images1.csv')

ground_truth = df['Ground_truth']
label1 = df['label1']
prediction1 = df['prediction1']
label2 = df['label2']
prediction2 = df['prediction2']
label3 = df['label3']
prediction3 = df['prediction3']
label4 = df['label4']
prediction4 = df['prediction4']
label5 = df['label5']
prediction5 = df['prediction5']

n_classes = 34
y_test = []
y_score = []

for gt, l1, p1, l2, p2, l3, p3, l4, p4, l5, p5 in zip(ground_truth, label1, prediction1, label2, prediction2,
                                                      label3, prediction3, label4, prediction4, label5, prediction5):
    y_score_aux = np.double(np.zeros(n_classes))
    y_test_aux = np.int64(np.zeros(n_classes))

    y_score_aux[l1] = double(p1) / 100
    y_score_aux[l2] = double(p2) / 100
    y_score_aux[l3] = double(p3) / 100
    y_score_aux[l4] = double(p4) / 100
    y_score_aux[l5] = double(p5) / 100
    y_score.append(y_score_aux)
    y_test_aux[gt] = 1
    y_test.append(y_test_aux)

y_score = np.array(y_score)
y_test = np.array(y_test)

###############################################################################
# Compute the average precision score
# ...................................
from sklearn.metrics import average_precision_score
average_precision = average_precision_score(y_test, y_score)

print('Average precision-recall score: {0:0.2f}'.format(
      average_precision))

###############################################################################
# Plot the Precision-Recall curve
# ................................
from sklearn.metrics import precision_recall_curve
import matplotlib.pyplot as plt








###############################################################################
# The average precision score in multi-label settings
# ....................................................
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score

# For each class
precision = dict()
recall = dict()
average_precision = dict()
for i in range(n_classes):
    precision[i], recall[i], _ = precision_recall_curve(y_test[:, i],
                                                        y_score[:, i])
    average_precision[i] = average_precision_score(y_test[:, i], y_score[:, i])

# A "micro-average": quantifying score on all classes jointly
precision["micro"], recall["micro"], _ = precision_recall_curve(y_test.ravel(),
    y_score.ravel())
average_precision["micro"] = average_precision_score(y_test, y_score,
                                                     average="micro")
print('Average precision score, micro-averaged over all classes: {0:0.2f}'
      .format(average_precision["micro"]))

###############################################################################
# Plot the micro-averaged Precision-Recall curve
# ...............................................
#

plt.figure()
plt.step(recall['micro'], precision['micro'], color='b', alpha=0.2,
         where='post')
plt.fill_between(recall["micro"], precision["micro"], step='post', alpha=0.2,
                 color='b')

plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0.0, 1.05])
plt.xlim([0.0, 1.0])
plt.title(
    'Average precision score, micro-averaged over all classes: AP={0:0.2f}'
    .format(average_precision["micro"]))

###############################################################################
# Plot Precision-Recall curve for each class and iso-f1 curves
# .............................................................
#
from itertools import cycle
# setup plot details
colors = cycle(['aqua', 'darkorange', 'cornflowerblue', 'black', 'red', 'gray', 'orange',
                'gold', 'blue', 'yellow', 'brown', 'cyan', 'violet', 'pink', 'green',
                'magenta', 'indigo', 'khaki', 'coral', 'cadetblue'])

plt.figure(figsize=(7, 8))
f_scores = np.linspace(0.2, 0.8, num=4)
lines = []
labels = []
for f_score in f_scores:
    x = np.linspace(0.01, 1)
    y = f_score * x / (2 * x - f_score)
    l, = plt.plot(x[y >= 0], y[y >= 0], color='gray', alpha=0.2)
    plt.annotate('f1={0:0.1f}'.format(f_score), xy=(0.9, y[45] + 0.02))

lines.append(l)
labels.append('iso-f1 curves')
l, = plt.plot(recall["micro"], precision["micro"], color='gold', lw=2)
lines.append(l)
labels.append('micro-average Precision-recall (area = {0:0.2f})'
              ''.format(average_precision["micro"]))

for i, color in zip(range(n_classes), colors):
    l, = plt.plot(recall[i], precision[i], color=color, lw=2)
    lines.append(l)
    label_x = ''
    x = i
    if i > 16:
        label_x = 'Zone_threat{0} (area = {1:0.2f})'
        x -= 16
    else:
        label_x = 'Zone{0} (area = {1:0.2f})'
        x += 1
    labels.append(label_x.format(x, average_precision[i]))



fig = plt.gcf()
fig.subplots_adjust(bottom=0.25)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Extension of Precision-Recall curve to multi-class')
#plt.legend(loc="lower right", prop={'size': 8})
plt.legend(lines, labels, loc=(0, -.38), prop=dict(size=8))


plt.show()
