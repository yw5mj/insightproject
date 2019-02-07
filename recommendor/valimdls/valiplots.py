import matplotlib.pyplot as plt
from surprise import dump
from surprise import accuracy
import sys
mdl=dump.load(sys.argv[1])[1]
testset=mdl.trainset.build_testset()
predictions=mdl.test(testset)
accuracy.rmse(predictions, verbose=True)
x=[i[3] for i in predictions[:2000]]
y=[i[2] for i in predictions[:2000]]
plt.plot(x,y,'ro')
plt.xlabel('true rating',fontsize=18)
plt.ylabel('predicted rating',fontsize=18)
plt.savefig(sys.argv[2])
