import pandas as pd
import matplotlib.pyplot as plt

August_data =pd.read_csv("August_pork.csv")
dataFrame = pd.DataFrame(August_data, columns=["Temp", "Pork", "Fish", "Chicken"])

temperature = dataFrame.Temp[1:5040]
Pork = dataFrame.Pork[1:5040]
Fish = dataFrame.Fish[1:5040]
Chicken = dataFrame.Chicken[1:5040]

fig, ax = plt.subplots()
labels = ['24h', '48h', '72h', '96h', '120h', '144h', "168"]
def set_axis_style(ax, labels):
    ax.get_xaxis().set_tick_params(direction='out')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xticks([720, 1440, 2160, 2880, 3600, 4320, 5040])
    ax.set_xticklabels(labels)

# temp
plt.title('Temperature - chicken in refrigerator')
plt.xlim(0, 2040)
plt.ylim(0,10)
set_axis_style(ax, labels)
plt.plot(temperature, color='green')
plt.xlabel("Time")
plt.ylabel("Temperature *C")
plt.show()

# # press
# plt.title('Air Pressure - Chicken in refrigerator')
# plt.xlim(0,2040)
# plt.ylim(1000, 1030)
# set_axis_style(ax, labels)
# plt.plot(pressure, color='red')
# plt.xlabel("Time")
# plt.ylabel("Pressure hPa")
# plt.show()


num_folds = 10
kfold = KFold(n_splits=num_folds, shuffle=True)
acc_per_fold=[]
loss_per_fold=[]
fold_no=1
for train_k, test_k in kfold.split(train_input, y_train):
  model = Sequential()
  model.add(Convolution1D(filters=512, kernel_size=1, input_shape=(nb_features, 2)))
  model.add(Activation('relu'))
  model.add(Flatten())
  model.add(Dropout(0.2))
  model.add(Dense(2048, activation='relu'))
  model.add(Dense(1024, activation='relu'))
  model.add(Dense(nb_class))
  model.add(Activation('softmax'))
  y_train = np_utils.to_categorical(y_train, nb_class)
  sgd = SGD(lr=0.001, nesterov=True, decay=1e-6, momentum=0.9)
  model.compile(loss='categorical_crossentropy',optimizer=sgd, metrics=['accuracy'])
  nb_epoch = 100
  history = model.fit(train_input[train_k], y_train[train_k], epochs=nb_epoch, batch_size=32)
  scores = model.evaluate(train_input[test_k], y_train[test], verbose=0)
  acc_per_fold.append(scores[1]*100)
  loss_per_fold.append(scores[0])
print(f'Accuracy: {np.mean(acc_per_fold)}(+-{np.std(acc_per_fold)})')